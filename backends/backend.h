#ifndef __BACKEND_H__
#define __BACKEND_H__

#include <stdarg.h>
#include <stdio.h>
#include <unistd.h>
#include <errno.h>

__attribute__ ((format (printf, 2, 3)))
void write_log(const char *log_file, const char *fmt, ...)
{
    int save_errno = errno;
    FILE *logger;
    va_list args;
    int rc;

    if (log_file == NULL)
        return;

    va_start(args, fmt);

    logger = fopen(log_file, "a");
    if (!logger)
        goto out;

    rc = vfprintf(logger, fmt, args);
    if (rc < 0)
        goto out;

    fclose(logger);

out:
    va_end(args);
    errno = save_errno;
}

int grh_init(char *context);

int grh_put(const char *uuid, const char *file_id, const char *context,
            const char *log_file);
int grh_get(const char *uuid, const char *file_id, const char *context,
            const char *log_file);
int grh_delete(const char *uuid, const char *file_id, const char *context,
               const char *log_file);

#endif  // __BACKEND_H__
