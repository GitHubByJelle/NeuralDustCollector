"""
Autonomous Robotic Systems Assignment 4
Author: Jelle Jansen
Date: 09-03-2021

Simulation.py

Simulates a mobile robot moving in an evironment with possible obstacles.

"""

import pygame

from EA.ann import ANN
from EA.evolutionary_algorithm import Genome
from Simulation.visualization import Visualizer


# Simulate a non-automatic robot.
def simulate(robot, obstacles, visualize=True):
    # delta_t for calculations and visualizations
    delta_t = 1.0 / 7

    start_pause = True

    if visualize:
        # Set-up visualizations
        pygame.init()
        pygame.display.set_caption('Simulation Robot | ARS')

        width, height = robot.room_size
        win = pygame.display.set_mode((width, height))

        vis = Visualizer(win, robot, obstacles)
        vis.visualize()

        clock = pygame.time.Clock()

    running = True
    while running:
        if visualize:
            print(clock.tick())
            clock.tick(int(1 / delta_t))

        robot.move(delta_t)
        print(sum(sum(robot.dust)), len(robot.dust2), robot.dust3.size - sum(sum(robot.dust3)))

        if visualize:
            vis.visualize()

            # temporary, give a chance to start recording
            # if start_pause:
            #  start_pause = False
            #  time.sleep(10)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False


# Simulate the robot automatically using a neural network.
def simulate_auto(robot, obstacles, weights, bias, visualize=True, steps=1e6):
    # delta_t for calculations and visualizations
    delta_t = 1.0 / 7

    start_pause = False

    genome = Genome(len(weights), len(bias))
    genome.weights = weights
    genome.biases = bias

    NN = ANN(1)
    NN.weight_update(genome)

    if visualize:
        # Set-up visualizations
        pygame.init()
        pygame.display.set_caption('Simulation Robot | ARS')

        width, height = robot.room_size
        win = pygame.display.set_mode((width, height))

        vis = Visualizer(win, robot, obstacles)
        vis.visualize()

        clock = pygame.time.Clock()

    running = True
    for i in range(steps):
        if visualize:
            clock.tick(int(1 / delta_t))

        robot.determine_v(NN)

        robot.move(delta_t)

        if visualize:
            vis.visualize()

            # temporary, give a chance to start recording
            if start_pause:
                pygame.time.wait(1)
                start_pause = False

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
