FROM gcc:4.9
COPY . /client
WORKDIR /client/
RUN gcc -o client client.c linked_list.c sockets.c -i sockets.h linked_list.h
ENTRYPOINT  ["./client"]
