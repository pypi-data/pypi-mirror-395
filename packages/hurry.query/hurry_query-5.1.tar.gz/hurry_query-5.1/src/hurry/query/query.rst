Hurry Query
===========

The hurry query system for the zope.catalog builds on its catalog
indexes, as well as the indexes in zc.catalog. It is in part inspired
by AdvancedQuery for Zope 2 by Dieter Maurer, though has an independent
origin.

You can have a look at the doc tests in the package for more
information regarding the usage.

.. contents::

Setup
-----

Let's define a simple content object. First its interface:

  >>> from zope.interface import Interface, Attribute, implementer
  >>> class IContent(Interface):
  ...     f1 = Attribute('f1')
  ...     f2 = Attribute('f2')
  ...     f3 = Attribute('f3')
  ...     f4 = Attribute('f4')
  ...     t1 = Attribute('t1')
  ...     t2 = Attribute('t2')

And its implementation:

  >>> import functools
  >>> from zope.container.contained import Contained
  >>> @functools.total_ordering
  ... @implementer(IContent)
  ... class Content(Contained):
  ...     def __init__(self, id, f1='', f2='', f3='', f4='', t1='', t2=''):
  ...         self.id = id
  ...         self.f1 = f1
  ...         self.f2 = f2
  ...         self.f3 = f3
  ...         self.f4 = f4
  ...         self.t1 = t1
  ...         self.t2 = t2
  ...     def __lt__(self, other):
  ...         return self.id < other.id
  ...     def __eq__(self, other):
  ...         return self.id == other.id
  ...     def __repr__(self):
  ...         return '<Content "{}">'.format(self.id)

The id attribute is just so we can identify objects we find again
easily. By including the __cmp__ method we make sure search results
can be stably sorted.

We use a fake int id utility here so we can test independent of
the full-blown zope environment:

  >>> from zope import interface
  >>> import zope.intid.interfaces
  >>> @interface.implementer(zope.intid.interfaces.IIntIds)
  ... class DummyIntId(object):
  ...     MARKER = '__dummy_int_id__'
  ...     def __init__(self):
  ...         self.counter = 0
  ...         self.data = {}
  ...     def register(self, obj):
  ...         intid = getattr(obj, self.MARKER, None)
  ...         if intid is None:
  ...             setattr(obj, self.MARKER, self.counter)
  ...             self.data[self.counter] = obj
  ...             intid = self.counter
  ...             self.counter += 1
  ...         return intid
  ...     def getId(self, obj):
  ...         return getattr(obj, self.MARKER)
  ...     def getObject(self, intid):
  ...         return self.data[intid]
  ...     def __iter__(self):
  ...         return iter(self.data)
  >>> intid = DummyIntId()
  >>> from zope.component import provideUtility
  >>> provideUtility(intid, zope.intid.interfaces.IIntIds)

Now let's register a catalog:

  >>> from zope.catalog.interfaces import ICatalog
  >>> from zope.catalog.catalog import Catalog
  >>> catalog = Catalog()
  >>> provideUtility(catalog, ICatalog, 'catalog1')

And set it up with various indexes:

  >>> from zope.catalog.field import FieldIndex
  >>> from zope.catalog.text import TextIndex
  >>> catalog['f1'] = FieldIndex('f1', IContent)
  >>> catalog['f2'] = FieldIndex('f2', IContent)
  >>> catalog['f3'] = FieldIndex('f3', IContent)
  >>> catalog['f4'] = FieldIndex('f4', IContent)
  >>> catalog['t1'] = TextIndex('t1', IContent)
  >>> catalog['t2'] = TextIndex('t2', IContent)

Now let's create some objects so that they'll be cataloged:

  >>> content = [
  ... Content(1, 'a', 'b', 'd'),
  ... Content(2, 'a', 'c'),
  ... Content(3, 'X', 'c'),
  ... Content(4, 'a', 'b', 'e'),
  ... Content(5, 'X', 'b', 'e'),
  ... Content(6, 'Y', 'Z')]

