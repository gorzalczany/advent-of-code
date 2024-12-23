#!/usr/bin/python3
"""AOC 23th day."""
import sys
from collections import defaultdict

class LanGroup:
    def __init__(self, members):
        self.members = members
        self.members.sort()
   
    def __hash__(self):
        return hash(",".join(self.members))
    
    def __eq__(self, other):
        return self.members == other.members
    
    def __str__(self):
        return str(self.members)
    
    def __repr__(self):
        return str(self.members)


def main(input_file, isTest):
    lines =  input_file.read().splitlines()
    connections = []
    for line in lines:
        a, b = line.split("-")
        connections.append((a,b))
     
    lan_dict = defaultdict(set)
    for a,b in connections:
        lan_dict[a].add(b)
        lan_dict[b].add(a)  

    lan_parties = set()
    for me, mine in lan_dict.items():
        for other in mine:
            for common in lan_dict[other]:
                if common in mine and common not in [me, other]:
                    lan_parties.add(LanGroup([me, other, common]))  
      
    print("pt1:", len([party for party in lan_parties if any(member.startswith("t") for member in party.members)]))
    
    # pt2:
    lan_parties = set()
    for me, mine in lan_dict.items():
        for other in mine:
            lan_parties.add(LanGroup([me, other]+[x for x in lan_dict[other] if x in mine]))
            
    def areMembersInterconnected(lan_party):
        members = lan_party.members
        for me in members:
            my_connections = lan_dict[me]
            for other in members:
                if other not in my_connections and other != me:
                    return False
        return True
    
    interconnected_parties = [it.members for it in (filter(areMembersInterconnected, list(lan_parties)))]
    largest_party = sorted(interconnected_parties, key=lambda it: len(it)).pop()
    print("pt2:", ",".join(largest_party))

    
if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('01.txt' if not env_test_run else '00.txt', 'r'), env_test_run)