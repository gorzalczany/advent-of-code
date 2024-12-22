#!/usr/bin/python3
"""AOC 22th day."""
import sys
from collections import deque, defaultdict

def evolve(secret):
    res_mult = secret * 64
    secret = mix(secret, res_mult)
    secret = prune(secret)
    
    secret = mix(secret, secret // 32)
    secret = prune(secret)
    
    res_mult = secret * 2048
    secret = mix(secret, res_mult)
    return prune(secret)
    
def mix(secret, other):
    return secret ^ other

def prune(secret):
    return secret % 16777216

def main(input_file, isTest):
    lines =  input_file.read().splitlines()
    initial_sn = list(map(int, lines))
    
    evolved = initial_sn[:]
    for _ in range(2000):
        for i, sn in enumerate(evolved):
            evolved[i] = evolve(sn)
    print("pt1:", sum(evolved))
    
    sequence_to_bananas_count = defaultdict(int)       
    for buyer_secret in initial_sn:
        buyer_secret = buyer_secret
        buyer_sequence = deque([], 4)
        seen_sequences = set()
        for _ in range(2000):
            evolved_secret = evolve(buyer_secret)
            price, prev_price = evolved_secret % 10, buyer_secret % 10
            diff = price - prev_price
            buyer_secret = evolved_secret
            
            buyer_sequence.append(diff)
            sequence_key = str(list(buyer_sequence))

            if len(buyer_sequence) == 4 and sequence_key not in seen_sequences:
                sequence_to_bananas_count[sequence_key] += price
                seen_sequences.add(sequence_key)
                
    print("pt2:", max(sequence_to_bananas_count.values()))
    
if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('01.txt' if not env_test_run else '00.txt', 'r'), env_test_run)