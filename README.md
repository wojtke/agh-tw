# Concurrency theory
Project for Concurrency theory (teoria współbieżności) at AGH UST - fall 2022.


### Algorithms
Algorithm that builds a diekert graph and finds Foata normal form of a given problem.
Try out examples: [`fnf_example.py`](fnf_example.py), [`fnf_example_gauss.py`](fnf_example_gauss.py).
See [`fnf.py`](fnf.py) for implementation.


```
Input:
    "a": "x := x + y",
    "b": "y := y + 2z",
    "c": "x := 3x + z",
    "d": "z := y − z"
    word = "baadcb"
    
Output:
    Dependencies:
    {('d', 'c'), ('b', 'b'), ('a', 'c'), ('c', 'c'), ('b', 'a'), ('c', 'd'), ('d', 'd'), ('d', 'b'), ('c', 'a'), ('a', 'a'), ('a', 'b'), ('b', 'd')}
    FNF:
    [{'b'}, {'d', 'a'}, {'a'}, {'c', 'b'}]
```

### Gaussian elimination
Gaussian elimination algorithm with python's threading and multiprocessing library.
Implementations: [`gauss.py`](gauss.py), [`gauss_threading.py`](gauss_threading.py), [`gauss_multiprocessing.py`](gauss_multiprocessing.py).

Run [`main.py`](main.py) to see the results. 



![erfr](diekert%20graphs/4.png)

### Checker

[An official checker for the project](https://github.com/macwozni/Matrices.git)
