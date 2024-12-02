import sys

def is_safe(levels):
    if len(levels) <= 1:
        return True
    
    increasing = decreasing = True
    
    for i in range(1, len(levels)):
        diff = levels[i] - levels[i-1]
        if not (1 <= abs(diff) <= 3):
            increasing = False
            decreasing = False
        elif diff < 0:
            increasing = False
        elif diff > 0:
            decreasing = False
    
    return increasing or decreasing

def can_be_safe_by_removing_one(levels):
    for i in range(len(levels)):
        if is_safe(levels[:i] + levels[i+1:]):
            return True
    return False

with open(sys.argv[1]) as f:
    content = f.read().strip().split('\n')
    result = 0
    
    for line in content:
        levels = list(map(int, line.split()))
        if is_safe(levels) or can_be_safe_by_removing_one(levels):
            result += 1
    
    print(result)