#!/usr/bin/python3
"""AOC 24th day."""
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
    
    initial_wires = {}
    for wire in wire_values_raw:
        wire_id, wire_value = wire.split(': ')
        initial_wires[wire_id] = int(wire_value)
    
    gates_origin = []        
    for gate in gates_raw:
        input, output = gate.split(' -> ')            
        wire1, operation_raw, wire2 = input.split()
        gates_origin.append((wire1, operation_raw, wire2, output))
    

    def getBinaryForKeys(keys, wire_values):
        values = [str(wire_values[wire_key]) for wire_key in keys]
        return"".join(values)
        
    def callculateOutuputsThroughGates(gates = gates_origin, wire_values = initial_wires):
        gates = gates.copy()
        wire_values = dict(wire_values)
        while gates:
            notFoundCount = 0
            for gate in gates:
                wire1, operation_raw, wire2, output = gate
                if wire1 not in wire_values or wire2 not in wire_values:
                    notFoundCount += 1
                    continue
                else:
                    operation = XOR if operation_raw == "XOR" else AND if operation_raw == "AND" else OR
                    result = operation(wire_values[wire1], wire_values[wire2])
                    wire_values[output] = result
                    gates.remove(gate)
            if notFoundCount >0 and notFoundCount == len(gates): 
                return None
        return wire_values
    
    #pt 1
    wire_values = callculateOutuputsThroughGates()
    z_keys = sorted(filter(lambda it: it.startswith('z'), list(wire_values.keys())), reverse=True)
    binary = getBinaryForKeys(z_keys, wire_values)
    print("pt1:", int(binary, 2))
    
    
    
    #pt 2
    x_keys = sorted(filter(lambda it: it.startswith('x'), list(wire_values.keys())), reverse=True)
    y_keys = sorted(filter(lambda it: it.startswith('y'), list(wire_values.keys())), reverse=True)
    z_keys = sorted(filter(lambda it: it.startswith('z'), list(wire_values.keys())), reverse=True)
    
    x, y, z = getBinaryForKeys(x_keys, wire_values), getBinaryForKeys(y_keys, wire_values), getBinaryForKeys(z_keys, wire_values)
    ix, iy, iz = list(map(lambda b: int(b, 2), [x,y,z])) 
    expected = bin(ix + iy)[2:]
    actual = bin(iz)[2:]
    
    
    gates = gates_origin[:]
    inputs = [(w1, opr, w2) for  w1,opr,w2,o in gates]
    outputs = [o for  w1,opr,w2,o in gates]
     
    # z05, z z11 and z23 was clearly confirmed by looking at graph
    # z38 was uncertain so lets check every possible swap that produces correct result
    for node_name in outputs:        
        for swap in outputs:
            gates = gates_origin[:]
            inputs = [(w1, opr, w2) for  w1,opr,w2,o in gates]
            outputs = [o for  w1,opr,w2,o in gates]

            swap_index = outputs.index(swap)
            z11_index = outputs.index(node_name)
            
            gates = []
            for i, input in enumerate(inputs):
                (w1, opr, w2) = input
                o = outputs[i]
                if i == z11_index:
                    gates.append((w1, opr, w2, swap))
                elif i == swap_index:
                    gates.append((w1, opr, w2, node_name))
                else:
                    gates.append((w1, opr, w2, o))
                
            wire_values = callculateOutuputsThroughGates(gates, initial_wires)
            if wire_values is None:
                continue

            x, y, z = getBinaryForKeys(x_keys, wire_values), getBinaryForKeys(y_keys, wire_values), getBinaryForKeys(z_keys, wire_values)
            ix, iy, iz = list(map(lambda b: int(b, 2), [x,y,z])) 

            if z == expected:
                print(f"swap {node_name} with {swap}", )
        

if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('01.txt' if not env_test_run else '00.txt', 'r'), env_test_run)