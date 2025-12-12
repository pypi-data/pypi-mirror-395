# PRACTICAL 10A
# Simple Genetic Algorithm

import random

POPULATION_SIZE = 100
GENES = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890, .-;:_!"#%&/()=?@${[]}'''
TARGET = "I love GeeksforGeeks"

class Individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.cal_fitness()

    @classmethod
    def mutated_genes(cls):
        return random.choice(GENES)

    @classmethod
    def create_gnome(cls):
        return [cls.mutated_genes() for _ in range(len(TARGET))]

    def mate(self, par2):
        child = []
        for g1, g2 in zip(self.chromosome, par2.chromosome):
            prob = random.random()
            if prob < 0.45:
                child.append(g1)
            elif prob < 0.90:
                child.append(g2)
            else:
                child.append(self.mutated_genes())
        return Individual(child)

    def cal_fitness(self):
        return sum(gs != gt for gs, gt in zip(self.chromosome, TARGET))


def main():
    generation = 1
    population = [Individual(Individual.create_gnome()) for _ in range(POPULATION_SIZE)]

    while True:
        population = sorted(population, key=lambda x: x.fitness)

        if population[0].fitness == 0:
            break

        new_gen = []
        s = int(0.1 * POPULATION_SIZE)
        new_gen.extend(population[:s])

        s = int(0.9 * POPULATION_SIZE)
        for _ in range(s):
            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])
            new_gen.append(parent1.mate(parent2))

        population = new_gen

        print(f"Generation: {generation}  String: {''.join(population[0].chromosome)}  Fitness: {population[0].fitness}")
        generation += 1

    print(f"\nFinal Generation: {generation}")
    print("Evolved String:", ''.join(population[0].chromosome))
    print("Fitness:", population[0].fitness)

if __name__ == "__main__":
    main()
