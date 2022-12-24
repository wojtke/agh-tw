import ctypes
import multiprocessing as mp

import numpy as np

from gauss import GaussElimination


def to_numpy_array(shared_array, shape):
    arr = np.ctypeslib.as_array(shared_array)
    return arr.reshape(shape)


def init_worker(shared_array, aux1, aux2, shape):
    global M, m_aux, n_aux
    M = to_numpy_array(shared_array, shape)
    m_aux = aux1
    n_aux = aux2


def task_A(i, k):
    m_aux[(k, i)] = M[k, i] / M[i, i]


def task_B(i, j, k):
    n_aux[(i, j, k)] = M[i, j] * m_aux[(k, i)]


def task_C(i, j, k):
    M[k, j] -= n_aux[(i, j, k)]


def mp_elimination(gauss_elimination):
    size = gauss_elimination.M.size
    shape = gauss_elimination.M.shape

    shared_array = mp.RawArray(ctypes.c_double, size)
    M = to_numpy_array(shared_array, shape)
    np.copyto(M, gauss_elimination.M)

    m_aux = mp.Manager().dict()
    n_aux = mp.Manager().dict()

    pool = mp.Pool(
        processes=16,
        initializer=init_worker,
        initargs=(shared_array, m_aux, n_aux, shape)
    )

    n = gauss_elimination.n
    for i in range(n - 1):
        pool.starmap(task_A, [(i, k) for k in range(i + 1, n)])
        pool.starmap(task_B, [(i, j, k) for k in range(i + 1, n) for j in range(i, n + 1)])
        pool.starmap(task_C, [(i, j, k) for k in range(i + 1, n) for j in range(i, n + 1)])

    np.copyto(gauss_elimination.M, M)


class MPGaussElimination(GaussElimination):
    def run_elimination(self):
        mp_elimination(self)
        return self
