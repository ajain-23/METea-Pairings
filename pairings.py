import csv, random
from csv import reader as csvreader
from itertools import count


def names_21(li):
    for i in range(0, 40): #file start to co21 end
        yield li[i]

def names_22(li):
    for i in range(40, 92): #co21 end to file end (aka co22)
        yield li[i]

with open("names.csv", 'r') as fp:
    reader = csvreader(fp)
    names = list(reader)

with open("used_pairs.csv", 'r') as fp:
    reader = csvreader(fp)
    exceptions = list(reader)

def used_pairs():
    for i in count():
        try:
            yield exceptions[i]
        except IndexError:
            break

co_21 = list(names_21(names))
co_22 = list(names_22(names))
pairs = []
used_pairs = list(used_pairs())
for lists in used_pairs: #lazily dealing with badly written elements, works efficiently otherwise
    if lists[-1] == '':
        lists.pop(-1)

def ltf_write(guest_list, filename, appending):
    """Write the list to csv file."""
    if not appending:
        with open(filename, "w") as outfile:
            for list in guest_list:
                for entry in list:
                    if list[-1] == entry:
                        outfile.write(entry)
                    else:
                        outfile.write(entry + ", ")
                outfile.write("\n")
    else:
        with open(filename,'a') as outfile:
            for list in guest_list:
                for entry in list:
                    outfile.write(entry + ",")
                outfile.write("\n")

def make_pairs(li_1, li_2):
    for i in range(0, len(li_1)):
        name_1, name_2 = random.choice(li_1), random.choice(li_2)
        pair_init = [name_1[0], name_2[0]]
        while pair_init in used_pairs:
            name_1, name_2 = random.choice(li_1), random.choice(li_2)
            pair_init = [name_1[0], name_2[0]]

        li_1.remove(name_1)
        li_2.remove(name_2)
        pairs.append(pair_init)

    while len(li_2) > 0:
        name_3 = random.choice(li_2)
        pair_final = random.choice(pairs)
        if len(pair_final) == 2:
            pair_final.append(name_3[0])
            li_2.remove(name_3)

    for i in range(0, len(pairs)):
        used_pairs.append(pairs[i])

make_pairs(co_21, co_22)
ltf_write(pairs, "used_pairs.csv", True)
ltf_write(pairs, "pairs.csv", False)

#duplicate pair/triplet identifier, for debugging purposes only
with open('used_pairs.csv') as f:
    seen = set()
    for line in f:
        line_lower = line.lower()
        if line_lower in seen:
            print(line)
        else:
            seen.add(line_lower)
