import functools
import time
import unittest

import zope.component.testing
import zope.intid.interfaces
from testfixtures import LogCapture
from zope.catalog.catalog import Catalog
from zope.catalog.field import FieldIndex
from zope.catalog.interfaces import ICatalog
from zope.catalog.text import TextIndex
from zope.component import getUtility
from zope.component import provideUtility
from zope.container.contained import Contained
from zope.interface import Attribute
from zope.interface import Interface
from zope.interface import implementer

from hurry.query import query
from hurry.query.interfaces import IQuery


"""Bring `query` testcoverage to 100% without polluting the doctest"""


class IContent(Interface):
    f1 = Attribute('f1')
    f2 = Attribute('f2')
    f3 = Attribute('f3')
    f4 = Attribute('f4')
    t1 = Attribute('t1')
    t2 = Attribute('t2')


@functools.total_ordering
@implementer(IContent)
class Content(Contained):

    def __init__(self, id, f1='', f2='', f3='', f4='', t1='', t2=''):
        self.id = id
        self.f1 = f1
        self.f2 = f2
        self.f3 = f3
        self.f4 = f4
        self.t1 = t1
        self.t2 = t2

    def __lt__(self, other):
        return self.id < other.id

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f'<Content "{self.id}">'


@implementer(zope.intid.interfaces.IIntIds)
class DummyIntId:
    MARKER = '__dummy_int_id__'

    def __init__(self):
        self.counter = 0
        self.data = {}

    def register(self, obj):
        intid = getattr(obj, self.MARKER, None)
        if intid is None:
            setattr(obj, self.MARKER, self.counter)
            self.data[self.counter] = obj
            intid = self.counter
            self.counter += 1
        return intid

    def getId(self, obj):
        return getattr(obj, self.MARKER)

    def getObject(self, intid):
        return self.data[intid]

    def __iter__(self):
        return iter(self.data)


f1 = ('catalog1', 'f1')


class QueryTestBase(unittest.TestCase):

    tearDown = zope.component.testing.tearDown

    def setUp(self):
        """emulate the doctest fixtures"""
        self.intid = DummyIntId()
        provideUtility(self.intid, zope.intid.interfaces.IIntIds)
        self.catalog = Catalog()
        provideUtility(self.catalog, ICatalog, 'catalog1')
        self.catalog['f1'] = FieldIndex('f1', IContent)
        self.catalog['f2'] = FieldIndex('f2', IContent)
        self.catalog['f3'] = FieldIndex('f3', IContent)
        self.catalog['f4'] = FieldIndex('f4', IContent)
        self.catalog['t1'] = TextIndex('t1', IContent)
        self.catalog['t2'] = TextIndex('t2', IContent)
        provideUtility(query.Query(), IQuery)
        self.setup_content()

    def setup_content(self):
        content = [
            Content(1, 'a', 'b', 'd'),
            Content(2, 'a', 'c'),
            Content(3, 'X', 'c'),
            Content(4, 'a', 'b', 'e'),
            Content(5, 'X', 'b', 'e'),
            Content(6, 'Y', 'Z')]
        for entry in content:
            self.catalog.index_doc(self.intid.register(entry), entry)

    def searchResults(self, q, **kw):
        query = getUtility(IQuery)
        return query.searchResults(q, **kw)

    def displayQuery(self, q, **kw):
        r = self.searchResults(q, **kw)
        return [e.id for e in sorted(list(r))]

    def test_setup(self):
        """verify test fixtures by reproducing first doctest"""
        self.assertEqual(self.displayQuery(
            query.All(f1)),
            [1, 2, 3, 4, 5, 6])


class TimingTest(QueryTestBase):

    def test_init(self):
        timer = query.Timing('foo', 1)
        self.assertEqual(timer.key, 'foo')
        self.assertGreater(timer.start, 0)
        self.assertEqual(timer.start_order, 1)
        self.assertEqual(timer.end, None)
        self.assertEqual(timer.end_order, None)

    def test_done(self):
        timer = query.Timing()
        timer.done(2)
        self.assertGreater(timer.end, 0)
        self.assertEqual(timer.end_order, 2)

    def test_total(self):
        timer = query.Timing()
        time.sleep(.1)
        timer.done()
        self.assertGreater(timer.total, 0)

    def test_total_wo_end(self):
        timer = query.Timing()
        self.assertEqual(timer.total, None)


