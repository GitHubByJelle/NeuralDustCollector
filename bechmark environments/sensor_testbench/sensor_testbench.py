
import sys, pygame, math

import shapely
from shapely.geometry import LineString, Point

from robot import Robot
from sensor import Sensor

def posint(pos):
  p0 = int(round(pos[0]))
  p1 = int(round(pos[1]))
  return (p0, p1)

pygame.init()

pygame.display.set_caption('Sensor testbench')

size = width, height = 320, 240

black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
yellow = 255, 255, 0

font = pygame.font.Font('freesansbold.ttf', 18)

# Display sensor readings
text0 = font.render('--', True, yellow, black)
text0Rect = text0.get_rect()
text0Rect.center = (64, 140)

text1 = font.render('--', True, yellow, black)
text1Rect = text0.get_rect()
text1Rect.center = (64, 160)

text2 = font.render('--', True, yellow, black)
text2Rect = text0.get_rect()
text2Rect.center = (64, 180)

text3 = font.render('--', True, yellow, black)
text3Rect = text0.get_rect()
text3Rect.center = (64, 200)

screen = pygame.display.set_mode(size)

delta_x = 0.04
twopi = 2*math.pi

# Initialize robot: position, theta, d
robot0 = Robot((160.0, 60.0), math.pi/2.0, 16)

################################################################################
#### Initialize sensors: max_d, theta_offset
################################################################################

nr_sensors = 4
sensor_list = []
for i0 in range(nr_sensors):
  sensor_list.append(Sensor(50, twopi*(1+2*i0)/(2*nr_sensors)))

################################################################################

# Static environment
obstacle_list = []

p0 = Point(50, 20)
p1 = Point(50, 220)
line0 = LineString([p0, p1])
obstacle_list.append(line0)

p0 = Point(270, 20)
p1 = Point(270, 220)
line0 = LineString([p0, p1])
obstacle_list.append(line0)

p0 = Point(50, 20)
p1 = Point(270, 20)
line0 = LineString([p0, p1])
obstacle_list.append(line0)

p0 = Point(50, 220)
p1 = Point(270, 220)
line0 = LineString([p0, p1])
obstacle_list.append(line0)

p0 = Point(50, 16)
p1 = Point(270, 16)
line0 = LineString([p0, p1])
obstacle_list.append(line0)
line0 = LineString([p0, p1])
obstacle_list.append(line0)

while 1:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()

  screen.fill(black)

  ## Static environment: draw
  for obstacle in obstacle_list:
    p0 = obstacle.coords[0]
    p1 = obstacle.coords[1]
    pygame.draw.line(screen, red, p0, p1, 1)

  # Robot: draw
  pygame.draw.circle(screen, blue, posint(robot0.position), robot0.d)
  pygame.draw.line(screen, red, robot0.position, [robot0.position[0]+robot0.d*math.cos(robot0.theta), robot0.position[1]-robot0.d*math.sin(robot0.theta)], 1)

  # Robot: update
  robot0.theta = (robot0.theta+twopi/15000.0)%twopi
  if robot0.position[0]>=270-robot0.d:
    delta_x = -delta_x
  elif robot0.position[0]<=50+robot0.d:
    delta_x = -delta_x
  x0 = robot0.position[0]+delta_x
  robot0.position = (x0, robot0.position[1])

################################################################################
#### Sensor
################################################################################

  for sensor in sensor_list:
    sensor.calculate_distance(robot0.position, robot0.d, robot0.theta, obstacle_list)
    sensor.draw_ray(screen, robot0.position)

################################################################################

  # Visualize sensor d
  text0 = font.render('d0: '+str(round(sensor_list[0].d, 1)), True, yellow, black)
  screen.blit(text0, text0Rect)
  text1 = font.render('d1: '+str(round(sensor_list[1].d, 1)), True, yellow, black)
  screen.blit(text1, text1Rect)
  text2 = font.render('d2: '+str(round(sensor_list[2].d, 1)), True, yellow, black)
  screen.blit(text2, text2Rect)
  text3 = font.render('d3: '+str(round(sensor_list[3].d, 1)), True, yellow, black)
  screen.blit(text3, text3Rect)

  pygame.display.flip()
