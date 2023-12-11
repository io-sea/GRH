#define _GNU_SOURCE         /* See feature_test_macros(7) */
#include <stdio.h>

#include "backend.h"
#include "hestia/hestia.h"
#include "hestia/hestia_iosea.h"

#include <string.h>
#include <stdlib.h>

int grh_init(char *context)
{
    (void)context;

    write_log("/tmp/grh_log.txt", "Init function of the hestia lib\n");

    return 0;
}

int grh_put(const char *file_id, const char *context, const char *log_file)
{
    HestiaIoContext io_context;
    HestiaTier tier;
    HestiaId id;
    int rc = 0;

    (void) context;

    hestia_initialize("/etc/hestia/hestiad.yaml", NULL, NULL);
    rc = hestia_init_id(&id);
    if (rc)
        return rc;

    id.m_uuid = strdup(file_id);
    if (id.m_uuid == NULL)
        return -ENOMEM;

    rc = hestia_init_io_ctx(&io_context);
    if (rc)
        goto free_id;

    io_context.m_type = HESTIA_IO_PATH;
    io_context.m_offset = 0;
    io_context.m_path = strdup(file_id);
    if (io_context.m_path == NULL) {
        rc = -ENOMEM;
        goto free_id;
    }

    rc = hestia_init_tier(&tier);
    if (rc)
        goto free_context;

    rc = hestia_object_put(&id, HESTIA_CREATE, &io_context, &tier);

free_context:
    free(io_context.m_path);

free_id:
    free(id.m_uuid);

    return rc;
}

int grh_get(const char *file_id, const char *context, const char *log_file)
{
    HestiaIoContext io_context;
    HestiaTier tier;
    HestiaId id;
    int rc = 0;

    (void) context;

    hestia_initialize("/etc/hestia/hestiad.yaml", NULL, NULL);
    rc = hestia_init_id(&id);
    if (rc)
        return rc;

    id.m_uuid = strdup(file_id);
    if (id.m_uuid == NULL)
        return -ENOMEM;

    rc = hestia_init_io_ctx(&io_context);
    if (rc)
        goto free_id;

    io_context.m_type = HESTIA_IO_PATH;
    io_context.m_offset = 0;
    io_context.m_path = strdup(file_id);
    if (io_context.m_path == NULL) {
        rc = -ENOMEM;
        goto free_id;
    }

    rc = hestia_init_tier(&tier);
    if (rc)
        goto free_context;

    rc = hestia_object_get(&id, &io_context, &tier);

free_context:
    free(io_context.m_path);

free_id:
    free(id.m_uuid);

    return rc;
}

int grh_delete(const char *file_id, const char *context, const char *log_file)
{
    HestiaId id;
    int rc = 0;

    (void) context;

    hestia_initialize("/etc/hestia/hestiad.yaml", NULL, NULL);

    rc = hestia_init_id(&id);
    if (rc)
        return rc;

    id.m_uuid = strdup(file_id);
    if (id.m_uuid == NULL)
        return -ENOMEM;

    rc = hestia_object_remove(&id);

    free(id.m_uuid);

    return rc;
}
