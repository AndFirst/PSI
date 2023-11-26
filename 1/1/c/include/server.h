#include <netinet/in.h>
#include <stdint.h>
#include <sys/socket.h>
int makeDatagramSocket(uint16_t port);
void buildSockaddr(struct sockaddr_in *name, const char *hostname,
                   uint16_t port);