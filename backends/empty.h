#ifndef __EMPTY_H__
#define __EMPTY_H__

int init(char *context);

int put(char *file_id, char *context, char *log_file);
int get(char *file_id, char *context, char *log_file);
int delete(char *file_id, char *context, char *log_file);

#endif  // __EMPTY_H__
