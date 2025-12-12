#!/usr/bin/env python3
# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4; encoding:utf-8 -*-
#
# Copyright 2002 Ben Escoto
# Copyright 2007 Kenneth Loafman
#
# This file is part of duplicity.
#
# Duplicity is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# Duplicity is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with duplicity; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import glob
import os
import shutil
import subprocess
import sys
import warnings

warnings.filterwarnings("ignore", message="setup.py install is deprecated")
warnings.filterwarnings("ignore", message="easy_install command is deprecated")
warnings.filterwarnings("ignore", message="pyproject.toml does not contain a tool.setuptools_scm section")
warnings.filterwarnings("ignore", message="Configuring installation scheme with distutils config files")

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

# check that we can function here
if os.environ.get("PYTEST_VERSION") is not None:
    pass
elif not ((3, 9) <= sys.version_info[:2] <= (3, 14)):
    print("Sorry, duplicity requires version 3.9 thru 3.14 of Python.", file=sys.stderr)
    sys.exit(1)

Version: str = "3.0.7.dev0"

# READTHEDOCS uses setup.py sdist but can't handle extensions
ext_modules = list()
incdir_list = list()
libdir_list = list()
if os.environ.get("READTHEDOCS", None) is None:
    # set incdir and libdir for librsync
    if os.name == "posix":
        LIBRSYNC_DIR = os.environ.get("LIBRSYNC_DIR", "")
        args = sys.argv[:]
        for arg in args:
            if arg.startswith("--librsync-dir="):
                LIBRSYNC_DIR = arg.split("=")[1]
                sys.argv.remove(arg)
        if LIBRSYNC_DIR:
            incdir_list.append(os.path.join(LIBRSYNC_DIR, "include"))
            libdir_list.append(os.path.join(LIBRSYNC_DIR, "lib"))

    # set incdir and libdir for pyenv
    if pyenv_root := os.environ.get("PYENV_ROOT", None):
        major, minor, patch = sys.version_info[:3]
        incdir_list.append(
            os.path.join(
                f"{pyenv_root}",
                f"versions",
                f"{major}.{minor}.{patch}",
                f"include",
                f"python{major}.{minor}",
            )
        )
        libdir_list.append(
            os.path.join(
                f"{pyenv_root}",
                f"versions",
                f"{major}.{minor}.{patch}",
                f"lib",
                f"python{major}.{minor}",
            )
        )

    # add standard locs
    incdir_list.append("/usr/local/include")
    libdir_list.append("/usr/local/lib")
    incdir_list.append("/usr/include")
    libdir_list.append("/usr/lib")

    # build the librsync extension
    ext_modules = [
        Extension(
            name=r"duplicity._librsync",
            sources=["duplicity/_librsyncmodule.c"],
            include_dirs=incdir_list,
            library_dirs=libdir_list,
            libraries=["rsync"],
        )
    ]


def get_data_files():
    """gen list of data files"""

    # static data files
    data_files = [
        (
            "share/man/man1",
            [
                "man/duplicity.1",
            ],
        ),
        (
            f"share/doc/duplicity-{Version}",
            [
                "CHANGELOG.md",
                "AUTHORS.md",
                "COPYING",
                "README.md",
                "README-LOG.md",
                "README-REPO.md",
                "README-TESTING.md",
            ],
        ),
    ]

    # short circuit fot READTHEDOCS
    if os.environ.get("READTHEDOCS") == "True":
        return data_files

    # msgfmt the translation files
    assert os.path.exists("po"), "Missing 'po' directory."

    linguas = glob.glob("po/*.po")
    for lang in linguas:
        lang = lang[3:-3]
        try:
            os.mkdir(os.path.join("po", lang))
        except os.error:
            pass
        subprocess.run(f"cp po/{lang}.po po/{lang}", shell=True, check=True)
        subprocess.run(f"msgfmt po/{lang}.po -o po/{lang}/duplicity.mo", shell=True, check=True)

    for root, dirs, files in os.walk("po"):
        for file in files:
            path = os.path.join(root, file)
            if path.endswith("duplicity.mo"):
                lang = os.path.split(root)[-1]
                data_files.append((f"share/locale/{lang}/LC_MESSAGES", [f"po/{lang}/duplicity.mo"]))

    return data_files


def cleanup():
    if os.path.exists("po/LINGUAS"):
        linguas = open("po/LINGUAS").readlines()
        for line in linguas:
            langs = line.split()
            for lang in langs:
                shutil.rmtree(os.path.join("po", lang), ignore_errors=True)


class BuildExtCommand(build_ext):
    """Build extension modules."""

    def run(self):
        # build the _librsync.so module
        print("Building extension for librsync...")
        self.inplace = True
        build_ext.run(self)


setup(
    version=Version,
    packages=[
        "duplicity",
        "duplicity.backends",
        "duplicity.backends.pyrax_identity",
    ],
    package_dir={
        "duplicity": "duplicity",
        "duplicity.backends": "duplicity/backends",
    },
    ext_modules=ext_modules,
    data_files=get_data_files(),
    include_package_data=True,
    cmdclass={
        "build_ext": BuildExtCommand,
    },
)

cleanup()
