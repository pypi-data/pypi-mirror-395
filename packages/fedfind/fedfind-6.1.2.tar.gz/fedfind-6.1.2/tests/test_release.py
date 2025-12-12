# Copyright Red Hat
#
# This file is part of fedfind.
#
# fedfind is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Adam Williamson <awilliam@redhat.com>

# these are all kinda inappropriate for pytest patterns
# pylint: disable=old-style-class, no-init, protected-access, no-self-use, unused-argument
# pylint: disable=invalid-name, too-few-public-methods, too-many-public-methods, too-many-lines

"""Tests for release.py."""

from __future__ import unicode_literals
from __future__ import print_function

import codecs
import datetime
import json
import os
import pytest

try:
    # Python >= 3.3
    from unittest import mock
except ImportError:
    # Python < 3.3
    import mock

import six

import fedfind.release

# Some chunks of HTML from mirror package directories for testing
# get_package_nvras. FC6 has generic release (no fcXX), F16 has
# fcXX, F21 is split by initials. FC6 is from a mirror, F18 and F21
# are from dl.fp.o.

FC6PACKAGEHTML = """
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
<title>Index of /fedora/archive/fedora/linux/core/6/source/SRPMS/</title>
<style type="text/css">
a, a:active {text-decoration: none; color: blue;}
a:visited {color: #48468F;}
a:hover, a:focus {text-decoration: underline; color: red;}
body {background-color: #F5F5F5;}
h2 {margin-bottom: 12px;}
table {margin-left: 12px;}
th, td { font: 90% monospace; text-align: left;}
th { font-weight: bold; padding-right: 14px; padding-bottom: 3px;}
td {padding-right: 14px;}
td.s, th.s {text-align: right;}
div.list { background-color: white; border-top: 1px solid #646464; border-bottom: 1px solid #646464; padding-top: 10px; padding-bottom: 14px;}
div.foot { font: 90% monospace; color: #787878; padding-top: 4px;}
</style>
</head>
<body>
<h2>Index of /fedora/archive/fedora/linux/core/6/source/SRPMS/</h2>
<div class="list">
<table summary="Directory Listing" cellpadding="0" cellspacing="0">
<thead><tr><th class="n">Name</th><th class="m">Last Modified</th><th class="s">Size</th><th class="t">Type</th></tr></thead>
<tbody>
<tr><td class="n"><a href="../">Parent Directory</a>/</td><td class="m">&nbsp;</td><td class="s">- &nbsp;</td><td class="t">Directory</td></tr>
<tr><td class="n"><a href="repodata/">repodata</a>/</td><td class="m">2006-Oct-17 21:22:24</td><td class="s">- &nbsp;</td><td class="t">Directory</td></tr>
<tr><td class="n"><a href="am-utils-6.1.5-4.src.rpm">am-utils-6.1.5-4.src.rpm</a></td><td class="m">2006-Oct-05 17:06:36</td><td class="s">1.8M</td><td class="t">application/x-rpm</td></tr>
<tr><td class="n"><a href="amanda-2.5.0p2-4.src.rpm">amanda-2.5.0p2-4.src.rpm</a></td><td class="m">2006-Oct-05 14:53:24</td><td class="s">1.7M</td><td class="t">application/x-rpm</td></tr>
<tr><td class="n"><a href="amtu-1.0.4-3.1.src.rpm">amtu-1.0.4-3.1.src.rpm</a></td><td class="m">2006-Oct-05 15:01:09</td><td class="s">58.9K</td><td class="t">application/x-rpm</td></tr>
<tr><td class="n"><a href="anaconda-11.1.1.3-1.src.rpm">anaconda-11.1.1.3-1.src.rpm</a></td><td class="m">2006-Oct-17 19:46:31</td><td class="s">3.7M</td><td class="t">application/x-rpm</td></tr>
<tr><td class="n"><a href="anacron-2.3-41.fc6.src.rpm">anacron-2.3-41.fc6.src.rpm</a></td><td class="m">2006-Oct-12 23:23:17</td><td class="s">42.0K</td><td class="t">application/x-rpm</td></tr>
<tr><td class="n"><a href="ant-1.6.5-2jpp.2.src.rpm">ant-1.6.5-2jpp.2.src.rpm</a></td><td class="m">2006-Oct-05 16:00:10</td><td class="s">5.0M</td><td class="t">application/x-rpm</td></tr>
<tr><td class="n"><a href="anthy-7900-2.fc6.src.rpm">anthy-7900-2.fc6.src.rpm</a></td><td class="m">2006-Oct-05 17:13:24</td><td class="s">4.4M</td><td class="t">application/x-rpm</td></tr>
<tr><td class="n"><a href="antlr-2.7.6-4jpp.2.src.rpm">antlr-2.7.6-4jpp.2.src.rpm</a></td><td class="m">2006-Oct-05 14:54:40</td><td class="s">1.3M</td><td class="t">application/x-rpm</td></tr>
<tr><td class="n"><a href="apmd-3.2.2-5.src.rpm">apmd-3.2.2-5.src.rpm</a></td><td class="m">2006-Oct-05 17:06:38</td><td class="s">99.6K</td><td class="t">application/x-rpm</td></tr>
<tr><td class="n"><a href="apr-1.2.7-10.src.rpm">apr-1.2.7-10.src.rpm</a></td><td class="m">2006-Oct-05 17:04:36</td><td class="s">1.0M</td><td class="t">application/x-rpm</td></tr>
<tr><td class="n"><a href="basesystem-8.0-5.1.1.src.rpm">basesystem-8.0-5.1.1.src.rpm</a></td><td class="m">2006-Oct-05 14:53:05</td><td class="s">3.7K</td><td class="t">application/x-rpm</td></tr>
<tr><td class="n"><a href="bash-3.1-16.1.src.rpm">bash-3.1-16.1.src.rpm</a></td><td class="m">2006-Oct-05 17:08:36</td><td class="s">4.4M</td><td class="t">application/x-rpm</td></tr>
<tr><td class="n"><a href="bc-1.06-21.src.rpm">bc-1.06-21.src.rpm</a></td><td class="m">2006-Oct-05 18:46:45</td><td class="s">236.9K</td><td class="t">application/x-rpm</td></tr>
"""

F16PACKAGEHTML = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
 <head>
  <title>Index of /pub/archive/fedora/linux/releases/16/Everything/source/SRPMS</title>
 </head>
 <body>
