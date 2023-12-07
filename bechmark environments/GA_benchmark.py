"""
Autonomous Robotic Systems Assignment 3
Author: Jelle Jansen, Elisha A. Nieuwburg
Date: 02-03-2021

GA_benchmark.py

Program that lets an evolutionary algorithm perform
on a Rosenbrock or Rastrigin benchmark.

"""

import evolutionary_algorithm as GA
import numpy as np
import time
import argparse
from plot import plot


def EA(f, benchmark):
    # Get the genetic algorithm.
    ga = GA.GeneticAlgorithm(50, 2, 0, False)

    generations = 100
    for gen in range(generations):
        
        # Plot the genomes on a benchmark contour plot.
        plot(ga.population, gen, f, benchmark)

        ga.update_fitness(f, 10)

        # Print the genome with the best fitness.
        best = ga.get_best_genome()
        print("[x, y] = [{:.4f},{:.4f}]. Fitness = {:.4f}".format(best.weights[0],\
            best.weights[1], best.fitness))

        # Make a new population for the next generation.
        ga.upgrade_population()


# Acquire EA variables from user.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Program for an Evolutionary Algorithm (EA)\
        displayed using a certain benchmark.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        'benchmark',
        choices=['rosenbrock', 'rastrigin'],
        type=str,
        help='The benchmark type.'
    )

    args = parser.parse_args()

    if args.benchmark == 'rosenbrock':
        a = 0
        b = 100
        f = lambda x, y: (a - x)**2 + b*(y - x**2)**2
    elif args.benchmark == 'rastrigin':
        f = lambda x, y: \
            20 + x**2 + y**2 - 10*(np.cos(2*np.pi*x) + np.cos(2*np.pi*y))
    else:
        raise TypeError(
            'This benchmark is not an option,\
            please choose either Rosenbrock or Rastrigin.'
        )

    # Perform the EA on given benchmark.
    EA(f, args.benchmark)