class TimingAwareCacheTest(QueryTestBase):

    def test_init(self):
        cache = query.TimingAwareCache({})
        self.assertEqual(cache.cache, {})
        self.assertEqual(cache.timing, {})
        self.assertEqual(cache.count, 0)
        self.assertEqual(cache.post, None)

    def test_start_post(self):
        cache = query.TimingAwareCache({})
        cache.start_post()
        self.assertGreater(cache.post.start, 0)

    def test_end_post(self):
        cache = query.TimingAwareCache({})
        with self.assertRaises(AttributeError):
            cache.end_post()

        cache.start_post()
        time.sleep(0.1)
        cache.end_post()
        self.assertGreater(cache.post.total, 0)

    def test_get_uncached(self):
        cache = query.TimingAwareCache({})
        self.assertNotIn('foo', cache.timing)
        self.assertEqual(cache.count, 0)
        value = cache.get('foo')
        self.assertEqual(value, None)
        self.assertIn('foo', cache.timing)
        self.assertGreater(cache.timing['foo'].start, 0)
        self.assertEqual(cache.timing['foo'].end, None)
        self.assertEqual(cache.count, 1)

    def test_get_cached(self):
        cache = query.TimingAwareCache({'foo': 'bar'})
        self.assertNotIn('foo', cache.timing)
        self.assertEqual(cache.count, 0)
        value = cache.get('foo')
        self.assertEqual(value, 'bar')
        self.assertNotIn('foo', cache.timing)
        self.assertEqual(cache.count, 0)

    def test_dunder_setitem(self):
        cache = query.TimingAwareCache({})
        self.assertNotIn('foo', cache.timing)
        self.assertEqual(cache.count, 0)
        cache['foo'] = 'bar'
        self.assertNotIn('foo', cache.timing)
        self.assertEqual(cache.count, 0)

    def test_dunder_setitem_timing(self):
        cache = query.TimingAwareCache({})
        self.assertNotIn('foo', cache.timing)
        self.assertEqual(cache.count, 0)
        cache.get('foo')
        self.assertEqual(cache.count, 1)
        cache['foo'] = 'bar'
        self.assertIn('foo', cache.timing)
        self.assertGreater(cache.timing['foo'].start, 0)
        self.assertGreater(cache.timing['foo'].end, 0)
        self.assertEqual(cache.count, 2)

    def test_report_empty(self):
        with LogCapture() as logged:
            cache = query.TimingAwareCache({})
            cache.report()
            records = logged.records

        self.assertEqual(records, [])

    def test_report_uncached(self):
        with LogCapture() as logged:
            cache = query.TimingAwareCache({})
            cache.get('foo')
            cache['foo'] = 'bar'
            cache.report()
            records = logged.records

        self.assertEqual(records[0].levelname, 'INFO')
        self.assertEqual(records[0].module, 'query')
        self.assertIn('Catalog query', records[0].msg)
        self.assertIn('s for terms', records[0].msg)
        self.assertIn('s to finish', records[0].msg)
        self.assertIn('s: foo', records[1].msg)

    def test_report_uncached_post(self):
        with LogCapture() as logged:
            cache = query.TimingAwareCache({})
            cache.start_post()
            cache.get('foo')
            cache['foo'] = 'bar'
            cache.end_post()
            cache.report()
            records = logged.records

        self.assertEqual(records[0].levelname, 'INFO')
        self.assertEqual(records[0].module, 'query')
        self.assertIn('Catalog query', records[0].msg)
        self.assertIn('s for terms', records[0].msg)
        self.assertIn('s to finish', records[0].msg)
        self.assertIn('s: foo', records[1].msg)

    def test_report_uncached_post_under_over(self):
        with LogCapture() as logged:
            cache = query.TimingAwareCache({})
            cache.start_post()
            cache.get('foo')
            cache['foo'] = 'bar'
            cache.end_post()
            cache.report(over=1)
            records = logged.records

        self.assertEqual(records, [])

    def test_report_uncached_mixedup_order(self):
        with LogCapture() as logged:
            cache = query.TimingAwareCache({})
            cache.get('foobar')
            cache['foobar'] = 'foobar'
            cache.get('foo')
            cache.get('bar')
            cache['bar'] = 'bar'
            cache['foo'] = 'foo'
            cache.get('baz')
            cache['baz'] = 'baz'
            cache.report()
            records = logged.records

        # verify dedent from 5 spaces to 1 space
        self.assertEqual(len(records[1].msg) - len(records[1].msg.lstrip(' ')),
                         5)
        self.assertEqual(len(records[3].msg) - len(records[3].msg.lstrip(' ')),
                         1)

    def test_report_uncached_no_end_post(self):
        with LogCapture() as logged:
            cache = query.TimingAwareCache({})
            cache.start_post()
            cache.get('foo')
            cache.end_post()
            cache.get('foobar')
            cache['foo'] = 'bar'
            cache.report()
            records = logged.records

        self.assertTrue(records[2].msg.endswith('  ?: foobar.'))


