"""Utilities to handle a request"""

from .dispatch import dispatch, init

def handle(file_id, action, backend):
    with open("/tmp/blob_handle.txt", "a") as f:
        f.write("file_id = " + file_id + "\n")
        f.write("action = " + action + "\n")
        f.write("backend = " + backend + "\n")
        dispatch(file_id, action, backend)
        f.write("end\n")
        init()
        f.write("true end\n\n")
