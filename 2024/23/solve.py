#!/usr/bin/python3
"""AOC 23th day."""
import sys
from collections import defaultdict

def main(input_file, isTest):
    LanParty = frozenset
    
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
                    lan_parties.add(LanParty([me, other, common]))  
      
    print("pt1:", len([party for party in lan_parties if any(member.startswith("t") for member in party)]))
    
    # pt2:
    lan_parties = set()
    for me, mine in lan_dict.items():
        for other in mine:
            lan_parties.add(LanParty(sorted([me, other]+[x for x in lan_dict[other] if x in mine])))
            
    def areMembersInterconnected(lan_party):
        for me in lan_party:
            my_connections = lan_dict[me]
            for other in lan_party:
                if other not in my_connections and other != me:
                    return False
        return True
    
    interconnected_parties = sorted(filter(areMembersInterconnected, lan_parties), key=len)
    print("pt2:", ",".join(interconnected_parties.pop()))

    
if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('01.txt' if not env_test_run else '00.txt', 'r'), env_test_run)