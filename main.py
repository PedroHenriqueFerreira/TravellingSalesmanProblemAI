from tsp import TSP
from solvers import Solver, HillClimbing, GeneticAlgorithm, SimulatedAnnealing, TabuSearch
from screen import draw

# Instância do problema

tsp = TSP('instances/att48_d.txt', 'instances/att48_s.txt', 'instances/att48_xy.txt')

# Inicialização dos algoritmos

solvers: dict[str, Solver] = {
    'HILL CLIMBING': HillClimbing(tsp),
    'GENETIC ALGORITHM': GeneticAlgorithm(tsp),
    'SIMULATED ANNEALING': SimulatedAnnealing(tsp),
    'TABU SEARCH': TabuSearch(tsp)
}

# Execução dos algoritmos

for solver in solvers:
    print(f'RUNNING {solver}...')
    solvers[solver].run()
    print('-' * 50)

# Exibição dos resultados

for solver in solvers:
    print(f'{solver}: ')
    
    print(f'* STEPS: {len(solvers[solver].steps)}')
    print(f'* TIME: {solvers[solver].timer}')
    
    s = solvers[solver].steps[-1]
    
    print(f'* SOLUTION COST: {s.cost}')
    print(f'* SOLUTION VALUE: {s.value}')
    
    print('-' * 50)

if tsp.s is not None:
    print('OPTIMAL SOLUTION: ')    
    print(f'* COST: {tsp.s.cost}')
    print(f'* SOLUTION: {tsp.s.value}')

    print('-' * 50)

# Exibição da tela

print('DRAWING...')

# draw(solvers['GENETIC ALGORITHM'])