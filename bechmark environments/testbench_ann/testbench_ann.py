
import numpy as np
import matplotlib.pyplot as plt

from ann import ANN

if __name__ == '__main__':

    print('########')
    print('## Start simulation')
    print('########')

    # Controller with 8 delays in pipeline
    ann_controller = ANN(8)

    # Check initialisation

    genome = ann_controller.get_genome()
    print('')
    print('genome:')
    print(genome)

    print('')
    print('W0, b0:')
    print(len(ann_controller.weights['W0']))
    print(len(ann_controller.weights['b0']))
    print('')
    print('W1, b1:')
    print(ann_controller.weights['W1'])
    print(ann_controller.weights['b1'])

    # Simulate ann-controller

    # New genome from EA to ANN

    genome = np.random.rand(1, 78) * 0.02 - 0.01
    genome = genome[0]
    print('')
    print('genome:')
    print(genome)
    ann_controller.weight_update(genome)
    print('')
    print('W0, b0:')
    print(ann_controller.weights['W0'])
    print(ann_controller.weights['b0'])
    print('')
    print('W1, b1:')
    print(ann_controller.weights['W1'])
    print(ann_controller.weights['b1'])

    # Sensor input

    X = np.random.rand(12, 1) * 300

    # ANN output

    # left wheel, right wheel
    Y = ann_controller.forward_propagation(X)
    print('')
    print('Y:')
    print(Y)

    # Sensor investigation
    A = 16.0
    alpha = 1.0/A
    tau = 40.0

    x_list = []
    y_list = []

    for d in range(300):
        s = ann_controller.sensor_convert(d, A, alpha, tau)
        x_list.append(d)
        y_list.append(s)

    plt.ylabel('s')
    plt.xlabel('d')
    plt.title('A = 16.0, alpha = 1.0/A, tau = 40.0')

    plt.plot(x_list, y_list)

    plt.savefig('sensor.png', dpi=None, facecolor='w', edgecolor='w',
                orientation='portrait', format=None,
                transparent=False, bbox_inches=None, pad_inches=0.1,
                metadata=None)
    # plt.show()
    plt.close()
