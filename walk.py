import cirq
import numpy as np


def perform_quantum_walk(number_qubits, n_steps, repetitions, verbose=False):

    qubits = cirq.GridQubit.rect(1, number_qubits)
    circuit = cirq.Circuit()

    circuit.append(cirq.X(qubits[1]))
    circuit.append(cirq.X(qubits[-1]))
    for _ in range(n_steps):
        circuit = one_quantum_step(circuit, qubits)

    circuit.append(cirq.measure(*qubits[: number_qubits - 1], key="x"))

    if verbose:
        print(circuit)

    final = run_simulation(circuit, repetitions)
    x_array, y_array = get_values_from_dict(final)
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


def random_walk(pr, N, i):

    position = i

    # Repeatedly queries our random variable and moves our walker for the specified number of steps

    for j in range(N):

        coin_flip = list(
            np.random.choice(2, 1, p=[1 - pr, pr])
        )  # Flips our weighted coin
        position += 2 * coin_flip[0] - 1  # Moves our walker according to the coin flip

    return position


def dist(runs, N):

    positions = range(-1 * N, N + 1)
    instances = [0 for i in range(-1 * N, N + 1)]

    for k in range(runs):

        result = random_walk(pr, N, i)
        instances[positions.index(result)] += 1

    plt.bar(positions, [n / runs for n in instances])
    plt.show()


def get_values_from_dict(final):

    x_arr = list(final.keys())
    y_arr = [dict(final)[j] for j in dict(final).keys()]

    x_arr_final = []
    y_arr_final = []

    while (len(x_arr) > 0):

        x_arr_final.append(min(x_arr))
        y_arr_final.append(y_arr[x_arr.index(min(x_arr))])
        holder = x_arr.index(min(x_arr))
        del x_arr[holder]
        del y_arr[holder]
    return x_arr_final, y_arr_final
