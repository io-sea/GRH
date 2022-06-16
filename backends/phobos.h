#ifndef __PHOBOS_H__
#define __PHOBOS_H__

#include "phobos_store.h"

int init(char *context);

int put(const char *file_id, const char *context, const char *log_file);
int get(const char *file_id, const char *context, const char *log_file);
int delete(const char *file_id, const char *context, const char *log_file);

#endif  // __PHOBOS_H__
