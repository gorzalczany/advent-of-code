"""AOC 2nd day."""

file = open('1.txt', 'r')
line = file.readline()
ranges = line.split(',')

invalid_numbers_1 = set()
invalid_numbers_2 = set()

for range_s in ranges:
    start_s, stop_s = range_s.split('-')
    start = int(start_s)
    stop = int(stop_s)

    for number in range(start, stop + 1):
        str_num = str(number)

        # p1
        first_half = str_num[:len(str_num)//2]
        second_half = str_num[len(str_num)//2:]
        if first_half == second_half:
            invalid_numbers_1.add(number)

        # p2
        sut = str_num[0]
        for i in range(1, len(str_num)):
            if len(sut) > len(str_num)//2:
                break
            if str_num == sut * (len(str_num)//i):
                invalid_numbers_2.add(number)
                break
            sut += str_num[i]
        
    

print(sum(invalid_numbers_1))
print(sum(invalid_numbers_2))