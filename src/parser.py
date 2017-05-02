import numpy as np
import pickle
import gzip

import os



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
        #data = f.readlines()

        P = float(f.readline())
        M = float(f.readline())
        N = int(f.readline())
        C = int(f.readline())

        items = []
        constraints = []
        for i in range(N):
          name, cls, weight, cost, val = f.readline().split(";")
          items.append([name, int(cls), float(weight), float(cost), float(val)])
        for i in range(C):
          constraint = set(eval(f.readline()))
          constraints.append(constraint)

    # # Clean white space
    # data = [x.strip() for x in data]
    # P = float(data[0])
    # M = float(data[1])
    # N = int(data[2])
    # C = int(data[3])

    # print("P: " + str(P) +  " M: " + str(M) + " N: " + str(N) + " C: " + str(C) + "\n")

    # items = data[4:4+N]
    # constraints = data[4+N:5+N+C]

    return [P, M, items, constraints]

def read_input(filename):
  """
  P: float
  M: float
  N: integer
  C: integer
  items: list of tuples
  constraints: list of sets
  """
  with open(filename) as f:
    P = float(f.readline())
    M = float(f.readline())
    N = int(f.readline())
    C = int(f.readline())
    items = []
    constraints = []
    for i in range(N):
      name, cls, weight, cost, val = f.readline().split(";")
      items.append((name, int(cls), float(weight), float(cost), float(val)))
    for i in range(C):
      constraint = set(eval(f.readline()))
      constraints.append(constraint)
  
  return P, M, N, C, items, constraints


def parse_item(item):
    return item.split(";")

def parse_constraint(constraint):
    assert(constraint != "")

    constraints = constraint.split(",")
    for i in range(len(constraints)):
        constraints[i] = int(constraints[i])

    return constraints

def write_output(filename, items_chosen, new_best, p_num):

    best_path = "../best/output_" + p_num + "_best.out"

    b = open(best_path, "r")
    old_best = b.readline()

    if (old_best == "" or (new_best > float(old_best))):
        print(filename)
        print("OLD BEST: " + old_best)
        print("NEW BEST: " + str(new_best))

        b.close()
        os.remove(best_path)
        b = open(best_path, "w+")
        b.write(str(new_best))
        
        if (os.path.isfile(filename)):
          os.remove(filename)
        
        f = open(filename, "w+")

        for i in items_chosen:
            f.write("{0}\n".format(i))

