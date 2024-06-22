from tsp import TSP
from solvers import HillClimbing, GeneticAlgorithm, SimulatedAnnealing, TabuSearch

# Instância do problema
tsp = TSP('instances/fri26_d.txt', 'instances/fri26_s.txt')

# Inicialização dos algoritmos

hill_climbing = HillClimbing(tsp)
generic_algorithm = GeneticAlgorithm(tsp)
simulated_annealing = SimulatedAnnealing(tsp)
tabu_search = TabuSearch(tsp)

# Execução dos algoritmos

print('Running Hill Climbing...')
hill_climbing.run()

print('Running Genetic Algorithm...')
generic_algorithm.run()

print('Running Simulated Annealing...')
simulated_annealing.run()

print('Running Tabu Search...')
tabu_search.run()

print('-' * 50)

# Exibição dos resultados

print('Hill Climbing: ')
print(f'STEPS: {hill_climbing.steps} | TIME SPENT: {hill_climbing.timer} | COST: {hill_climbing.solution.cost}')
print(f'SOLUTION: {hill_climbing.solution.value}')

print('-' * 50)

print('Genetic Algorithm: ')
print(f'STEPS: {generic_algorithm.steps} | TIME SPENT: {generic_algorithm.timer} | COST: {generic_algorithm.solution.cost}')
print(f'SOLUTION: {generic_algorithm.solution.value}')

print('-' * 50)

print('Simulated Annealing: ')
print(f'STEPS: {simulated_annealing.steps} | TIME SPENT: {simulated_annealing.timer} | COST: {simulated_annealing.solution.cost}')
print(f'SOLUTION: {simulated_annealing.solution.value}')

print('-' * 50)

print('Tabu Search: ')
print(f'STEPS: {tabu_search.steps} | TIME SPENT: {tabu_search.timer} | COST: {tabu_search.solution.cost}')
print(f'SOLUTION: {tabu_search.solution.value}')

print('-' * 50)
print(f'OPTIMAL SOLUTION: {tsp.s}')