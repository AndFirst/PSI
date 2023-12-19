#include "sockets.h"
#include "linked_list.h"

#include <errno.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include <arpa/inet.h>

#define MAX_IP_LENGTH 40  // IPv6 address length is longer than IPv4
#define PORT 8000
#define MESSAGE_LEN 1000

void processReceivedLinkedList(char *packed_data, int packed_size)
{
    struct LinkedList ll;
    ll.head = NULL;

    unpack_linked_list(&ll, packed_data, packed_size);

    printf("Received Linked List:\n");
    display_linked_list(&ll);

    free_linked_list(&ll);
}

void dispatchResponse(int socketFD, char *message)
{
    int bytesSent;
    size_t messageLen = strlen(message) + 1;
    bytesSent = send(socketFD, message, messageLen, 0);
    if (bytesSent < 0)
    {
        perror("send (server)");
        exit(EXIT_FAILURE);
    }
}

void processRecvError()
{
    perror("recv (server)");
    exit(EXIT_FAILURE);
}

int verifyDataCorrectness(char *message, int size)
{
    printf("Data correctness status: ");

    int data_length;
    memcpy(&data_length, message, sizeof(int));
    data_length = swapEndianness(data_length);
    printf("size: %d data_len: %d\n", size, data_length);
    if (size != data_length)
    {
        printf("not correct length\n");
        return 0;
    }
    printf("correct\n");
    return 1;
}

void conductReception(int socketFD)
{
    struct sockaddr_storage clientAddress;
    socklen_t clientAddressSize = sizeof(clientAddress);
    char message[MESSAGE_LEN];
    int bytesReceived;
    char *response;

    if (listen(socketFD, 5) < 0)
    {
        perror("listen (server)");
        exit(EXIT_FAILURE);
    }

    while (1)
    {
        int clientSocketFD = accept(socketFD, (struct sockaddr *)&clientAddress, &clientAddressSize);
        if (clientSocketFD < 0)
        {
            perror("accept (server)");
            exit(EXIT_FAILURE);
        }

        if (clientAddress.ss_family == AF_INET)
        {
            struct sockaddr_in *ipv4 = (struct sockaddr_in *)&clientAddress;
            inet_ntop(AF_INET, &(ipv4->sin_addr), message, MAX_IP_LENGTH);
        }
        else
        {
            struct sockaddr_in6 *ipv6 = (struct sockaddr_in6 *)&clientAddress;
            inet_ntop(AF_INET6, &(ipv6->sin6_addr), message, MAX_IP_LENGTH);
        }

        printf("Connection from: %s\n", message);

        bytesReceived = recv(clientSocketFD, message, MESSAGE_LEN, 0);
        if (bytesReceived < 0)
            processRecvError();

        processReceivedLinkedList(message + sizeof(int), bytesReceived - sizeof(int));

        response = verifyDataCorrectness(message, bytesReceived) ? "Data correct\0" : "Invalid data\0";
        dispatchResponse(clientSocketFD, response);

        close(clientSocketFD);
    }
}

int main()
{
    int socketFD;

    socketFD = createStreamSocketIPv6(PORT);  // Pass a flag to indicate IPv6

    conductReception(socketFD);

    close(socketFD);
    return 0;
}