class QueryTest(QueryTestBase):

    def test_injected_caching(self):
        class MockCaching:
            _cache = dict()
            _get = 0
            _set = 0

            def get(self, key):
                self._get += 1
                return self._cache.get(key)

            def __setitem__(self, key, value):
                self._set += 1
                self._cache[key] = value

        caching = MockCaching()
        self.searchResults(query.And(query.All(f1)), caching=caching)
        self.assertEqual(caching._get, 2)
        self.assertEqual(caching._set, 2)

        self.searchResults(query.And(query.All(f1)), caching=caching)
        self.assertEqual(caching._get, 3)
        self.assertEqual(caching._set, 2)
        self.assertEqual(
            sorted(caching._cache.keys()),
            [('all', 'catalog1', 'f1'), ('and', ('all', 'catalog1', 'f1'))])
        self.assertEqual(
            [v.keys() for v in caching._cache.values()],
            [[0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]])

    def test_timing(self):
        with LogCapture() as logged:
            self.searchResults(
                query.And(query.All(f1)), timing=.00000001)
            records = logged.records

        self.assertEqual(len(records), 3)
        self.assertIn("('and', ('all', 'catalog1', 'f1')", records[1].msg)
        self.assertIn("('all', 'catalog1', 'f1')", records[2].msg)

    def test_timing_cutoff(self):
        with LogCapture() as logged:
            self.searchResults(query.And(query.All(f1)), timing=5)
            records = logged.records

        self.assertEqual(len(records), 0)

    def test_timing_noresult(self):
        with LogCapture() as logged:
            results = self.displayQuery(
                query.And(query.Eq(f1, 'foo')), timing=.00000001)
            records = logged.records

        self.assertEqual(results, [])
        self.assertEqual(len(records), 3)


class TermsTest(QueryTestBase):

    def test_Term_apply(self):
        term = query.Term()
        with self.assertRaises(NotImplementedError):
            term.apply(None)

    def test_Term_dunder_rand(self):
        class AndDisabledAll(query.All):

            def __and__(self, other):
                return NotImplemented

        left = AndDisabledAll(f1)
        right = query.All(f1)

        self.assertEqual(self.displayQuery(
            left & right),
            [1, 2, 3, 4, 5, 6])

    def test_Term_dunder_ror(self):
        class OrDisabledAll(query.All):

            def __or__(self, other):
                return NotImplemented

        left = OrDisabledAll(f1)
        right = query.All(f1)

        self.assertEqual(self.displayQuery(
            left | right),
            [1, 2, 3, 4, 5, 6])

    def test_And_one_result(self):
        self.assertEqual(self.displayQuery(
            query.And(query.All(f1))),
            [1, 2, 3, 4, 5, 6])

    def test_And_empty_intersection(self):
        self.assertEqual(self.displayQuery(
            query.And(query.Eq(f1, 'a'), query.Eq(f1, 'X'))),
            [])

    def test_And_weighted(self):
        # this only executes the code path without any clue what the
        # impact of 'weighted' should be, if any
        self.assertEqual(self.displayQuery(
            query.And(query.All(f1), query.All(f1), weighted=True)),
            [1, 2, 3, 4, 5, 6])

    def test_And_weighted_empty_intersection(self):
        self.assertEqual(self.displayQuery(
            query.And(query.Eq(f1, 'a'), query.Eq(f1, 'X'), weighted=True)),
            [])

    def test_Or_one_empty_result(self):
        self.assertEqual(self.displayQuery(
            query.Or(query.Eq(f1, 'foo'))),
            [])

    def test_Or_one_result(self):
        self.assertEqual(self.displayQuery(
            query.Or(query.All(f1))),
            [1, 2, 3, 4, 5, 6])

    def test_Difference_one_empty_result(self):
        self.assertEqual(self.displayQuery(
            query.Difference(query.Eq(f1, 'foo'))),
            [])

    def test_Difference_second_empty_result(self):
        self.assertEqual(self.displayQuery(
            query.Difference(query.All(f1), query.Eq(f1, 'foo'))),
            [1, 2, 3, 4, 5, 6])

    def test_Difference_empty_difference(self):
        self.assertEqual(self.displayQuery(
            query.Difference(query.All(f1), query.All(f1))),
            [])

    def test_In_one_result(self):
        self.assertEqual(self.displayQuery(
            query.In(f1, ['Y', 'Z'])),
            [6])
