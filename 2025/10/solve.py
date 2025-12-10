#!/usr/bin/python3
"""AOC 10th day."""
import sys
import itertools
from ortools.sat.python import cp_model

class Button:
    def __init__(self, wiring):
        wiring = wiring[1:-1]
        self.wiring = list(map(int, wiring.split(',')))

    def press(self, machine):
        for index in self.wiring:
            machine.state[index] = not machine.state[index]
            machine.counters[index] += 1

    def buttonVector(self, target_length):
        vector = [0] * target_length
        for index in self.wiring:
            vector[index] += 1
        return vector
    
    def __repr__(self):
        return f'{self.wiring}'

class Machine:
    def __init__(self, indicators, button_wiring, joltage_req):
        self.buttons = [Button(wiring) for wiring in button_wiring.split(' ')]

        self.desired_state = list(map(lambda x: x == '#', indicators))
        self.state = [False] * len(self.desired_state)

        self.joltage_req = list(map(int, joltage_req.split(',')))
        self.counters = [0] * len(self.joltage_req)

    def reset(self):
        self.state = [False] * len(self.desired_state)
        self.counters = [0] * len(self.joltage_req)

    def hasDesiredState(self):
        return self.state == self.desired_state
    
    def metJoltageReq(self):
        return self.counters == self.joltage_req
    
    def __repr__(self):
        indicators = ''.join(['#' if x else '.' for x in self.state])
        counters = ','.join(map(str, self.counters))
        return f'{indicators} {{{counters}}}'

def solve1(machines):
    presses_per_machine = []
    for machine in machines:
        min_presses = None
        presses = 0
        while not machine.hasDesiredState():
            presses += 1
            for button_combination in itertools.combinations(machine.buttons, presses):
                machine.reset()
                for button in button_combination:
                    button.press(machine)
                if machine.state == machine.desired_state:
                    min_presses = presses
                    break
            if min_presses is not None:
                break
        presses_per_machine.append(min_presses)
    print('Solution 1:', sum(presses_per_machine))

def solve2(machines):
    presses_per_machine = []
    for index, machine in enumerate(machines):
        print(f'Solving machine {index+1}/{len(machines)}')
        machine.reset()
        min_presses = None
        presses = 0
        while not machine.metJoltageReq():
            presses += 1
            for button_combination in itertools.combinations_with_replacement(machine.buttons, presses):
                machine.reset()
                for button in button_combination:
                    button.press(machine)
                if machine.counters == machine.joltage_req:
                    min_presses = presses
                    break
            if min_presses is not None:
                break
        presses_per_machine.append(min_presses)
    print('Solution 2:', sum(presses_per_machine))

def solve2_in_finite_time(machines):
    presses_per_machine = []
    for machine in machines:
        buttons = machine.buttons
        # B1*x1​+B2*​x2​+...+Bn*​xn​=C
        #   where Bi is the button vector,
        #   xi is the number of times button i is pressed
        #   and C is the machine.desired_counters
        target = machine.joltage_req
        target_length = len(target)
        button_vectors = [button.buttonVector(target_length) for button in buttons]
        solution = solve_with_or_tools(button_vectors, target)
        solution_sum = sum(solution)
        presses_per_machine.append(solution_sum)
    print('Solution 2 (finite time):', sum(presses_per_machine))


def solve_with_or_tools(buttons, target):
    n = len(buttons)
    dim = len(target)
    model = cp_model.CpModel()

    # Variables: number of presses per button
    # Bound is safe upper bound based on target max
    max_target = max(target)
    x = [model.NewIntVar(0, max_target, f"x{i}") for i in range(n)]

    # For each counter dimension: sum(button[i][dim] * x[i]) == target[dim]
    for idx in range(dim):
        model.Add(sum(buttons[i][idx] * x[i] for i in range(n)) == target[idx])

    # Optional: minimize total presses
    model.Minimize(sum(x))

    solver = cp_model.CpSolver()
    result = solver.Solve(model)

    if result == cp_model.OPTIMAL or result == cp_model.FEASIBLE:
        return [solver.Value(v) for v in x]
    return None

def main(input_file):
    lines =  input_file.read().splitlines()

    inputs = []
    for index, line in enumerate(lines):
        indicators, rest = line[1:].split('] ')
        button_wiring, rest = rest.split(' {')
        joltage_req = rest.split('}')[0]
        inputs.append(Machine(indicators, button_wiring, joltage_req))

    solve1(inputs)
    solve2_in_finite_time(inputs)
                
if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('1.txt' if not env_test_run else '0.txt', 'r'))