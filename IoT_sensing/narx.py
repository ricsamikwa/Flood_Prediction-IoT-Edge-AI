import math
import numpy as np
import matplotlib.pylab as plt
from pyneurgen.neuralnet import NeuralNet
from pyneurgen.recurrent import NARXRecurrent


def plot_results(x, y, y_true):
    plt.subplot(3, 1, 1)
    plt.plot([i[1] for i in population])
    plt.title("Population")
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(x, y, 'bo', label='targets')
    plt.plot(x, y_true, 'ro', label='actuals')
    plt.grid(True)
    plt.legend(loc='lower left', numpoints=1)
    plt.title("Test Target Points vs Actual Points")

    plt.subplot(3, 1, 3)
    plt.plot(list(range(1, len(net.accum_mse) + 1, 1)), net.accum_mse)
    plt.xlabel('epochs')
    plt.ylabel('mean squared error')
    plt.grid(True)
    plt.title("Mean Squared Error by Epoch")
    plt.show()

def generate_data():
    # all samples are drawn from this population
    pop_len = 200
    factor = 1.0 / float(pop_len)
    population = [[i, math.sin(float(i) * factor * 10.0)] for i in range(pop_len)]
    population_shuffle = population[:]

    all_inputs = []
    all_targets = []

    np.random.shuffle(population_shuffle)
    for position, target in population_shuffle:
        all_inputs.append([position * factor])
        all_targets.append([target])
        # print(all_inputs[-1], all_targets[-1])
    return population, all_inputs, all_targets 

# generate data
population, all_inputs, all_targets =  generate_data()

# NARXRecurrent
input_nodes, hidden_nodes, output_nodes = 1, 10, 1
output_order, incoming_weight_from_output = 3, .6
input_order, incoming_weight_from_input = 2, .4

# init neural network
net = NeuralNet()
net.init_layers(input_nodes, [hidden_nodes], output_nodes,
                NARXRecurrent(output_order, incoming_weight_from_output, 
                              input_order, incoming_weight_from_input))
net.randomize_network()
net.set_halt_on_extremes(True)

# set constrains and rates
net.set_random_constraint(.5)
net.set_learnrate(.1)

# set inputs and outputs
net.set_all_inputs(all_inputs)
net.set_all_targets(all_targets)

# set lengths
length = len(all_inputs)
learn_end_point = int(length * .8)

# set ranges
net.set_learn_range(0, learn_end_point)
net.set_test_range(learn_end_point + 1, length - 1)

# add activation to layer 1
net.layers[1].set_activation_type('tanh')

# fit data to model
net.learn(epochs=150, show_epoch_results=True, random_testing=False)

# define mean squared error
mse = net.test()
print("Testing mse = ", mse)

# define data
x = [item[0][0] * 200.0 for item in net.get_test_data()]
y = [item[0][0] for item in net.test_targets_activations]
y_true = [item[1][0] for item in net.test_targets_activations]

# plot results
plot_results(x, y, y_true)
