#include <climits>
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
    std::string size_attr;
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

    size_attr = "{\"size\": " + std::to_string(size) + "}";
    rc = hestia::set_attrs(oid, size_attr.c_str());
    if (rc < 0)
        write_log(log_file, "Failed to set size attr '%s'", size_attr);

out:
    input_file.close();
    return rc;
}

static int attr2uint(const struct hestia::hsm_uint oid, const char *attr,
                     std::size_t *value)
{
    std::string str_attr = hestia::get_attrs(oid, attr);
    std::size_t found;
    int save_errno;
    int rc = 0;

    if (str_attr.empty())
        return -ENODATA;

    found = str_attr.find(":") + 1;
    str_attr = str_attr.substr(found);

    save_errno = errno;
    errno = 0;
    *value = std::stoull(str_attr, NULL, 0);
    if (errno && ULLONG_MAX)
        rc = errno;

    errno = save_errno;

    return rc;
}

int grh_get(const char *file_id, const char *context, const char *log_file)
{
    struct hestia::hsm_uint oid;
    struct hestia::hsm_obj obj;
    std::ofstream output_file;
    std::vector<char> buffer;
    std::uint8_t tier;
    std::size_t size;
    int rc = 0;

    (void)context;

    oid.lower = charsum(file_id);
    hestia::create_object(oid, obj);

    rc = attr2uint(oid, "size", &size);
    if (rc) {
        write_log(log_file, "Failed to retrieve size of file '%s'\n", file_id);
        return rc;
    }

    rc = attr2uint(oid, "tier", (std::size_t*)&tier);
    if (rc) {
        write_log(log_file, "Failed to retrieve tier of file '%s'\n", file_id);
        return rc;
    }

    buffer.reserve(size);
    rc = hestia::get(oid, &obj, buffer.data(), 0, size, tier, 0);
    if (rc < 0)
        write_log(log_file, "Failed to get file '%s' with oid '%ld'",
                  file_id, oid.lower);

    output_file.open(file_id, std::ofstream::binary);
    if (!output_file) {
        write_log(log_file, "Failed to open '%s', err: '%s'\n",
                  file_id, strerror(errno));
        return -errno;
    }

    if (!output_file.write(&buffer[0], size)) {
        write_log(log_file, "Failed to write content to '%s'\n", file_id);
        rc = -errno;
    }

    output_file.close();
    return rc;
}

int grh_delete(const char *file_id, const char *context, const char *log_file)
{
    struct hestia::hsm_uint oid(charsum(file_id));
    int rc;

    rc = hestia::remove(oid);
    if (rc < 0)
        write_log(log_file, "Failed to remove file '%s' with oid '%ld'",
                  file_id, oid.lower);

    return rc;
}
