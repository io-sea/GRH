#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

#include "empty.h"

void foo(void)
{
    puts("Hello, I am a shared library");
}

void init(int input)
{
    int fd = open("/tmp/blob_c.txt", O_CREAT | O_RDWR, S_IROTH);
    char *buf = malloc(15);

    write(fd, "blob_c\n", 7);
    sprintf(buf, "input = |%d|\n", input);

    write(fd, buf, 15);
}

void blob(char *file_id)
{
    int fd = open("/tmp/blob_c_bis.txt", O_CREAT | O_RDWR, S_IROTH);

    write(fd, "blob_c_bis\n", 7);
    write(fd, "input = |", 9);
    write(fd, file_id, 15);
    write(fd, "|\n", 2);
}
