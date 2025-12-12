#!/usr/bin/python3
"""AOC 11th day."""
import sys
from collections import deque

def solve1(devices):
    print(countPaths(devices, "you", []))

def solve2(devices):
    print(countPaths(devices, "svr", ["dac", "fft"]))

def get_devices_reaching_out(devices):
    found = set()
    queue = deque([d for d in devices if "out" in devices[d]])
    while queue:
        device = queue.popleft()
        if device in found:
            continue
        found.add(device)
        for d in devices:
            if device in devices[d] and d not in found:
                queue.append(d)
    return found
                
def countPaths(devices, start, required_nodes):
    devices_reaching_out = get_devices_reaching_out(devices)
    failure_condition = lambda node_name: node_name not in devices_reaching_out
    success_condition = lambda node_name, keywords_found: node_name == "out" and all(k in keywords_found for k in required_nodes)

    def counting_dfs(node_name, already_found_required, memo = {}):
        memo_key = (node_name, frozenset(already_found_required))
        if memo_key in memo:
            return memo[memo_key]

        if failure_condition(node_name):
            return 0

        count = 0
        for attached_device in devices[node_name]:
            if success_condition(attached_device, already_found_required):
                count += 1
                continue
            newly_found = already_found_required.copy()
            for node in required_nodes:
                if node in attached_device:
                    newly_found.add(node)

            count += counting_dfs(attached_device, newly_found, memo)

        memo[memo_key] = count
        return count

    return counting_dfs(start, set(), dict())


def main(input_file):
    lines =  input_file.read().splitlines()

    devices = {}
    for _, line in enumerate(lines):
        device_name, attachments_list = line.split(': ')
        devices[device_name] = set(attachments_list.split())

    solve1(devices)
    solve2(devices)
                
if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('1.txt' if not env_test_run else '0.txt', 'r'))