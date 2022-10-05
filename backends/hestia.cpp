#include <fstream>

#include "backend.h"
#include "hestia.h"

/* This method may cause collisions, but it is temporary and will be changed
 * soon.
 */
static uint64_t charsum(const char *file_id)
{
    uint64_t res = 0;
    int i = 0;

    while (file_id[i])
        res += file_id[i++];

    return res;
}

int grh_init(char *context)
{
    (void)context;

    write_log("/tmp/grh_log.txt", "Init function of the hestia lib\n");

    return 0;
}

int grh_put(const char *file_id, const char *context, const char *log_file)
{
    std::ifstream input_file(file_id, std::ifstream::binary);
    struct hestia::hsm_uint oid;
    struct hestia::hsm_obj obj;
    std::vector<char> buffer;
    std::streampos size;
    int rc = 0;

    (void)context;

    if (!input_file) {
        write_log(log_file, "Failed to open '%s', err: '%s'\n",
                  file_id, strerror(errno));
        return -errno;
    }

    oid.lower = charsum(file_id);

    if (!input_file.seekg(0, std::ios::end)) {
        write_log(log_file, "Failed to seek to the end of '%s'\n", file_id);
        rc = -errno;
        goto out;
    }

    size = input_file.tellg();
    if (size < 0) {
        write_log(log_file, "Failed to get the size of '%s'\n", file_id);
        rc = -errno;
        goto out;
    }

    if (!input_file.seekg(0)) {
        write_log(log_file, "Failed to seek to the start of '%s'\n", file_id);
        rc = -errno;
        goto out;
    }

    buffer.reserve(size);
    if (!input_file.read(&buffer[0], size)) {
        write_log(log_file, "Failed to read content of '%s'\n", file_id);
        rc = -errno;
        goto out;
    }

    rc = hestia::put(oid, &obj, false, buffer.data(), 0, size, 0);
    if (rc < 0)
        write_log(log_file, "Failed to put file '%s' with oid '%ld'",
                  file_id, oid.lower);

out:
    input_file.close();
    return rc;
}

int grh_get(const char *file_id, const char *context, const char *log_file)
{
    return -ENOTSUP;
}

int grh_delete(const char *file_id, const char *context, const char *log_file)
{
    return -ENOTSUP;
}
