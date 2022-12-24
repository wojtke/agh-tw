import argparse

import numpy as np
from gauss import GaussElimination, dependence_fun
from fnf import FNFMaker

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('n', default=3, type=int, help='Matrix size')
    args = parser.parse_args()

    assert args.n > 1, "Matrix size must be at least 2x2"
    assert args.n < 10, "Please, don't use this program for such big matrices"

    A = np.random.uniform(-10, 10, (args.n, args.n))
    b = np.random.uniform(-10, 10, args.n)

    ge = GaussElimination(A, b)
    ge.run_elimination()
    ge.run_substitution()
    ge.check()

    maker = FNFMaker(
        alphabet=ge.task_run_list,
        dependence_fun=dependence_fun
    )

    print("Dependencies:\n", maker.get_dependencies())

    G = maker.build_graph(ge.task_run_list)
    maker.draw_graph(G, ge.task_run_list)
    fnf = maker.getFNF(G, ge.task_run_list)

    print("FNF:\n", fnf)
