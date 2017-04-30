import numpy as np
import pickle
import gzip


path = "../inputs/project_instances/"

# Load in all the inputs (NOTE: Maybe turn into nparray?)
def load_inputs(start_num, end_num):
    print("Loading the inputs...")

    inputs = []

    for i in range(start_num, end_num + 1):
        print("Loading Input " + str(i) + ":")
        data_path = path + "problem" + str(i) + ".in"
        data = parse_input(data_path)
        inputs += [data]
 
    #print(inputs)
    return inputs

# Parse each individual input file
def parse_input(path):
    # Load the data
    with open(path) as f:
        data = f.readlines()

    # Clean white space
    data = [x.strip() for x in data]
    P = float(data[0])
    M = float(data[1])
    N = int(data[2])
    C = int(data[3])

    print("P: " + str(P) +  " M: " + str(M) + " N: " + str(N) + " C: " + str(C) + "\n")

    items = data[4:4+N]
    constraints = data[4+N:5+N+C]

    return [P, M, items, constraints]

def parse_item(item):
    return item.split(";")

def parse_constraint(constraint):
    return item.split(",")

