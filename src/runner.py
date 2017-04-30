import numpy as np

from parser import load_inputs, parse_item
import sys
import queue


# Run all input files
def runner(start_in = 1, end_in = 21):
    data = load_inputs(start_in, end_in)

    for input_data in data:
        res = solver(input_data)
        #TODO: Write this data to a file, maybe in utils.py




# solve each individual input file
def solver(data):
    P = float(data[0])
    M = float(data[1])
    items = data[2]
    constraints = data[3]

    # Add items to PQ
    for item in items:
        item = parse_item(item)

        pq = queue.PriorityQueue()

        priority = calc_priority(P, M, item)

        # Skip this item if it is not profitable
        if (priority == -1):
            continue;

        item_name = item[0]
        item_class = item[1]

        pq.put((-priority, item))

    incompat_list = {}
    # Create constraint list
    for constraint in constraints:
        constraint = parse_constraint(constraint)       
        

def calc_priority(P, M, item):
    print(item)
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