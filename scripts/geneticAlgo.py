from random import choices
from typing import List
from typing import Tuple, Callable
import collections
from random import randint, random, randrange
from functools import partial 

Genome = List[int]
Population = List[Genome]
FitnessFunc = Callable[[Genome], int]
PopulateFunc = Callable[[], Population]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
Crossoverfunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable [[Genome], Genome]

Thing = collections.namedtuple('Thing', ['name', 'value', 'weight'])

things= [
    
    Thing ('Refrigerator A', '2999.7', '2.253'),
    Thing ('Cell phone', '4398.24','0.0001798'),
    Thing ('TV 55', '21734.95', '2'),
    Thing ('TV 50', '19999.5', '1.45'),
    Thing ('TV 42', '14995' , '1'),
    Thing ('Notebook A', '9999.6','0.014'),
    Thing ('Ventilator', '2398.8', '5.952'),
    Thing('Microwave A', '2160.62', '0.2968'),
    Thing('Microwave B', '3009.3', '0.3808'),
    Thing ('Microwave C', '2693.61', '0.2871'),
    Thing ('Refrigerator B', '3396', '2.54'),
    Thing ('Refrigerator C', '2399.78', '1.74'),
    Thing ('Notebook B', '11994', '2.988'),
    Thing ('Notebook C', '23,994', '3.162')
    
    
    ]

def generate_genome(length: int) -> Genome:
    return choices([0, 1], k=length)

def generate_population(size: int, genome_length: int) -> Population:
    return [generate_genome(genome_length) for _ in range(size)]

def fitness(genome: Genome, things: [Thing], weight_limit: int) -> int:
    if len(genome) != len(things):
        raise ValueError("genome and things must be of same length")

    weight = 0
    value = 0
    for i, thing in enumerate(things):
        if genome[i] == 1:
            weight += thing.weight
            value += thing.value

            if weight > weight_limit:
                return 0

    return value

def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
   return choices(
       population=population,
       weights=[fitness_func(genome) for genome in population],
       k=2
       
       
    )

def single_point_crossover(a: Genome, b: Genome ) -> Tuple[Genome, Genome]:
    if len(a) != len(b):
        raise ValueError("Genome a and b must be of same length")
    length = len(a)
    if length < 2:
        return a, b 
    
    
    
    p = randint(1, length -1)
    return a[0:p] + b[p:], b[0:p] + a[p:]


def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        index = randrange(len(genome))
        genome[index] = genome[index] if random() > probability else abs(genome[index] - 1)
    return genome 


def run_evolution(
        populate_func: PopulateFunc,
        fitness_func: FitnessFunc,
        fitness_limit: int,
        selection_func: SelectionFunc = selection_pair,
        crossover_func: Crossoverfunc = single_point_crossover,
        mutation_func: MutationFunc = mutation,
        generation_limit: int = 180
    
) -> Tuple[Population, int]:
    population = populate_func()
    
    
    for i in range(generation_limit):
        population = sorted(
            population,
            key=lambda genome: fitness_func(genome),
            reverse=True
            
        )
        
        if fitness_func(population[0]) >= fitness_limit:
            break
        
        next_generation = population[0:2]
        
        for j in range(int(len(population)/ 2) - 1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]
            
        population = next_generation
        
    population = sorted(
        population,
        key=lambda genome: fitness_func(genome),
        reverse=True 
        
    ) 
    
    return population, i

population, generations = run_evolution(
    populate_func=partial(
        generate_population, size=10, genome_length=len(things)
    ),
    
    fitness_func=partial(
        fitness, things=things, weight_limit=3000
        ),
    
    fitness_limit = 8.07,
    generation_limit=50
    )       
        

def genome_to_things(genome: Genome, things: [Thing]) -> [Thing]:
    result = []
    for i, thing in enumerate(things):
        if genome[i] == 1:
            result += [thing.name]
            
            
    return result 

print(f"number of generations: {generations}")
print(f"best solution: {genome_to_things(population[0], things)}")
            




    

    
   
    
   
    
   
    
   
    
   
    