<h1>Index of /pub/archive/fedora/linux/releases/16/Everything/source/SRPMS</h1>
<pre><img src="/icons/blank.gif" alt="Icon "> <a href="?C=N;O=D">Name</a>                                                                         <a href="?C=M;O=A">Last modified</a>      <a href="?C=S;O=A">Size</a>  <a href="?C=D;O=A">Description</a><hr><img src="/icons/back.gif" alt="[PARENTDIR]"> <a href="/pub/archive/fedora/linux/releases/16/Everything/source/">Parent Directory</a>                                                                                  -   
<img src="/icons/unknown.gif" alt="[   ]"> <a href="amanda-3.3.0-2.fc16.src.rpm">amanda-3.3.0-2.fc16.src.rpm</a>                                                  2011-07-30 03:39  4.0M  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="amanith-0.3-17.fc16.src.rpm">amanith-0.3-17.fc16.src.rpm</a>                                                  2011-07-30 03:18  7.3M  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="amarok-2.4.3-1.fc16.src.rpm">amarok-2.4.3-1.fc16.src.rpm</a>                                                  2011-08-02 02:53   17M  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="amavisd-new-2.6.6-1.fc16.src.rpm">amavisd-new-2.6.6-1.fc16.src.rpm</a>                                             2011-09-19 17:12  950K  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="amide-1.0.0-1.fc16.src.rpm">amide-1.0.0-1.fc16.src.rpm</a>                                                   2011-10-11 00:33  1.5M  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="amoebax-0.2.0-7.fc15.src.rpm">amoebax-0.2.0-7.fc15.src.rpm</a>                                                 2011-07-30 01:29   10M  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="amora-1.1-6.fc15.src.rpm">amora-1.1-6.fc15.src.rpm</a>                                                     2011-07-30 02:16  161K  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="amqp-1.0.819819-2.fc15.src.rpm">amqp-1.0.819819-2.fc15.src.rpm</a>                                               2011-07-30 03:46  225K  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="amsn-0.98.4-4.fc16.src.rpm">amsn-0.98.4-4.fc16.src.rpm</a>                                                   2011-07-30 04:03   13M  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="amtterm-1.3-1.fc16.src.rpm">amtterm-1.3-1.fc16.src.rpm</a>                                                   2011-07-30 03:51   43K  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="amtu-1.0.8-8.fc15.src.rpm">amtu-1.0.8-8.fc15.src.rpm</a>                                                    2011-07-30 05:09  142K  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="anaconda-16.25-1.fc16.src.rpm">anaconda-16.25-1.fc16.src.rpm</a>                                                2011-11-03 02:14  5.1M  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="anaconda-yum-plugins-1.0-6.fc15.src.rpm">anaconda-yum-plugins-1.0-6.fc15.src.rpm</a>                                      2011-07-30 02:19   14K  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="basesystem-10.0-5.fc16.src.rpm">basesystem-10.0-5.fc16.src.rpm</a>                                               2011-07-30 02:47  5.7K  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="bash-4.2.10-4.fc16.src.rpm">bash-4.2.10-4.fc16.src.rpm</a>                                                   2011-07-30 04:23  6.7M  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="bash-completion-1.3-6.fc16.src.rpm">bash-completion-1.3-6.fc16.src.rpm</a>                                           2011-09-06 16:43  233K  
<hr></pre>
"""

F18PACKAGEHTMLA = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
 <head>
  <title>Index of /pub/archive/fedora/linux/releases/18/Everything/source/SRPMS/a</title>
 </head>
 <body>
<h1>Index of /pub/archive/fedora/linux/releases/18/Everything/source/SRPMS/a</h1>
<pre><img src="/icons/blank.gif" alt="Icon "> <a href="?C=N;O=D">Name</a>                                                           <a href="?C=M;O=A">Last modified</a>      <a href="?C=S;O=A">Size</a>  <a href="?C=D;O=A">Description</a><hr><img src="/icons/back.gif" alt="[PARENTDIR]"> <a href="/pub/archive/fedora/linux/releases/18/Everything/source/SRPMS/">Parent Directory</a>                                                                    -   
<img src="/icons/unknown.gif" alt="[   ]"> <a href="am-utils-6.1.5-23.fc18.src.rpm">am-utils-6.1.5-23.fc18.src.rpm</a>                                 2012-08-11 04:16  1.9M  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="amanda-3.3.2-2.fc18.src.rpm">amanda-3.3.2-2.fc18.src.rpm</a>                                    2012-09-18 17:58  4.2M  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="amanith-0.3-22.fc18.src.rpm">amanith-0.3-22.fc18.src.rpm</a>                                    2012-08-11 04:50  7.3M  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="amarok-2.6.0-4.fc18.src.rpm">amarok-2.6.0-4.fc18.src.rpm</a>                                    2012-09-12 18:15   40M  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="amavisd-new-2.8.0-2.fc18.src.rpm">amavisd-new-2.8.0-2.fc18.src.rpm</a>                               2012-08-11 06:33  1.0M  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="ambdec-0.5.1-3.fc18.src.rpm">ambdec-0.5.1-3.fc18.src.rpm</a>                                    2012-08-11 06:47  225K  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="amide-1.0.0-3.fc18.src.rpm">amide-1.0.0-3.fc18.src.rpm</a>                                     2012-08-11 04:36  1.5M  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="amoebax-0.2.0-10.fc18.src.rpm">amoebax-0.2.0-10.fc18.src.rpm</a>                                  2012-08-11 04:41   10M  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="amora-1.1-9.fc18.src.rpm">amora-1.1-9.fc18.src.rpm</a>                                       2012-11-02 03:48  161K  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="amqp-1.0.819819-4.fc18.src.rpm">amqp-1.0.819819-4.fc18.src.rpm</a>                                 2012-08-11 07:05  225K  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="ams-2.0.1-5.fc18.src.rpm">ams-2.0.1-5.fc18.src.rpm</a>                                       2012-10-26 06:52  291K  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="amsn-0.98.9-4.fc18.src.rpm">amsn-0.98.9-4.fc18.src.rpm</a>                                     2012-08-11 07:22   13M  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="amtterm-1.3-4.fc18.src.rpm">amtterm-1.3-4.fc18.src.rpm</a>                                     2012-08-11 05:06   44K  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="amtu-1.0.8-12.fc18.src.rpm">amtu-1.0.8-12.fc18.src.rpm</a>                                     2012-08-11 04:53  143K  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="anaconda-18.37.11-1.fc18.src.rpm">anaconda-18.37.11-1.fc18.src.rpm</a>                               2013-01-08 04:12  3.7M  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="anaconda-yum-plugins-1.0-8.fc18.src.rpm">anaconda-yum-plugins-1.0-8.fc18.src.rpm</a>                        2012-08-11 04:20   14K  
"""

F18PACKAGEHTMLB = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
 <head>
  <title>Index of /pub/archive/fedora/linux/releases/18/Everything/source/SRPMS/b</title>
 </head>
 <body>
