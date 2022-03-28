#ifndef __EMPTY_H__
#define __EMPTY_H__

int init(char *context);

int put(const char *file_id, const char *context, const char *log_file);
int get(const char *file_id, const char *context, const char *log_file);
int delete(const char *file_id, const char *context, const char *log_file);

#endif  // __EMPTY_H__
