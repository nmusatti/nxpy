# nxpy ------------------------------------------------------------------------

# Copyright Nicola Musatti 2024
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy. ---------------------------------------

r"""
Use pip to install all libraries.

"""
import os
import subprocess
import sys

from six import iteritems

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

if __name__ == '__main__':
    develop = len(sys.argv) == 2 and sys.argv[1] in ( "-d", "--develop")
    install_libs(SOURCES, develop)
