#define _GNU_SOURCE

#include <fcntl.h>
#include <sys/stat.h>

#include <phobos_store.h>

#include "backend.h"

/**
 * Return the open flags corresponding to the xfer flags
 */
static int xfer2open_flags(enum pho_xfer_flags flags)
{
    return (flags & PHO_XFER_OBJ_REPLACE) ? O_CREAT|O_WRONLY|O_TRUNC
                                          : O_CREAT|O_WRONLY|O_EXCL;
}

/**
 * Open the file descriptor contained in the xfer descriptor data structure
 * using path, op and flags.
 * Return the file descriptor or negative error code on failure.
 */
static int xfer_desc_open_path(struct pho_xfer_desc *xfer, const char *path,
                               enum pho_xfer_op op, enum pho_xfer_flags flags)
{
    struct stat st;

    if (path == NULL) {
        xfer->xd_fd = -1;
        return -EINVAL;
    }

    xfer->xd_op = op;
    xfer->xd_flags = flags;

    if (xfer->xd_op == PHO_XFER_OP_GET)
        /* Set file permission to 666 and let user umask filter unwanted bits */
        xfer->xd_fd = open(path, xfer2open_flags(xfer->xd_flags));
    else
        xfer->xd_fd = open(path, O_RDONLY);

    if (xfer->xd_fd < 0)
        return -errno;

    if (xfer->xd_op == PHO_XFER_OP_PUT) {
        fstat(xfer->xd_fd, &st);
        xfer->xd_params.put.size = st.st_size;
        xfer->xd_params.put.overwrite = true;
    }

    return xfer->xd_fd;
}

/**
 * Close the file descriptor contained in the xfer dsecriptor data structure.
 * Return 0 on success, -errno on failure.
 */
static int xfer_desc_close_fd(struct pho_xfer_desc *xfer)
{
    int rc;

    if (xfer->xd_fd >= 0) {
        rc = close(xfer->xd_fd);
        if (rc)
            return -errno;
    }

    return 0;
}

static int open_xfer_alloc_oid(struct pho_xfer_desc *xfer, const char *file_id,
                               enum pho_xfer_op op, const char *log_file)
{
    int rc = 0;

    /* open the xfer path and properly set xfer values */
    rc = xfer_desc_open_path(xfer, file_id, op, 0);
    if (rc < 0) {
        write_log(log_file, "Failed to open file '%s'", file_id);
        goto out;
    }

    xfer->xd_params.put.family = PHO_RSC_DIR;
    xfer->xd_objid = strdup(file_id);
    if (!xfer->xd_objid) {
        write_log(log_file, "Couldn't allocate oid '%s'\n", file_id);
        rc = -ENOMEM;
        goto clean_xfer;
    }

    return 0;

clean_xfer:
    xfer_desc_close_fd(xfer);
    pho_xfer_desc_clean(xfer);

out:
    return rc;
}

int grh_init(char *context)
{
    write_log("/tmp/grh_log.txt", "Init function of the phobos lib\n");

    return 0;
}

int grh_put(const char *file_id, const char *context, const char *log_file)
{
    struct pho_xfer_desc xfer = {0};
    int rc;

    (void) context;

    rc = open_xfer_alloc_oid(&xfer, file_id, PHO_XFER_OP_PUT, log_file);
    if (rc)
        goto out;

    /* put the object and close the descriptor */
    rc = phobos_put(&xfer, 1, NULL, NULL);
    if (rc) {
        write_log(log_file, "Failed to put file '%s' with oid '%s'",
                  file_id, xfer.xd_objid);
        goto clean;
    }

clean:
    xfer_desc_close_fd(&xfer);
    pho_xfer_desc_clean(&xfer);
    free(xfer.xd_objid);

out:
    return rc;
}

int grh_get(const char *file_id, const char *context, const char *log_file)
{
    struct pho_xfer_desc xfer = {0};
    int rc;

    (void) context;

    rc = open_xfer_alloc_oid(&xfer, file_id, PHO_XFER_OP_GET, log_file);
    if (rc)
        goto out;

    rc = phobos_get(&xfer, 1, NULL, NULL);
    if (rc) {
        write_log(log_file, "Failed to get file '%s' with oid '%s'",
                  file_id, xfer.xd_objid);
        goto clean;
    }

clean:
    xfer_desc_close_fd(&xfer);
    pho_xfer_desc_clean(&xfer);
    free(xfer.xd_objid);

out:
    return rc;
}

int grh_delete(const char *file_id, const char *context, const char *log_file)
{
    struct pho_xfer_desc xfer = {0};
    int rc;

    (void) context;

    xfer.xd_objid = strdup(file_id);
    if (!xfer.xd_objid) {
        write_log(log_file, "Couldn't allocate oid '%s'\n", file_id);
        rc = -ENOMEM;
        goto out;
    }

    rc = phobos_delete(&xfer, 1);
    if (rc) {
        write_log(log_file, "Failed to delete file '%s' with oid '%s'",
                  file_id, xfer.xd_objid);
        goto out;
    }

out:
    free(xfer.xd_objid);
    return rc;
}
