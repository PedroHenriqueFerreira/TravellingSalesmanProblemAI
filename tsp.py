from typing import Optional
from random import sample

class TSP:
    def __init__(self, d_file: str, s_file: Optional[str] = None):        
        self.d_file = d_file # Arquivo que possui a matriz de distâncias
        self.s_file = s_file # Arquivo que possui todos os passos da solução ótima
        
        self.d: list[list[float]] = [] # Matriz de distâncias
        self.s: Optional[list[int]] = None # Passos da solução ótima
        
        self.load()
        
    def load(self) -> None:
        ''' Carrega todos os dados contidos nos arquivos '''
        
        with open(self.d_file) as f:
            d_data = f.readlines()
            
        for line in d_data:
            row = [float(value) for value in line.split() if value]
            
            if len(row) > 0:
                self.d.append(row)
            
        if self.s_file is None:
            return
        
        self.s = []
        
        with open(self.s_file) as f:
            s_data = f.readlines()
            
        for line in s_data:
            row = [int(value) for value in line.split() if value]
            
            if len(row) > 0:
                self.s.extend(row)

    def random_state(self) -> 'TSPState':
        ''' Gera um estado aleatório '''
        
        return TSPState(self, sample(range(1, len(self.d) + 1), len(self.d)))

class TSPState:
    def __init__(self, tsp: TSP, value: list[int]):
        self.tsp = tsp # Instância do problema
        self.value = value # Estado atual
        
        self.cost = sum(tsp.d[i-1][j-1] for i,j in zip(value, value[1:]+value[:1])) # Custo do estado atual

    def __eq__(self, other: 'TSPState') -> bool:
        return self.value == other.value
    
    def __ne__(self, other: 'TSPState') -> bool:
        return self.value != other.value

    def successors(self):
        ''' Gera todos os vizinhos do estado atual '''
        
        neighbors: list[TSPState] = []
        
        for i in range(len(self.value)):
            for j in range(i, len(self.value)):
                if i == j:
                    continue
                
                neighbors.append(self.swap(i, j))
        
        return neighbors

    def merge(self, other: 'TSPState', i: int):
        ''' Realiza a fusão de dois estados '''
        
        value = self.value[:i]
        
        for item in other.value:
            if item in value:
                continue
            
            value.append(item)
        
        return TSPState(self.tsp, value)

    def swap(self, i: int, j: int):
        ''' Troca a posição de dois elementos '''
        
        value = self.value[:]
        
        value[i], value[j] = value[j], value[i]
        
        return TSPState(self.tsp, value)

    def shuffle(self, i: int, j: int):
        ''' Embaralha a ordem dos elementos no intervalo '''
        
        value = self.value[:]
        
        value[i:j + 1] = sample(value[i:j + 1], len(value[i:j + 1]))
        
        return TSPState(self.tsp, value)
    
    def reverse(self, i: int, j: int):
        ''' Inverte a ordem dos elementos no intervalo '''
        
        value = self.value[:]
        
        value[i:j + 1] = reversed(value[i:j + 1])
        
        return TSPState(self.tsp, value)