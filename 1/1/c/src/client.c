#include <netinet/in.h>
#include <server.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#define SERVER_HOSTNAME "localhost"
#define SERVER_PORT 8000
#define PORT 8001
#define MESSAGE_MAXLEN 1000

void generateValidData(char *message, short int length)
{
    message[0] = (length & 0xFF00) >> 8;
    message[1] = length & 0x00FF;
    for (int i = 0; i + 2 < length - 1; ++i)
    {
        *(message + i + 2) = ('A' + (i % 26));
    }
    message[length - 1] = '\0';
}

int main()
{
    int socketFD;
    struct sockaddr_in serverAddress;
    int bytesSent;
    int bytesReceived;

    char message[MESSAGE_MAXLEN];
    size_t messageLength = 100;
    char messageReceived[MESSAGE_MAXLEN];
    generateValidData(message, messageLength);

    int length = message[0] << 8;
    length += message[1];

    socketFD = makeDatagramSocket(8001);

    buildSockaddr(&serverAddress, SERVER_HOSTNAME, SERVER_PORT);
    char ipAddress[INET_ADDRSTRLEN];
    
    // Convert binary IP address to string representation
    if (inet_ntop(AF_INET, &(serverAddress.sin_addr), ipAddress, INET_ADDRSTRLEN) == NULL) {
        perror("inet_ntop");
    }
    int port = ntohs(serverAddress.sin_port);
    printf("C client\n");
    printf("Server address: %s\n", ipAddress);    
    printf("Server port: %d\n", port);    
    printf("Message length: %d\n", length);
    printf("Content: %s\n", message + 2);
    bytesSent = sendto(socketFD, message, messageLength, 0,
                       (struct sockaddr *)&serverAddress, sizeof(serverAddress));

    if (bytesSent < 0)
    {
        perror("sendto (client)");
        exit(EXIT_FAILURE);
    }

    bytesReceived = recvfrom(socketFD, messageReceived, MESSAGE_MAXLEN, 0, NULL, 0);
    if (bytesReceived < 0)
    {
        perror("recvfrom (client)");
        exit(EXIT_FAILURE);
    }

    printf("Received response: %s\n", messageReceived);

    close(socketFD);
    return 0;
}