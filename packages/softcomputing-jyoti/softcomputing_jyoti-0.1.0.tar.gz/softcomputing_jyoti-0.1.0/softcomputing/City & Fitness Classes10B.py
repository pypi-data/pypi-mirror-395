# PRACTICAL 10B
# City & Fitness Classes using Genetic Algorithm

import numpy as np

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, other):
        return np.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __repr__(self):
        return f"City({self.x}, {self.y})"

class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness = 0

    def calculate_distance(self):
        if self.distance == 0:
            d = 0
            for i in range(len(self.route)):
                a = self.route[i]
                b = self.route[(i+1) % len(self.route)]
                d += a.distance_to(b)
            self.distance = d
        return self.distance

    def calculate_fitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.calculate_distance())
        return self.fitness

if __name__ == "__main__":
    city1 = City(0, 0)
    city2 = City(3, 4)
    city3 = City(6, 0)

    route = [city1, city2, city3]

    fit = Fitness(route)
    print("Route:", route)
    print("Total Distance:", fit.calculate_distance())
    print("Fitness Score:", fit.calculate_fitness())
