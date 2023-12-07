"""
Autonomous Robotic Systems Assignment 2
Author: Sacha L. Sindorf
Date: 23-02-2021

Sensor.py

Sensor class that defines an infrared distance sensor.

"""

import math
from shapely.geometry import LineString, Point


class Sensor:
    def __init__(self, max_d, theta_offset):
        self.max_d = max_d  # Maximal reach
        self.theta_offset = theta_offset  # Angle with Robot's face-forward direction
        self.d = max_d  # Measured distance
        self.p_isect = (0.0, 0.0)  # Measured location for visualisation or debugging

    def calculate_distance(self, robot_position, robot_d, robot_theta, obstacle_list):

        # - robot_position: robot center position
        # - robot_d: robot radius
        # - robot_theta: angle between robot facing forward and positive x-axis, counter-clockwise
        # - obstacle_list: list of shapely lines presenting obstactles

        # Assume sensor is placed on robot exterior circle, facing outward.
        # Line of sight starts from robot center plus the sensors maximal distance
        d_ray = robot_d + self.max_d
        x1 = robot_position[0] + d_ray * math.cos(robot_theta + self.theta_offset)
        y1 = robot_position[1] + d_ray * math.sin(robot_theta + self.theta_offset)

        # line in shapely
        p0 = Point(robot_position[0], robot_position[1])
        p1 = Point(x1, y1)
        line_sensor = LineString([p0, p1])

        # Detect
        self.d = self.max_d  # to find minimal detected distance, start with maximal
        self.p_isect = (x1, y1)  # maximal possible intersection point
        for obstacle in obstacle_list:
            # Intersection with obstacle
            # Assume that robot interior does not contain obstacle. (line starts from center)
            int_pt = line_sensor.intersection(LineString([obstacle.from_coords, obstacle.to_coords]))
            if int_pt:
                # Distance to obstacle.
                # Distance is measured from robot exterior, where this sensor is located.
                # Distance is zero means sensor is directed towards obstacle and robot is touching this
                # obstacle.
                d0 = p0.distance(int_pt) - robot_d
                # store minimum distance
                if d0 < self.d:
                    self.d = d0
                    self.p_isect = (int_pt.x, int_pt.y)
