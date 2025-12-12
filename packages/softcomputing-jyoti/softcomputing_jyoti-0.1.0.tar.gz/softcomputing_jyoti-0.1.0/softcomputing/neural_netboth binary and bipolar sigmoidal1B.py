import numpy as np

# Define activation functions
def binary_sigmoid(x):
    return 1 / (1 + np.exp(-x))

def bipolar_sigmoid(x):
    return (2 / (1 + np.exp(-x))) - 1

# Function to calculate neural network output
def calculate_neural_net_output(inputs, weights, biases, activation_function):
    # Compute the net input to the neurons
    net_input = np.dot(inputs, weights) + biases
    # Apply the activation function
    return activation_function(net_input)

# Example usage
if __name__ == "__main__":
    # Define inputs, weights, and biases
    inputs = np.array([0.5, -0.2, 0.1])
    weights = np.array([
        [0.4, 0.3, 0.5],
        [-0.3, 0.8, -0.6]
    ]).T  # Transpose to match dimensions
    biases = np.array([0.1, -0.1])

    # Calculate outputs using binary sigmoid
    binary_output = calculate_neural_net_output(inputs, weights, biases, binary_sigmoid)
    print("Binary Sigmoid Output:", binary_output)

    # Calculate outputs using bipolar sigmoid
    bipolar_output = calculate_neural_net_output(inputs, weights, biases, bipolar_sigmoid)
    print("Bipolar Sigmoid Output:", bipolar_output)
