#include "sockets.h"
#include "linked_list.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

#define CLIENT_HOSTNAME "localhost"
#define CLIENT_PORT 8001
#define SERVER_HOSTNAME "localhost"
#define SERVER_PORT 8000
#define MESSAGE_SIZE 1000

int main() {
    int clientSocketFD;
    struct sockaddr_in serverAddress;
    int bytesSent;
    int bytesReceived;

    // Create a linked list and populate it with example data
    struct LinkedList ll;
    ll.head = NULL;

    struct MyData data1 = {.int_value = 123, .fixed_string = "FixedString1-123", .variable_string = "Sample String 1"};
    struct MyData data2 = {.int_value = 456, .fixed_string = "FixedString2-456", .variable_string = "Another Sample String"};
    struct MyData data3 = {.int_value = 321, .fixed_string = "FixedString3-321", .variable_string = "3rd sample string"};
    struct MyData data4 = {.int_value = 654, .fixed_string = "FixedString4-654", .variable_string = "And yet another Sample String"};

    append_to_linked_list(&ll, &data1);
    append_to_linked_list(&ll, &data2);
    append_to_linked_list(&ll, &data3);
    append_to_linked_list(&ll, &data4);

    // Convert the linked list to bytes
    char *packed_data;
    int packed_size;
    pack_linked_list(&ll, &packed_data, &packed_size);

    // Create a buffer to hold the size and packed data
    int buffer_size = sizeof(int) + packed_size;
    char *buffer = (char *)malloc(buffer_size);
    if (buffer == NULL) {
        fprintf(stderr, "Memory allocation error.\n");
        exit(EXIT_FAILURE);
    }

    // Copy the packed size into the buffer
    int32_t value = swapEndianness(packed_size + 4);
    memcpy(buffer, &value, sizeof(int));

    // Copy the packed data into the buffer
    memcpy(buffer + sizeof(int), packed_data, packed_size);

    // Create a TCP socket
    clientSocketFD = createStreamSocket(CLIENT_PORT);

    // Set up server address
    constructSocketAddress(&serverAddress, SERVER_HOSTNAME, SERVER_PORT);
    char ipAddress[INET_ADDRSTRLEN];

    // Convert binary IP address to string representation
    if (inet_ntop(AF_INET, &(serverAddress.sin_addr), ipAddress, INET_ADDRSTRLEN) == NULL) {
        perror("inet_ntop");
        exit(EXIT_FAILURE);
    }
    int port = ntohs(serverAddress.sin_port);
    printf("C client\n");
    printf("Server address: %s\n", ipAddress);
    printf("Server port: %d\n", port);
    printf("Content:\n");
    display_linked_list(&ll);

    // Connect to the server
    if (connect(clientSocketFD, (struct sockaddr *)&serverAddress, sizeof(serverAddress)) < 0) {
        perror("connect");
        exit(EXIT_FAILURE);
    }

    // Send the buffer containing size and packed data
    bytesSent = send(clientSocketFD, buffer, buffer_size, 0);

    if (bytesSent < 0) {
        perror("send (client)");
        exit(EXIT_FAILURE);
    }

    // Receive response from the server
    char receivedMessage[MESSAGE_SIZE];
    bytesReceived = recv(clientSocketFD, receivedMessage, MESSAGE_SIZE, 0);
    if (bytesReceived < 0) {
        perror("recv (client)");
        exit(EXIT_FAILURE);
    }

    printf("Received response: %s\n", receivedMessage);

    // Clean up
    free(buffer);
    free_linked_list(&ll);
    close(clientSocketFD);

    return 0;
}
