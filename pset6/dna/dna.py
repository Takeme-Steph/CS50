from sys import argv, exit
import csv

# check if 2 csv files were inputed
if len(argv) != 3:
    print("input 2 files only - Database and Sequence")
    exit(1)

# open database file
preader = open(argv[1], "r")
# load values into a dictionary 
people = csv.DictReader(preader)
    
# open and store sequence text
sdata = (open(argv[2], 'r')).read()

# create dictionary to store search results 
results = {}

# loop through the dic once
for line in people:
    # check for STR in dic
    for seq in line:
        if seq == 'name':  # skip name column
            continue
        # find the position of the first occurence of the STR
        sloc = sdata.find(seq)
        # skip this STR if not found
        if sloc == -1:
            continue
        slen = len(seq)  # store length of current sequence name
        ppos = 0  # store previous position
        cpos = 0  # store current position
        count = 0  # store count of sequence
        maxc = 0  # store max count of sequence
        i = sloc
        # loop through text file to find STR repeats
        while i < len(sdata):
            # update current position
            cpos = sdata.find(seq, i)
            # if not found
            if cpos == -1:
                if count > 0:
                    if count > maxc:
                        maxc = count  # swap max if current count is higher
                    break
                break
            # if first run
            elif ppos == 0:
                count += 1
                ppos = cpos
                i = cpos + slen  # update i to make it loop through faster
            # if a consecutive repeat
            elif cpos == (ppos + slen):
                count += 1
                ppos = cpos
                i = cpos + slen
            # if a new non-consecutive occurence
            else:
                if count > 0:
                    if count > maxc:
                        maxc = count
                    count = 1
                    ppos = cpos
                    i = cpos + slen
                else:   
                    ppos = cpos
                    i = cpos + slen
        # store results
        results[seq] = maxc

    # break so it runs only once, just the first line
    break

# close files
preader.close()

# re-open files to check for match
with open(argv[1], "r") as preader:
    people = csv.DictReader(preader)
    # loops through each line in database
    for line in people:
        match = 0  # set match counter
        #loop through each STR in results
        for seq in results:
            # increase match count if STR values match
            if int(line[seq]) == int(results[seq]):
                match += 1
        # check if all value matched excluding name column(-1)
        if match == (len(line) - 1):
            print(line['name'])  # print match name
            exit(0)
    print('No match')
    