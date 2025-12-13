#include "myers.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE_LENGTH 4096
#define INITIAL_CAPACITY 1024

typedef struct {
    char **lines;
    int count;
    int capacity;
} StringList;

static void init_string_list(StringList *list) {
    list->lines = malloc(INITIAL_CAPACITY * sizeof(char *));
    list->count = 0;
    list->capacity = INITIAL_CAPACITY;
}

static void add_line(StringList *list, const char *line) {
    if (list->count >= list->capacity) {
        list->capacity *= 2;
        list->lines = realloc(list->lines, list->capacity * sizeof(char *));
    }
    list->lines[list->count] = strdup(line);
    list->count++;
}

static void free_string_list(StringList *list) {
    for (int i = 0; i < list->count; i++) {
        free(list->lines[i]);
    }
    free(list->lines);
}

static StringList read_file(const char *filename) {
    StringList list;
    init_string_list(&list);
    FILE *f = fopen(filename, "r");
    if (!f) {
        fprintf(stderr, "Cannot open file: %s\n", filename);
        exit(1);
    }
    char buffer[MAX_LINE_LENGTH];
    while (fgets(buffer, MAX_LINE_LENGTH, f)) {
        size_t len = strlen(buffer);
        if (len > 0 && buffer[len - 1] == '\n') {
            buffer[len - 1] = '\0';
        }
        add_line(&list, buffer);
    }
    fclose(f);
    return list;
}

int main(int argc, char *argv[]) {
    if (argc == 3) {
        StringList a = read_file(argv[1]);
        StringList b = read_file(argv[2]);
        EditScript *script = myers_diff((const char **)a.lines, a.count,
                                        (const char **)b.lines, b.count);
        print_edit_script(script);
        printf("\nEdit distance: %d\n", script->count);
        free_edit_script(script);
        free_string_list(&a);
        free_string_list(&b);
        return 0;
    }
    printf("=== Myers Diff Algorithm Demo ===\n\n");
    const char *list_a[] = {"A", "B", "C", "A", "B", "B", "A"};
    const char *list_b[] = {"C", "B", "A", "B", "A", "C"};
    int n = sizeof(list_a) / sizeof(list_a[0]);
    int m = sizeof(list_b) / sizeof(list_b[0]);
    printf("List A (%d elements): ", n);
    for (int i = 0; i < n; i++) printf("%s ", list_a[i]);
    printf("\n");
    printf("List B (%d elements): ", m);
    for (int i = 0; i < m; i++) printf("%s ", list_b[i]);
    printf("\n\n");
    EditScript *script = myers_diff(list_a, n, list_b, m);
    print_edit_script(script);
    printf("\nEdit distance (minimum operations): %d\n", script->count);
    free_edit_script(script);
    printf("\n=== File-based Example ===\n\n");
    const char *file_a[] = {
        "line 1: hello",
        "line 2: world",
        "line 3: foo",
        "line 4: bar",
        "line 5: baz"
    };
    const char *file_b[] = {
        "line 1: hello",
        "line 2: world modified",
        "line 3: foo",
        "line 4: qux",
        "line 5: baz"
    };
    n = sizeof(file_a) / sizeof(file_a[0]);
    m = sizeof(file_b) / sizeof(file_b[0]);
    printf("File A:\n");
    for (int i = 0; i < n; i++) printf("  %s\n", file_a[i]);
    printf("\nFile B:\n");
    for (int i = 0; i < m; i++) printf("  %s\n", file_b[i]);
    printf("\n");
    script = myers_diff(file_a, n, file_b, m);
    print_edit_script(script);
    printf("\nEdit distance: %d\n", script->count);
    free_edit_script(script);
    return 0;
}

