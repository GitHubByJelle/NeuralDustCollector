# Using Neural Networks and a Genetic Algorithm to vacuum
This project is part of an group assignment for the course Autonomous Robotic Systems for my Master's in Artificial Intelligence. The project contains an implementation of a simulated vacuum cleaner robot trying to remove dust, as fast as possible. The robot contains 8 sensors which measure the distance to the closest wall. Based on the distance of all these sensors, the robot makes its decisions by using a our own implemented (Recurrent) Neural Network (RNN). The RNN is trained using our own implemented Genetic Algorithm. The robot with the trained weights is visualised using pygame.

## Implementation Details
The code is written in Python and relies on the following packages:
* pygame
* numpy

For AI functionality, the code leverages the following techniques/algorithms:
* Neural Networks
* Genetic Algorithms

Everything major is implemented ourselfs, including circular robot movement, obstacles, collision detections, etc.

## How to use
First install the requirements.txt
```bash
pip install -r requirements.txt
```

To train the robots without visualisation run `train_robot.py`
```bash
python train_robot.py
```

To visualise the robot run `visualise_simulation.py`
```bash
python visualise_simulation.py
```