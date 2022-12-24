from concurrent.futures import ThreadPoolExecutor

from gauss import GaussElimination


class Scheduler:
    def __init__(self, max_workers=8):
        self.tasks = []
        self.max_workers = max_workers

    def add_task(self, task, *args):
        self.tasks.append((task, *args))

    def run_tasks(self, tasks):
        self.tasks = tasks
        self.run()

    def run(self):
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for task in self.tasks:
                executor.submit(*task)
        self.tasks = []


class ThreadedGaussElimination(GaussElimination):
    def run_elimination(self):
        scheduler = Scheduler()
        for i in range(self.n):
            scheduler.run_tasks(
                [(self.task_A, i, k) for k in range(i + 1, self.n)]
            )
            scheduler.run_tasks(
                [(self.task_B, i, j, k) for k in range(i + 1, self.n) for j in range(i, self.n + 1)]
            )
            scheduler.run_tasks(
                [(self.task_C, i, j, k) for k in range(i + 1, self.n) for j in range(i, self.n + 1)]
            )
