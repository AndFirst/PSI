#include "linked_list.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FIXED_STRING_LENGTH 16

void pack_data(struct MyData *data, char **packed_data, int *packed_size) {
    char fixed_string_padded[FIXED_STRING_LENGTH];
    memset(fixed_string_padded, 0, sizeof(fixed_string_padded));
    strncpy(fixed_string_padded, data->fixed_string, FIXED_STRING_LENGTH);

    int variable_string_length = strlen(data->variable_string);
    *packed_size = sizeof(int) + FIXED_STRING_LENGTH + sizeof(int) + variable_string_length;

    *packed_data = (char *)malloc(*packed_size);
    if (*packed_data == NULL) {
        fprintf(stderr, "Memory allocation error.\n");
        exit(EXIT_FAILURE);
    }

    memcpy(*packed_data, &(data->int_value), sizeof(int));
    memcpy(*packed_data + sizeof(int), fixed_string_padded, FIXED_STRING_LENGTH);
    memcpy(*packed_data + sizeof(int) + FIXED_STRING_LENGTH, &variable_string_length, sizeof(int));
    memcpy(*packed_data + sizeof(int) + FIXED_STRING_LENGTH + sizeof(int),
           data->variable_string, variable_string_length);
}

struct MyData *unpack_data(char *packed_data) {
    struct MyData *unpacked_data = (struct MyData *)malloc(sizeof(struct MyData));
    if (unpacked_data == NULL) {
        fprintf(stderr, "Memory allocation error.\n");
        exit(EXIT_FAILURE);
    }

    memcpy(&(unpacked_data->int_value), packed_data, sizeof(int));
    memcpy(unpacked_data->fixed_string, packed_data + sizeof(int), FIXED_STRING_LENGTH);
    unpacked_data->fixed_string[FIXED_STRING_LENGTH] = '\0';

    int variable_string_length;
    memcpy(&variable_string_length, packed_data + sizeof(int) + FIXED_STRING_LENGTH, sizeof(int));

    unpacked_data->variable_string = (char *)malloc(variable_string_length + 1);
    if (unpacked_data->variable_string == NULL) {
        fprintf(stderr, "Memory allocation error.\n");
        exit(EXIT_FAILURE);
    }

    memcpy(unpacked_data->variable_string,
           packed_data + sizeof(int) + FIXED_STRING_LENGTH + sizeof(int), variable_string_length);
    unpacked_data->variable_string[variable_string_length] = '\0';

    return unpacked_data;
}

struct Node *create_node(struct MyData *data) {
    struct Node *new_node = (struct Node *)malloc(sizeof(struct Node));
    if (new_node == NULL) {
        fprintf(stderr, "Memory allocation error.\n");
        exit(EXIT_FAILURE);
    }
    new_node->data = *data;
    new_node->next = NULL;
    return new_node;
}

void append_to_linked_list(struct LinkedList *ll, struct MyData *data) {
    struct Node *new_node = create_node(data);
    if (ll->head == NULL) {
        ll->head = new_node;
        return;
    }
    struct Node *current = ll->head;
    while (current->next != NULL) {
        current = current->next;
    }
    current->next = new_node;
}

void display_linked_list(struct LinkedList *ll) {
    struct Node *current = ll->head;
    while (current != NULL) {
        printf("Int Value: %d\n", current->data.int_value);
        printf("Fixed String: %s\n", current->data.fixed_string);
        printf("Variable String: %s\n", current->data.variable_string);
        printf("-----------------\n");
        current = current->next;
    }
}

void free_linked_list(struct LinkedList *ll) {
    struct Node *current = ll->head;
    while (current != NULL) {
        struct Node *temp = current;
        current = current->next;
        free(temp->data.variable_string);
        free(temp);
    }
    ll->head = NULL;
}

void pack_linked_list(struct LinkedList *ll, char **packed_data, int *packed_size) {
    struct Node *current = ll->head;
    int total_packed_size = 0;
    *packed_data = NULL;

    while (current != NULL) {
        char *node_packed_data;
        int node_packed_size;
        pack_data(&(current->data), &node_packed_data, &node_packed_size);

        // Reallocate memory to accommodate the new node data
        *packed_data = realloc(*packed_data, total_packed_size + node_packed_size);
        if (*packed_data == NULL) {
            fprintf(stderr, "Memory allocation error.\n");
            exit(EXIT_FAILURE);
        }

        // Copy the packed node data into the main packed data buffer
        memcpy(*packed_data + total_packed_size, node_packed_data, node_packed_size);
        total_packed_size += node_packed_size;

        // Free memory used for individual node data
        free(node_packed_data);

        current = current->next;
    }

    *packed_size = total_packed_size;
}

void unpack_linked_list(struct LinkedList *ll, char *packed_data, int packed_size) {
    int offset = 0;

    while (offset < packed_size) {
        struct MyData *unpacked_data = unpack_data(packed_data + offset);
        append_to_linked_list(ll, unpacked_data);

        offset += sizeof(int) + FIXED_STRING_LENGTH + sizeof(int) + strlen(unpacked_data->variable_string);
        free(unpacked_data); // Free the allocated unpacked data since it's copied into the linked list
    }
}