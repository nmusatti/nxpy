# nxpy ------------------------------------------------------------------------

# Copyright Nicola Musatti 2018 - 2021
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy. ---------------------------------------

r"""
Packaging information.

Note that this setup is only used for development and testing.
A single package including all the libraries is not currently available.

"""

from __future__ import absolute_import

import codecs
import os
import subprocess
import sys

from six import iteritems

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info

PACKAGE_NAME = 'Nxpy'
SOURCES = {
  'nxpy_abstract'               : 'libs/abstract',
  'nxpy_backup_file'            : 'libs/backup_file',
  'nxpy_command'                : 'libs/command',
  'nxpy_core'                   : 'libs/core',
  'nxpy_file'                   : 'libs/file',
  'nxpy_file_object'            : 'libs/file_object',
  'nxpy_maven'                  : 'libs/maven',
  'nxpy_memo'                   : 'libs/memo',
  'nxpy_nonblocking_subprocess' : 'libs/nonblocking_subprocess',
  'nxpy_past'                   : 'libs/past',
  'nxpy_path'                   : 'libs/path',
  'nxpy_ply'                    : 'libs/ply',
  'nxpy_sequence'               : 'libs/sequence',
  'nxpy_sort'                   : 'libs/sort',
  'nxpy_svn'                    : 'libs/svn',
  'nxpy_temp_file'              : 'libs/temp_file',
  'nxpy_test'                   : 'libs/test',
  'nxpy_xml'                    : 'libs/xml',
}

def install_libs(sources, develop=False):
    """ Use pip to install all libraries.  """
    print("installing all libs in {} mode".format(
              "development" if develop else "normal"))
    wd = os.getcwd()
    for k, v in iteritems(sources):
        try:
            os.chdir(os.path.join(wd, v))
            if develop:
                subprocess.call([sys.executable, '-m', 'pip', 'install', '-e', '.'])
            else:
                subprocess.call([sys.executable, '-m', 'pip', 'install', '.'])
        except Exception as e:
            print("Oops, something went wrong installing", k)
            print(e)
        finally:
            os.chdir(wd)

class DevelopCmd(develop):
    """ Add custom steps for the develop command """
    def run(self):
        install_libs(SOURCES, develop=True)
        develop.run(self)

class InstallCmd(install):
    """ Add custom steps for the install command """
    def run(self):
#        install_libs(SOURCES, develop=False)
        install.run(self)

class EggInfoCmd(egg_info):
    """ Add custom steps for the egg-info command """
    def run(self):
#        install_libs(SOURCES, develop=True)
        egg_info.run(self)

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here,'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=PACKAGE_NAME,
    version="1.0.6rc1",
    author="Nicola Musatti",
    author_email="nicola.musatti@gmail.com",
    description = "Nick's Python Toolbox",
    long_description = long_description,
    project_urls={
        "Documentation": "https://nxpy.readthedocs.io/en/latest/",
        "Source Code": "https://github.com/nmusatti/nxpy",
    },
    license="Boost Software License 1.0 (BSL-1.0)",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Boost Software License 1.0 (BSL-1.0)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=[
        'six',
    ],
    cmdclass={
        'install': InstallCmd,
        'develop': DevelopCmd,
        'egg_info': EggInfoCmd,
    },
)