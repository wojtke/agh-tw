import numpy as np


class GaussElimination:
    def __init__(self, A, b):
        A = np.array(A)
        b = np.array(b).reshape(-1, 1)

        assert A.shape[0] == A.shape[1]
        assert b.shape[0] == A.shape[0]

        self.A, self.b = A, b
        self.M = np.hstack([A, b])  # M is the augmented matrix of A and b
        self.M = self.M.astype(np.double)

        self.m_aux = {}
        self.n_aux = {}

        self.n = len(b)

        self.task_run_list = []

    def task(fun):
        def wrapper(self, *args):
            self.task_run_list.append((fun.__name__[-1], *args))
            fun(self, *args)

        return wrapper

    def __repr__(self):
        return self.M.__repr__()

    def get_result(self):
        return self.M[:, -1].reshape(-1, 1)

    def run_elimination(self):
        for i in range(self.n):  # for each row
            for k in range(i + 1, self.n):  # for each row below
                self.task_A(i, k)
                for j in range(i + 1, self.n + 1):  # for each col
                    self.task_B(i, j, k)
                    self.task_C(i, j, k)

        return self

    def run_substitution(self):
        for i in range(self.n):
            self.M[i] /= self.M[i, i]

        for j in range(self.n - 1, -1, -1):  # for each col from the last to the first
            for i in range(j):  # for each row above
                self.M[i, self.n] -= self.M[i, j] * self.M[j, self.n]
        return self

    def check(self, eps=1e-6):
        x = self.get_result()
        return all(self.A @ x - self.b < eps)

    @task
    def task_A(self, i, k):
        """Znalezienie mnożnika dla wiersza i, do odejmowania go od k-tego wiersza"""
        self.m_aux[(k, i)] = self.M[k, i] / self.M[i, i]

    @task
    def task_B(self, i, j, k):
        """Pomnożenie j-tego elementu wiersza i przez mnożnik - do odejmowania od k-tego wiersza"""
        self.n_aux[(i, j, k)] = self.M[i, j] * self.m_aux[(k, i)]

    @task
    def task_C(self, i, j, k):
        """Odjęcie j-tego elementu wiersza i od wiersza k"""
        self.M[k, j] -= self.n_aux[(i, j, k)]


def op_get_read_write(task):
    if task[0] == 'A':
        i, k = task[1:]
        return ["M[{}, {}]".format(k, i)], "m_aux[{}, {}]".format(k, i)
    elif task[0] == 'B':
        i, j, k = task[1:]
        return ["M[{}, {}]".format(i, j), "m_aux[{}, {}]".format(k, i)], "n_aux[{}, {}, {}]".format(i, j, k)
    elif task[0] == 'C':
        i, j, k = task[1:]
        return ["n_aux[{}, {}, {}]".format(i, j, k)], "M[{}, {}]".format(k, j)


def dependence_fun(op1, op2):
    reads_list_1, write_1 = op_get_read_write(op1)
    reads_list_2, write_2 = op_get_read_write(op2)

    return write_1 in reads_list_2 or write_2 in reads_list_1
