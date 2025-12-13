# myers-diff

High-performance Myers diff algorithm implementation in C with Python bindings.

## Installation

```bash
pip install myers-diff
```

## Usage

```python
import myers_diff

# Compare two lists
list_a = ["hello", "world", "foo", "bar"]
list_b = ["hello", "there", "foo", "baz"]

# Get full edit operations
ops = myers_diff.diff(list_a, list_b)
for op in ops:
    print(f"{op['type']} [{op['index']}]: {op['line']}")
# DELETE [1]: world
# INSERT [1]: there
# DELETE [3]: bar
# INSERT [3]: baz

# Get just the edit count
count = myers_diff.diff_count(list_a, list_b)
print(f"Edit distance: {count}")  # 4

# Bounded diff - early exit if distance exceeds max_d
ops = myers_diff.diff(list_a, list_b, max_d=2)
if ops is None:
    print("Lists are too different (> 2 edits)")
else:
    print(f"Found {len(ops)} edits")
```

## API

### `diff(a, b, max_d=-1)`
Compute the edit operations to transform list `a` into list `b`.

- `a`: Source list of strings
- `b`: Target list of strings  
- `max_d`: Maximum allowed edit distance. If the actual distance exceeds this, returns `None` for early exit. Use `-1` (default) for no limit.

Returns a list of operations `[{"type": "DELETE"|"INSERT", "index": int, "line": str}, ...]` or `None` if `max_d` is exceeded.

### `diff_count(a, b, max_d=-1)`
Get the number of edit operations without building the full operation list.

Returns the count as an integer, or `None` if `max_d` is exceeded.

### `distance(a, b)`
Compute the edit distance using dynamic programming (no early exit option).

Returns the edit distance as an integer.

## Performance

Optimized C implementation with:
- Pre-computed string hashes for fast comparison
- Common prefix/suffix trimming
- Compact trace storage
- Optional early termination with `max_d` parameter

Benchmarks on ~4500 word lists with ~2200 edits:
- Full diff: ~10ms
- Bounded diff with early exit: <1ms

## License

MIT
