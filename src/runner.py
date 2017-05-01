import numpy as np

from parser import load_inputs, parse_item, parse_constraint, write_output
import sys
import queue

MAX_LIST_LEN = 200001

# Run all input files
def runner(start_in = 1, end_in = 21):
    data = load_inputs(start_in, end_in)

    prob_num = 1
    for input_data in data:
        print("PROBLEM NUMBER: " + str(prob_num))
        res = solver(input_data, prob_num)
        prob_num += 1
        #TODO: Write this data to a file, maybe in utils.py




# solve each individual input file
def solver(data, problem_num):
    P = float(data[0])
    M = float(data[1])
    items = data[2]
    print("LEN ITEMS: " + str(len(items)))
    constraints = data[3]
    C = len(constraints)
    N = len(items)
    pq = queue.PriorityQueue()

    # Add items to PQ
    for item in items:
        #item = parse_item(item)

        priority = calc_priority(P, M, item)

        # Skip this item if it is not profitable
        if (priority == -1):
            continue;

        item_name = item[0]
        item_class = item[1]

        pq.put([priority, item])

    incompat_list = [set() for _ in range(MAX_LIST_LEN + 1)]

    # Iterate through each constraint list in ALL constraint lists
    for c_list in constraints:

        # print(c_list)
        #c_list = parse_constraint(c_list)

        # Iter through each constraint
        for constraint in c_list:
            for other in c_list:
                incompat_list[constraint + 1].add(other)   

    # Pop off our PQ and add to our garg bag
    output = []    
    total_money = 0

    patience = N / 3

    print("QUEUE SIZE: " + str(pq.qsize()))

    while (not pq.empty()):
        if (patience == 0):
            break;

        next = pq.get()
        priority = next[0]
        item = next[1]

        name = item[0] 
        cls = int(item[1])
        weight = float(item[2])
        cost = float(item[3])
        resale = float(item[4])

        if (weight < P and cost < M and isCompatible(output, cls, incompat_list[cls])):
            output.append(name)
            P -= weight
            M -= cost
            total_money += resale - cost
            patience += N / 1000
        else:
            patience -= 1

    total_money += M


    write_output("../outputs/problem" + str(problem_num) + ".out", output, total_money, str(problem_num))

def isCompatible(sack, cls, incom_list):
    for item in sack:
        if item in incom_list:
            return False

    return True

def calc_priority(P, M, item):
    #print(item)
    weight = float(item[2])
    cost = float(item[3])
    resale = float(item[4])
    profit = resale - cost

    # Return flag if we should never add this item
    if (profit <= 0):
        return -1

    # Check if cost is 0
    if (cost == 0):
        return 10 * resale

    return (resale / cost)
    # (resale / cost) * (weight / P)

if __name__ == '__main__':
    # Load and start running our runner
    if (len(sys.argv) == 3):
        start_in = sys.argv[1]
        end_in = sys.argv[2]
        print("Launching running with range [" + start_in + ", " + end_in + "].")
        runner(int(start_in), int(end_in))
    else:
        print("Launching the default runner")
        runner()