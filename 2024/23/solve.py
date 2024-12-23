#!/usr/bin/python3
"""AOC 23th day."""
import sys

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
     
    lan_dict = {}
    for a,b in connections:
        if a in lan_dict:
            lan_dict[a].add(b)
        else:
            lan_dict[a] = set([b]) 
        if b in lan_dict:
            lan_dict[b].add(a)  
        else:
            lan_dict[b] = set([a])
    for k, v in lan_dict.items():
        vl = list(v)
        vl.sort()
        lan_dict[k] = set(vl)

    lan_groups = set()
    for me, mine in lan_dict.items():
        for other in mine:
            potential_commons = lan_dict[other]
            for common in potential_commons:
                if common == me or common == other:
                    continue
                if common in mine:
                    lan_groups.add(LanGroup([me, other, common]))  
      
    counter = 0  
    for lan_group in lan_groups:
        for member in lan_group.members:
            if member.startswith("t"):
                counter += 1
                break            
    print("pt1:", counter)
    
    # pt2:
    lan_groups = set()
    for me, mine in lan_dict.items():
        for other in mine:
            potential_commons = lan_dict[other]
            commons = [me, other]
            for common in potential_commons:
                if common == me or common == other:
                    continue
                if common in mine:
                    commons.append(common)
            lan_groups.add(LanGroup(commons))
            
    def areMembersInterconnected(lan_party):
        members = lan_party.members
        for member in members:
            my_connections = lan_dict[member]
            for other in members:
                if other not in my_connections:
                    if other == member:
                        continue
                    return False
        return True
    
    interconnectedGroups = list(filter(areMembersInterconnected, list(lan_groups)))
    inter_members = map(lambda it: it.members, interconnectedGroups)
    
    def sortListFromLongest(list):
        return -len(list)
    
    max_group = sorted(inter_members, key=sortListFromLongest)[0]
    print("pt2:", ",".join(max_group))
                  

    
if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('01.txt' if not env_test_run else '00.txt', 'r'), env_test_run)