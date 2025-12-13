# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
from libc.stdlib cimport malloc, free
from cpython.bytes cimport PyBytes_AsString

cdef extern from "myers.h":
    ctypedef enum OperationType:
        OP_DELETE
        OP_INSERT
    ctypedef struct EditOperation:
        OperationType type
        int index
        const char *line
    ctypedef struct EditScript:
        EditOperation *ops
        int count
        int capacity
        int exceeded
    EditScript *myers_diff(const char **a, int n, const char **b, int m, int max_d)
    int myers_distance(const char **a, int n, const char **b, int m)
    void free_edit_script(EditScript *script)

def diff(list a, list b, int max_d=-1):
    cdef int n = len(a)
    cdef int m = len(b)
    cdef const char **arr_a = <const char **>malloc(n * sizeof(char *))
    cdef const char **arr_b = <const char **>malloc(m * sizeof(char *))
    cdef list a_bytes = [s.encode('utf-8') if isinstance(s, str) else s for s in a]
    cdef list b_bytes = [s.encode('utf-8') if isinstance(s, str) else s for s in b]
    cdef int i
    for i in range(n):
        arr_a[i] = PyBytes_AsString(a_bytes[i])
    for i in range(m):
        arr_b[i] = PyBytes_AsString(b_bytes[i])
    cdef EditScript *script = myers_diff(arr_a, n, arr_b, m, max_d)
    cdef list result = None
    if not script.exceeded:
        result = []
        for i in range(script.count):
            op_type = "DELETE" if script.ops[i].type == OP_DELETE else "INSERT"
            line = script.ops[i].line.decode('utf-8') if script.ops[i].line else ""
            result.append({"type": op_type, "index": script.ops[i].index, "line": line})
    free_edit_script(script)
    free(arr_a)
    free(arr_b)
    return result

def diff_count(list a, list b, int max_d=-1):
    cdef int n = len(a)
    cdef int m = len(b)
    cdef const char **arr_a = <const char **>malloc(n * sizeof(char *))
    cdef const char **arr_b = <const char **>malloc(m * sizeof(char *))
    cdef list a_bytes = [s.encode('utf-8') if isinstance(s, str) else s for s in a]
    cdef list b_bytes = [s.encode('utf-8') if isinstance(s, str) else s for s in b]
    cdef int i
    for i in range(n):
        arr_a[i] = PyBytes_AsString(a_bytes[i])
    for i in range(m):
        arr_b[i] = PyBytes_AsString(b_bytes[i])
    cdef EditScript *script = myers_diff(arr_a, n, arr_b, m, max_d)
    cdef int count = -1 if script.exceeded else script.count
    free_edit_script(script)
    free(arr_a)
    free(arr_b)
    return None if count < 0 else count

def distance(list a, list b):
    cdef int n = len(a)
    cdef int m = len(b)
    cdef const char **arr_a = <const char **>malloc(n * sizeof(char *))
    cdef const char **arr_b = <const char **>malloc(m * sizeof(char *))
    cdef list a_bytes = [s.encode('utf-8') if isinstance(s, str) else s for s in a]
    cdef list b_bytes = [s.encode('utf-8') if isinstance(s, str) else s for s in b]
    cdef int i
    for i in range(n):
        arr_a[i] = PyBytes_AsString(a_bytes[i])
    for i in range(m):
        arr_b[i] = PyBytes_AsString(b_bytes[i])
    cdef int dist = myers_distance(arr_a, n, arr_b, m)
    free(arr_a)
    free(arr_b)
    return dist

def edit_distance(list a, list b):
    return diff_count(a, b)
