#ifndef __BACKEND_H__
#define __BACKEND_H__

#include <stdarg.h>
#include <stdio.h>
#include <unistd.h>

__attribute__ ((format (printf, 2, 3)))
void write_log(const char *log_file, const char *fmt, ...)
{
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
}

int init(char *context);

int put(const char *file_id, const char *context, const char *log_file);
int get(const char *file_id, const char *context, const char *log_file);
int delete(const char *file_id, const char *context, const char *log_file);

#endif  // __BACKEND_H__
