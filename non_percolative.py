from qiskit import *
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')
from qiskit.tools.visualization import plot_histogram


def x_measure(qc,qubit,cbit):
    '''Measure qubit in the X-basis, and store the result in cbit'''
    qc.barrier()
    qc.h(qubit)
    qc.measure(qubit, cbit)
    qc.h(qubit)
    qc.barrier()
    return qc

# Create a Quantum Circuit with 5 data qubits, 10 ancilla qubits and 8 classical bits for measurement
qc = QuantumCircuit(15, 8)

#State Preparation

#Change flag qubits to Sign basis
qc.h([0,1,3,5])

for i in range(9,14):
    qc.h(i)

for i in range(9,14):
    if i != 13:
        qc.cz(i,i+1)
    else:
        qc.cz(13,9)

qc.barrier()

for i in range(9,14):
    qc.h(i)
    
qc.barrier()


#Stabilizer XIXZZ onto S0
qc.cx(13,6)
qc.cx(5,6)
qc.swap(5,6)
qc.cx(12,5)
qc.swap(4,5)
qc.swap(5,6)
qc.barrier()
qc.h(11)
qc.cx(11,4)
qc.h(11)
qc.barrier()
qc.swap(3,4)
qc.swap(4,5)
qc.swap(2,3)
qc.swap(3,4)
qc.cx(3,2)
qc.barrier()
qc.h(9)
qc.cx(9,2)
qc.h(9)
qc.barrier()


#Stabilizer ZXIXZ onto S1
qc.swap(1,2)
qc.swap(2,3)
qc.swap(0,1)
qc.swap(1,2)
qc.swap(0,7)
qc.swap(1,8)
qc.cx(13,6)
qc.cx(5,6)
qc.swap(5,6)
qc.barrier()
qc.h(12)
qc.cx(12,5)
qc.h(12)
qc.barrier()
qc.swap(4,5)
qc.swap(5,6)
qc.swap(3,4)
qc.swap(4,5)
qc.barrier()
qc.h(10)
qc.cx(10,3)
qc.barrier()
qc.swap(2,3)
qc.swap(3,4)
qc.cx(3,2)
qc.cx(9,2)
qc.barrier()

#Stabilizer ZZXIX onto S2
qc.swap(1,2)
qc.swap(2,3)
qc.swap(0,1)
qc.swap(1,2)
qc.barrier()
qc.h(13)
qc.cx(13,6)
qc.h(13)
qc.barrier()
qc.cx(5,6)
qc.swap(5,6)
qc.swap(4,5)
qc.swap(5,6)
qc.barrier()
qc.h(11)
qc.cx(11,4)
qc.h(11)
qc.barrier()
qc.swap(3,4)
qc.swap(4,5)
qc.cx(10,3)
qc.swap(2,3)
qc.swap(3,4)
qc.swap(2,3)
qc.cx(3,2)
qc.cx(9,2)
qc.barrier()

#Stabilizer IXZZX onto S3
qc.swap(13,14)
qc.barrier()
qc.h(14)
qc.cx(14,13)
qc.h(14)
qc.barrier()
qc.cx(6,13)
qc.cx(12,13)
qc.swap(5,6)
qc.swap(12,13)
qc.swap(11,12)
qc.swap(4,5)
qc.cx(12,11)
qc.cx(4,11)
qc.barrier()
qc.h(10)
qc.cx(10,11)
qc.h(10)
qc.barrier()


#Measurement and simulation

qc.measure(7,0)
qc.measure(0,1)
qc.measure(2,2)
qc.measure(11,3)
qc.measure(8,4)
qc.measure(1,5)
qc.measure(3,6)
qc.measure(4,7)

sim = Aer.get_backend('qasm_simulator')
job = execute(qc, sim, shots=256)
result = job.result()
counts = result.get_counts(qc)
print(counts)
qc.draw(output = 'mpl')
