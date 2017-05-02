import numpy as np

from parser import load_inputs, parse_item, parse_constraint, write_output
import sys
import queue
import random

MAX_LIST_LEN = 200001

# Run all input files
def runner(start_in = 1, end_in = 21, num_iter = 1):
    data = load_inputs(start_in, end_in)
    prob_num = start_in
    prob_num = 1
    for input_data in data:
        print("PROBLEM NUMBER: " + str(prob_num))
        res = solver(input_data, prob_num, num_iter)
        prob_num += 1



# solve each individual input file
def solver(data, problem_num, num_iter):
    P = float(data[0])
    M = float(data[1])
    items = data[2]
    print("LEN ITEMS: " + str(len(items)))
    constraints = data[3]
    C = len(constraints)
    N = len(items)

    y = random.randint(1, 200)
    batch_size = N // y

    incompat_list = createIncompatList(constraints)

    for i in range(num_iter):
        pq = createAndFillPQ(items, P, M)
        output, profit = find_solution(pq, incompat_list, N, P, M, batch_size)
        write_output("../outputs/problem" + str(problem_num) + ".out", output, profit, str(problem_num))

def createIncompatList(constraints):
    incompat_list = [set() for _ in range(MAX_LIST_LEN + 1)]

    # Iterate through each constraint list in ALL constraint lists
    for c_list in constraints:
        # Iter through each constraint
        for constraint in c_list:
            for other in c_list:
                if (other != constraint):
                    incompat_list[constraint].add(other)

    return incompat_list

def isCompatible(sack, cls, incom_list):
    for item in sack:
        if item in incom_list:
            return False

    return True

def createAndFillPQ(items, P, M):
    pq = queue.PriorityQueue()
    x = random.randint(0, 3)

    # Add items to PQ
    for item in items:
        priority = calc_priority(P, M, item, x)

        # Skip this item if it is not profitable
        if (priority == -1):
            continue;

        pq.put([priority, item])

    return pq

def calc_priority(P, M, item, x):
    #print(item)
    weight = float(item[2])
    cost = float(item[3])
    resale = float(item[4])
    profit = resale - cost

    # Return flag if we should never add this item
    if (profit <= 0):
        return -1

    # Check if cost is 0
    if (cost == 0 or weight == 0):
        return 10 * resale

    if (x == 0):
        return (resale / (cost))
    elif (x == 1):
        return (resale / (cost + weight))
    elif (x == 2):
        return (resale / weight)
    else:
        a = random.uniform(0.1, 0.9)
        b = 1 - a
        return resale / (a*cost + b*weight)

def find_solution(pq, incompat_list, N, P, M, batch_size):
    # Pop off our PQ and add to our garg bag
    output = []   
    incompat_classes = set()
     
    total_money = 0

    patience = N

    print("QUEUE SIZE: " + str(pq.qsize()))

    while (not pq.empty()):
        batch = []
        for i in range(batch_size):
            if (pq.empty()):
                break;

            batch.append(pq.get())

        random.shuffle(batch)

        for next in batch:
            priority = next[0]
            item = next[1]

            name = item[0] 
            cls = int(item[1])
            weight = float(item[2])
            cost = float(item[3])
            resale = float(item[4])

            if (weight < P and cost < M and isCompatible(incompat_classes, cls, incompat_list[cls])):
                output.append(name)
                incompat_classes.add(cls)
                P -= weight
                M -= cost
                total_money += resale
                patience += N / 1000
            else:
                patience -= 1

    # Add the remaining money
    total_money += M

    return output, total_money

if __name__ == '__main__':
    # Load and start running our runner
    if (len(sys.argv) == 4):
        start_in = sys.argv[1]
        end_in = sys.argv[2]
        num_iter = sys.argv[3]
        print("Launching running with " + num_iter + " iterations on problems ranging from [" + start_in + ", " + end_in + "].")
        runner(int(start_in), int(end_in), int(num_iter))
    else:
        print("Launching the default runner")
        runner()