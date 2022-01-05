"""Utilities to handle a request"""

def handle(file_id, action, backend):
    with open("/tmp/blob.txt", "a") as f:
        f.write("hello\n")
        f.write("file_id = " + file_id + "\n")
        f.write("action = " + action + "\n")
        f.write("backend = " + backend + "\n")
        f.write("end\n\n")

#    """Migrate `fsname`/`fid` according to `hints` and `stripe-count`"""
#    stripe_count = (striping.get("stripe_count", None) if striping else None)
#    stripe_size = (striping.get("stripe_size", None) if striping else None)

#    command = ([CCC_HSM_CMD, "migrate_local_fid"]
#             + (["-c " + str(stripe_count)] if stripe_count is not None else [])
#             + (["-S " + str(stripe_size)] if stripe_size is not None else [])
#             + ["--" + hint for hint in hints]
#             + [fsname, fid])

    # If `command` fails, its output (stdout & stderr) is recorded in a
    # CalledProcessError exception.
#    subprocess.check_output(command, stderr=subprocess.STDOUT)
