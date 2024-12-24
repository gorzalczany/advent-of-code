#!/usr/bin/python3
"""AOC 19th day."""
import sys


def XOR(wire1, wire2):
    return 1 if wire1 != wire2 else 0

def OR(wire1, wire2):
    return 1 if any([wire1 == 1, wire2 == 1]) else 0
    
def AND(wire1, wire2):
    return 1 if wire1 == 1 and wire2 == 1 else 0
    

def main(input_file, isTest):
    input = input_file.read()
    
    wire_values_group, gates_group = input.split('\n\n')
    wire_values_raw = wire_values_group.splitlines()
    gates_raw = gates_group.splitlines()
    
    wire_values = {}
    for wire in wire_values_raw:
        wire_id, wire_value = wire.split(': ')
        wire_values[wire_id] = int(wire_value)
    
    gates = []        
    for gate in gates_raw:
        input, output = gate.split(' -> ')            
        wire1, operation_raw, wire2 = input.split()
        gates.append((wire1, operation_raw, wire2, output))
    
    while gates:
        for gate in gates:
            wire1, operation_raw, wire2, output = gate
            if wire1 not in wire_values or wire2 not in wire_values:
                continue
            else:
                operation = XOR if operation_raw == "XOR" else AND if operation_raw == "AND" else OR
                result = operation(wire_values[wire1], wire_values[wire2])
                wire_values[output] = result
                gates.remove(gate)
                
    z_keys = sorted(filter(lambda it: it.startswith('z'), list(wire_values.keys())))
    z_values = [wire_values[wire_key] for wire_key in z_keys]
    z_values.reverse()
    binary = "".join(map(str, z_values))
    print(binary)
    result = int(binary, 2)
    print(result)


if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('01.txt' if not env_test_run else '00.txt', 'r'), env_test_run)