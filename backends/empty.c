#include <errno.h>
#include <string.h>

#include "backend.h"

int grh_init(char *context)
{
    write_log("/tmp/grh_log.txt", "Init function of the empty lib\n");
    strcpy(context, "hello\n");

    return 0;
}

int grh_put(const char *uuid, const char *file_id, const char* context,
            const char *log_file)
{
    if (context == NULL)
        write_log("/tmp/grh_log.txt",
                  "Put function of the empty lib, no context\n");
    else
        write_log("/tmp/grh_log.txt",
                  "Put function of the empty lib, context = '%s'\n", context);

    write_log(log_file, "Not implemented yet !\n");

    return -ENOTSUP;
}

int grh_get(const char *uuid, const char *file_id, const char* context,
            const char *log_file)
{
    if (context == NULL)
        write_log("/tmp/grh_log.txt",
                  "Get function of the empty lib, no context\n");
    else
        write_log("/tmp/grh_log.txt",
                  "Get function of the empty lib, context = '%s'\n", context);

    write_log(log_file, "Not implemented yet !\n");

    return -ENOTSUP;
}

int grh_delete(const char *uuid, const char *file_id, const char* context,
               const char *log_file)
{
    if (context == NULL)
        write_log("/tmp/grh_log.txt",
                  "Delete function of the empty lib, no context\n");
    else
        write_log("/tmp/grh_log.txt",
                  "Delete function of the empty lib, context = '%s'\n",
                  context);

    write_log(log_file, "Not implemented yet !\n");

    return -ENOTSUP;
}
