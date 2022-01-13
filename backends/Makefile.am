CFLAGS = -Wall -Wextra -O2 -g
LDFLAGS = -shared
RM = rm -f

.PHONY: all clean

EMPTY_LIB = libempty.so
EMPTY_SRCS = empty.c

$(EMPTY_LIB): $(EMPTY_SRCS)
	$(CC) $(CFLAGS) -o $(EMPTY_LIB) $(EMPTY_SRCS) -fPIC $(LDFLAGS)

ALL_LIBS = libempty.so

all: ${ALL_LIBS}

clean:
	${RM} *.o *.so
