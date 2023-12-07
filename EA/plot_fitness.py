"""
Autonomous Robotic Systems Assignment 4
Author: Elisha A. Nieuwburg
Date: 09-03-2021

Plot_fitness.py

Plots the maximum and average fitnesses of the EA.
Plots the diversity of the EA.

"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

def plotting(fitnesses, diversity, generations): 

    x = np.arange(0, generations, 1)
    error = np.std([fitness[0] for fitness in fitnesses])
    print(error)

    # Plot the maximum and average fitnesses of each generation.
    plt.figure(figsize=(12, 7))
    plt.plot(x, [fitness[1] for fitness in fitnesses], label='Average fitness')
    plt.plot(x, [fitness[0] for fitness in fitnesses], label='Maximum fitness')
    plt.ylabel('fitness')
    plt.xlabel('generations')
    plt.legend(loc="upper left")

    plt.savefig('Fitness.png',
                format='png',
                dpi=100,
                bbox_inches='tight')

    # Plot the diversity and the maximum fitness of each generation.
    fig,ax = plt.subplots()
    ax.plot(x, diversity, label='Diversity', color="red")
    ax.set_xlabel("Generations")
    ax.set_ylabel("Diversity", color="red")
    ax.set_ylim(0, 1000)

    ax2=ax.twinx()
    ax2.plot(x, [fitness[0] for fitness in fitnesses], label='Maximum fitness', color="blue")
    ax2.set_ylabel("Maximum fitness",color="blue")

    fig.savefig('Diversity.png',
                format='png',
                dpi=100,
                bbox_inches='tight')
