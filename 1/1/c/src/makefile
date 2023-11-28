INCLUDE_DIR=../include
CC=gcc
CFLAGS=-I$(INCLUDE_DIR)
OBJECT_DIR=../obj
BUILD_DIR=../build

LIBS=-lm

_DEPS = sockets.h
DEPS = $(patsubst %,$(INCLUDE_DIR)/%,$(_DEPS))

_OBJ = server.o sockets.o
OBJ = $(patsubst %,$(OBJECT_DIR)/%,$(_OBJ))

_CLIENT_OBJ = client.o sockets.o
CLIENT_OBJ = $(patsubst %,$(OBJECT_DIR)/%,$(_CLIENT_OBJ))

$(OBJECT_DIR)/%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

server: $(OBJ)
	$(CC) -o $(BUILD_DIR)/$@ $^ $(CFLAGS) $(LIBS)

client: $(CLIENT_OBJ)
	$(CC) -o $(BUILD_DIR)/$@ $^ $(CFLAGS) $(LIBS)

.PHONY: clean

clean:
	rm -f $(OBJECT_DIR)/*.o *~ core $(INCLUDE_DIR)/*~