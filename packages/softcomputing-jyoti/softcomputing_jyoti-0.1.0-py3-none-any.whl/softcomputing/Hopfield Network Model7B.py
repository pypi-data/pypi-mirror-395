# PRACTICAL 7B
# Hopfield Network Model — Associative Memory

from neurodynex.hopfield_network import network, pattern_tools, plot_tools
import numpy as np

pattern_size = 5
hopfield_net = network.HopfieldNetwork(nr_neurons=pattern_size**2)

factory = pattern_tools.PatternFactory(pattern_size, pattern_size)
random_patterns = factory.create_random_pattern_list(5, on_probability=0.5)

plot_tools.plot_pattern_list(random_patterns)

overlap_matrix = pattern_tools.compute_overlap_matrix(random_patterns)
plot_tools.plot_overlap_matrix(overlap_matrix)

hopfield_net.store_patterns(random_patterns)

noisy_pattern = pattern_tools.flip_percentage(random_patterns[0], 0.3)
hopfield_net.set_state_from_pattern(noisy_pattern)

states = hopfield_net.run_with_monitoring(6)
patterns = factory.reshape_patterns(states)

plot_tools.plot_state_sequence_and_overlap(patterns, random_patterns, reference_idx=0,
    suptitle="Network Dynamics with Noisy Pattern")
