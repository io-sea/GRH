#!/usr/bin/env python3

#
#  All rights reserved (c) 2014-2022 CEA/DAM.
#
#  This file is part of the Ganesha Request Handler.
#
#  The Ganesha Request Handler is free software: you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public License as
#  published by the Free Software Foundation, either version 2.1 of the License,
#  or (at your option) any later version.
#
#  The Ganesha Request Handler is distributed in the hope that it will be
#  useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with the Ganesha Request Handler. If not,
#  see <http://www.gnu.org/licenses/>.
#

"""
Dispatcher of each requests to the backends.
"""

import ctypes
from ctypes import CDLL
from ctypes.util import find_library

backend_list = ["phobos", "s3", "empty", "test"]
backends = {}

def init():
    with open("/tmp/blob_init.txt", "a") as f:
        f.write(str(backend_list) + "\n")
        for backend in backend_list:
            f.write("backend = |" + backend + "|\n")
            libbackend_name = find_library(backend)
            f.write("libbackend_name = |" + str(libbackend_name) + "|\n")
            if libbackend_name is None:
                continue

            try:
                backend_lib = CDLL(libbackend_name)
                f.write("lib found\n")
                backends[libbackend_name] = backend_lib
                f.write("backend_lib = |" + str(backend_lib) + "|\n")
                f.write("elt_count = |" + str(len(backends)) + "|\n")
                f.write("calling backend init\n")
                backend_lib.init(len(backend))
                f.write("backend init ended\n")
                f.write("calling backend blob func\n")
                test_str = "test"
                b_test_str = test_str.encode('utf-8')
                pointer = ctypes.c_char_p(b_test_str)
                backend_lib.blob(pointer)
                f.write("backend blob ended\n")
            except OSError as err:
                f.write("Err = " + str(err) + ", type = " + str(type(err)) + "\n")
            f.write("\n")

def dispatch(file_id, action, backend):
    with open("/tmp/blob_dispatch.txt", "a") as f:
        f.write(backend + (" is in list\n" if backend in backend_list else " is not in list\n"))
