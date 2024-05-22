import cirq
import numpy as np
from utils import get_values_from_dict


def perform_quantum_walk(
    number_qubits,
    n_steps,
    repetitions,
    coin_set=True,
    symmetric=False,
    verbose=False,
    percentage=True,
):
    """
    Perform a quantum walk.

    This function simulates a quantum walk for a given number of repetitions. It returns the x and y arrays
    for the quantum walk. If the percentage flag is set to True, it returns the percentage of each outcome.

    Args:
        number_qubits (int): The number of qubits.
        n_steps (int): The number of steps.
        repetitions (int): The number of repetitions.
        coin_set (bool, optional): If True, the coin is set. Defaults to True.
        symmetric (bool, optional): If True, the walk is symmetric. Defaults to False.
        verbose (bool, optional): If True, print the circuit. Defaults to False.
        percentage (bool, optional): If True, return the percentage of each outcome. Defaults to True.

    Returns:
        tuple: The x and y arrays for the quantum walk.
    """
    qubits = cirq.GridQubit.rect(1, number_qubits)
    circuit = cirq.Circuit()

    circuit.append(cirq.X(qubits[4]))
    if coin_set:
        circuit.append(cirq.X(qubits[-1]))
    if symmetric:
        circuit.append(cirq.H(qubits[-1]))
        circuit.append(cirq.S(qubits[-1]))

    for _ in range(n_steps):
        circuit = one_quantum_step(circuit, qubits)

    circuit.append(cirq.measure(*qubits[: number_qubits - 1], key="x"))

    if verbose:
        print(circuit)

    final = run_simulation(circuit, repetitions)
    x_array, y_array = get_values_from_dict(final)
    if percentage:
        y_array = np.asarray(y_array) / sum(y_array)
    return x_array, y_array


def run_simulation(circuit, repetitions):
    """
    Run a simulation.

    This function simulates the given circuit for a specified number of repetitions. It returns a dictionary
    with the histogram of the simulation results.

    Args:
        circuit (cirq.Circuit): The circuit to simulate.
        repetitions (int): The number of repetitions.

    Returns:
        dict: The histogram of the simulation results.
    """
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=repetitions)
    final = result.histogram(key="x")
    return dict(final)


def one_quantum_step(circuit, qubits):
    """
    Perform one step of a quantum walk.

    This function applies a Hadamard operator, left shift operator, and right shift operator to the given circuit
    and qubits. It returns the updated circuit.

    Args:
        circuit (cirq.Circuit): The circuit to perform the step on.
        qubits (list): The qubits to perform the step with.

    Returns:
        cirq.Circuit: The circuit after performing the step.
    """
    number_qubits = len(qubits)
    qubits = cirq.GridQubit.rect(1, number_qubits)
    # Hadarmard Operator
    circuit.append(cirq.H(qubits[-1]))

    # Left Shift Operator
    for i in range(number_qubits - 1, 0, -1):
        controlling_qubits = [
            cirq.GridQubit(0, v) for v in range(number_qubits - 1, i - 1, -1)
        ]
        cn_x = cirq.X.on(cirq.GridQubit(0, i - 1)).controlled_by(*controlling_qubits)
        circuit.append(cn_x)

    # Right shift Operator
    for i in range(number_qubits - 1, 0, -1):
        if i < number_qubits:
            circuit.append(cirq.X.on(cirq.GridQubit(0, i)))
        controlling_qubits = [
            cirq.GridQubit(0, v) for v in range(number_qubits - 1, i - 1, -1)
        ]
        cn_x = cirq.X.on(cirq.GridQubit(0, i - 1)).controlled_by(*controlling_qubits)
        circuit.append(cn_x)

    for i in range(1, number_qubits):
        circuit.append(cirq.X.on(cirq.GridQubit(0, i)))

    return circuit


def one_random_step(pr, n_steps, position):
    """
    Disclaimer: This function is taken by the Google Tutorial about Random Walks

    Perform one step of a random walk.

    This function repeatedly queries a random variable and moves the walker for the specified number of steps.

    Args:
        pr (float): The probability of moving right.
        n_steps (int): The number of steps.
        position (int): The initial position.

    Returns:
        int: The position after performing the step.
    """
    # Repeatedly queries our random variable and moves our walker for the specified number of steps
    for _ in range(n_steps):

        coin_flip = list(
            np.random.choice(2, 1, p=[1 - pr, pr])
        )  # Flips our weighted coin
        position += 2 * coin_flip[0] - 1  # Moves our walker according to the coin flip

    return position


def perform_random_walk(
    repetitions, n_steps, pr=0.5, initial_position=0, percentage=True
):
    """
    Perform a random walk.

    This function simulates a random walk for a given number of repetitions. It returns the positions and instances
    of the walk. If the percentage flag is set to True, it returns the percentage of each outcome.

    Args:
        repetitions (int): The number of repetitions.
        n_steps (int): The number of steps.
        pr (float, optional): The probability of moving right. Defaults to 0.5.
        initial_position (int, optional): The initial position. Defaults to 0.
        percentage (bool, optional): If True, return the percentage of each outcome. Defaults to True.

    Returns:
        tuple: The positions and instances for the random walk.
    """
    positions = range(-1 * n_steps, n_steps + 1)
    instances = [0 for _ in range(-1 * n_steps, n_steps + 1)]

    for _ in range(repetitions):

        result = one_random_step(pr, n_steps, initial_position)
        instances[positions.index(result)] += 1
    if percentage:
        instances = np.asarray(instances) / sum(instances)
    return list(positions), instances
