# nxpy -----------------------------------------------------------------------

# Copyright Nicola Musatti 2011 -2014
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See http://nxpy.sourceforge.net for library home page. ---------------------

r"""
Test environment setup.

"""

from __future__ import absolute_import
from __future__ import print_function

import logging
import os
import os.path
import shutil
import sys

import six
from six.moves import input

import nxpy.core.path
import nxpy.svn.svn
import nxpy.svn.svnadmin


logging.basicConfig(stream=sys.__stderr__, level=logging.INFO)


def main(msgs=False):
    if msgs:
        six.print_("Nxpy test data setup")
    base_src_dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
    try:
        env_dir = os.environ["NXPY_TEST_DIR"]
        if not os.path.isdir(env_dir):
            env_dir = ""
    except KeyError:
        env_dir = ""
    base_dest_dir = ""
    if msgs:
        base_dest_dir = input("Test data directory [" + env_dir + "]: ")
        six.print_("Directory:", base_dest_dir)
    if len(base_dest_dir) == 0:
        if len(env_dir) == 0:
            sys.exit("Empty directory name")
        base_dest_dir = env_dir
    if os.path.isdir(base_dest_dir):
        if msgs:
            ans = input("Directory " + base_dest_dir + " exists. Remove? [Y]: ")
        else:
            ans = "Y"
        if len(ans) == 0:
            ans = "Y"
        if ans.upper() != "Y":
            sys.exit("Execution aborted")
        else:
            try:
                nxpy.core.path.blasttree(base_dest_dir)
            except Exception:
                sys.exit("Error removing directory " + base_dest_dir)
    try:
        os.mkdir(base_dest_dir)
    except OSError:
        sys.exit(base_dest_dir + ": Invalid directory")
    if msgs:
        six.print_("Copying test data to the backup directory")
    bck_src_dir = os.path.join(base_src_dir, "backup")
    bck_dest_dir = os.path.join(base_dest_dir, "backup")
    shutil.copytree(bck_src_dir, bck_dest_dir)
    if msgs:
        six.print_("Creating the test Subversion repository")
    repo_dir = os.path.join(base_dest_dir, "repo")
    svnadm = nxpy.svn.svnadmin.SvnAdmin()
    repo_url = svnadm.create(repo_dir)
    svn = nxpy.svn.svn.Svn()
    wcopy_dir = os.path.join(base_dest_dir, "wcopy")
    os.mkdir(wcopy_dir)
    
    aggrs = { "maven" : "aggregator", "msvs" : "solution" }
    for pkg in ( "maven", "msvs"):
        if msgs:
            six.print_(("Importing test data for the " + pkg + " package"))
        url = repo_url + "/" + pkg
        svn.import_(os.path.join(bck_src_dir, pkg), url)
        if msgs:
            six.print_(("Checking out test data for the " + pkg + " package"))
        d = os.path.join(wcopy_dir, pkg)
        os.mkdir(d)
        aggr_url = str(url) + "/" + aggrs[pkg] + "/trunk"
        aggr_dir = os.path.join(wcopy_dir, pkg, aggrs[pkg])
        svn.checkout(aggr_url, aggr_dir)
        projs = [ p[0:-1] for p in svn.list(url) ]
        ext = {}
        for proj in projs:
            u = str(url) + "/" + proj
            svn.mkdir(u + "/branches", u + "/tags")
            if proj != aggrs[pkg]:
                ext[proj] = u + "/trunk"
        svn.setexternals(ext, aggr_dir)
        svn.commit(aggr_dir)
        svn.update(aggr_dir, ignore_externals=False)

    if msgs:
        six.print_("Copying test default configuration to the conf directory")
    src_dir = os.path.join(base_src_dir, "conf")
    dest_dir = os.path.join(base_dest_dir, "conf")
    shutil.copytree(src_dir, dest_dir)

    if msgs:
        six.print_("Copying test data to the data directory")
    src_dir = os.path.join(base_src_dir, "data")
    dest_dir = os.path.join(base_dest_dir, "data")
    shutil.copytree(src_dir, dest_dir)

    if msgs:
        six.print_("Done.")
        six.print_("To run tests that use these data set the NXPY_TEST_DIR environment variable to " + 
                base_dest_dir)


if __name__ == '__main__':
    main()