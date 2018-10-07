# nxpy_core -------------------------------------------------------------------

# Copyright Nicola Musatti 2018
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy/tree/master/libs/core. -----------------

r"""
Packaging information.

"""

import codecs
import os

from setuptools import setup

lib_name = 'nxpy_core'

here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here,'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=lib_name,
    version="1.0.0",
    author="Nicola Musatti",
    author_email="nicola.musatti@gmail.com",
    description="Infrastructure common to the Nxpy libraries",
    project_urls={
        "Documentation": "https://nxpy.readthedocs.io/en/latest/core.html",
        "Source Code": "https://github.com/nmusatti/nxpy/tree/master/libs/core",
    },
    license="Boost Software License 1.0 (BSL-1.0)",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Boost Software License 1.0 (BSL-1.0)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
    ],
    namespace_packages=['nxpy', 'nxpy.core'],
    packages=['nxpy.core.error', 'nxpy.core._impl'],
    install_requires=[
    ],
)