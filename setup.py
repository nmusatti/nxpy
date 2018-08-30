# nxpy -----------------------------------------------------------------------

# Copyright Nicola Musatti 2018
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
Packaging information.

"""

from __future__ import absolute_import

import codecs
import os
import os.path
import subprocess
import sys

from six import iteritems

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info

PACKAGE_NAME = 'Nxpy'
SOURCES = {
  'nxpy.abstract'               : 'libs/abstract',
  'nxpy.backup_file'            : 'libs/backup_file',
  'nxpy.command'                : 'libs/command',
  'nxpy.core'                   : 'libs/core',
  'nxpy.file'                   : 'libs/file',
  'nxpy.file_object'            : 'libs/file_object',
  'nxpy.memo'                   : 'libs/memo',
  'nxpy.nonblocking_subprocess' : 'libs/nonblocking_subprocess',
  'nxpy.past'                   : 'libs/past',
  'nxpy.path'                   : 'libs/path',
  'nxpy.ply'                    : 'libs/ply',
  'nxpy.sequence'               : 'libs/sequence',
  'nxpy.sort'                   : 'libs/sort',
  'nxpy.temp_file'              : 'libs/temp_file',
  'nxpy.test'                   : 'libs/test',
  'nxpy.xml'                    : 'libs/xml',
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
        install_libs(SOURCES, develop=False)
        install.run(self)

class EggInfoCmd(egg_info):
    """ Add custom steps for the egg-info command """
    def run(self):
        install_libs(SOURCES, develop=True)
        egg_info.run(self)

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here,'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=PACKAGE_NAME,
    version="1.0.0",
    author="Nicola Musatti",
    author_email="nicola.musatti@gmail.com",
    description = "Nick's Python Toolchest",
    long_description = long_description,
    license="Boost Software License version 1.0",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
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