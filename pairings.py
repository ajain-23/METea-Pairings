import csv, random
from csv import reader as csvreader
from itertools import count

with open("names.csv", 'r') as fp:
    reader = csvreader(fp)
    names = list(reader)

with open("used_pairs.csv", 'r') as fp:
    reader = csvreader(fp)
    used_pairs = list(reader)
    for lists in used_pairs: #lazily dealing with badly formatted elements, works efficiently otherwise
        if lists[-1] == '':
            lists.pop(-1)

co_21 = [names[i] for i in range(0, 40)]
co_22 = [names[i] for i in range(40, 92)]

pairs, with_triplets = [], []

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
        name_3 = random.choice(li_2)[0]
        pair_final = random.choice(pairs)
        while [pair_final[0], name_3] in used_pairs or pair_final in used_pairs or [pair_final[1], name_3] in used_pairs:
            pair_final = random.choice(pairs)
        if len(pair_final) == 2:
            pair_final.append(name_3)

            with_triplets.append([pair_final[0], pair_final[1]])
            with_triplets.append([pair_final[0], pair_final[2]])
            with_triplets.append([pair_final[1], pair_final[2]])

            li_2.remove([name_3])

    for i in range(0, len(pairs)):
        with_triplets.append(pairs[i])


def matchmaker():
    ''' Created a function despite not having explicit benefit
        b/c allows for easier file additions and modifications. '''
    make_pairs(co_21, co_22)
    ltf_write(with_triplets, "used_pairs.csv", True)
    ltf_write(pairs, "pairs.csv", False)

    print("{} unique pairs created. Success!".format(len(pairs)))

# Duplicate pair/triplet identifier, for debugging purposes only
with open('used_pairs.csv') as f:
    seen = set()
    for line in f:
        line_lower = line.lower()
        if line_lower in seen:
            print(line)
        else:
            seen.add(line_lower)

# Identifies MET Students who have not yet submitted appropriate Google Form, not part of pairing algorithm
with open("form_sub.csv", 'r') as fp:
    reader = csvreader(fp)
    form_names = list(reader)

nosub_21 = [co_21[j] for j in range(len(co_21)) if co_21[j] not in form_names]
nosub_22 = [co_22[j] for j in range(len(co_22)) if co_22[j] not in form_names]

ltf_write(nosub_21, "no_sub.csv", False)
ltf_write(nosub_22, "no_sub.csv", True)

matchmaker() # Finalize pairings and output to pairs.csv + add them to used_pairs registry
