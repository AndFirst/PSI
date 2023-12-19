#include "sockets.h"
#include <errno.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

// Zmieniona implementacja funkcji do obsługi zarówno IPv4, jak i IPv6

int createStreamSocketIPv6(uint16_t port)
{
    int sock;
    struct sockaddr_in6 name;

    sock = socket(AF_INET6, SOCK_STREAM, 0);
    if (sock < 0)
    {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    name.sin6_family = AF_INET6;
    name.sin6_port = htons(port);
    name.sin6_addr = in6addr_any;

    if (bind(sock, (struct sockaddr *)&name, sizeof(name)) < 0)
    {
        perror("bind");
        exit(EXIT_FAILURE);
    }

    return sock;
}

void constructSocketAddressIPv6(struct sockaddr_in6 *address, const char *hostname, uint16_t port)
{
    struct addrinfo hints, *res;
    int status;

    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_INET6;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags = AI_PASSIVE; 

    char service[6];  
    snprintf(service, sizeof(service), "%d", port); 

    if ((status = getaddrinfo(hostname, service, &hints, &res)) != 0)
    {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(status));
        exit(EXIT_FAILURE);
    }

    memcpy(address, res->ai_addr, res->ai_addrlen);
    freeaddrinfo(res);
}
