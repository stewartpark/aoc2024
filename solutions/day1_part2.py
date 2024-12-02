import sys
from collections import Counter

with open(sys.argv[1]) as f:
    lines = f.readlines()

left_list = []
right_list = []

for line in lines:
    left, right = map(int, line.split())
    left_list.append(left)
    right_list.append(right)

right_count = Counter(right_list)
similarity_score = sum(x * right_count[x] for x in left_list)

print(similarity_score)