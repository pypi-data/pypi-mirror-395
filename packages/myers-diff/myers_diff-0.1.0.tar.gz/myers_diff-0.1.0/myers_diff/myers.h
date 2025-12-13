#ifndef MYERS_H
#define MYERS_H
#include <stddef.h>
typedef enum { OP_DELETE, OP_INSERT } OperationType;
typedef struct { OperationType type; int index; const char *line; } EditOperation;
typedef struct { EditOperation *ops; int count; int capacity; int exceeded; } EditScript;
EditScript *myers_diff(const char **a, int n, const char **b, int m, int max_d);
int myers_distance(const char **a, int n, const char **b, int m);
void free_edit_script(EditScript *script);
void print_edit_script(EditScript *script);
#endif
