#ifndef __EMPTY_H__
#define __EMPTY_H__

void* init(void);

int put(char *file_id, void *context, char *log_file);
int get(char *file_id, void *context, char *log_file);
int delete(char *file_id, void *context, char *log_file);

#endif  // __EMPTY_H__
