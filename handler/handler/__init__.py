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

"""Utilities to handle a request"""

from ctypes import CDLL, create_string_buffer, c_char_p
from ctypes.util import find_library
import errno
import os
import tempfile

def init(backend_list):
    backends = {}
    for backend in backend_list:
        libbackend_name = find_library(backend)
        if libbackend_name is None:
            continue

        try:
            backend_lib = CDLL(libbackend_name)
        except Exception as err:
            raise RuntimeError(str(errno.ELIBACC) + " Failed to open lib " +
                               str(libbackend_name) + "! Err = " +
                               os.strerror(errno.ELIBACC))

        context_str = create_string_buffer(16)
        rc = backend_lib.init(context_str)
        if rc is not 0:
            raise RuntimeError(str(-rc) + "Initialisation failed, init " +
                               "returned '" + os.strerror(-rc) + "'")

        backends[backend] = context_str.value.decode("utf-8")

    return backends

def dispatch(file_id, action, backend, backends_ctx):
    with open("/tmp/blob_handler_dispatch.txt", "a") as f:
        f.write("in dispatch\n")
        f.write("backends_ctx = " + str(backends_ctx) + "\n")
        f.write("file_id = " + str(file_id) + "\n")
        f.write("action = " + str(action) + "\n")
        f.write("backend = " + str(backend) + "\n")

    if backend not in backends_ctx:
        raise RuntimeError("95 Not supported yet !")

    file_id_ptr = c_char_p(file_id.encode('utf-8'))

    libbackend_name = find_library(backend)
    backend_lib = CDLL(libbackend_name)

    log_fd, log_path = tempfile.mkstemp()
    log_path_ptr = c_char_p(log_path.encode('utf-8'))

    b_ctx = backends_ctx[backend].encode('utf-8')
    ptr_ctx = c_char_p(b_ctx)

    if action == "put":
        rc = backend_lib.put(file_id_ptr, ptr_ctx, log_path_ptr)
    elif action == "get":
        rc = backend_lib.get(file_id_ptr, ptr_ctx, log_path_ptr)
    elif action == "delete":
        rc = backend_lib.delete(file_id_ptr, ptr_ctx, log_path_ptr)

    if rc is not 0:
        os.fsync(log_fd)
        with open(log_path, "r") as logger:
            full_log = logger.read()

    os.close(log_fd)
    os.remove(log_path)

    if rc is not 0:
        raise RuntimeError(str(rc) + " " + full_log)
