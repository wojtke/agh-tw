import argparse
import time

import numpy as np

from gauss import GaussElimination
from gauss_multiprocessing import MPGaussElimination
from gauss_threading import ThreadedGaussElimination

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='in', type=str, help='Input file', )
    parser.add_argument('--output', default='out', type=str, help='Output file')
    parser.add_argument('--method', default="threading", choices=["threading", "multiprocessing", "normal"],
                        type=str, help='Method')
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        lines = f.readlines()
        n = int(lines[0])
        A = [[float(x) for x in line.split()] for line in lines[1:n + 1]]
        b = [float(x) for x in lines[n + 1].split()]

    print(f"Input: {args.input}, Out: {args.output}, Method: {args.method}")
    if args.method == "threading":
        solver = ThreadedGaussElimination(A, b)
    elif args.method == "multiprocessing":
        solver = MPGaussElimination(A, b)
    else:
        solver = GaussElimination(A, b)

    start = time.perf_counter()
    solver.run_elimination()
    solver.run_substitution()
    x = solver.get_result()
    end = time.perf_counter()

    print("Correct:", solver.check())

    with open(args.output, 'w') as f:
        f.write(str(n) + '\n')
        f.writelines([" ".join([str(e) for e in row]) + '\n' for row in np.eye(n)])
        f.write(" ".join([str(e) for e in x.flatten()]) + '\n')

    print(f"Time: {end - start}")
