import re
from collections import defaultdict

# Load the log data from the file
with open('/mnt/data/logfile.txt', 'r') as file:
    log_data = file.read()

# Regular expression pattern to match each commit block
commit_pattern = re.compile(r'--\w+--\d{4}-\d{2}-\d{2}--\w+\n((?:.+\n)+)', re.MULTILINE)

# Regular expression pattern to match file changes within a commit
file_change_pattern = re.compile(r'\d+\s+\d+\s+(.+)', re.MULTILINE)

# Dictionary to hold file co-change counts
co_change_counts = defaultdict(lambda: defaultdict(int))

# Process each commit to find co-changed files
for commit in commit_pattern.findall(log_data):
    changed_files = file_change_pattern.findall(commit)
    
    # Increment the count for every pair of changed files in the commit
    for i in range(len(changed_files)):
        for j in range(i + 1, len(changed_files)):
            file1, file2 = sorted([changed_files[i], changed_files[j]])
            co_change_counts[file1][file2] += 1

# Convert the dictionary to a sorted list of file pairs and their co-change counts
co_change_list = [(f'{file1} & {file2}', count) 
                  for file1, related_files in co_change_counts.items()
                  for file2, count in related_files.items()]

# Sort the list by co-change counts in descending order to identify the most common co-changes
sorted_co_change_list = sorted(co_change_list, key=lambda x: x[1], reverse=True)

sorted_co_change_list[:10]  # Display top 10 co-changed file pairs
