#!/usr/bin/python3
"""AOC 9th day."""
import sys

class File(object):
    def __init__(self, length , content):
        self.length = length
        self.content = content
        self.moved = False if content != "." else True
    def __eq__(self, other):
        self.length = other.length
        self.content = other.content
        self.moved = other.moved

def move_file(files):
    for file_index, file in enumerate(files[::-1]):
        if file.moved: continue
        if file.content == ".": continue
        file.moved = True
        for space_index, space in enumerate(files):
            if space.content != ".": continue
            if space.length < file.length: continue
            true_file_index = len(files)-1-file_index
            if true_file_index < space_index:
                return files
            file_diff = space.length - file.length
            files[space_index] = file
            files[true_file_index] = File(file.length, ".")
            if file_diff > 0:
                files.insert(space_index+1, File(file_diff, "."))
            return files
    return files

def getFiles(disk):
    files = []
    for value in disk:
        if len(files) == 0:
            files.append(File(1, value))
            continue
        if files[-1].content == value:
            files[-1].length += 1
            continue
        files.append(File(1, value))  
    return files

def makeDiskFromFiles(files):
    newDisk = []
    for file in files:
        for i in range(0, file.length):
            newDisk.append(file.content)
    return newDisk

def getChecksum(disk):
    checksum = 0
    for i, block in enumerate(disk):
        if block == ".": continue
        checksum += i * block
    return checksum

def getDisk(input):
    disk = []
    enumerator = 0
    for id, block in enumerate(input):
        for i in range(0, int(block)):
            if id % 2 == 0:
                disk.append(enumerator)
            else:
                disk.append(".")
        if id % 2 == 0:
            enumerator += 1
    return disk

def main(input_file):
    input = input_file.read()
    disk = getDisk(input)

    # pt 1
    for i, value in enumerate(disk):
        if value == ".":
            tuple = next((x for x in enumerate(disk[::-1]) if x[1] != "."), None)
            if not tuple: break
            index, last = tuple
            last_index = len(disk)-1-index
            if i > last_index: break
            disk[last_index] = "."
            disk[i] = last    
    print(getChecksum(disk))
    
    # pt 2
    disk = getDisk(input)
    files = getFiles(disk)
    while True:
        files = move_file(files)
        if not len(list(filter(lambda x: x.moved == False, files))) > 0: break
    disk = makeDiskFromFiles(files)
    print(getChecksum(disk))

if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('01.txt' if not env_test_run else '00.txt', 'r'))