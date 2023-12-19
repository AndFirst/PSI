#ifndef SOCKETS_H
#define SOCKETS_H

#include <netinet/in.h>
#include <stdint.h>

// Zmodyfikowane funkcje do obsługi zarówno IPv4, jak i IPv6

int createStreamSocketIPv6(uint16_t port);
void constructSocketAddressIPv6(struct sockaddr_in6 *address, const char *hostname,
                                uint16_t port);

#endif
