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
    struct sockaddr_in clientAddress;
    size_t clientAddressSize = sizeof(clientAddress);
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
        int clientSocketFD = accept(socketFD, (struct sockaddr *)&clientAddress, (socklen_t *)&clientAddressSize);
        if (clientSocketFD < 0)
        {
            perror("accept (server)");
            exit(EXIT_FAILURE);
        }

        bytesReceived = recv(clientSocketFD, message, MESSAGE_LEN, 0);
        if (bytesReceived < 0)
            processRecvError();
        recordReceivedMessage(message, &clientAddress);
        response = verifyDataCorrectness(message, bytesReceived) ? "Data correct\0" : "Invalid data\0";
        dispatchResponse(clientSocketFD, response);
        
        close(clientSocketFD);
    }

}

int main()
{
    int socketFD;

    socketFD = createStreamSocket(PORT);

    conductReception(socketFD);

    close(socketFD);
    return 0;
}
