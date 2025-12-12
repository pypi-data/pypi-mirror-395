# Copyright Red Hat
#
# fedfind is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author:   Adam Williamson <awilliam@redhat.com>

"""Setuptools script."""

from os import path
from setuptools import setup

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
try:
    with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
        LONGDESC = f.read()
except TypeError:
    with open(path.join(HERE, 'README.md')) as f:
        LONGDESC = f.read()

setup(
    name="fedfind",
    version="6.1.2",
    entry_points={'console_scripts': ['fedfind = fedfind.cli:main'],},
    author="Adam Williamson",
    author_email="awilliam@redhat.com",
    description="Fedora Finder finds Fedora - images, more to come?",
    license="GPLv3+",
    keywords="fedora release image media iso",
    url="https://pagure.io/fedora-qa/fedfind",
    packages=["fedfind"],
    package_dir={"": "src"},
    install_requires=open('install.requires').read().splitlines(),
    long_description=LONGDESC,
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 or later "
        "(GPLv3+)",
    ],
)

# vim: set textwidth=100 ts=8 et sw=4:
