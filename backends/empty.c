#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

#include "empty.h"

int init(char *context)
{
    FILE *fp = fopen("/tmp/grh_log.txt", "w");
    int rc;

    fprintf(fp, "Init function of the empty lib\n");

    rc = fclose(fp);
    if (rc)
        return -errno;

    strcpy(context, "hello\n");

    return 0;
}

int put(char *file_id, char* context, char *log_file)
{
    FILE *fp = fopen("/tmp/grh_log.txt", "a");
    int rc;

    if (context == NULL)
        fprintf(fp, "Put function of the empty lib, no context\n");
    else
        fprintf(fp, "Put function of the empty lib, context = '%s'\n", context);

    rc = fclose(fp);
    if (rc)
        return -errno;

    if (log_file != NULL) {
        FILE *logger = fopen(log_file, "w");

        fprintf(logger, "Not implemented yet !\n");
        fclose(logger);
    }

    return -ENOTSUP;
}

int get(char *file_id, char* context, char *log_file)
{
    FILE *fp = fopen("/tmp/grh_log.txt", "a");
    int rc;

    if (context == NULL)
        fprintf(fp, "Get function of the empty lib, no context\n");
    else
        fprintf(fp, "Get function of the empty lib, context = '%s'\n", context);

    rc = fclose(fp);
    if (rc)
        return -errno;

    if (log_file != NULL) {
        FILE *logger = fopen(log_file, "w");

        fprintf(logger, "Not implemented yet !\n");
        fclose(logger);
    }

    return -ENOTSUP;
}

int delete(char *file_id, char* context, char *log_file)
{
    FILE *fp = fopen("/tmp/grh_log.txt", "a");
    int rc;

    if (context == NULL)
        fprintf(fp, "Delete function of the empty lib, no context\n");
    else
        fprintf(fp, "Delete function of the empty lib, context = '%s'\n",
                context);

    rc = fclose(fp);
    if (rc)
        return -errno;

    if (log_file != NULL) {
        FILE *logger = fopen(log_file, "w");

        fprintf(logger, "Not implemented yet !\n");
        fclose(logger);
    }

    return -ENOTSUP;
}
