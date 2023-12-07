"""
Autonomous Robotic Systems Assignment 4
Author: Sacha L. Sindorf
Date: 09-03-2021

ANN.py

ANN class that defines an artificial neural network.

"""

import numpy as np


class ANN():
    def __init__(self, delay):
        # Create random initial weights.
        W0 = np.random.rand(4, 16) * 0.02 - 0.01
        b0 = np.random.rand(4, 1) * 0.02 - 0.01

        W1 = np.random.rand(2, 4) * 0.02 - 0.01
        b1 = np.random.rand(2, 1) * 0.02 - 0.01

        self.weights = {'W0': W0, 'b0': b0, 'W1': W1, 'b1': b1}

        self.delay = delay

        self.pipeline = np.zeros((self.delay, 4, 1))
        self.rd_addr = 0
        self.wr_addr = delay-1  # pipeline distance

        self.A = 16.0
        self.alpha = 1.0/self.A
        self.tau = 40.0

    # Update weights and biases to the genome weights and biases. 
    def weight_update(self, genome):
        W0 = np.array([genome.weights[0:64]]).reshape(4, 16)
        W1 = np.array([genome.weights[64:72]]).reshape(2, 4)
        b0 = np.array([genome.biases[0:4]]).reshape(4, 1)
        b1 = np.array([genome.biases[4:6]]).reshape(2, 1)
        self.weights = {'W0': W0, 'b0': b0, 'W1': W1, 'b1': b1}

    # Convert sensor distance to measurement value.
    def sensor_convert(self, d, A, alpha, tau):
        return A+(A*alpha-A)*(1-np.exp(-d/tau))

    def forward_propagation(self, X):
        # Recursion read.
        R = self.pipeline[self.rd_addr]
        self.rd_addr = (self.rd_addr + 1) % self.delay

        # A closer distance to an obstacle is more alarming.
        S = self.sensor_convert(X, self.A, self.alpha, self.tau)

        # Append recursion to input.
        XR = np.append(S, R).reshape(16, 1)

        # Create network.
        Z0 = np.dot(self.weights['W0'], XR) + self.weights['b0']
        A0 = np.tanh(Z0)
        Z1 = np.dot(self.weights['W1'], A0) + self.weights['b1']
        A1 = np.tanh(Z1)

        # Recursion write.
        self.pipeline[self.wr_addr] = A0
        self.wr_addr = (self.wr_addr+1) % self.delay

        return A1
