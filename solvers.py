from typing import Optional
from random import choices, choice, random, randint
from math import exp
from time import time

from tsp import TSP, TSPState

class Solver:
    def __init__(self):
        self.timer = 0 # Tempo de execução
        
        self.steps = 0 # Número de passos
        self.solution: Optional[TSPState] = None # Solução do problema

    def clean(self):
        ''' Limpa os atributos do solver '''
        
        self.timer = time()
        
        self.steps = 0
        self.solution = None
    
    def finish_timer(self):
        ''' Atualiza o tempo de execução '''
        
        self.timer = time() - self.timer
        
    def run(self):
        ''' Executa o algoritmo '''
        
        raise NotImplementedError()

class HillClimbing(Solver):
    def __init__(self, tsp: TSP):
        super().__init__()
        
        self.tsp = tsp # Instância do problema
    
    def run(self):
        ''' Executa o algoritmo de subida de encosta '''
        
        self.clean()
        
        current = self.tsp.random_state()
        
        while True:
            neighbor = min(current.successors(), key=lambda item: item.cost)
            
            if neighbor.cost >= current.cost:
                break
            
            current = neighbor
            
            self.steps += 1
        
        self.finish_timer()
        
        self.solution = current
        
class GeneticAlgorithm(Solver):
    def __init__(self, tsp: TSP, population_size=100, sample_size=10, mutation_rate=0.2, generations=1000):
        super().__init__()
        
        self.tsp = tsp # Instância do problema
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
        
        self.clean()
        
        population = [self.tsp.random_state() for _ in range(self.population_size)]

        for _ in range(self.generations):
            new_population: list[TSPState] = []
            
            for _ in range(self.population_size):
                x = self.selection(population)
                y = self.selection(population)
                
                child = self.reproduce(x, y)
                
                if random() < self.mutation_rate:
                    child = self.mutate(child)
                    
                new_population.append(child)
            
            population = new_population
            
            self.steps += 1
            
        self.finish_timer()
        
        self.solution = min(population, key=lambda item: item.cost)

class SimulatedAnnealing(Solver):
    def __init__(self, tsp: TSP, initial_temperature=1000, final_temperature=1e-3, cooling_rate=0.999):
        super().__init__()
        
        self.tsp = tsp # Instância do problema
        self.initial_temperature = initial_temperature # Temperatura inicial
        self.final_temperature = final_temperature # Temperatura final
        self.cooling_rate = cooling_rate # Taxa de resfriamento
        
    def run(self):
        ''' Executa o algoritmo de recozimento simulado '''
        
        self.clean()
        
        current = self.tsp.random_state()
        
        T = self.initial_temperature
        
        while True:
            if T < self.final_temperature:
                break
            
            next = choice(current.successors())
            
            delta_E = current.cost - next.cost
            
            if delta_E > 0:
                current = next
            elif random() < exp(delta_E / T):
                current = next
                
            T *= self.cooling_rate
            
            self.steps += 1
        
        self.finish_timer()
        
        self.solution = current
        
class TabuSearch(Solver):
    def __init__(self, tsp: TSP, tabu_list_size=100, max_iteration=1000):
        super().__init__()
        
        self.tsp = tsp # Instância do problema
        self.tabu_list_size = tabu_list_size # Tamanho máximo da lista tabu
        self.max_iteration = max_iteration # Número máximo de iterações
        
    def run(self):
        ''' Executa o algoritmo de busca tabu '''
        
        self.clean()
        
        current = self.tsp.random_state()
        best = current
        
        tabu_list: list[TSPState] = []
        tabu_list.append(current)
         
        for _ in range(self.max_iteration):
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
                
            self.steps += 1
        
        self.finish_timer()
        
        self.solution = best
    