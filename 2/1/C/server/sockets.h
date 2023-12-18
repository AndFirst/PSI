#ifndef SOCKETS_H
#define SOCKETS_H

#include <netinet/in.h>
#include <stdint.h>

int createStreamSocket(uint16_t port);
void constructSocketAddress(struct sockaddr_in *address, const char *hostname,
                            uint16_t port);

#endif
