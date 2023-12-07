"""
Autonomous Robotic Systems Assignment 4
Author: Elisha A. Nieuwburg, Jelle Jansen
Date: 09-03-2021

Robot.py

Robot class that defines a differential drive robot with a sensor option.
The robot collects dust.

"""

import numpy as np
from shapely.geometry import LineString, Point
from Robot.sensor import Sensor

class Robot(object):

    def __init__(self, position, theta, v_max, l, r, offset_sensors, obstacles, vl, vr, room_size, max_a):
        # initialise parameters
        self.position = position
        self.vl = vl
        self.vr = vr
        self.l = l
        self.v_max = v_max
        self.max_a = max_a

        self.theta = theta
        self.r = r
        self.obstacles = obstacles

        # Make sensors
        self.sensors = [Sensor(300, offset) for offset in offset_sensors]

        # Make rotation matrix for movement
        self.rot_mat = [position[0], position[1], theta]

        # Make dust matrix (for fitness)
        self.room_size = room_size
        self.dust = np.zeros(room_size)
        self.dust2 = set()
        self.dust_dist = 25
        self.dust3 = np.ones([int(np.ceil(room_size[0] / self.dust_dist)),
                              int(np.ceil(room_size[0] / self.dust_dist))])
        self.collision_par = 0
        self.update_dust()

    def update_sensors(self):
        # Update all sensors
        for sensor in self.sensors:
            sensor.calculate_distance(self.position, self.r, self.theta, self.obstacles)

    def collision_handling(self, next_pos):
        # Make point for start position
        p0 = Point(self.position[0], self.position[1])

        # Look at all obstacles
        for obstacle in self.obstacles:
            # Look at next point, make a line for the step, and a line for the obstacle (wall)
            p1 = Point(next_pos[0], next_pos[1])
            line_step = LineString([p0, p1])
            line_obstacle = LineString([obstacle.from_coords, obstacle.to_coords])

            # Check distance to obstacle and intersection with obstacle
            int_pt = line_step.intersection(line_obstacle)
            distance_obstacle = line_obstacle.distance(p1)

            # Check if line is exactly on the obstacle. If yes, make a parallel line and place robot on parallel line
            if distance_obstacle == 0:
                # Get new position
                next_pos = self.get_pos_parallel(p0, p1, line_obstacle, next_pos)

                self.collision_par += 1

            # Check if the robot stepped over / crosses an obstacle. If yes, calculate closest point to to obstacle,
            # and place the robot next to the closest point (on the correct side, taking the radius into account)
            elif int_pt:
                closest_point = line_obstacle.interpolate(line_obstacle.project(p1))

                # Calculate new position
                next_pos = [p1.x + (distance_obstacle + self.r) / distance_obstacle * (closest_point.x - p1.x),
                            p1.y + (distance_obstacle + self.r) / distance_obstacle * (closest_point.y - p1.y),
                            next_pos[2]]

                self.collision_par += 1

            # Check if the robot is to close the an obstacle (checking it's radius). If yes, calculate the closest point,
            # and place the robot on the correct position (by taking it's radius into account).
            elif distance_obstacle < self.r:
                closest_point = line_obstacle.interpolate(line_obstacle.project(p1))

                # Calculate new position
                next_pos = [closest_point.x + self.r / distance_obstacle * (p1.x - closest_point.x),
                            closest_point.y + self.r / distance_obstacle * (p1.y - closest_point.y),
                            next_pos[2]]

                self.collision_par += 1

        return next_pos

    def get_pos_parallel(self, p0, p1, line_obstacle, next_pos):
        # Make a parallel line to the obstacle
        line_parallel = line_obstacle.parallel_offset(self.r, 'right')

        # Change line if placed on the wrong side
        if p0.distance(line_parallel) > p0.distance(line_obstacle):
            line_parallel = line_obstacle.parallel_offset(self.r, 'left')

        # Calculate point that's closest on the parallel line (for the next step)
        par_point = line_parallel.interpolate(line_parallel.project(p1))
        next_pos = [par_point.x, par_point.y, next_pos[2]]

        return next_pos

    def move(self, delta_t):
        # Go straight forward if the motor speeds of the wheels are equal.
        if self.vr == self.vl:
            est_position = np.array([self.position[0] + self.vl * np.cos(self.theta) * delta_t,
                                     self.position[1] + self.vl * np.sin(self.theta) * delta_t, self.theta])

        else:
            R = (self.l / 2) * ((self.vr + self.vl) / (self.vr - self.vl))
            omega = (self.vr - self.vl) / self.l

            ICC = [self.position[0] - R * np.sin(self.theta), self.position[1] + R * np.cos(self.theta)]
            est_position = np.array([[np.cos(omega * delta_t), -np.sin(omega * delta_t), 0],
                                     [np.sin(omega * delta_t), np.cos(omega * delta_t), 0], [0, 0, 1]]).dot(
                np.array([self.position[0] - ICC[0], self.position[1] - ICC[1], self.theta])) + \
                           np.array([ICC[0], ICC[1], omega * delta_t])

        # Check twice for a possible collision.
        # We have toch check twice to prevent that the robot gets placed inside an obstacle that's already checked
        est_position = self.collision_handling(est_position)
        est_position = self.collision_handling(est_position)

        # Make the actual move
        self.position = [est_position[0], est_position[1]]

        # Change theta and rotation matrix
        self.theta = est_position[2]
        self.rot_mat = est_position

        # Update sensors
        self.update_sensors()

        # Update dust (for fitness)
        self.update_dust()

    def determine_v(self, NN):
        # Update sensor list and NN.
        d_sensors = np.array([sensor.d for sensor in self.sensors])
        new_velocity = NN.forward_propagation(d_sensors)

        self.vl = float(new_velocity[0]) * self.v_max
        self.vr = float(new_velocity[1]) * self.v_max

    # Update dust in new position.
    def update_dust(self):
        for x in range(self.dust3.shape[0]):
            for y in range(self.dust3.shape[1]):
                if np.linalg.norm((self.position[0] - x*self.dust_dist,
                                   self.position[1] - y*self.dust_dist)) < self.r:
                    self.dust3[x, y] = 0

    # Compute fitness based on dust.
    def calculate_fitness(self):
        return self.dust3.size - np.sum(self.dust3)

