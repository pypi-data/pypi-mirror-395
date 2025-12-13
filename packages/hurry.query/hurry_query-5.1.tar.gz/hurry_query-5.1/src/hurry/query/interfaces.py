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
"""Query interfaces
"""

from zope.interface import Attribute
from zope.interface import Interface


class IQuery(Interface):

    def searchResults(
            query, context=None, sort_field=None, limit=None, reverse=False,
            start=0, caching=False):
        """Query indexes.

        The query argument is a query composed of terms. Optionally
        provide the `context` parameter for the component lookups.

        Optionally provide a `sort_field` tuple that determines the
        index used to sort the result set with. This index is required
        to provide IIndexSort.

        Optionally provide a `limit` parameter to limit the result set
        to the given size.

        Optionally provide a `reverse` parameter to reverse the order
        of the result set.

        Optionally provide a `start` parameter to ignore the first
        result in set to the given start position.

        Optionally provide a `caching` parameter to cache terms result
        across multiple search queries. Accepted parameter values are:

            `True` for `threading.local` based and transaction boundary-aware
            caching. The cache for multiple `searchResults()` calls is
            invalidated at the end of the transaction.

            `False` to cache only for individual `searchResults()` calls.

            Or a `dict`-like object where invalidation is handled by the
            caller of the multiple `searchResults()` call.
        """


class ITerm(Interface):

    def key(context=None):
        """Return a unique key for this term.
        """

    def apply(cache, context=None):
        """Search and return the results for this term as an IFSet or
        something compatible with it.
        """

    def cached_apply(cache, context=None):
        """Look up in the cache and return results or apply the term if needed.
        """


class IResults(Interface):

    total = Attribute(
        'Total number of results (without start/limit restrictions)')

    count = Attribute(
        'Number of results (with start/limit restrictions)')

    def first():
        """Return only the first result of the query or None.
        """

    def __len__():
        """Return the number of results (with start/limit restrictions), that
        is the same than count.
        """

    def __iter__():
        """Iterate over the matching objects.
        """
