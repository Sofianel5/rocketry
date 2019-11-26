import numpy as np
from motoranalytics import evalFitnessFromValList
bounds = [
(0.06, 0.1),#throat diameter
(0.125, 0.31), #exit diameter
(0.125, 0.31), # motor width
(0.1, 3), #motor length
(0.005, 0.02), #fin width
(0.005, 0.02), #fin length
(0.01,0.1), #inner width
]
def de(fobj, bounds, mut=0.8, crossp=0.7, popsize=1500, its=1):
    dimensions = len(bounds)
    pop = np.random.rand(popsize, dimensions)
    min_b, max_b = np.asarray(bounds).T
    diff = np.fabs(min_b - max_b)
    pop_denorm = min_b + pop * diff
    print(pop_denorm)
    fitness = np.asarray([fobj(ind) for ind in pop_denorm])
    best_idx = np.argmin(fitness)
    best = pop_denorm[best_idx]
    for i in range(its):
        print("iteration: ", i)
        for j in range(popsize):
            print("population index: ", j)
            idxs = [idx for idx in range(popsize) if idx != j]
            a, b, c = pop[np.random.choice(idxs, 3, replace = False)]
            mutant = np.clip(a + mut * (b - c), 0, 1)
            cross_points = np.random.rand(dimensions) < crossp
            if not np.any(cross_points):
                cross_points[np.random.randint(0, dimensions)] = True
            trial = np.where(cross_points, mutant, pop[j])
            trial_denorm = min_b + trial * diff
            f = fobj(trial_denorm)
            if f < fitness[j]:
                fitness[j] = f
                pop[j] = trial
                if f < fitness[best_idx]:
                    best_idx = j
                    best = trial_denorm
        print(best)
        yield best, fitness[best_idx]
result = list(de(evalFitnessFromValList, bounds))
with open("result.txt", "w") as f:
    for item in result:
        f.write("%s\n\n" % string(item))