And catalog them now:

  >>> for entry in content:
  ...     catalog.index_doc(intid.register(entry), entry)

Now let's register a query utility:

  >>> from hurry.query.query import Query
  >>> from hurry.query.interfaces import IQuery
  >>> provideUtility(Query(), IQuery)

Set up some code to make querying and display the result
easy:

  >>> from zope.component import getUtility
  >>> from hurry.query.interfaces import IQuery
  >>> def displayQuery(q, context=None):
  ...     query = getUtility(IQuery)
  ...     r = query.searchResults(q, context)
  ...     return [e.id for e in sorted(list(r))]

FieldIndex Queries
------------------

We can query for all objects indexed in this index:

  >>> from hurry.query import All
  >>> f1 = ('catalog1', 'f1')
  >>> displayQuery(All(f1))
  [1, 2, 3, 4, 5, 6]

Now for a query where f1 equals a:

  >>> from hurry.query import Eq
  >>> f1 = ('catalog1', 'f1')
  >>> displayQuery(Eq(f1, 'a'))
  [1, 2, 4]

Not equals (this is more efficient than the generic ~ operator):

  >>> from hurry.query import NotEq
  >>> displayQuery(NotEq(f1, 'a'))
  [3, 5, 6]

Testing whether a field is in a set:

  >>> from hurry.query import In
  >>> displayQuery(In(f1, ['a', 'X']))
  [1, 2, 3, 4, 5]

Whether documents are in a specified range:

  >>> from hurry.query import Between
  >>> displayQuery(Between(f1, 'X', 'Y'))
  [3, 5, 6]

You can leave out one end of the range:

  >>> displayQuery(Between(f1, 'X', None)) # 'X' < 'a'
  [1, 2, 3, 4, 5, 6]
  >>> displayQuery(Between(f1, None, 'X'))
  [3, 5]

You can also use greater-equals and lesser-equals for the same purpose:

  >>> from hurry.query import Ge, Le
  >>> displayQuery(Ge(f1, 'X'))
  [1, 2, 3, 4, 5, 6]
  >>> displayQuery(Le(f1, 'X'))
  [3, 5]

It's also possible to use not with the ~ operator:

  >>> displayQuery(~Eq(f1, 'a'))
  [3, 5, 6]

Using and (&):

  >>> f2 = ('catalog1', 'f2')
  >>> displayQuery(Eq(f1, 'a') & Eq(f2, 'b'))
  [1, 4]

Using or (|):

  >>> displayQuery(Eq(f1, 'a') | Eq(f2, 'b'))
  [1, 2, 4, 5]

These can be chained:

  >>> displayQuery(Eq(f1, 'a') & Eq(f2, 'b') & Between(f1, 'a', 'b'))
  [1, 4]
  >>> displayQuery(Eq(f1, 'a') | Eq(f1, 'X') | Eq(f2, 'b'))
  [1, 2, 3, 4, 5]

And nested:

  >>> displayQuery((Eq(f1, 'a') | Eq(f1, 'X')) & (Eq(f2, 'b') | Eq(f2, 'c')))
  [1, 2, 3, 4, 5]

"and" and "or" can also be spelled differently:

  >>> from hurry.query import And, Or
  >>> displayQuery(And(Eq(f1, 'a'), Eq(f2, 'b')))
  [1, 4]
  >>> displayQuery(Or(Eq(f1, 'a'), Eq(f2, 'b')))
  [1, 2, 4, 5]

Combination of In and &
-----------------------

A combination of 'In' and '&':

  >>> displayQuery(In(f1, ['a', 'X', 'Y', 'Z']))
  [1, 2, 3, 4, 5, 6]
  >>> displayQuery(In(f1, ['Z']))
  []
  >>> displayQuery(In(f1, ['a', 'X', 'Y', 'Z']) & In(f1, ['Z']))
  []


SetIndex queries
----------------

The SetIndex is defined in zc.catalog.

  >>> from hurry.query import set

