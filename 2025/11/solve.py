#!/usr/bin/python3
"""AOC 11th day."""
import sys
from collections import deque

def filter_nodes_reaching_node(adjacency_map, end_node):
    found = set()
    queue = deque([node for node in adjacency_map if end_node in adjacency_map[node]])
    while queue:
        node = queue.popleft()
        if node in found:
            continue
        found.add(node)
        for adjacent in adjacency_map:
            if node in adjacency_map[adjacent] and adjacent not in found:
                queue.append(adjacent)
    return found
                
def countPaths(adjacency_map, start, end, nodes_required_on_path):
    nodes_reaching_end_node = filter_nodes_reaching_node(adjacency_map, end)
    
    def failure_condition(node_name):
        return node_name not in nodes_reaching_end_node
    def success_condition(node_name, visited_required):
        return node_name == end and all(k in visited_required for k in nodes_required_on_path)

    def counting_dfs(node_name, visited_required, memo = {}):
        memo_key = (node_name, frozenset(visited_required))
        if memo_key in memo:
            return memo[memo_key]

        if failure_condition(node_name):
            return 0

        count = 0
        for adjacent in adjacency_map[node_name]:
            if success_condition(adjacent, visited_required):
                count += 1
                continue
            visited = visited_required.copy()
            if adjacent in nodes_required_on_path:
                visited.add(adjacent)

            count += counting_dfs(adjacent, visited, memo)

        memo[memo_key] = count
        return count

    return counting_dfs(start, set(), dict())


def main(input_file):
    lines =  input_file.read().splitlines()

    devices = {}
    for _, line in enumerate(lines):
        device_name, attachments_list = line.split(': ')
        devices[device_name] = set(attachments_list.split())

    solve1 = countPaths(devices, "you", "out", [])
    solve2 = countPaths(devices, "svr", "out", ["dac", "fft"])
        
    print(solve1)
    print(solve2)
                
if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('1.txt' if not env_test_run else '0.txt', 'r'))