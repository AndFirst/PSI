INCLUDE_DIR=../include
CC=gcc
CFLAGS=-I$(INCLUDE_DIR)
OBJECT_DIR=../obj
BUILD_DIR=../build

LIBS=-lm

_DEPS = server.h
DEPS = $(patsubst %,$(INCLUDE_DIR)/%,$(_DEPS))

_OBJ = server.o make_socket.o
OBJ = $(patsubst %,$(OBJECT_DIR)/%,$(_OBJ))

_CLIENT_OBJ = client.o make_socket.o
CLIENT_OBJ = $(patsubst %,$(OBJECT_DIR)/%,$(_CLIENT_OBJ))

# _CLIENT2_OBJ = client_1_2.o make_socket.o
# CLIENT2_OBJ = $(patsubst %,$(OBJECT_DIR)/%,$(_CLIENT2_OBJ))

$(OBJECT_DIR)/%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

server: $(OBJ)
	$(CC) -o $(BUILD_DIR)/$@ $^ $(CFLAGS) $(LIBS)

client: $(CLIENT_OBJ)
	$(CC) -o $(BUILD_DIR)/$@ $^ $(CFLAGS) $(LIBS)

# client_1_2: $(CLIENT2_OBJ)
# 	$(CC) -o $(BUILD_DIR)/$@ $^ $(CFLAGS) $(LIBS)

.PHONY: clean

clean:
	rm -f $(OBJECT_DIR)/*.o *~ core $(INCLUDE_DIR)/*~