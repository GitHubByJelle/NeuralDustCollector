"""
Autonomous Robotic Systems Assignment 4
Author: Jelle Jansen
Date: 09-03-2021

Visualization.py

Visualizes a mobile robot collecting dust in an environment and
handles keyboard input using Pygame. Therefore the pygame
library must be imported and initialized.

"""

import numpy as np

import pygame
import operator


class Visualizer(object):
    def __init__(self, surface, robot, obstacles):
        # Initialise, robot, sensors, surface, sensors and obstacles
        self.surface = surface
        self.robot = robot
        self.obstacles = obstacles

        # Get width and height
        self.width, self.height = surface.get_size()

        # Default draw options
        self.sensor_lines = False
        self.sensor_numbers = True
        self.show_dust = True

        # Make font
        pygame.font.init()
        self.sensor_font = pygame.font.SysFont('Calibri', int(robot.r * 0.4))

    def visualize(self):
        # Make the visualization
        self.draw_background()
        self.draw_dust()
        self.draw_robot()
        self.draw_sensors()
        self.draw_obstacles()

        # Update the window
        pygame.display.update()

        # Handle new input
        self.handle_input()

    def draw_background(self):
        self.surface.fill((255, 255, 255))

    def draw_dust(self):
        if self.show_dust:
            # 1
            # for x in range(self.robot.dust.shape[0]):
            #     for y in range(self.robot.dust.shape[1]):
            #         if self.robot.dust[(x,y)]:
            #             self.surface.fill((130, 164, 228), (self.pygame_coords([x, y]), (1, 1)))
            # 2
            # for coord in self.robot.dust2:
            #     self.surface.fill((130, 164, 228), (self.pygame_coords(coord), (1, 1)))
            # 3
            for x in range(self.robot.dust3.shape[0]):
                for y in range(self.robot.dust3.shape[1]):
                    if self.robot.dust3[(x,y)]:
                        # self.surface.fill((130, 164, 228), (self.pygame_coords([x*self.robot.dust_dist,
                        #                                                         y*self.robot.dust_dist]),
                        #                                     (1, 1)))
                        pygame.draw.circle(self.surface, (130, 164, 228), self.pygame_coords([x*self.robot.dust_dist,
                                                                                y*self.robot.dust_dist]),1)

    def draw_robot(self):
        pygame.draw.circle(self.surface, (100, 149, 237), self.pygame_coords(self.robot.position), self.robot.r)

        pygame.draw.line(self.surface, (0, 0, 0), self.pygame_coords(self.robot.position),
                         self.pygame_coords(self.robot.position + \
                                            np.array([self.robot.r * np.cos(self.robot.theta), \
                                                      self.robot.r * np.sin(self.robot.theta)])))

        # Draw the speed of the wheels (as numbers)
        self.add_centered_text("{:.0f}".format(self.robot.vl),
                               self.pygame_coords(self.robot.position + np.array(
                                   [self.robot.r * .5 * np.cos(self.robot.theta + np.pi / 2),
                                    self.robot.r * .5 * np.sin(self.robot.theta + np.pi / 2)])))

        self.add_centered_text("{:.0f}".format(self.robot.vr),
                               self.pygame_coords(self.robot.position + np.array(
                                   [self.robot.r * .5 * np.cos(self.robot.theta - np.pi / 2),
                                    self.robot.r * .5 * np.sin(self.robot.theta - np.pi / 2)])))

    def draw_sensors(self):
        # For every sensor
        for sensor in self.robot.sensors:
            # Draw lines
            if self.sensor_lines:
                pygame.draw.line(self.surface, (0, 0, 0),
                                 self.pygame_coords(self.robot.position + np.array(
                                     [self.robot.r * np.cos(self.robot.theta + sensor.theta_offset),
                                      self.robot.r * np.sin(self.robot.theta + sensor.theta_offset)])),
                                 self.pygame_coords(self.robot.position + np.array(
                                     [(self.robot.r + sensor.d) * np.cos(self.robot.theta + sensor.theta_offset),
                                      (self.robot.r + sensor.d) * np.sin(self.robot.theta + sensor.theta_offset)])),
                                 2)

            # Draw numbers
            if self.sensor_numbers:
                self.add_centered_text("{:.0f}".format(sensor.d),
                                       self.pygame_coords(self.robot.position + np.array([(
                                            self.robot.r + self.robot.r * .4) * np.cos(
                                                self.robot.theta + sensor.theta_offset),
                                            (self.robot.r + self.robot.r * .4) * np.sin(
                                                self.robot.theta + sensor.theta_offset)])))

    def draw_obstacles(self):
        # For every obstacle
        for obstacle in self.obstacles:
            # Draw the obstacle
            if obstacle.sort == 'wall':
                pygame.draw.line(self.surface, (255, 0, 0), self.pygame_coords(obstacle.from_coords),
                                 self.pygame_coords(obstacle.to_coords), 4)

    # Convert normal coords to pygame coords (y-axes is mirrored)
    def pygame_coords(self, coords):
        return np.array([int(coords[0]), int(self.height - coords[1])])

    # Add text to image
    def add_centered_text(self, text, loc):
        text = self.sensor_font.render(text, False, (0, 0, 0))
        text_rect = text.get_rect(center=loc)
        self.surface.blit(text, text_rect)

    def handle_input(self):
        # Input
        keys = pygame.key.get_pressed()
        speed_modifier = .001

        for key in keys:
            # Speed input
            if keys[pygame.K_w]:
                if self.robot.vl < self.robot.v_max:
                    self.robot.vl += speed_modifier
            if keys[pygame.K_s]:
                if self.robot.vl > -self.robot.v_max:
                    self.robot.vl -= speed_modifier
            if keys[pygame.K_o]:
                if self.robot.vr < self.robot.v_max:
                    self.robot.vr += speed_modifier
            if keys[pygame.K_l]:
                if self.robot.vr > -self.robot.v_max:
                    self.robot.vr -= speed_modifier
            if keys[pygame.K_t]:
                if self.robot.vl < self.robot.v_max and self.robot.vr < self.robot.v_max:
                    self.robot.vl += speed_modifier
                    self.robot.vr += speed_modifier
            if keys[pygame.K_g]:
                if self.robot.vl > -self.robot.v_max and self.robot.vr > -self.robot.v_max:
                    self.robot.vl -= speed_modifier
                    self.robot.vr -= speed_modifier
            if keys[pygame.K_x]:
                self.robot.vl = 0
                self.robot.vr = 0

            # Visualization settings
            if keys[pygame.K_1]:
                self.sensor_lines = False
                self.sensor_numbers = True
            if keys[pygame.K_2]:
                self.sensor_lines = True
                self.sensor_numbers = False
            if keys[pygame.K_3]:
                self.show_dust = True
            if keys[pygame.K_4]:
                self.show_dust = False
