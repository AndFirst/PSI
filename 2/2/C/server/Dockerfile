FROM gcc:4.9
COPY . /server
WORKDIR /server/
RUN gcc -o server server.c linked_list.c sockets.c -I sockets.h linked_list.h
ENTRYPOINT  ["./server"]
