##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
import html
import os

from setuptools import setup


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        text = f.read()
    return html.escape(text)


tests_require = [
    'testfixtures',
    'zope.container',
]

setup(
    name="hurry.query",
    version='5.1',
    author='Infrae',
    author_email='zope-dev@zope.dev',
    description="Higher level query system for zope.catalog.",
    url="https://github.com/zopefoundation/hurry.query",
    long_description=(read('README.rst') +
                      '\n\n' +
                      read('CHANGES.rst')),
    license='ZPL-2.1',
    keywords="zope zope3 catalog index query",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Framework :: Zope :: 3',
    ],
    package_data={
        '': ['*.txt', '*.zcml'],
    },
    zip_safe=False,
    python_requires='>=3.10',
    install_requires=[
        'BTrees',
        'setuptools',
        'transaction',
        'zc.catalog',
        'zope.cachedescriptors',
        'zope.catalog',
        'zope.component',
        'zope.index',
        'zope.interface',
        'zope.intid',
        'zope.location',
    ],
    extras_require={'test': tests_require},
)
