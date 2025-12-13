##############################################################################
#
# Copyright (c) 2005-2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Basic query implementation

This module contains an IQuery utility implementation, basic query term
implementations and concrete term implementations for zope.catalog indexes.

"""
import itertools
import logging
import os
import time

from BTrees.IFBTree import IFSet
from BTrees.IFBTree import difference
from BTrees.IFBTree import intersection
from BTrees.IFBTree import multiunion
from BTrees.IFBTree import weightedIntersection
from zope.cachedescriptors.property import Lazy
from zope.catalog.field import IFieldIndex
from zope.catalog.interfaces import ICatalog
from zope.catalog.text import ITextIndex
from zope.component import IComponentLookup
from zope.component import getSiteManager
from zope.component import getUtility
from zope.index.interfaces import IIndexSort
from zope.index.text.parsetree import ParseError
from zope.interface import implementer
from zope.intid.interfaces import IIntIds
from zope.location.location import LocationProxy
from zope.location.location import located

from hurry.query import interfaces


logger = logging.getLogger('hurry.query')
HURRY_QUERY_TIMING = 0.0  # log queries taking longer than this, in seconds
if 'HURRY_QUERY_TIMING' in os.environ:
    try:
        HURRY_QUERY_TIMING = float(os.environ['HURRY_QUERY_TIMING'])
    except (ValueError, TypeError):
        pass

_perf_counter = time.perf_counter


class Locator:

    def __init__(self, container, get):
        self.container = container
        self.get = get

    def __call__(self, oid):
        contained = self.get(oid)
        return located(
            LocationProxy(contained), self.container, contained.__name__)


@implementer(interfaces.IResults)
class Results:

    def __init__(self, context, all_results, selected_results,
                 wrapper=None, locate_to=None):
        self.context = context
        self.locate_to = locate_to
        self.wrapper = wrapper
        self.__all = all_results
        self.__selected = selected_results

    @Lazy
    def get(self):
        get = getUtility(IIntIds, '', self.context).getObject
        if self.wrapper is not None:
            get = (lambda get: lambda id: self.wrapper(get(id)))(get)
        if self.locate_to is not None:
            return Locator(self.locate_to, get)
        return get

    @property
    def total(self):
        return len(self.__all)

    @property
    def count(self):
        return len(self.__selected)

    def first(self):
        for uid in self.__selected:
            return self.get(uid)

    def __len__(self):
        return len(self.__selected)

    def __iter__(self):
        for uid in self.__selected:
            yield self.get(uid)


@implementer(interfaces.IResults)
class NoResults:

    count = 0
    total = 0

    def first(self):
        return None

    def __len__(self):
        return 0

    def __iter__(self):
        return iter([])


no_results = NoResults()


class Timing:

    def __init__(self, key=None, order=0):
        self.key = key
        self.start = _perf_counter()
        self.start_order = order
        self.end = None
        self.end_order = None

    def done(self, order=0):
        self.end = _perf_counter()
        self.end_order = order

    @property
    def total(self):
        if self.end is not None:
            return self.end - self.start
        return None


class TimingAwareCache:

    def __init__(self, cache):
        self.cache = cache
        self.timing = {}
        self.count = 0
        self.post = None

    def start_post(self):
        self.post = Timing()

    def end_post(self):
        self.post.done()

    def __setitem__(self, key, value):
        self.cache[key] = value
        timing = self.timing.get(key)
        if timing is not None:
            timing.done(self.count)
            self.count += 1

    def get(self, key):
        value = self.cache.get(key)
        if value is None:
            self.timing[key] = Timing(key, self.count)
            self.count += 1
        return value

    def report(self, over=0):
        all_timing = sorted(self.timing.values(), key=lambda t: t.start_order)
        if not len(all_timing):
            return  # pragma: no cover (peephole optimizer interferes)
        total_post = 0 if self.post is None else self.post.total
        total_terms = all_timing[0].total
        if (total_terms + total_post) < over:
            return
        indent = 0
        order = [all_timing[0].end_order]
        logger.info(
            'Catalog query took {:.4f}s for terms, {:.4f}s to finish.'.format(
                total_terms, total_post))
        for timing in all_timing:
            if order == [] or timing.start_order < order[-1]:
                indent += 4
                order.append(timing.end_order)
            total = timing.total and f'{timing.total:.4f}s' or '?'
            logger.info(
                '{} {}: {}.'.format(
                    ' ' * indent, total, str(timing.key)))
            if timing.end_order and len(order) \
               and timing.end_order > order[-1]:
                indent -= 4
                order.pop()


@implementer(interfaces.IQuery)
class Query:

    def searchResults(
            self, query, context=None, sort_field=None, limit=None,
            reverse=False, start=0, caching=None, timing=HURRY_QUERY_TIMING,
            wrapper=None, locate_to=None):

        if context is None:
            context = getSiteManager()
        else:
            context = IComponentLookup(context)

        if caching in (True, False, None):
            cache = {}
        else:
            # A custom cache object was injected, use it.
            cache = caching

        timer = None
        if timing:
            timer = cache = TimingAwareCache(cache)
        all_results = query.cached_apply(cache, context)
        if not all_results:
            if timer is not None:
                timer.report(over=timing)
            return no_results

        if timer is not None:
            timer.start_post()

        is_iterator = False
        if sort_field is not None:
            # Like in zope.catalog's searchResults we require the given
            # index to sort on to provide IIndexSort. We bail out if
            # the index does not.
            if not IIndexSort.providedBy(sort_field):
                assert isinstance(sort_field, tuple) and len(sort_field) == 2
                catalog_name, index_name = sort_field
                catalog = getUtility(ICatalog, catalog_name, context)
                sort_field = catalog[index_name]
                if not IIndexSort.providedBy(sort_field):
                    raise ValueError(
                        'Index {} in catalog {} does not support '
                        'sorting.'.format(index_name, catalog_name))
            sort_limit = None
            if limit:
                sort_limit = limit
                if start:
                    sort_limit += start
            selected_results = sort_field.sort(
                all_results,
                limit=sort_limit,
                reverse=reverse)
            if start:
                selected_results = itertools.islice(
                    selected_results, start, None)
            is_iterator = True
        else:
            # There's no sort_field given. We still allow to reverse
            # and/or limit the resultset. This mimics zope.catalog's
            # searchResults semantics.
            selected_results = all_results
            if reverse:
                selected_results = reversed(selected_results)
                is_iterator = True
            if limit or start:
                slice_end = limit and start + limit or None
                selected_results = itertools.islice(
                    selected_results, start, slice_end)
                is_iterator = True

        if is_iterator:
            selected_results = list(selected_results)

        if timer is not None:
            timer.end_post()
            timer.report(over=timing)

        return Results(
            context, all_results, selected_results, wrapper, locate_to)


@implementer(interfaces.ITerm)
class Term:

    def key(self, context=None):
        raise NotImplementedError()

    def apply(self, cache, context=None):
        raise NotImplementedError()

    def cached_apply(self, cache, context=None):
        try:
            key = self.key(context)
        except NotImplementedError:
            return self.apply(cache, context)
        cached = cache.get(key)
        if cached is not None:
            return cached
        result = self.apply(cache, context)
        cache[key] = result
        return result

    def __and__(self, other):
        return And(self, other)

    def __rand__(self, other):
        return And(other, self)

    def __or__(self, other):
        return Or(self, other)

    def __ror__(self, other):
        return Or(other, self)

    def __invert__(self):
        return Not(self)


class And(Term):

    def __init__(self, *terms, **kwargs):
        self.terms = terms
        self.weighted = kwargs.get('weighted', False)

    def apply(self, cache, context=None):
        results = []
        for term in self.terms:
            result = term.cached_apply(cache, context)
            if not result:
                # Empty results
                return result
            results.append(result)

        if len(results) == 1:
            return results[0]

        # Sort results to have the smallest set first to optimize the
        # set operation.
        results.sort(key=lambda r: len(r))

        result = results.pop(0)
        for r in results:
            if self.weighted:
                _, result = weightedIntersection(result, r)
            else:
                result = intersection(result, r)
            if not result:
                # Empty results
                return result

        return result

    def key(self, context=None):
        return ('and',) + tuple(term.key(context) for term in self.terms)


class Or(Term):

    def __init__(self, *terms):
        self.terms = terms

    def apply(self, cache, context=None):
        results = []
        for term in self.terms:
            result = term.cached_apply(cache, context)
            # empty results
            if not result:
                continue
            results.append(result)

        if len(results) == 0:
            return IFSet()
        if len(results) == 1:
            return results[0]

        return multiunion(results)

    def key(self, context=None):
        return ('or',) + tuple(term.key(context) for term in self.terms)


class Difference(Term):

    def __init__(self, *terms):
        self.terms = terms

    def apply(self, cache, context=None):
        results = []

        for index, term in enumerate(self.terms):
            result = term.cached_apply(cache, context)
            # If we do not have any results for the first index, just
            # return an empty set and stop here.
            if not result:
                if not index:
                    return IFSet()
                continue  # pragma: no cover (peephole optimizer interferes)
            results.append(result)

        result = results.pop(0)
        for other in results:
            result = difference(result, other)
            if not result:
                # Empty results
                return result
        return result

    def key(self, context=None):
        return ('difference',) + tuple(
            term.key(context) for term in self.terms)


class Not(Term):
    # XXX This term will load all the intids of your application
    # resulting in major and heavy performance issues. It is advised
    # not to use it.

    def __init__(self, term):
        self.term = term

    def apply(self, cache, context=None):
        return difference(self._all(), self.term.cached_apply(cache, context))

    def _all(self):
        return IFSet(uid for uid in getUtility(IIntIds))

    def key(self, context=None):
        return ('not', self.term.key(context))


class Objects(Term):

    def __init__(self, objects):
        self.objects = objects
        self._ids = None

    def ids(self, context=None):
        if self._ids is None:
            get_uid = getUtility(IIntIds, '', context).getId
            self._ids = tuple(get_uid(o) for o in self.objects)
        return self._ids

    def apply(self, cache, context=None):
        return IFSet(self.ids(context))

    def key(self, context=None):
        return ('objects', self.ids(context))


class Ids(Term):

    def __init__(self, *ids):
        self.ids = ids

    def apply(self, cache, context=None):
        return IFSet(self.ids)

    def key(self, context=None):
        return ('ids', self.ids)


class IndexTerm(Term):

    def __init__(self, catalog_name__and__index_name):
        self.catalog_name = catalog_name__and__index_name[0]
        self.index_name = catalog_name__and__index_name[1]

    def getIndex(self, context):
        catalog = getUtility(ICatalog, self.catalog_name, context)
        index = catalog[self.index_name]
        return index


class Text(IndexTerm):

    def __init__(self, index_id, text):
        super().__init__(index_id)
        self.text = text

    def getIndex(self, context):
        index = super().getIndex(context)
        assert ITextIndex.providedBy(index)
        return index

    def apply(self, cache, context=None):
        index = self.getIndex(context)
        try:
            return index.apply(self.text)
        except ParseError:
            logger.error(
                f'search text "{self.text}" yielded a ParseError')
            return IFSet()

    def key(self, context=None):
        return ('text', self.catalog_name, self.index_name, self.text)


class FieldTerm(IndexTerm):

    def getIndex(self, context):
        index = super().getIndex(context)
        assert IFieldIndex.providedBy(index)
        return index


class Eq(FieldTerm):

    def __init__(self, index_id, value):
        assert value is not None
        super().__init__(index_id)
        self.value = value

    def apply(self, cache, context=None):
        return self.getIndex(context).apply((self.value, self.value))

    def key(self, context=None):
        return ('equal', self.catalog_name, self.index_name, self.value)


class NotEq(FieldTerm):

    def __init__(self, index_id, value):
        super().__init__(index_id)
        self.value = value

    def apply(self, cache, context=None):
        index = self.getIndex(context)
        values = index.apply((None, None))
        matches = index.apply((self.value, self.value))
        return difference(values, matches)

    def key(self, context=None):
        return ('not equal', self.catalog_name, self.index_name, self.value)


class All(FieldTerm):

    def apply(self, cache, context=None):
        return self.getIndex(context).apply((None, None))

    def key(self, context=None):
        return ('all', self.catalog_name, self.index_name)


class Between(FieldTerm):

    def __init__(self, index_id,
                 minimum=None, maximum=None):
        super().__init__(index_id)
        self.options = (minimum, maximum)

    def apply(self, cache, context=None):
        return self.getIndex(context).apply(self.options)

    def key(self, context=None):
        return ('between', self.catalog_name, self.index_name, self.options)


class Ge(Between):

    def __init__(self, index_id, min_value):
        super().__init__(index_id, min_value, None)


class Le(Between):

    def __init__(self, index_id, max_value):
        super().__init__(index_id, None, max_value)


class In(FieldTerm):

    def __init__(self, index_id, values):
        assert None not in values
        super().__init__(index_id)
        self.values = tuple(values)

    def apply(self, cache, context=None):
        results = []
        index = self.getIndex(context)
        for value in self.values:
            r = index.apply((value, value))
            # empty results
            if not r:
                continue
            results.append(r)

        if len(results) == 0:
            return IFSet()
        if len(results) == 1:
            return results[0]

        return multiunion(results)

    def key(self, context=None):
        return ('in', self.catalog_name, self.index_name, self.values)
