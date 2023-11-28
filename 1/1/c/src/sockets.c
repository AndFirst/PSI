#include "sockets.h"
#include <errno.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

int createDatagramSocket(uint16_t port)
{
    int sock;
    struct sockaddr_in name;

    sock = socket(PF_INET, SOCK_DGRAM, 0);
    if (sock < 0)
    {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    name.sin_family = AF_INET;
    name.sin_port = htons(port);
    name.sin_addr.s_addr = htonl(INADDR_ANY);
    if (bind(sock, (struct sockaddr *)&name, sizeof(name)) < 0)
    {
        perror("bind");
        exit(EXIT_FAILURE);
    }

    return sock;
}

void constructSocketAddress(struct sockaddr_in *address, const char *hostname,
                            uint16_t port)
{
    struct hostent *hostinfo;

    address->sin_family = AF_INET;
    address->sin_port = htons(port);
    hostinfo = gethostbyname(hostname);
    if (hostinfo == NULL)
    {
        fprintf(stderr, "Unknown host %s.\n", hostname);
        exit(EXIT_FAILURE);
    }
    address->sin_addr = *(struct in_addr *)(hostinfo->h_addr_list[0]);
}
