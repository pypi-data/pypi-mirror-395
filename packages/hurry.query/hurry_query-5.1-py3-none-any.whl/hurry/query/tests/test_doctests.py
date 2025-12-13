import doctest


def test_suite():
    return doctest.DocFileSuite('../query.rst')
