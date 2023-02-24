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
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=repetitions)
    final = result.histogram(key="x")
    return dict(final)


def one_quantum_step(circuit, qubits):

    number_qubits = len(qubits)
    qubits = cirq.GridQubit.rect(1, number_qubits)
    # Hadarmard Operator
    circuit.append(cirq.H(qubits[-1]))

    # Left Shift Operator
    for i in range(number_qubits - 1, 0, -1):
        controlling_qubits = [
            cirq.GridQubit(0, v) for v in range(number_qubits - 1, i - 1, -1)
        ]
        cnX = cirq.X.on(cirq.GridQubit(0, i - 1)).controlled_by(*controlling_qubits)
        circuit.append(cnX)

    # Right shift Operator
    for i in range(number_qubits - 1, 0, -1):
        if i < number_qubits:
            circuit.append(cirq.X.on(cirq.GridQubit(0, i)))
        controlling_qubits = [
            cirq.GridQubit(0, v) for v in range(number_qubits - 1, i - 1, -1)
        ]
        cnX = cirq.X.on(cirq.GridQubit(0, i - 1)).controlled_by(*controlling_qubits)
        circuit.append(cnX)

    for i in range(1, number_qubits):
        circuit.append(cirq.X.on(cirq.GridQubit(0, i)))

    return circuit


"""
Disclaimer: This function is taken by the Google Tutorial about Random Walks
"""


def one_random_step(pr, n_steps, position):

    # Repeatedly queries our random variable and moves our walker for the specified number of steps

    for j in range(n_steps):

        coin_flip = list(
            np.random.choice(2, 1, p=[1 - pr, pr])
        )  # Flips our weighted coin
        position += 2 * coin_flip[0] - 1  # Moves our walker according to the coin flip

    return position


def perform_random_walk(
    repetitions, n_steps, pr=0.5, initial_position=0, percentage=True
):
    # positions = np.arange(-1 * n_steps, n_steps + 1, 1)
    positions = range(-1 * n_steps, n_steps + 1)
    instances = [0 for i in range(-1 * n_steps, n_steps + 1)]

    for _ in range(repetitions):

        result = one_random_step(pr, n_steps, initial_position)
        instances[positions.index(result)] += 1
    if percentage:
        instances = np.asarray(instances) / sum(instances)
    return list(positions), instances
