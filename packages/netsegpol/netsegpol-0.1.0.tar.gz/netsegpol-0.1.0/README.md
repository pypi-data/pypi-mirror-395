# NetSegPol

This repository provides a lightweight, object-oriented Python toolkit for computing structural polarization and segregation measures in networks. It implements a wide range of classical and modern network mixing, segregation, and polarization indices used in sociology, computational social science, and network science.



## How to use?

**You should not use descriptive measures without a null-model.** 

```{python}

from netsegpol import Measurer

edges = [
    # Group 0 
    (0, 1), (0, 2), (1, 2), (1, 3),
    (2, 3), (2, 4), (3, 4), (0, 4),

    # Group 1 
    (5, 6), (5, 7), (6, 7), (6, 8),
    (7, 8), (7, 9), (8, 9), (5, 9),

    # Sparse inter-group edges
    (2, 6), (3, 7), (1, 8), (4, 9)
]

membership = {
    0: 0, 1: 0, 2: 0, 3: 0, 4: 0,
    5: 1, 6: 1, 7: 1, 8: 1, 9: 1
}

measurer = Measurer(edges, 
                    membership,
                    directed = False,
                    safe_create = True)

print(measurer.segregation_matrix_index()) # or the function that you want to use
```


## What should I be careful of? 

You should be careful if you are using an external package like [igraph](https://python.igraph.org/en/stable/) and getting the edge list directly since indexing methods might differ and your edgelist and membership dictionary might not match.


## Will there be new measures? 

This is still a project in its infancy, hence a few of the measures will be developed later on, such as Ergodic Markov Chain mixing time or Spectral Segregation etc. 