<h1>Index of /pub/archive/fedora/linux/releases/18/Everything/source/SRPMS/b</h1>
<pre><img src="/icons/blank.gif" alt="Icon "> <a href="?C=N;O=D">Name</a>                                                           <a href="?C=M;O=A">Last modified</a>      <a href="?C=S;O=A">Size</a>  <a href="?C=D;O=A">Description</a><hr><img src="/icons/back.gif" alt="[PARENTDIR]"> <a href="/pub/archive/fedora/linux/releases/18/Everything/source/SRPMS/">Parent Directory</a>                                                                    -   
<img src="/icons/unknown.gif" alt="[   ]"> <a href="basesystem-10.0-7.fc18.src.rpm">basesystem-10.0-7.fc18.src.rpm</a>                                 2012-08-11 05:28  6.0K  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="bash-4.2.39-3.fc18.src.rpm">bash-4.2.39-3.fc18.src.rpm</a>                                     2012-11-30 03:56  6.8M  
<img src="/icons/unknown.gif" alt="[   ]"> <a href="bash-completion-2.0-2.fc18.src.rpm">bash-completion-2.0-2.fc18.src.rpm</a>
"""


class FakeRelease(object):
    """Release stub used for testing nightly respin guessing. Gives
    the magic 'good' values for exists and status if respin is 3 and
    release is 24 or Rawhide.
    """

    def __init__(self, respin="", *args, **kwargs):
        self.exists = False
        self.status = "DOOMED"
        self.respin = respin
        if respin == 3:
            self.exists = True
            self.status = "FINISHED"


class FakeResponsePackages(object):
    """urlopen response stub used for get_package_nvr testing."""

    def __init__(self, url):
        self.url = url

    def read(self):
        """Returns the appropriate chunk of HTML (see above) if the
        correct URL was given.
        """
        arcbase = "{}/archive/fedora/linux/".format(fedfind.const.HTTPS)
        branchbase = "https://kojipkgs.fedoraproject.org/compose/branched/Fedora-24-20160321.n.0/"
        mapping = {
            # we just pretend 1 is 6, it's easier
            arcbase + "core/1/SRPMS/": FC6PACKAGEHTML,
            arcbase + "core/6/source/SRPMS/": FC6PACKAGEHTML,
            arcbase + "releases/16/Everything/source/SRPMS/": F16PACKAGEHTML,
            arcbase + "releases/18/Everything/source/SRPMS/a/": F18PACKAGEHTMLA,
            arcbase + "releases/18/Everything/source/SRPMS/b/": F18PACKAGEHTMLB,
            arcbase + "releases/18/Everything/source/SRPMS/f/": "",
            # similarly we just use the 18 content for 24
            branchbase + "compose/Everything/source/tree/Packages/a/": F18PACKAGEHTMLA,
            branchbase + "compose/Everything/source/tree/Packages/b/": F18PACKAGEHTMLB,
            branchbase + "compose/Everything/source/tree/Packages/f/": "",
        }
        if self.url in mapping:
            return six.b(mapping[self.url])
        else:
            raise ValueError("URL {} not expected!".format(self.url))


def urlopen_fake_package(url, accept="*/*"):
    """Stub for urlopen_retries which returns FakeResponsePackages."""
    return FakeResponsePackages(url)


@pytest.mark.usefixtures("clean_home")
class TestRelease:
    """Tests for release.py."""

    @pytest.mark.parametrize(
        (
            "release",
            "milestone",
            "compose",
            "respin",
            "dist",
            "expclass",
            "exprel",
            "expmile",
            "expcomp",
            "expspin",
        ),
        # rel/mile/comp/respin to pass, expected class, expected rel/mile/comp/respin
        # None indicates check should not be done
        [
            # Archive stable.
            (15, "", "", None, "Fedora", fedfind.release.ArchiveRelease, "15", None, None, None),
            # Fedora Core stable (release string).
            ("6", "", "", None, "Fedora", fedfind.release.CoreRelease, "6", None, None, None),
            # 'Final' treated as stable.
            ("6", "Final", "", None, "Fedora", fedfind.release.CoreRelease, "6", None, None, None),
            # Milestone.
            (23, "Beta", "", None, "Fedora", fedfind.release.Milestone, "23", "Beta", None, None),
            # Branched nightly.
            (
                23,
                "Branched",
                "datestr",
                1,
                "Fedora",
                fedfind.release.BranchedNightly,
                "23",
                "Branched",
                "datestr",
                "1",
            ),
            # Rawhide nightly.
            (
                "Rawhide",
                "",
                "datestr",
                2,
                "Fedora",
                fedfind.release.RawhideNightly,
                "Rawhide",
                "",
                "datestr",
                "2",
            ),
            # Cloud nightly (old, milestone way).
            (
                25,
                "Cloud",
                "datestr",
                0,
                "Fedora",
                fedfind.release.CloudNightly,
                "25",
                "Nightly",
                "datestr",
                "0",
            ),
            # Cloud nightly (new, dist way).
            (
                25,
                "",
                "datestr",
                0,
                "Fedora-Cloud",
                fedfind.release.CloudNightly,
                "25",
                "Nightly",
                "datestr",
                "0",
            ),
            # Container nightly (new, dist way).
            (
                28,
                "",
                "datestr",
                0,
                "Fedora-Container",
                fedfind.release.ContainerNightly,
                "28",
                "Nightly",
                "datestr",
                "0",
            ),
            # IoT nightly.
            (
                28,
                "",
                "datestr",
                0,
                "Fedora-IoT",
                fedfind.release.IoTNightly,
                "28",
                "Nightly",
                "datestr",
                "0",
            ),
            # Updates nightly.
            (
                28,
                "Updates",
                "datestr",
                0,
                "Fedora",
                fedfind.release.Updates,
                "28",
                "Updates",
                "datestr",
                "0",
            ),
            # Updates-testing nightly.
            (
                28,
                "Updates-testing",
                "datestr",
                0,
                "Fedora",
                fedfind.release.UpdatesTesting,
                "28",
                "Updates-testing",
                "datestr",
                "0",
            ),
            # ELN nightly.
            (
                "ELN",
                "",
                "datestr",
                2,
                "Fedora",
                fedfind.release.ElnNightly,
                "eln",
                "",
                "datestr",
                "2",
            ),
            # Wikitcms format Rawhide.
            (
                "24",
                "Rawhide",
                "datestr.n.0",
                None,
                "Fedora",
                fedfind.release.RawhideNightly,
                "Rawhide",
                "",
                "datestr",
                "0",
            ),
            # OFFLINE GUESSES
            # Date guesses.
            (
                23,
                "Branched",
                "",
                0,
                "Fedora",
                fedfind.release.BranchedNightly,
                "23",
                "Branched",
                "datestr",
                "0",
            ),
            (
                "Rawhide",
                "",
                "",
                0,
                "Fedora",
                fedfind.release.RawhideNightly,
                "Rawhide",
                "",
                "datestr",
                "0",
            ),
            (
                25,
                "Cloud",
                "",
                0,
                "Fedora",
                fedfind.release.CloudNightly,
                "25",
                "Nightly",
                "datestr",
                "0",
            ),
            (
                28,
                "",
                "",
                0,
                "Fedora-Container",
                fedfind.release.ContainerNightly,
                "28",
                "Nightly",
                "datestr",
                "0",
            ),
            (
                28,
                "",
                "",
                0,
                "Fedora-IoT",
                fedfind.release.IoTNightly,
                "28",
                "Nightly",
                "datestr",
                "0",
            ),
            # Default, check None is handled.
            (
                None,
                None,
                None,
                0,
                "Fedora",
                fedfind.release.RawhideNightly,
                "Rawhide",
                "",
                "datestr",
                "0",
            ),
        ],
    )
    # pylint:disable=too-many-arguments
    def test_get_release_simple(
        self, release, milestone, compose, respin, dist, expclass, exprel, expmile, expcomp, expspin
    ):
        """Tests for get_release that require no online guessing or
        checking, hence no mocking.
        """
        datestr = datetime.date.today().strftime("%Y%m%d")
        if compose:
            compose = compose.replace("datestr", datestr)
        if expcomp:
            expcomp = expcomp.replace("datestr", datestr)
        got = fedfind.release.get_release(release, milestone, compose, respin, dist=dist)
        assert isinstance(got, expclass)
        if exprel is not None:
            assert got.release == exprel
        if expmile is not None:
            assert got.milestone == expmile
        if expcomp is not None:
            assert got.compose == expcomp
        if expspin is not None:
            assert got.respin == expspin

        # Sanity check tests.
        with pytest.raises(ValueError):
            fedfind.release.get_release("foobar")

        with pytest.raises(ValueError):
            fedfind.release.get_release("23", "", "RC2")

    @mock.patch("fedfind.release.Production.label", "Alpha-1.1")
    def test_get_release_production(self):
        """Explicitly getting a Production (i.e. a production compose
        on kojipkgs, not mirrored to alt, which is a Compose). This
        is the same path hit if get_release is called with a compose
        ID for a production compose, and promote is not set True.
        """
        ret = fedfind.release.get_release(24, "Production", "20160314", 0)
        assert isinstance(ret, fedfind.release.Production)
        assert ret.release == "24"
        assert ret.milestone == "Alpha"
        assert ret.compose == "1"
        assert ret.respin == "1"

    @mock.patch("fedfind.helpers.label_from_cid", return_value="Alpha-1.1", autospec=True)
    @mock.patch("fedfind.release.Compose.exists", True)
    def test_get_release_cid_promote(self, fakelab):
        """Requesting release from a production compose ID with
        promote set to True should return a Compose if possible.
        """
        ret = fedfind.release.get_release(cid="Fedora-24-20160314.0", promote=True)
        assert isinstance(ret, fedfind.release.Compose)
        assert ret.release == "24"
        assert ret.milestone == "Alpha"
        assert ret.compose == "1"
        assert ret.respin == "1"
        fakelab.assert_called_with("Fedora-24-20160314.0")

    @mock.patch("fedfind.helpers.label_from_cid", return_value="Alpha-1.1", autospec=True)
    @mock.patch("fedfind.helpers.cid_from_label", autospec=True)
    @mock.patch("fedfind.release.Compose.exists", False)
    # this is to avoid a network trip for the get_release CID check
    @mock.patch("fedfind.release.Production.cid", "Fedora-24-20160314.0")
    def test_get_release_cid_promote_fail(self, fakecid, fakelab):
        """This tests a rather snaky path: we call get_release with
        a CID and promote=True; the specified compose has a label, so
        we try and get a Compose, but the compose is not mirrored, so
        we fail. In this case we should fall back on a Production *and
        not waste time on a remote trip to recreate the CID*, instead
        it should be reused.
        """
        ret = fedfind.release.get_release(cid="Fedora-24-20160314.0", promote=True)
        assert isinstance(ret, fedfind.release.Production)
        fakelab.assert_called_with("Fedora-24-20160314.0")
        assert fakecid.call_count == 0

    @mock.patch("fedfind.release.ContainerNightly.cid", "Fedora-Container-28-20180605.0")
    def test_get_release_cid_container(self):
        """Test that nightly stable Container compose IDs are handled.
        They have 'Fedora-Container' as the product name instead of
        'Fedora'.
        """
        ret = fedfind.release.get_release(cid="Fedora-Container-28-20180605.0")
        assert isinstance(ret, fedfind.release.ContainerNightly)
        assert ret.release == "28"
        assert ret.compose == "20180605"
        assert ret.respin == "0"

    @mock.patch("fedfind.release.IoTNightly.cid", "Fedora-IoT-28-20180605.0")
    def test_get_release_cid_iot(self):
        """Test that nightly stable IoT compose IDs are handled.
        They have 'Fedora-IoT' as the product name instead of
        'Fedora'.
        """
        ret = fedfind.release.get_release(cid="Fedora-IoT-28-20180605.0")
        assert isinstance(ret, fedfind.release.IoTNightly)
        assert ret.release == "28"
        assert ret.compose == "20180605"
        assert ret.respin == "0"

    @mock.patch("fedfind.release.CloudNightly.cid", "Fedora-Cloud-26-20170217.3")
    def test_get_release_cid_cloud(self):
        """Test that nightly stable Cloud compose IDs are handled.
        They have 'Fedora-Cloud' as the product name instead of
        'Fedora'.
        """
        ret = fedfind.release.get_release(cid="Fedora-Cloud-26-20170217.3")
        assert isinstance(ret, fedfind.release.CloudNightly)
        assert ret.release == "26"
        assert ret.compose == "20170217"
        assert ret.respin == "3"

    def test_get_release_cid_fake_stable(self):
        """Getting a release based on the fake CID produced for stable
        releases should return the same release.
        """
        rel = fedfind.release.get_release(15)
        rel2 = fedfind.release.get_release(cid=rel.cid)
        assert rel2.version == rel.version

    def test_get_release_url_cid_rawhide(self):
        """Getting a release based on a correct Rawhide nightly URL
        should work.
        """
        url = (
            "https://kojipkgs.fedoraproject.org/"
            "compose/rawhide/Fedora-Rawhide-20170126.n.0/compose/"
        )
        ret = fedfind.release.get_release(url=url)
        assert isinstance(ret, fedfind.release.RawhideNightly)
        assert ret.release == "Rawhide"
        assert ret.compose == "20170126"
        assert ret.respin == "0"

    def test_get_release_url_cid_branched(self):
        """Getting a release based on a correct Branched nightly URL
        should work.
        """
        url = (
            "https://kojipkgs.fedoraproject.org/" "compose/branched/Fedora-27-20170816.n.0/compose/"
        )
        ret = fedfind.release.get_release(url=url)
        assert isinstance(ret, fedfind.release.BranchedNightly)
        assert ret.release == "27"
        assert ret.compose == "20170816"
        assert ret.respin == "0"

    def test_get_release_url_cid_updates(self):
        """Getting a release based on a correct updates compose
        URL should work.
        """
        url = (
            "https://kojipkgs.fedoraproject.org/"
            "compose/updates/Fedora-28-updates-20180605.0/compose/"
        )
        ret = fedfind.release.get_release(url=url)
        assert isinstance(ret, fedfind.release.Updates)
        assert ret.release == "28"
        assert ret.compose == "20180605"
        assert ret.respin == "0"

    def test_get_release_url_cid_updates_testing(self):
        """Getting a release based on a correct updates-testing
        compose URL should work.
        """
        url = (
            "https://kojipkgs.fedoraproject.org/"
            "compose/updates/Fedora-28-updates-testing-20180605.0/compose/"
        )
        ret = fedfind.release.get_release(url=url)
        assert isinstance(ret, fedfind.release.UpdatesTesting)
        assert ret.release == "28"
        assert ret.compose == "20180605"
        assert ret.respin == "0"

    def test_get_release_url_cid_eln(self):
        """Getting a release based on a correct ELN nightly URL
        should work.
        """
        url = "https://kojipkgs.fedoraproject.org/compose/eln/Fedora-eln-20240830.n.7/compose/"
        ret = fedfind.release.get_release(url=url)
        assert isinstance(ret, fedfind.release.ElnNightly)
        assert ret.release == "eln"
        assert ret.compose == "20240830"
        assert ret.respin == "7"

    def test_get_release_url_cid_epel(self):
        """EPEL is explicitly unsupported."""
        url = (
            "https://kojipkgs.fedoraproject.org/"
            "compose/epel/Fedora-Epel-Playground-8-20220128.n.0/compose/"
        )
        with pytest.raises(fedfind.exceptions.UnsupportedComposeError):
            rel = fedfind.release.get_release(url=url)
        url = (
            "https://kojipkgs.fedoraproject.org/"
            "compose/epel10/Fedora-EPEL-10-20240918.n.0/compose/"
        )
        with pytest.raises(fedfind.exceptions.UnsupportedComposeError):
            rel = fedfind.release.get_release(url=url)

    def test_get_release_url_cid_unknown(self):
        """Getting a release based on an unknown URL should return
        a generic Pungi4Release instance, so long as the URL starts
        with an acceptable string (to avoid puiterwijk's 'evil URL
        input' scenario).
        """
        ret = fedfind.release.get_release(
            url="https://kojipkgs.fedoraproject.org/compose/whatthehellisthis/ihavenoidea/compose/"
        )
        assert isinstance(ret, fedfind.release.Pungi4Release)

    def test_get_release_url_cid_unknown_evil(self):
        """Getting a release based on an unknown URL that doesn't
        start with one of our known prefixes should raise a value
        error.
        """
        url = "https://foobar.fedoraproject.org/compose/whatthehellisthis/ihavenoidea/compose/"
        with pytest.raises(ValueError):
            fedfind.release.get_release(url=url)

    def test_get_release_url_check(self):
        """Test the URL match check for get_release: if we get a
        release by URL, but the URL of the discovered Release instance
        doesn't match the requested URL, an exception should occur.
        """
        with pytest.raises(fedfind.exceptions.UrlMatchError):
            url = "https://kojipkgs.fedoraproject.org/wrong/Fedora-Rawhide-20180117.n.0/compose/"
            fedfind.release.get_release(url=url)

    # This would be the correct compose ID value for a Rawhide nightly
    @mock.patch("fedfind.release.RawhideNightly.cid", "Fedora-Rawhide-20180117.n.0")
    def test_get_release_cid_check(self):
        """Test the CID match check for get_release: if we get a
        release by CID, but the CID of the discovered Release instance
        doesn't match the requested CID, an exception should occur.
        """
        with pytest.raises(fedfind.exceptions.CidMatchError):
            # real compose IDs for Rawhide are always '.n.', as we
            # patch above; get_release will successfully handle this
            # CID, though, and give us a RawhideNightly instance
            cid = "Fedora-Rawhide-20180117.0"
            fedfind.release.get_release(cid=cid)
        # now check it works if we do it right
        cid = "Fedora-Rawhide-20180117.n.0"
        ret = fedfind.release.get_release(cid=cid)
        assert isinstance(ret, fedfind.release.RawhideNightly)
        assert ret.release == "Rawhide"
        assert ret.compose == "20180117"
        assert ret.respin == "0"

    # these mocks avoid network round trips to figure out that the
    # compose does not exist, and to try and get the compose ID from
    # the compose location
    @mock.patch("fedfind.release.RawhideNightly.cid", "")
    @mock.patch("fedfind.release.RawhideNightly.exists", False)
    def test_get_release_cid_mda(self, httpkp):
        """Test getting a release by compose ID when that release is a
        Pungi 4 compose that has been garbage-collected, but whose
        metadata is in the archive. We have a special code path here
        which reads in the metadata from the archive.
        """
        # use a compose our metadata archive test fixture has data for
        ret = fedfind.release.get_release(cid="Fedora-Rawhide-20240829.n.1")
        assert isinstance(ret, fedfind.release.RawhideNightly)
        assert ret.release == "Rawhide"
        assert ret.compose == "20240829"
        assert ret.respin == "1"
        # this tests we got the metadata right - there are 89 images
        # in the canned metadata the httpkp fixture uses
        assert len(ret.all_images) == 89
        # check a random value from composeinfo
        assert ret.metadata["composeinfo"]["payload"]["release"]["type"] == "ga"

    @mock.patch("fedfind.release.Compose.exists", True)
    def test_get_release_compose(self):
        """A production/candidate compose. This tests the case where
        the compose is found on the mirror system. Also tests that
        'Final' is converted to 'RC'.
        """
        ret = fedfind.release.get_release(24, "Final", 1, 1)
        assert isinstance(ret, fedfind.release.Compose)
        assert ret.release == "24"
        assert ret.milestone == "RC"
        assert ret.compose == "1"
        assert ret.respin == "1"
        assert ret.label == "RC-1.1"

    @mock.patch(
        "fedfind.helpers.cid_from_label", return_value="Fedora-24-20160316.3", autospec=True
    )
    @mock.patch("fedfind.release.Compose.exists", False)
    def test_get_release_compose_fallback(self, fakecid):
        """A production/candidate compose. This tests the case where
        the compose is not found on the mirror system so we fall back
        on finding the compose ID and returning a Production.
        """
        ret = fedfind.release.get_release(24, "Alpha", 1, 5)
        assert isinstance(ret, fedfind.release.Production)
        fakecid.assert_called_with(24, "Alpha-1.5")

    @mock.patch("fedfind.release.CurrentRelease.exists", True)
    def test_get_stable_current(self):
        """Ensure that if it exists, get_release for a recent stable
        returns CurrentRelease. Tested number must be higher than the
        'just return ArchiveRelease' cutoff, so bump this test when
        bumping that cutoff.
        """
        ret = fedfind.release.get_release(40)
        assert isinstance(ret, fedfind.release.CurrentRelease)
        assert ret.release == "40"

    @mock.patch("fedfind.release.CurrentRelease.exists", False)
    @mock.patch("fedfind.release.ArchiveRelease.exists", True)
    def test_get_stable_archive(self):
        """Ensure that if CurrentRelease does not exist but
        ArchiveRelease does exist, get_release for a recent stable
        returns it. Tested number must be higher than the 'just return
        ArchiveRelease' cutoff (or else this test will pass even if
        the feature is broken), so bump this test when bumping that
        cutoff.
        """
        ret = fedfind.release.get_release(39)
        assert isinstance(ret, fedfind.release.ArchiveRelease)
        assert ret.release == "39"

    @mock.patch("fedfind.helpers.get_current_release", return_value=23, autospec=True)
    def test_get_release_guess_release(self, fakecurrent):
        """Release guessing. We can't test this very hard or we'd have
        to keep updating the tests all the goddamned time, or the test
        would duplicate the logic of get_current_release and that
        seems pointless. But we can at least check it's not crashing
        and returns the right class.
        """
        datestr = datetime.date.today().strftime("%Y%m%d")

        got = fedfind.release.get_release("", "Branched", "", 0)
        assert isinstance(got, fedfind.release.BranchedNightly)
        assert got.compose == datestr
        assert got.release == "24"

        # old 'milestone' style
        got = fedfind.release.get_release("", "Cloud", "", 0)
        assert isinstance(got, fedfind.release.CloudNightly)
        assert got.compose == datestr
        assert got.release == "23"

        # new 'dist' style
        got = fedfind.release.get_release("", "", "", 0, dist="Fedora-Cloud")
        assert isinstance(got, fedfind.release.CloudNightly)
        assert got.compose == datestr
        assert got.release == "23"

        got = fedfind.release.get_release("", "", "", 0, dist="Fedora-Container")
        assert isinstance(got, fedfind.release.ContainerNightly)
        assert got.compose == datestr
        assert got.release == "23"

        got = fedfind.release.get_release("", "", "", 0, dist="Fedora-IoT")
        assert isinstance(got, fedfind.release.IoTNightly)
        assert got.compose == datestr
        assert got.release == "23"

        # updates
        got = fedfind.release.get_release("", "Updates", "", 0)
        assert isinstance(got, fedfind.release.Updates)
        assert got.compose == datestr
        assert got.release == "23"

        # updates-testing
        got = fedfind.release.get_release("", "Updates-testing", "", 0)
        assert isinstance(got, fedfind.release.UpdatesTesting)
        assert got.compose == datestr
        assert got.release == "23"

    @mock.patch("fedfind.release.RawhideNightly", FakeRelease)
    @mock.patch("fedfind.release.BranchedNightly", FakeRelease)
    @mock.patch("fedfind.release.CloudNightly", FakeRelease)
    @mock.patch("fedfind.release.ContainerNightly", FakeRelease)
    @mock.patch("fedfind.release.IoTNightly", FakeRelease)
    @mock.patch("fedfind.release.Updates", FakeRelease)
    @mock.patch("fedfind.release.UpdatesTesting", FakeRelease)
    @mock.patch("fedfind.release.ElnNightly", FakeRelease)
    def test_get_release_guess_respin(self):
        """Test the 'respin guessing' code works (when you request a
        nightly but don't provide a respin number). Uses the fake
        release class's feature of 'existing' when the respin is 3.
        """
        got = fedfind.release.get_release(24, "Branched", "20160314")
        assert isinstance(got, fedfind.release.BranchedNightly)
        assert got.respin == 3
        got = fedfind.release.get_release("Rawhide", "", "20160314")
        assert isinstance(got, fedfind.release.RawhideNightly)
        assert got.respin == 3
        # old 'milestone' style
        got = fedfind.release.get_release(24, "Cloud", "20160628")
        assert isinstance(got, fedfind.release.CloudNightly)
        assert got.respin == 3
        # new 'dist' style
        got = fedfind.release.get_release(24, "", "20160628", dist="Fedora-Cloud")
        assert isinstance(got, fedfind.release.CloudNightly)
        assert got.respin == 3
        got = fedfind.release.get_release(24, "", "20160628", dist="Fedora-Container")
        assert isinstance(got, fedfind.release.ContainerNightly)
        assert got.respin == 3
        got = fedfind.release.get_release(24, "", "20160628", dist="Fedora-IoT")
        assert isinstance(got, fedfind.release.IoTNightly)
        assert got.respin == 3
        # updates
        got = fedfind.release.get_release(24, "Updates", "20160628")
        assert isinstance(got, fedfind.release.Updates)
        assert got.respin == 3
        # updates-testing
        got = fedfind.release.get_release(24, "UpdatesTesting", "20160628")
        assert isinstance(got, fedfind.release.UpdatesTesting)
        assert got.respin == 3
        # eln
        got = fedfind.release.get_release("ELN", "", "20160628")
        assert isinstance(got, fedfind.release.ElnNightly)
        assert got.respin == 3

    @mock.patch.object(fedfind.release.BranchedNightly, "exists", True)
    @mock.patch.object(fedfind.release.BranchedNightly, "status", "FINISHED")
    def test_get_release_no_milestone_branched(self):
        """If we specify a date and a release number, but no milestone,
        fedfind should return BranchedNightly.
        """
        got = fedfind.release.get_release(25, "", "20161006")
        assert isinstance(got, fedfind.release.BranchedNightly)
        got = fedfind.release.get_release(25, "", "20161006", 3)
        assert isinstance(got, fedfind.release.BranchedNightly)

    def test_get_release_respinrelease(self, http):
        """Test get_release for RespinRelease class. We use the fake
        web server here as RespinRelease has to discover its own
        release and compose from the image list.
        """
        # old milestone style
        got = fedfind.release.get_release("", "Respin", "")
        assert isinstance(got, fedfind.release.RespinRelease)
        assert got.release == "39"
        assert got.milestone == "Respin"
        assert got.compose == "20240415"
        # getting a release from the fake compose ID should get the
        # same release
        got2 = fedfind.release.get_release(cid=got.cid)
        assert got.version == got2.version
        # getting a release with the old form of fake compose ID also
        got3 = fedfind.release.get_release(cid="FedoraRespin-39-20240415.0")
        assert got.version == got3.version
        # getting a release from the URL should get the same release
        got4 = fedfind.release.get_release(url="https://dl.fedoraproject.org/pub/alt/live-respins/")
        assert got4.version == got3.version
        # new dist style (should match others)
        got5 = fedfind.release.get_release("", "", "", dist="FedoraRespin")
        assert got5.version == got4.version
        # trying to get RespinRelease with a non-matching release
        # or compose should raise an error
        with pytest.raises(ValueError):
            fedfind.release.get_release("25", "Respin", "")
        with pytest.raises(ValueError):
            fedfind.release.get_release("", "Respin", "20170305")
        with pytest.raises(ValueError):
            fedfind.release.get_release("25", "Respin", "20170305")
        with pytest.raises(ValueError):
            fedfind.release.get_release(cid="FedoraRespin-25-updates-20170305.0")

    def test_get_release_eln_notdate(self):
        """Test that we correctly raise ValueError for get_release ELN
        with a non-date compose value.
        """
        with pytest.raises(ValueError):
            fedfind.release.get_release("eln", "", "103")

    @mock.patch("fedfind.helpers.urlopen_retries", urlopen_fake_package)
    def test_get_package_nvras_fc1(self):
        """FC1: no /Everything, no /source, no split-by-initials."""
        rel = fedfind.release.get_release(1)
        pkgs = rel.get_package_nvras(["amanda", "anaconda", "bash", "fakepackage"])
        assert pkgs == {
            "amanda": "amanda-2.5.0p2-4.src",
            "anaconda": "anaconda-11.1.1.3-1.src",
            "bash": "bash-3.1-16.1.src",
            "fakepackage": "",
        }

    @mock.patch("fedfind.helpers.urlopen_retries", urlopen_fake_package)
    def test_get_package_nvras_fc6(self):
        """FC6: Still no /Everything, /source appeared, no
        split-by-initials.
        """
        rel = fedfind.release.get_release(6)
        pkgs = rel.get_package_nvras(["amanda", "anaconda", "bash", "fakepackage"])
        assert pkgs == {
            "amanda": "amanda-2.5.0p2-4.src",
            "anaconda": "anaconda-11.1.1.3-1.src",
            "bash": "bash-3.1-16.1.src",
            "fakepackage": "",
        }

    @mock.patch("fedfind.helpers.urlopen_retries", urlopen_fake_package)
    def test_get_package_nvras_f16(self):
        """F16: /Everything showed up, still no split-by-initials."""
        rel = fedfind.release.get_release(16)
        pkgs = rel.get_package_nvras(["amanda", "anaconda", "bash", "fakepackage"])
        assert pkgs == {
            "amanda": "amanda-3.3.0-2.fc16.src",
            "anaconda": "anaconda-16.25-1.fc16.src",
            "bash": "bash-4.2.10-4.fc16.src",
            "fakepackage": "",
        }

    @mock.patch("fedfind.helpers.urlopen_retries", urlopen_fake_package)
    def test_get_package_nvras_f18(self):
        """F18: split-by-initials now in effect."""
        rel = fedfind.release.get_release(18)
        pkgs = rel.get_package_nvras(["amanda", "anaconda", "bash", "fakepackage"])
        assert pkgs == {
            "amanda": "amanda-3.3.2-2.fc18.src",
            "anaconda": "anaconda-18.37.11-1.fc18.src",
            "bash": "bash-4.2.39-3.fc18.src",
            "fakepackage": "",
        }

    @mock.patch("fedfind.helpers.urlopen_retries", urlopen_fake_package)
    @mock.patch("fedfind.release.BranchedNightly.cid", "Fedora-24-20160321.n.0")
    def test_get_package_nvras_f24(self):
        """F24: Different layout again under /Everything. mock values
        are same as for F18.
        """
        rel = fedfind.release.get_release(24, "Branched", "20160321", 0)
        pkgs = rel.get_package_nvras(["amanda", "anaconda", "bash", "fakepackage"])
        assert pkgs == {
            "amanda": "amanda-3.3.2-2.fc18.src",
            "anaconda": "anaconda-18.37.11-1.fc18.src",
            "bash": "bash-4.2.39-3.fc18.src",
            "fakepackage": "",
        }

    def test_all_paths_sizes(self, http, httpkp):
        """Check that all_paths_sizes works correctly with both
        formats. Note the test data has a line edited to test this.
        We use the httpkp fixture to avoid network roundtrips for
        a label->cid lookup attempt and to ensure we don't get real
        metadata from the archive (our mock data does not include this
        release). Instead we're forced back on synthesis. Then we use
        all_images to check that all_paths_sizes and metadata both do
        their job properly.
        """
        rel = fedfind.release.get_release(23)
        imgs = rel.all_images
        assert len(imgs) == 52
        for img in imgs:
            if "Fedora-Server-DVD-x86_64-23.iso" in img["path"]:
                # this is the line that's edited to have a size
                assert img["size"] == 2149580800
            else:
                # old-style line, size should not be in dict at all
                assert "size" not in img

    @mock.patch("fedfind.release.CurrentRelease.exists", True)
    def test_all_stable(self, http, httpkp):
        """Test that we get the expected image dicts for all stable
        releases, using the test dl.fp.o and kojipkgs.fp.o servers.
        Also check there are no missing expected images (as a test
        for check_expected). Note this test is sensitive to the stupid
        'current/archive' detection in get_release: it will fail if
        the hardcoded cutoff there doesn't match the data in
        allstable.json.
        """
        ref = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "allstable.json")
        with codecs.open(ref, encoding="utf-8") as reffh:
            expected = json.loads(reffh.read())
        # one thing we can handily check here, each time we bump the
        # backing data for this test to include a new release, is if
        # any sneaky new subvariants showed up...
        subvs = [subv.name for subv in fedfind.const.SUBVARIANTS]
        for relnum in expected:
            rel = fedfind.release.get_release(relnum)
            imgs = sorted(rel.all_images, key=lambda x: x["path"])
            assert expected[relnum] == imgs
            for img in imgs:
                subv = img.get("subvariant")
                if subv:
                    assert subv in subvs
            # we have to force the release to 'exist' or else
            # check_expected bails
            rel._exists = True
            assert not rel.check_expected()

    def test_images_respinrelease(self, http):
        """Test that we get approximately the expected image dicts for
        RespinRelease. This depends on the contents of imagelist-alt
        in the fake http server; if that's updated, this test may have
        to change. Especially note that the 20161120 respin didn't
        have an SOAS image, the 20201016 had no source image, and the
        20211201 had no SoaS or source, but added i3.
        """
        rel = fedfind.release.RespinRelease()
        imgs = rel.all_images
        assert len(imgs) == 11
        # ditch source if it exists, as we don't care much about it
        imgs = [img for img in imgs if img["subvariant"] != "Source"]
        assert len(imgs) == 11
        assert all(img["type"] == "live" for img in imgs)
        # this is a lie, but it's the lie we decided to tell
        assert all(img["variant"] == "Spins" for img in imgs)
        assert all(img["arch"] == "x86_64" for img in imgs)
        exp = [
            "Budgie",
            "Cinnamon",
            "KDE",
            "LXDE",
            "LXQt",
            "Mate",
            "SoaS",
            "Sway",
            "Workstation",
            "Xfce",
            "i3",
        ]
        got = sorted([img["subvariant"] for img in imgs])
        assert got == exp

    def test_compose_urls(self, http):
        """Check that get_release(url=) works sanely for a list of 180
        days worth of compose URLs. List is generated by fedfindloc.py
        script.
        """
        urlfn = "compose-urls-20240423.json"
        urlfp = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", urlfn)
        with codecs.open(urlfp, encoding="utf-8") as urlfh:
            urls = json.loads(urlfh.read())
        for url in urls:
            try:
                assert fedfind.release.get_release(url=url)
            except fedfind.exceptions.UnsupportedComposeError:
                pass

    @mock.patch("fedfind.release.logger.info", autospec=True)
    @mock.patch("fedfind.release.logger.error", autospec=True)
    @mock.patch("fedfind.helpers.download_json", autospec=True)
    @mock.patch("fedfind.release.RawhideNightly.exists", True)
    @pytest.mark.parametrize(
        ("composeinfo", "images", "done"),
        [
            (True, True, True),
            (True, False, True),
            (False, True, True),
            (False, False, True),
            (True, True, False),
            (True, False, False),
            (False, True, False),
            (False, False, False),
        ],
    )
    # pylint:disable=too-many-arguments
    def test_metadata_from_compose(self, fakejson, fakeerror, fakeinfo, composeinfo, images, done):
        """Check that getting metadata from the compose tree - the
        normal path, for productmd composes - works OK.
        """
        rel = fedfind.release.RawhideNightly("20230831", 0, "Fedora-Rawhide-20230831.n.0")
        if composeinfo:
            cise = ciex = ["here"]
        else:
            cise = ValueError("not found")
            ciex = {}
        if images:
            imse = imex = ["here"]
        else:
            imse = ValueError("not found")
            imex = {}
        fakejson.side_effect = (cise, imse, cise, imse)
        with mock.patch("fedfind.release.RawhideNightly.done", done):
            # do it twice to check caching
            md = rel.metadata
            md = rel.metadata
        assert md == {"composeinfo": ciex, "images": imex}
        if done and composeinfo:
            # due to caching we only do the retrievals once
            multiplier = 1
        else:
            # we do them twice
            multiplier = 2
        # two downloads per attempt
        assert fakejson.call_count == 2 * multiplier
        if composeinfo:
            assert fakeerror.call_count == 0
        else:
            # if no composeinfo, we should log an error once per attempt
            assert fakeerror.call_count == 1 * multiplier
        if composeinfo and not images:
            # if composeinfo but no images, an info once per attempt
            assert fakeinfo.call_count == 1 * multiplier
        else:
            assert fakeinfo.call_count == 0

    def test_relnum_branched(self, releases_branched):
        """Check relnum property across Fedora and ELN (when branched
        releases exist).
        """
        rawrel = fedfind.release.RawhideNightly("20230831", 0, "Fedora-Rawhide-20230831.n.0")
        assert rawrel.relnum == 33
        brel = fedfind.release.BranchedNightly("32", "20230831", 0, "Fedora-32-20230831.n.0")
        assert brel.relnum == 32
        elnrel = fedfind.release.ElnNightly("20250606", 0)
        assert elnrel.relnum == 10

    def test_relnum_nobranched(self, releases_nobranched):
        """Check relnum property across Fedora and ELN (when no
        branched releases exist).
        """
        rawrel = fedfind.release.RawhideNightly("20230831", 0, "Fedora-Rawhide-20230831.n.0")
        assert rawrel.relnum == 32
        elnrel = fedfind.release.ElnNightly("20250606", 0)
        assert elnrel.relnum == 9

    @mock.patch("fedfind.helpers.download_json", autospec=True, return_value={"eol": "2024-05-16"})
    def test_eol(self, fakedljson):
        """Test eol property works as expected."""
        rawrel = fedfind.release.RawhideNightly("20230831", 0, "Fedora-Rawhide-20230831.n.0")
        elnrel = fedfind.release.ElnNightly("20250606", 0)
        crel = fedfind.release.CurrentRelease("40")
        assert rawrel.eol is None
        assert elnrel.eol is None
        assert fakedljson.call_count == 0
        assert crel.eol == "2024-05-16"
        assert fakedljson.call_count == 1
        assert fakedljson.call_args == (("https://bodhi.fedoraproject.org/releases/F40",),)

    @mock.patch("fedfind.release.get_release", autospec=True)
    def test_previous_release(self, fakeget, httpkp):
        """Test previous_release - the metadata archive-based
        one in Pungi4Release, not the ugly old one - works as
        expected.
        """
        rel = fedfind.release.Pungi4Release(
            "https://kojipkgs.fedoraproject.org/compose/branched/Fedora-40-20240413.n.0/",
            cid="Fedora-40-20240413.n.0",
        )
        rel._status = "FINISHED_INCOMPLETE"
        rel.previous_release
        assert fakeget.call_args[1] == {"cid": "Fedora-40-20240412.n.1"}

    @mock.patch("fedfind.helpers.url_exists", autospec=True)
    @pytest.mark.parametrize(
        ("rel", "expurl"),
        [
            (
                fedfind.release.Compose("42", "Beta", "1", "2"),
                "https://dl.fedoraproject.org/pub/alt/stage/42_Beta-1.2/metadata/images.json",
            ),
            (
                fedfind.release.RawhideNightly("20230831", 0, "Fedora-Rawhide-20230831.n.0"),
                "https://kojipkgs.fedoraproject.org/compose/rawhide/Fedora-Rawhide-20230831.n.0/compose",
            ),
            (
                fedfind.release.CurrentRelease("40"),
                "http://localhost:5001/pub/fedora/linux/releases/40/Everything",
            ),
        ],
    )
    def test_exists(self, fakehue, rel, expurl):
        """Tests for the exists property for various release classes."""
        fakehue.return_value = False
        assert not rel.exists
        assert fakehue.call_count == 1
        assert fakehue.call_args[0] == (expurl,)
        fakehue.return_value = True
        assert rel.exists
        assert fakehue.call_count == 2
        assert rel.exists
        assert fakehue.call_count == 2


# vim: set textwidth=100 ts=8 et sw=4:
