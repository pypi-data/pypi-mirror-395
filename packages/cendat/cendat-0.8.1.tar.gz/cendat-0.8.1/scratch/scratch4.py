from collections import defaultdict

schema = ["zero", "one", "two", "three", "two", "four", "five", "one", "six"]

data = [
    [0, 1, 2, 3, 2, 4, 5, 1, 6],
    [0, 1, 2, 3, 2, 4, 5, 1, 6],
    [0, 1, 2, 3, 2, 4, 5, 1, 6],
]

index_map = defaultdict(list)
for index, name in enumerate(schema):
    index_map[name].append(index)

removals = set()
for indexes in index_map.values():
    if len(indexes) > 1:
        removals.update(indexes[1:])

new_schema = [var for i, var in enumerate(schema) if i not in removals]
new_data = [[datum for i, datum in enumerate(row) if i not in removals] for row in data]

print(f"{schema=}")
print(f"{index_map=}")
print(f"{removals=}")
print(f"{new_schema=}")
print(f"{new_data=}")
