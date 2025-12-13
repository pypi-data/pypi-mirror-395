import json
import myers_wrapper
import time
with open("words_a.json") as f:
    list_a = json.load(f)
with open("words_b.json") as f:
    list_b = json.load(f)

print(f"List A: {len(list_a)} words")
print(f"List B: {len(list_b)} words")
print()

start = time.time()
operations = myers_wrapper.diff(list_a, list_b, max_d=-1)
end = time.time()
print(f"Time taken: {end - start} seconds")
# print(f"Edit operations ({len(operations)} total):")
# for op in operations:
#     print(f"  {op['type']} [{op['index']}]: \"{op['line']}\"")

# print(f"\nEdit distance: {myers_wrapper.edit_distance(list_a, list_b)}")
