#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

#include "empty.h"

void* init()
{
    FILE *fp = fopen("/tmp/grh_log.txt", "w");
    int rc;

    fprintf(fp, "Init function of the empty lib\n");

    rc = fclose(fp);
    if (rc)
        return NULL;

    return NULL;
}

int put(char *file_id, void* context)
{
    FILE *fp = fopen("/tmp/grh_log.txt", "a");
    int rc;

    if (context == NULL)
        fprintf(fp, "Put function of the empty lib, no context\n");
    else
        fprintf(fp, "Put function of the empty lib\n");

    rc = fclose(fp);
    if (rc)
        return -errno;

    return -ENOTSUP;
}

int get(char *file_id, void* context)
{
    FILE *fp = fopen("/tmp/grh_log.txt", "a");
    int rc;

    if (context == NULL)
        fprintf(fp, "Get function of the empty lib, no context\n");
    else
        fprintf(fp, "Get function of the empty lib\n");

    rc = fclose(fp);
    if (rc)
        return -errno;

    return -ENOTSUP;
}

int delete(char *file_id, void* context)
{
    FILE *fp = fopen("/tmp/grh_log.txt", "a");
    int rc;

    if (context == NULL)
        fprintf(fp, "Delete function of the empty lib, no context\n");
    else
        fprintf(fp, "Delete function of the empty lib\n");

    rc = fclose(fp);
    if (rc)
        return -errno;

    return -ENOTSUP;
}
