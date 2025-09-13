from itertools import groupby

data = [
    {'name': 'Alice', 'department': 'HR'},
    {'name': 'Bob', 'department': 'IT'},
    {'name': 'Charlie', 'department': 'HR'},
    {'name': 'David', 'department': 'IT'},
    {'name': 'Eve', 'department': 'Marketing'}
]

# Sort the data by the 'department' key
sorted_data = sorted(data, key=lambda x: x['department'])

result = []
for key, group in groupby(sorted_data, key=lambda x: x['department']):
    result.append(list(group))
print(result)
