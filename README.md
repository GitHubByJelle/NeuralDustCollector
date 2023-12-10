# NeuralDustCollector: Using Neural Networks and a Genetic Algorithm to vacuum
This project is part of an group assignment for the course Autonomous Robotic Systems for my Master's in Artificial Intelligence. The project contains an implementation of a circular vacuum cleaner robot trying to clean dust as fast as possible. The robot contains 12 sensors which measure the distance to the closest wall. Based on the distance of all these sensors, the robot determines the velocity of its right and left wheel using our own implemented (Recurrent) Neural Network (RNN). The RNN is trained using our own implemented Genetic Algorithm. The robot with the trained weights is visualised using pygame.

<p align="center" width="100%">
    <img src="images\neural-dust-collector.gif" alt="Visualisation of the NEAT algorithm collecting data for training" width="70%">
</p>

## Implementation Details
For AI functionality, the code leverages the following techniques/algorithms:
* Neural Networks
* Genetic Algorithms

Everything major is implemented ourselfs, including circular robot movement, obstacles, collision detections, etc.

The robot implementation utilized in this project is closely tied to the one employed in my other project, '[Robot-Localization-Analysis](https://github.com/GitHubByJelle/Robot-Localization-Analysis).'

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