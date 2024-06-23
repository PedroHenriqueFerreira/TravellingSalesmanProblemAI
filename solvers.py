from random import choices, choice, random, randint
from math import exp
from time import time

from tsp import TSP, TSPState

class Solver:
    ''' Classe base para todos os solvers '''
    
    def __init__(self, tsp: TSP, verbose=False):
        self.tsp = tsp # Problema a ser resolvido
        self.verbose = verbose # Modo verboso
        
        self.timer = 0 # Tempo de execução
        
        self.steps: list[TSPState] = [] # Passos da solução

    def start_timer(self):
        ''' Limpa os atributos do solver '''
        
        self.timer = time()
        self.steps.clear()
    
    def finish_timer(self):
        ''' Atualiza o tempo de execução '''
        
        self.timer = time() - self.timer
        
    def run(self):
        ''' Executa o algoritmo '''
        
        raise NotImplementedError()

class HillClimbing(Solver):
    ''' Algoritmo de subida de encosta '''    
    
    def run(self):
        ''' Executa o algoritmo de subida de encosta '''
        
        self.start_timer()
        
        current = self.tsp.random_state()
        
        while True:
            self.steps.append(current)
            
            if self.verbose:
                print(f'* STEPS: {self.steps} | COST: {current.cost}')
            
            neighbor = min(current.successors(), key=lambda item: item.cost)
            
            if neighbor.cost >= current.cost:
                break
            
            current = neighbor
        
        self.finish_timer()
        
class GeneticAlgorithm(Solver):
    ''' Algoritmo genético '''
    
    def __init__(self, tsp: TSP, verbose=False, population_size=100, sample_size=10, mutation_rate=0.2, generations=1000):
        super().__init__(tsp, verbose)
        
        self.population_size = population_size # Tamanho da população
        self.sample_size = sample_size # Tamanho das amostras
        self.mutation_rate = mutation_rate # Taxa de mutação
        self.generations = generations # Número de gerações
    
    def selection(self, population: list[TSPState]):
        ''' Seleciona um indivíduo da população '''
        
        sample = choices(population, k=self.sample_size)
        
        return min(sample, key=lambda item: item.cost)
    
    def reproduce(self, x: TSPState, y: TSPState):
        ''' Realiza o cruzamento entre dois indivíduos '''
 
        i = randint(0, len(self.tsp.d))
 
        return x.merge(y, i)
      
    def mutate(self, individual: TSPState):
        ''' Realiza a mutação de um indivíduo '''
        
        i = randint(0, len(self.tsp.d) - 2)
        j = randint(i + 1, len(self.tsp.d) - 1)
        
        mutation = individual
        
        match randint(0, 2):
            case 0:
                mutation = individual.swap(i, j)
            case 1:
                mutation = individual.reverse(i, j)
            case 2:
                mutation = individual.shuffle(i, j)

        return mutation
        
    def run(self):
        ''' Executa o algoritmo genético '''
        
        self.start_timer()
        
        population = [self.tsp.random_state() for _ in range(self.population_size)]
        best = min(population, key=lambda item: item.cost)
        
        for _ in range(self.generations):
            self.steps.append(best)
            
            if self.verbose:
                print(f'* STEPS: {self.steps} | COST: {best.cost}')
            
            new_population: list[TSPState] = []
            
            for _ in range(self.population_size):
                x = self.selection(population)
                y = self.selection(population)
                
                child = self.reproduce(x, y)
                
                if random() < self.mutation_rate:
                    child = self.mutate(child)
                    
                new_population.append(child)
            
            population = new_population
            best = min(population, key=lambda item: item.cost)
            
        self.steps.append(best)
        self.finish_timer()

class SimulatedAnnealing(Solver):
    ''' Algoritmo de recozimento simulado '''
    
    def __init__(self, tsp: TSP, verbose=False, initial_temperature=20, final_temperature=0.1, cooling_rate=0.999):
        super().__init__(tsp, verbose)

        self.initial_temperature = initial_temperature # Temperatura inicial
        self.final_temperature = final_temperature # Temperatura final
        self.cooling_rate = cooling_rate # Taxa de resfriamento
           
    def run(self):
        ''' Executa o algoritmo de recozimento simulado '''
        
        self.start_timer()
        
        current = self.tsp.random_state()
        
        T = self.initial_temperature
        
        while True:
            self.steps.append(current)
            
            if self.verbose:
                print(f'* STEPS: {self.steps} | COST: {current.cost}')
            
            if T < self.final_temperature:
                break
            
            next = choice(current.successors())
            
            delta_E = current.cost - next.cost
            
            if delta_E > 0:
                current = next
            elif random() < exp(delta_E / T):
                current = next
                
            T *= self.cooling_rate
        
        self.steps.append(current)
        self.finish_timer()
        
class TabuSearch(Solver):
    ''' Algoritmo de busca tabu '''
    
    def __init__(self, tsp: TSP, verbose=False, tabu_list_size=100, max_iteration=1000):
        super().__init__(tsp, verbose)
        
        self.tabu_list_size = tabu_list_size # Tamanho máximo da lista tabu
        self.max_iteration = max_iteration # Número máximo de iterações
        
    def run(self):
        ''' Executa o algoritmo de busca tabu '''
        
        self.start_timer()
        
        current = self.tsp.random_state()
        best = current
        
        tabu_list: list[TSPState] = []
        tabu_list.append(current)
         
        for _ in range(self.max_iteration):
            self.steps.append(best)
            
            if self.verbose:
                print(f'* STEPS: {self.steps} | COST: {best.cost}')
            
            neighbors = current.successors()
            
            current_cost = float('inf')
            
            for neighbor in neighbors:
                if neighbor not in tabu_list and neighbor.cost < current_cost:
                    current = neighbor
                    current_cost = neighbor.cost
        
            if current_cost == float('inf'):
                break
            
            if current.cost < best.cost:
                best = current
                
            tabu_list.append(current)
            
            if len(tabu_list) > self.tabu_list_size:
                tabu_list.pop(0)
                
        self.steps.append(best)
        self.finish_timer()
    