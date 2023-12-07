import sys, pygame, math

import shapely
from shapely.geometry import LineString, Point

class Sensor():

  def __init__(self, max_d, theta_offset):
    self.max_d = max_d
    self.theta_offset = theta_offset
    self.d = max_d
    self.p_isect = (0.0, 0.0)

  def calculate_distance(self, robot_position, robot_d, robot_theta, obstacle_list):

    d_ray = robot_d + self.max_d
    x1 = robot_position[0]+d_ray*math.cos(robot_theta+self.theta_offset)
    y1 = robot_position[1]-d_ray*math.sin(robot_theta+self.theta_offset)

    # line in shapely
    p0 = Point(robot_position[0], robot_position[1])
    p1 = Point(x1, y1)
    line_sensor = LineString([p0, p1])

    # Detect
    self.d = self.max_d
    self.p_isect = (x1, y1)
    for obstacle in obstacle_list:
      int_pt = line_sensor.intersection(obstacle)
      if int_pt:
        # distance to obstacle
        d0 = p0.distance(int_pt)-robot_d
        print(d0)
        # store minimum distance
        if d0<self.d:
          self.d = d0
          self.p_isect = (int_pt.x, int_pt.y)

  def draw_ray(self, screen, robot_position):
    pygame.draw.line(screen, (0, 255, 0), robot_position, self.p_isect, 1)
