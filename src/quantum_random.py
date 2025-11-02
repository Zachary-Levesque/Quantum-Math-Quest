# Import qiskit libraries in order to create our quantum circuit
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# This function is used to randomly select a number between 0 and 3 using a quantum circuit
def quantum_rand_0_to_3():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.h(1)
    qc.measure(0, 0)
    qc.measure(1, 1)
    
    backend = AerSimulator()
    job = backend.run(transpile(qc, backend), shots=1, memory=True)
    bits = job.result().get_memory()[0]
    return int(bits[::-1], 2)

# This function is used to randomly select a number between 0 and 9 using a quantum circuit
def quantum_rand_1_to_10():
    backend = AerSimulator()
    qc = QuantumCircuit(4, 4)
    for i in range(4):
        qc.h(i)
        qc.measure(range(4), range(4))
        job = backend.run(transpile(qc, backend), shots=1, memory=True)
    bits = job.result().get_memory()[0]
    number = int(bits[::-1], 2)
    
    if number <= 9:
        return number + 1
    else:
        return quantum_rand_1_to_10()