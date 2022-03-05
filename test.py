""" Author: Venkatesh Krishnamurthy. Copyright 2022."""

from galvani import BioLogic
from impedance.models.circuits import CustomCircuit
import pandas as pd
import matplotlib.pyplot as plt
from impedance.visualization import plot_nyquist
import glob
from impedance import preprocessing
import numpy as np


# Convert data from mpr file into csv
filename = glob.glob('*.mpr')[0]
mpr_file = BioLogic.MPRfile(filename)
data = pd.DataFrame(mpr_file.data)

freq = np.array(data['freq/Hz'])
real_Z = np.array(data['Re(Z)/Ohm'])
imag_Z = -1*np.array(data['-Im(Z)/Ohm'])
np.savetxt('data.csv', np.column_stack((freq, real_Z, imag_Z)), delimiter=',')

# Read from csv file and pre-process
frequencies, Z = preprocessing.readCSV('data.csv')
frequencies, Z = preprocessing.ignoreBelowX(frequencies, Z)


# Define circuit with iniital values
circuit = 'R0-p(R1,C1)-p(R2,C2)'
initial_guess = [18, 500, 0.0001, 100, 0.001]
circuit = CustomCircuit(circuit, initial_guess=initial_guess)

# Fit to circuit and write outputs
circuit.fit(frequencies, Z, global_opt=True)
print(circuit)
circuit.save('circuit.json')
file = open('out.txt', 'w')
file.write(str(circuit))
file.close()

# Plot
fig, ax = plt.subplots()
plot_nyquist(ax, Z, fmt='o')
plot_nyquist(ax, circuit.predict(frequencies), fmt='-')
plt.legend(['Data', 'Fit'])
plt.title(filename)
plt.savefig('plot.png')
plt.show()