Let's make a catalog which uses it:

  >>> intid = DummyIntId()
  >>> provideUtility(intid, zope.intid.interfaces.IIntIds)
  >>> from zope.catalog.interfaces import ICatalog
  >>> from zope.catalog.catalog import Catalog
  >>> catalog = Catalog()
  >>> provideUtility(catalog, ICatalog, 'catalog1')
  >>> from zc.catalog.catalogindex import SetIndex
  >>> catalog['f1'] = SetIndex('f1', IContent)
  >>> catalog['f2'] = FieldIndex('f2', IContent)

First let's set up some new data:

  >>> content = [
  ... Content(1, ['a', 'b', 'c'], 1),
  ... Content(2, ['a'], 1),
  ... Content(3, ['b'], 1),
  ... Content(4, ['c', 'd'], 2),
  ... Content(5, ['b', 'c'], 2),
  ... Content(6, ['a', 'c'], 2),
  ... Content(7, ['z'], 2),
  ... Content(8, [], 2)]  # no value, so not indexed.

And catalog them now:

  >>> for entry in content:
  ...     catalog.index_doc(intid.register(entry), entry)

We can query for all indexes objects:

  >>> displayQuery(set.All(f1))
  [1, 2, 3, 4, 5, 6, 7]

Now do a a 'any of' query, which returns all documents that
contain any of the values listed:

  >>> displayQuery(set.AnyOf(f1, ['a', 'c']))
  [1, 2, 4, 5, 6]
  >>> displayQuery(set.AnyOf(f1, ['c', 'b']))
  [1, 3, 4, 5, 6]
  >>> displayQuery(set.AnyOf(f1, ['a']))
  [1, 2, 6]

Do a 'all of' query, which returns all documents that
contain all of the values listed:

  >>> displayQuery(set.AllOf(f1, ['a']))
  [1, 2, 6]
  >>> displayQuery(set.AllOf(f1, ['a', 'b']))
  [1]
  >>> displayQuery(set.AllOf(f1, ['a', 'c']))
  [1, 6]

The next interesting set of queries allows you to make evaluations of the
values. For example, you can ask for all objects between a certain set of
values:

  >>> displayQuery(set.SetBetween(f1, 'a', 'c'))
  [1, 2, 3, 4, 5, 6]

  >>> displayQuery(set.SetBetween(f1, 'a', 'c', exclude_min=True))
  [1, 3, 4, 5, 6]

  >>> displayQuery(set.SetBetween(f1, 'b', 'c', exclude_max=True))
  [1, 3, 5]

  >>> displayQuery(set.SetBetween(f1, 'a', 'c',
  ...                             exclude_min=True, exclude_max=True))
  [1, 3, 5]

You can also leave out one end of the range:

  >>> displayQuery(set.SetBetween(f1, 'c', None))
  [1, 4, 5, 6, 7]
  >>> displayQuery(set.SetBetween(f1, None, 'c', exclude_max=True))
  [1, 2, 3, 5, 6]

You can only pass True or False to the exclude_min and exclude_max parameters:

  >>> displayQuery(set.SetBetween(f1, 'a', 'c', exclude_min=None))
  Traceback (most recent call last):
  ...
  ValueError: Use a boolean for exclude_min

  >>> displayQuery(set.SetBetween(f1, 'a', 'c', exclude_max=None))
  Traceback (most recent call last):
  ...
  ValueError: Use a boolean for exclude_max

You can chain set queries:

  >>> displayQuery(set.AnyOf(f1, ['a']) & Eq(f2, 1))
  [1, 2]

