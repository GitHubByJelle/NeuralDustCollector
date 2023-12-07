"""
Autonomous Robotic Systems Assignment 4
Author: Jelle Jansen, Elisha A. Nieuwburg
Date: 09-03-2021

Evolutionary_algorithm.py

A file with an evolutionary algorithm class and a fitting genome class.

"""

import random
import numpy as np
import copy

class Genome():
    def __init__(self, num_weights, num_biases):
        # Create random initial weights and biases.
        self.fitness = 0
        self.weights = np.random.uniform(-1.0, 1.0, num_weights).tolist()
        self.biases = np.random.uniform(-1.0, 1.0, num_biases).tolist()

    def mutate(self):
        # Determine randomly which weights are mutated by adding a
        # random float number to it.
        mutate_rate = .05
        for i in range(len(self.weights)):
            if random.random() < mutate_rate:
                self.weights[i] += random.uniform(-.25, .25)

        for i in range(len(self.biases)):
            if random.random() < mutate_rate:
                self.biases[i] += random.uniform(-.25, .25)

class GeneticAlgorithm():
    def __init__(self, population_size, num_weights, num_biases, maximize = True):
        self.population = [Genome(num_weights, num_biases) for _ in range(population_size)]
        self.population_size = population_size
        self.num_weights = num_weights
        self.num_biases = num_biases
        self.reverse = maximize

    def tournament_selection(self):
        # Choose random pool of candidates.
        nr_candidates = 3
        candidates = random.choices(self.population, k=nr_candidates)
        candidates.sort(key=lambda x: x.fitness, reverse=self.reverse)

        # Return the candidate with the highest fitness.
        return candidates[0]

    def crossover(self, genome1, genome2):
        # Choose randomly the order of genomes.
        cross_over_rate = .9
        if random.random() < .5:
            genomes = [genome1, genome2]
        else:
            genomes = [genome2, genome1]

        # Create with crossover rate a new genome by mixing two genomes.
        if random.random() < cross_over_rate:
            weight_index = random.randint(0, len(genome1.weights))
            bias_index = random.randint(0, len(genome1.biases))

            new_genome = Genome(self.num_weights, self.num_biases)
            new_genome.weights = genomes[0].weights[:weight_index] + genomes[1].weights[weight_index:]
            new_genome.biases = genomes[0].biases[:bias_index] + genomes[1].biases[bias_index:]

            return new_genome

        # Else return only genome1 or genome2.
        else:
            return copy.deepcopy(genomes[0])

    # Update fitness of genome based on a benchmarks function.
    def update_fitness_bench(self, function, mult = 3):
        for genome in self.population:
            genome.fitness = function(genome.weights[0] * mult, genome.weights[1] * mult)

    # Update fitness of genome based on robots performance.
    def update_fitness(self, dust_lst1, dust_lst2, collision_lst1, collision_lst2):
        for i in range(len(dust_lst1)):
            self.population[i].fitness = 2*(dust_lst1[i].size - np.sum(dust_lst1[i])) + \
                                         (dust_lst2[i].size - np.sum(dust_lst2[i])) + \
                                         - collision_lst1[i] - 2*collision_lst2[i]

    def upgrade_population(self):
        self.population.sort(key=lambda x: x.fitness, reverse=self.reverse)

        # Elitism, keep best genomes
        new_genomes = [None] * self.population_size
        new_genomes[0] = self.population[0]
        new_genomes[1] = self.population[1]
        new_genomes[2] = self.population[2]
        new_genomes[3] = self.population[3]
        new_genomes[4] = self.crossover(self.population[0], self.population[1])
        new_genomes[5] = self.crossover(self.population[0], self.population[2])
        new_genomes[6] = self.crossover(self.population[0], self.population[3])
        new_genomes[7] = self.crossover(self.population[1], self.population[2])
        new_genomes[8] = self.crossover(self.population[1], self.population[3])
        new_genomes[9] = self.crossover(self.population[2], self.population[3])

        # Take all the other ones based on tournament selection
        for i in range(10, self.population_size):
            genome1 = self.tournament_selection()
            genome2 = self.tournament_selection()
            new_genomes[i] = self.crossover(genome1, genome2)

        # Mutate them all except the first one
        for i in range(1,self.population_size):
            new_genomes[i].mutate()

        # Save the new genomes
        self.population = new_genomes

        # Reset the fitness
        for genome in self.population:
            genome.fitness = 0

    # Return best fitness and average fitness.
    def get_best_average(self, gen, map, print_best=False):
        self.population.sort(key=lambda x: x.fitness, reverse=self.reverse)

        # Print necessary information if print_best is True.
        if print_best:
            print("Generation: {} on map {}, best fitness: {}".format(gen, map, self.population[0].fitness))
            print("Weight:\n{}".format(self.population[0].weights))
            print("Bias:\n{}\n".format(self.population[0].biases))

        
        fitnesses = [genome.fitness for genome in self.population]
        avg = sum(fitnesses) / len(fitnesses)

        return [self.population[0].fitness, avg]

    # Compute diversity of the population using Euclidean distance.
    def compute_diversity(self):
        d = 0
        for i in range(self.population_size):
            for j in range(i, self.population_size):
                genome1 = self.population[i]
                genome2 = self.population[j]
                d += np.linalg.norm(np.array(genome1.weights) - np.array(genome2.weights))
        
        return d
