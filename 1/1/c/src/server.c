#include "sockets.h"
#include <errno.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include <arpa/inet.h>

#define MAX_IP_LENGTH 17
#define PORT 8000
#define MESSAGE_LEN 1000

void obtainHostIP(char *hostname, struct sockaddr_in *address)
{
    strcpy(hostname, inet_ntoa(address->sin_addr));
}

void recordReceivedMessage(char *message, struct sockaddr_in *address)
{
    char hostIP[MAX_IP_LENGTH];
    unsigned short length = message[0] << 8;
    length += message[1];
    obtainHostIP(hostIP, address);
    printf("-------------------------------------\n");
    printf("Received message from: %s\n", hostIP);
    printf("Message length: %d\n", length);
    printf("Message: %s\n", message + 2);
    printf("-------------------------------------\n");
}

void dispatchResponse(int socketFD, struct sockaddr *addr,
                      size_t addressSize, char *message)
{
    int bytesReceived;
    size_t messageLen = strlen(message) + 1;
    bytesReceived = sendto(socketFD, message, messageLen,
                           0, addr, addressSize);
}

void processRecvError()
{
    perror("recvfrom (server)");
    exit(EXIT_FAILURE);
}

int verifyDataCorrectness(char *message, int size)
{
    printf("Data correctness status: ");
    if (size < 3)
    {
        printf("too short\n");
        return 0;
    }

    if (message[size - 1] != 0)
    {
        printf("no zero\n");
        return 0;
    }

    int data_length = (message[0] << 8) | message[1];

    if (size != data_length)
    {
        printf("not correct length\n");
        return 0;
    }

    const char *payload = message + 2;

    for (int i = 0; i < data_length - 3; i++)
    {
        if (!(payload[i] >= 65 && payload[i] <= 90))
        {
            printf("not A-Z\n");
            return 0;
        }
    }
    for (int i = 0; i < data_length - 4; i++)
    {
        if (!((payload[i + 1] - payload[i] == 1) || (payload[i] == 'Z' && payload[i + 1] == 'A')))
        {
            printf("wrong order\n");
            return 0;
        }
    }
    printf("correct\n");
    return 1;
}

void conductReception(int socketFD)
{
    int shouldStop = 0;
    struct sockaddr_in clientAddress;
    size_t clientAddressSize;
    char message[MESSAGE_LEN];
    int bytesReceived;
    char *response;
    while (!shouldStop)
    {
        clientAddressSize = sizeof(clientAddress);
        bytesReceived =
            recvfrom(socketFD, message, MESSAGE_LEN, 0,
                     (struct sockaddr *)&clientAddress, &clientAddressSize);
        if (bytesReceived < 0)
            processRecvError();
        recordReceivedMessage(message, &clientAddress);
        if (verifyDataCorrectness(message, bytesReceived))
        {
            response = "Data correct\0";
        }
        else
        {
            response = "Invalid data\0";
        }
        dispatchResponse(socketFD, (struct sockaddr *)&clientAddress,
                         clientAddressSize, response);
    }
}

int main()
{
    int socketFD;

    socketFD = createDatagramSocket(PORT);

    conductReception(socketFD);

    close(socketFD);
    return 0;
}
