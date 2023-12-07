#ifndef LINKEDLIST_H
#define LINKEDLIST_H

struct MyData {
    int int_value;
    char fixed_string[17]; // + 1 for null termination
    char *variable_string;
};

struct Node {
    struct MyData data;
    struct Node *next;
};

struct LinkedList {
    struct Node *head;
};

void pack_data(struct MyData *data, char **packed_data, int *packed_size);
struct MyData *unpack_data(char *packed_data);
struct Node *create_node(struct MyData *data);
void append_to_linked_list(struct LinkedList *ll, struct MyData *data);
void display_linked_list(struct LinkedList *ll);
void free_linked_list(struct LinkedList *ll);
void pack_linked_list(struct LinkedList *ll, char **packed_data, int *packed_size);
void unpack_linked_list(struct LinkedList *ll, char *packed_data, int packed_size);

#endif /* LINKEDLIST_H */
