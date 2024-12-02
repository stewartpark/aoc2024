import sys

def is_safe(report):
    levels = list(map(int, report.split()))
    increasing = decreasing = True
    
    for i in range(1, len(levels)):
        diff = abs(levels[i] - levels[i-1])
        if diff < 1 or diff > 3:
            return False
        if levels[i] > levels[i-1]:
            decreasing = False
        elif levels[i] < levels[i-1]:
            increasing = False
    
    return increasing or decreasing

def count_safe_reports(content):
    reports = content.strip().split('\n')
    safe_count = sum(1 for report in reports if is_safe(report))
    return safe_count

with open(sys.argv[1]) as f:
    content = f.read()
    print(count_safe_reports(content))