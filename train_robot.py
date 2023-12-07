"""
Autonomous Robotic Systems Assignment 4
Author: Jelle Jansen, Elisha A. Nieuwburg
Date: 09-03-2021

Train_robot.py

Trains the neural network of a mobile robot that uses the NN to
control its movement. The NN is optimized using an
evolutionary algorithm.

"""

from Robot.robot import Robot
from Robot.obstacle import Obstacle
from EA import evolutionary_algorithm as GA
from EA.ann import ANN
from EA.plot_fitness import plotting
import random
import numpy as np

# Create environment.
obstacles1 = [Obstacle([125, 75, 625, 75], 'wall'),
              Obstacle([625, 75, 625, 345], 'wall'),
              Obstacle([625, 345, 125, 345], 'wall'),
              Obstacle([125, 345, 125, 75], 'wall')]
obstacles2 = [Obstacle([100, 50, 650, 50], 'wall'),
              Obstacle([650, 50, 650, 370], 'wall'),
              Obstacle([650, 370, 100, 370], 'wall'),
              Obstacle([100, 370, 100, 50], 'wall'),
              Obstacle([180, 130, 570, 130], 'wall'),
              Obstacle([570, 130, 570, 290], 'wall'),
              Obstacle([570, 290, 180, 290], 'wall'),
              Obstacle([180, 290, 180, 130], 'wall')]
obstacles3 = [Obstacle([100, 50, 650, 100], 'wall'),
              Obstacle([650, 100, 650, 320], 'wall'),
              Obstacle([650, 320, 100, 370], 'wall'),
              Obstacle([100, 370, 100, 50], 'wall'),
              Obstacle([230, 130, 520, 180], 'wall'),
              Obstacle([520, 180, 520, 240], 'wall'),
              Obstacle([520, 240, 230, 290], 'wall'),
              Obstacle([230, 290, 230, 130], 'wall')]
obstacles4 = [Obstacle([50, 50, 650, 50], 'wall'),
              Obstacle([650, 50, 650, 200], 'wall'),
              Obstacle([650, 200, 400, 200], 'wall'),
              Obstacle([400, 200, 400, 250], 'wall'),
              Obstacle([400, 250, 650, 300], 'wall'),
              Obstacle([650, 300, 650, 370], 'wall'),
              Obstacle([650, 370, 50, 370], 'wall'),
              Obstacle([50, 370, 50, 300], 'wall'),
              Obstacle([50, 370, 50, 300], 'wall'),
              Obstacle([50, 300, 300, 250], 'wall'),
              Obstacle([300, 250, 300, 200], 'wall'),
              Obstacle([300, 200, 50, 200], 'wall'),
              Obstacle([50, 200, 50, 50], 'wall')]
obstacles5 = [Obstacle([100, 50, 650, 50], 'wall'),
              Obstacle([650, 50, 650, 370], 'wall'),
              Obstacle([650, 370, 100, 370], 'wall'),
              Obstacle([100, 370, 100, 50], 'wall'),
              Obstacle([450, 160, 570, 160], 'wall'),
              Obstacle([570, 160, 570, 240], 'wall'),
              Obstacle([570, 240, 450, 240], 'wall'),
              Obstacle([450, 240, 450, 160], 'wall'),
              Obstacle([100, 80, 120, 80], 'wall'),
              Obstacle([120, 80, 120, 140], 'wall'),
              Obstacle([120, 140, 100, 140], 'wall'),
              Obstacle([100, 140, 100, 80], 'wall'),
              Obstacle([200, 70, 250, 70], 'wall'),
              Obstacle([250, 70, 250, 150], 'wall'),
              Obstacle([250, 150, 200, 150], 'wall'),
              Obstacle([200, 150, 200, 70], 'wall')]
obstacles_lst = [obstacles1, obstacles2, obstacles3, obstacles4, obstacles5]
start_pos = [[200, 200], [610, 250], [200, 300], [150, 125], [610, 250]]

# Initialize the evolutionary algorithm and standard sensor settings.
ga = GA.GeneticAlgorithm(16, 72, 6)
nr_sensors = 12
offset_sensors = [(2 * np.pi * i0) / nr_sensors for i0 in range(nr_sensors)]

delta_t = 1.0 / 7

fitnesses, diversity = [], []
generations = 2
steps = 200

print("-----Started Training-----")

for gen in range(generations):
    # For each genome, create a robot and NN.
    # Control movement by updating the NN using the sensors output.
    dust_list1 = []
    coll_lst1 = []
    dust_list2 = []
    coll_lst2 = []

    # Select a random map (whole generations gets the same map)
    # map = random.randint(0, len(obstacles_lst)-1)
    for genome in ga.population:

        # Create NN with the genome weights and biases.
        NN = ANN(2)
        NN.weight_update(genome)

        # Robot neutral start position.
        map = 0
        robot = Robot(start_pos[map], np.pi / 2, 100, 50, 30, offset_sensors, obstacles_lst[map], 0, 0, (750, 420), 2)

        # For 100 timesteps, update NN and move robot accordingly.
        for _ in range(steps):
            robot.determine_v(NN)

            robot.move(delta_t)

        dust_list1.append(robot.dust3)
        coll_lst1.append(robot.collision_par)

        # Robot neutral start position.
        map = 2
        robot = Robot(start_pos[map], np.pi / 2, 100, 50, 30, offset_sensors, obstacles_lst[map], 0, 0, (750, 420), 2)

        # For 100 timesteps, update NN and move robot accordingly.
        for _ in range(steps):
            robot.determine_v(NN)

            robot.move(delta_t)

        dust_list2.append(robot.dust3)
        coll_lst2.append(robot.collision_par)

    # Update fitness of each genome in the population.
    ga.update_fitness(dust_list1, dust_list2, coll_lst1, coll_lst2)

    # Keep track of the best fitness, average fitness and diversity.
    info = ga.get_best_average(gen, map, print_best=True)
    fitnesses.append(info)
    diversity.append(ga.compute_diversity())

    # Make new population for the next generation.
    ga.upgrade_population()

# Plot the fitnesses and diversity.
plotting(fitnesses, diversity, generations)