The ``set` module also supports ``zc.catalog`` extents. The first query is
``ExtentAny``, which returns all douments matching the extent. If the the
extent is ``None``, all document ids are returned:

  >>> displayQuery(set.ExtentAny(f1, None))
  [1, 2, 3, 4, 5, 6, 7]

If we now create an extent that is only in the scope of the first four
documents,

  >>> from zc.catalog.extentcatalog import FilterExtent
  >>> extent = FilterExtent(lambda extent, uid, obj: True)
  >>> for i in range(4):
  ...     extent.add(i, i)

then only the first four are returned:

  >>> displayQuery(set.ExtentAny(f1, extent))
  [1, 2, 3, 4]

The opposite query is the ``ExtentNone`` query, which returns all ids in the
extent that are *not* in the index:

  >>> id = intid.register(Content(9, 'b'))
  >>> id = intid.register(Content(10, 'c'))
  >>> id = intid.register(Content(11, 'a'))

  >>> extent = FilterExtent(lambda extent, uid, obj: True)
  >>> for i in range(11):
  ...     extent.add(i, i)

  >>> displayQuery(set.ExtentNone(f1, extent))
  [8, 9, 10, 11]


ValueIndex queries
------------------

The ``ValueIndex`` is defined in ``zc.catalog`` and provides a generalization
of the standard field index.

  >>> from hurry.query import value

Let's set up a catalog that uses this index. The ``ValueIndex`` is defined in
``zc.catalog``. Let's make a catalog which uses it:

  >>> intid = DummyIntId()
  >>> provideUtility(intid, zope.intid.interfaces.IIntIds)

  >>> from zope.catalog.interfaces import ICatalog
  >>> from zope.catalog.catalog import Catalog
  >>> catalog = Catalog()
  >>> provideUtility(catalog, ICatalog, 'catalog1')

  >>> from zc.catalog.catalogindex import ValueIndex
  >>> catalog['f1'] = ValueIndex('f1', IContent)

Next we set up some content data to fill the indices:

  >>> content = [
  ... Content(1, 'a'),
  ... Content(2, 'b'),
  ... Content(3, 'c'),
  ... Content(4, 'd'),
  ... Content(5, 'c'),
  ... Content(6, 'a')]

And catalog them now:

  >>> for entry in content:
  ...     catalog.index_doc(intid.register(entry), entry)

We query for all indexes objects:

  >>> f1 = ('catalog1', 'f1')
  >>> displayQuery(value.All(f1))
  [1, 2, 3, 4, 5, 6]

Let's now query for all objects where ``f1`` equals 'a':

  >>> f1 = ('catalog1', 'f1')
  >>> displayQuery(value.Eq(f1, 'a'))
  [1, 6]

Next, let's find all objects where ``f1`` does not equal 'a'; this is more
efficient than the generic ``~`` operator:

  >>> displayQuery(value.NotEq(f1, 'a'))
  [2, 3, 4, 5]

If all the items in the catalog satisfy the NotEq condition, the query
does not crash.

  >>> displayQuery(value.NotEq(f1, 'z'))
  [1, 2, 3, 4, 5, 6]

You can also query for all objects where the value of ``f1`` is in a set of
values:

  >>> displayQuery(value.In(f1, ['a', 'd']))
  [1, 4, 6]

The next interesting set of queries allows you to make evaluations of the
values. For example, you can ask for all objects between a certain set of
values:

  >>> displayQuery(value.Between(f1, 'a', 'c'))
  [1, 2, 3, 5, 6]

  >>> displayQuery(value.Between(f1, 'a', 'c', exclude_min=True))
  [2, 3, 5]

  >>> displayQuery(value.Between(f1, 'a', 'c', exclude_max=True))
  [1, 2, 6]

  >>> displayQuery(value.Between(f1, 'a', 'c',
  ...                            exclude_min=True, exclude_max=True))
  [2]

You can also leave out one end of the range:

  >>> displayQuery(value.Between(f1, 'c', None))
  [3, 4, 5]
  >>> displayQuery(value.Between(f1, None, 'c'))
  [1, 2, 3, 5, 6]

You can only pass True or False to the exclude_min and exclude_max parameters:

  >>> displayQuery(value.Between(f1, 'a', 'c', exclude_min=None))
  Traceback (most recent call last):
  ...
  ValueError: Use a boolean for exclude_min

  >>> displayQuery(value.Between(f1, 'a', 'c', exclude_max=None))
  Traceback (most recent call last):
  ...
  ValueError: Use a boolean for exclude_max

You can also use greater-equals and lesser-equals for the same purpose:

  >>> displayQuery(value.Ge(f1, 'c'))
  [3, 4, 5]
  >>> displayQuery(value.Le(f1, 'c'))
  [1, 2, 3, 5, 6]

You can chain value queries:

  >>> displayQuery(value.Ge(f1, 'c') & value.Le(f1, 'c'))
  [3, 5]

The ``value`` module also supports ``zc.catalog`` extents. The first query is
``ExtentAny``, which returns all douments matching the extent. If the the
extent is ``None``, all document ids are returned:

  >>> displayQuery(value.ExtentAny(f1, None))
  [1, 2, 3, 4, 5, 6]

If we now create an extent that is only in the scope of the first four
documents,

  >>> from zc.catalog.extentcatalog import FilterExtent
  >>> extent = FilterExtent(lambda extent, uid, obj: True)
  >>> for i in range(4):
  ...     extent.add(i, i)

then only the first four are returned:

  >>> displayQuery(value.ExtentAny(f1, extent))
  [1, 2, 3, 4]

The opposite query is the ``ExtentNone`` query, which returns all ids in the
extent that are *not* in the index:

  >>> id = intid.register(Content(7, 'b'))
  >>> id = intid.register(Content(8, 'c'))
  >>> id = intid.register(Content(9, 'a'))

  >>> extent = FilterExtent(lambda extent, uid, obj: True)
  >>> for i in range(9):
  ...     extent.add(i, i)

  >>> displayQuery(value.ExtentNone(f1, extent))
  [7, 8, 9]


Querying different indexes
--------------------------

It's possible to specify the context when creating a query. This context
determines which index will be searched.

First setup a second registry and second catalog and populate it:

  >>> catalog2 = Catalog()
  >>> from zope.interface.registry import Components
  >>> import zope.interface
  >>> import zope.interface.interfaces
  >>> intid1 = DummyIntId()
  >>> @zope.interface.implementer(zope.interface.interfaces.IComponentLookup)
  ... class MockSite(object):
  ...     def __init__(self):
  ...         self.registry = Components('components')
  ...     def queryUtility(self, interface, name='', default=None):
  ...         if name == '': return intid1
  ...         else: return catalog2
  ...     def getSiteManager(self):
  ...         return self.registry
  >>> from zope.component.hooks import setSite
  >>> site1 = MockSite()
  >>> setSite(site1)
  >>> catalog2['f1'] = FieldIndex('f1', IContent)
  >>> content = [
  ... Content(1,'A'),
  ... Content(2,'B'),]
  >>> for entry in content:
  ...     catalog2.index_doc(intid1.register(entry), entry)

Now we can query this catalog by specifying the context:

  >>> query = getUtility(IQuery)
  >>> displayQuery(Eq(f1, 'A'), context=site1)
  [1]

  >>> displayQuery(In(f1, ['A', 'B']), context=site1)
  [1, 2]

Sorting and limiting the results
--------------------------------

It's possible to have the resultset sorted on one of the fields in the query:

  >>> catalog = Catalog()
  >>> provideUtility(catalog, ICatalog, 'catalog1')
  >>> catalog['f1'] = FieldIndex('f1', IContent)
  >>> catalog['f2'] = FieldIndex('f2', IContent)
  >>> catalog['t'] = TextIndex('t1', IContent)

First let's set up some new data:

  >>> content = [
  ... Content(1, 'a', 2, t1='Beautiful is better than ugly.'),
  ... Content(2, 'a', 3, t1='Explicit is better than implicit'),
  ... Content(3, 'b', 9, t1='Simple is better than complex'),
  ... Content(4, 'c', 8, t1='Complex is better than complicated'),
  ... Content(5, 'c', 7, t1='Readability counts'),
  ... Content(6, 'a', 1, t1='Although practicality beats purity')]

And catalog them now:

  >>> for entry in content:
  ...     catalog.index_doc(intid.register(entry), entry)

Define a convenience function for quickly displaying a result set without
performing any sorting here ourselves.

  >>> def displayResult(q, context=None, **kw):
  ...     query = getUtility(IQuery)
  ...     r = query.searchResults(q, context, **kw)
  ...     return [e for e in r]

Without using sorting in the query itself, the resultset has an undefined
order. We "manually" sort the results here to have something testable.

  >>> f1 = ('catalog1', 'f1')
  >>> [r for r in sorted(displayResult(Eq(f1, 'a')))]
  [<Content "1">, <Content "2">, <Content "6">]

Now we sort on the f2 index.

  >>> f1 = ('catalog1', 'f1')
  >>> displayResult(Eq(f1, 'a'), sort_field=('catalog1', 'f2'))
  [<Content "6">, <Content "1">, <Content "2">]

Reverse the order.

  >>> f1 = ('catalog1', 'f1')
  >>> displayResult(Eq(f1, 'a'), sort_field=('catalog1', 'f2'), reverse=True)
  [<Content "2">, <Content "1">, <Content "6">]

We can limit the amount of found items.

  >>> f1 = ('catalog1', 'f1')
  >>> displayResult(Eq(f1, 'a'), sort_field=('catalog1', 'f2'), limit=2)
  [<Content "6">, <Content "1">]

  >>> f1 = ('catalog1', 'f1')
  >>> displayResult(Eq(f1, 'a'), sort_field=('catalog1', 'f2'), limit=2, start=1)
  [<Content "1">, <Content "2">]

We can limit the reversed resultset too.

  >>> f1 = ('catalog1', 'f1')
  >>> displayResult(
  ...   Eq(f1, 'a'), sort_field=('catalog1', 'f2'), limit=2, reverse=True)
  [<Content "2">, <Content "1">]

You can directly pass the index as a sort field instead of a tuple:

  >>> f1 = ('catalog1', 'f1')
  >>> displayResult(Eq(f1, 'a'), sort_field=catalog['f2'])
  [<Content "6">, <Content "1">, <Content "2">]

Whenever a field is used for sorting that does not support is, an error is
raised.

  >>> f1 = ('catalog1', 'f1')
  >>> displayResult(Eq(f1, 'a'), sort_field=('catalog1', 't'))
  Traceback (most recent call last):
  ...
  ValueError: Index t in catalog catalog1 does not support sorting.

The resultset can still be reversed and limited even if there's no sort_field
given (Note that the actual order of the result set when not using explicit
sorting is not defined. In this test it is assumed that the natural order of
the tested index is deterministic enough to be used as a proper test).

  >>> f1 = ('catalog1', 'f1')
  >>> displayResult(Eq(f1, 'a'), limit=2)
  [<Content "1">, <Content "2">]

  >>> f1 = ('catalog1', 'f1')
  >>> displayResult(Eq(f1, 'a'), start=1)
  [<Content "2">, <Content "6">]

  >>> f1 = ('catalog1', 'f1')
  >>> displayResult(Eq(f1, 'a'), start=1, limit=1)
  [<Content "2">]

  >>> f1 = ('catalog1', 'f1')
  >>> displayResult(Eq(f1, 'a'), limit=2, reverse=True)
  [<Content "6">, <Content "2">]

Result counters
---------------

Result objects provide metadata about the result.

Define a convenience function for obtaining a result.

  >>> def getResult(q, context=None, **kw):
  ...     query = getUtility(IQuery)
  ...     return query.searchResults(q, context, **kw)

Performing a query with a sort_field gives a well-defined result:

  >>> f1 = ('catalog1', 'f1')
  >>> result = getResult(Eq(f1, 'a'), sort_field=catalog['f1'])
  >>> [e for e in result]
  [<Content "1">, <Content "2">, <Content "6">]

We can access 'total' and 'count' properties, and 'first()' on the result:

  >>> result.total
  3
  >>> result.count
  3
  >>> result.first()
  <Content "1">

Changing 'start' is reflected in the returned data:

>>> result = getResult(Eq(f1, 'a'), sort_field=catalog['f1'], start=1)
  >>> [e for e in result]
  [<Content "2">, <Content "6">]

It also changes 'count' and 'first()':

  >>> result.count
  2
  >>> result.first()
  <Content "2">

But 'total' still reflects all matches, including the hidden first one:

  >>> result.total
  3

Adding a limit:

  >>> result = getResult(Eq(f1, 'a'), sort_field=catalog['f1'], start=1,
  ...                    limit=1)
  >>> [e for e in result]
  [<Content "2">]
  >>> result.total
  3
  >>> result.count
  1
  >>> result.first()
  <Content "2">

The same accessors are available on an empty result:

  >>> result = getResult(Eq(f1, 'foo'), sort_field=catalog['f1'])
  >>> [e for e in result]
  []
  >>> result.total
  0
  >>> result.count
  0
  >>> result.first() is None
  True

Wrapper
-------

You can define a wrapper to be called on each result:

  >>> from zope.location import Location
  >>> class Wrapper(Location):
  ...    def __init__(self, parent):
  ...       self.parent = parent
  ...    def __repr__(self):
  ...       return '<Wrapper "{}">'.format(self.parent.id)

  >>> f1 = ('catalog1', 'f1')
  >>> displayResult(Eq(f1, 'a'), wrapper=Wrapper)
  [<Wrapper "1">, <Wrapper "2">, <Wrapper "6">]

Locate to
---------

You can define a location where the results should be located with a proxy:

  >>> def displayParent(q, context=None, **kw):
  ...     query = getUtility(IQuery)
  ...     r = query.searchResults(q, context, **kw)
  ...     return [(e.__parent__, e) or None for e in r]

  >>> f1 = ('catalog1', 'f1')
  >>> displayParent(Eq(f1, 'a'), limit=2)
  [(None, <Content "1">), (None, <Content "2">)]

  >>> parent = Content('parent')
  >>> displayParent(Eq(f1, 'a'), limit=2, locate_to=parent)
  [(<Content "parent">, <Content "1">), (<Content "parent">, <Content "2">)]

This can be used with a wrapper:

  >>> displayParent(Eq(f1, 'a'), limit=2, wrapper=Wrapper, locate_to=parent)
  [(<Content "parent">, <Wrapper "1">), (<Content "parent">, <Wrapper "2">)]

Text index
----------

You can search on text, here all the items that contains better:

  >>> from hurry.query import Text
  >>> t1 = ('catalog1', 't')
  >>> displayResult(Text(t1, 'better'))
  [<Content "1">, <Content "2">, <Content "3">, <Content "4">]

Invalid text query returns an empty results:

  >>> displayResult(Text(t1, '?*'))
  []


Other terms
-----------

You can do differences, here all the items that contains better but do
have a as f1:

  >>> from hurry.query import Difference
  >>> displayResult(Difference(Text(t1, 'better'), Eq(f1, 'a')))
  [<Content "3">, <Content "4">]


There is a special term that allows to mix objects with catalog
queries:

  >>> from hurry.query import Objects
  >>> displayResult(Objects(content))
  [<Content "1">, <Content "2">, <Content "3">, <Content "4">, <Content "5">, <Content "6">]

There is a special term that allows querying objects by intid:

  >>> from hurry.query import Ids
  >>> displayResult(Ids())
  []

  >>> all_intids = [intid.getId(x) for x in content]
  >>> displayResult(Ids(*all_intids))
  [<Content "1">, <Content "2">, <Content "3">, <Content "4">, <Content "5">, <Content "6">]

  >>> odd_intids = [intid.getId(x) for x in content if x.id % 2]
  >>> displayResult(Ids(*odd_intids))
  [<Content "1">, <Content "3">, <Content "5">]
