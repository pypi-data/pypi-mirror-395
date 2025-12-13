##############################################################################
#
# Copyright (c) 2005-2008 Zope Foundation and Contributors.
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
"""Query terms for zc.catalog's ValueIndex

$Id$
"""
from zc.catalog.interfaces import IValueIndex

from hurry.query import query


class ValueTerm(query.IndexTerm):

    def getIndex(self, context):
        index = super().getIndex(context)
        assert IValueIndex.providedBy(index)
        return index


class Eq(ValueTerm):

    def __init__(self, index_id, value):
        assert value is not None
        super().__init__(index_id)
        self.value = value

    def apply(self, cache, context=None):
        return self.getIndex(context).apply({'any_of': (self.value,)})

    def key(self, context=None):
        return ('equal', self.catalog_name, self.index_name, self.value)


class NotEq(ValueTerm):

    def __init__(self, index_id, value):
        super().__init__(index_id)
        self.value = value

    def apply(self, cache, context=None):
        index = self.getIndex(context)
        values = list(index.values())
        # the remove method produces a value error when the value to
        # be removed is not in the list in the first place.  Having a
        # try/except clause is more efficent than first searching the
        # list for the value to remove.
        try:
            values.remove(self.value)
        except ValueError:
            pass
        return index.apply({'any_of': values})

    def key(self, context=None):
        return ('not equal', self.catalog_name, self.index_name, self.value)


class All(ValueTerm):

    def apply(self, cache, context=None):
        return self.getIndex(context).apply({'any': None})

    def key(self, context=None):
        return ('all', self.catalog_name, self.index_name)


class Between(ValueTerm):

    def __init__(self, index_id, min_value=None, max_value=None,
                 exclude_min=False, exclude_max=False):
        super().__init__(index_id)
        if exclude_min not in {True, False}:
            raise ValueError("Use a boolean for exclude_min")
        if exclude_max not in {True, False}:
            raise ValueError("Use a boolean for exclude_max")
        self.options = (min_value, max_value, exclude_min, exclude_max)

    def apply(self, cache, context=None):
        return self.getIndex(context).apply({'between': self.options})

    def key(self, context=None):
        return ('between', self.catalog_name, self.index_name, self.options)


class Ge(Between):

    def __init__(self, index_id, min_value):
        super().__init__(index_id, min_value=min_value)


class Le(Between):

    def __init__(self, index_id, max_value):
        super().__init__(index_id, max_value=max_value)


class In(ValueTerm):

    def __init__(self, index_id, values):
        assert None not in values
        super().__init__(index_id)
        self.values = tuple(values)

    def apply(self, cache, context=None):
        return self.getIndex(context).apply({'any_of': self.values})

    def key(self, context=None):
        return ('in', self.catalog_name, self.index_name, self.values)


class ExtentAny(ValueTerm):
    """Any ids in the extent that are indexed by this index."""

    def __init__(self, index_id, extent):
        super().__init__(index_id)
        self.extent = extent

    def apply(self, cache, context=None):
        return self.getIndex(context).apply({'any': self.extent})


class ExtentNone(ValueTerm):
    """Any ids in the extent that are not indexed by this index."""

    def __init__(self, index_id, extent):
        super().__init__(index_id)
        self.extent = extent

    def apply(self, cache, context=None):
        return self.getIndex(context).apply({'none': self.extent})
