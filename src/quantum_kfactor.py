import numpy as numpy
from collections import deque
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# The purpose of this class is to estimate a "K" value (from 10 to 50)
# based on user performance using a quantum circuit.
# The K value is influenced by three features:


# 1. Accuracy Ratio: Proportion of correct answers in the recent window.
# 2. Signed Streak: Length of the current streak of correct/incorrect answers.
# 3. Speed Score: Based on median response time relative to a time cap.

class QuantumKEstimator:
    # Constructor to initialize parameters and data structures
    def __init__(self, window=10, shots=128, t_cap=8.0):
        self.window = window
        self.shots = shots
        self.time_cap_seconds = t_cap
        self.results = deque(maxlen=window)
        self.times = deque(maxlen=window)
        self.backend = AerSimulator()


    # Private method to compute features    
    def _features(self):
        if len(self.results) == 0:
            accuracy_ratio = 0.5
            signed_streak = 0.0
            speed_score = 0.5
            return accuracy_ratio, signed_streak, speed_score


        accuracy_ratio = sum(self.results) / len(self.results)


        last_result = self.results[-1]
        streak_length = 0
        for result in reversed(self.results):
            if result == last_result:
                streak_length += 1
            else:
                break
        signed_streak = min(streak_length / self.window, 1.0) * (1.0 if last_result else -1.0)


        if len(self.times) == 0:
            speed_score = 0.5
        else:
            median_response_time = float(numpy.median(self.times))
            speed_score = 1.0 - min(median_response_time / self.time_cap_seconds, 1.0)


        return accuracy_ratio, signed_streak, speed_score


    # Public method to compute the K value using a quantum circuit
    def k(self):
        # Extract features
        accuracy_ratio, signed_streak, speed_score = self._features()


        # Build quantum circuit ( See generated circuit in documentation for clarity)
        circuit = QuantumCircuit(2, 2)
        circuit.ry(numpy.pi * accuracy_ratio, 0)
        circuit.ry(numpy.pi * (0.5 * (signed_streak + 1.0)), 1)
        circuit.cx(0, 1)
        circuit.rx(numpy.pi * speed_score, 1)
        circuit.measure([0, 1], [0, 1])


        # Execute the circuit on the quantum backend
        job_result = self.backend.run(transpile(circuit, self.backend), shots=self.shots, memory=True)
        memories = job_result.result().get_memory()
        ones_count = sum(bitstring.count("1") for bitstring in memories)
        one_fraction = ones_count / (2 * len(memories))


        # Return K value scaled between 10 and 50
        return 10 + int(40 * one_fraction)


    # Public method to add a new result and response time
    def add(self, correct, response_time):
        self.results.append(bool(correct))
        self.times.append(float(response_time))


