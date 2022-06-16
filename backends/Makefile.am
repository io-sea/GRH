CFLAGS = -Wall -Wextra -O2 -g
LDFLAGS = -shared
RM = rm -f

.PHONY: all clean

EMPTY_LIB = libempty.so
EMPTY_SRCS = empty.c

$(EMPTY_LIB): $(EMPTY_SRCS)
	$(CC) $(CFLAGS) -o $(EMPTY_LIB) $(EMPTY_SRCS) -fPIC $(LDFLAGS)

PHOBOS_LIB = libphobos.so
PHOBOS_SRCS = phobos.c
PHOBOS_LDFLAGS = $(LDFLAGS) -lglib-2.0
PHOBOS_CFLAGS = $(CFLAGS) -I/usr/include/glib-2.0 -I/usr/lib64/glib-2.0/include

$(PHOBOS_LIB): $(PHOBOS_SRCS)
	$(CC) $(PHOBOS_CFLAGS) -o $(PHOBOS_LIB) $(PHOBOS_SRCS) \
		-fPIC $(PHOBOS_LDFLAGS) -lphobos_store

ALL_LIBS = libempty.so libphobos.so

all: ${ALL_LIBS}

clean:
	${RM} *.o *.so
