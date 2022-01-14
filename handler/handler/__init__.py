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

from .dispatch import dispatch, init

def handle(file_id, action, backend):
    with open("/tmp/blob_handle.txt", "a") as f:
        f.write("file_id = " + file_id + "\n")
        f.write("action = " + action + "\n")
        f.write("backend = " + backend + "\n")
        init()
        f.write("end\n")
        dispatch(file_id, action, backend, None)
