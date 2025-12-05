#!/usr/bin/python3
"""AOC 5th day."""
import sys

class InclusiveRange(object):
    def __init__(self,start,end):
        self.start = start
        self.end = end

    def is_intersecting(self, other):
        return not (self.end < other.start or other.end < self.start)

    def __str__(self):
        return f"[{self.start},{self.end}]"
    
    def __repr__(self):
        return f"[{self.start},{self.end}]"
    
    def __len__(self):
        return (self.end - self.start) + 1

def mergedOverlappingRanges(ranges: list[InclusiveRange]) -> list[InclusiveRange]:
    for current_range in ranges:
        for other_range in ranges:
            if current_range == other_range:
                continue
            if current_range.is_intersecting(other_range):
                new_start = min(current_range.start, other_range.start)
                new_end = max(current_range.end, other_range.end)
                new_range = InclusiveRange(new_start, new_end)
                ranges.remove(current_range)
                ranges.remove(other_range)
                ranges.append(new_range)
                return mergedOverlappingRanges(ranges)
    return ranges

def main(input_file):
    fresh_lines, available_lines =  input_file.read().strip().split('\n\n')

    inclusive_ranges = []
    for range_string in fresh_lines.splitlines():
        start_string, stop_string = range_string.split('-')
        start, stop = int(start_string), int(stop_string)
        fresh_range = range(start, stop+1)
        inclusive_range = InclusiveRange(start, stop)
        inclusive_ranges.append(inclusive_range)

    fresh_ids = set()
    for available_id in available_lines.splitlines():
        available_id = int(available_id)
        for fresh_range in inclusive_ranges:
            if available_id in range(fresh_range.start, fresh_range.end + 1):
                fresh_ids.add(available_id)
    
    solve_1 = len(fresh_ids)
    solve_2 = sum([len(range) for range in mergedOverlappingRanges(inclusive_ranges)])
    
    print("pt1:", solve_1)
    print("pt2:", solve_2)   
        
                
if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('1.txt' if not env_test_run else '0.txt', 'r'))