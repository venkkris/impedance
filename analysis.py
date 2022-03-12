""" Author: Venkatesh Krishnamurthy. Copyright 2022."""

from galvani.BioLogic import MPRfile
from impedance.models.circuits import CustomCircuit, Randles
from pandas import DataFrame
import matplotlib.pyplot as plt
from impedance.visualization import plot_nyquist, plot_bode
import glob
from impedance import preprocessing
import numpy as np


# Convert data from mpr file into csv
filename = glob.glob('*.mpr')[0]
# mpr_file = MPRfile(filename)
# data = DataFrame(mpr_file.data)

# freq = np.array(data['freq/Hz'])
# real_Z = np.array(data['Re(Z)/Ohm'])
# imag_Z = -1*np.array(data['-Im(Z)/Ohm'])
# np.savetxt('data.csv', np.column_stack((freq, real_Z, imag_Z)), delimiter=',')


# Read from csv file and pre-process
frequencies, Z = preprocessing.readCSV('data.csv')
frequencies, Z = preprocessing.ignoreBelowX(frequencies, Z)


# Define circuit with iniital values
# With CPE
# circuit = CustomCircuit('R0-p(R1,C1,CPE0)-p(R2,C2)', initial_guess=[18, 500,0.0001,20,1.0, 100,0.001])
# With Gerisher element
circuit = CustomCircuit('R0-p(R1,C1,G0)-p(R2,C2)', initial_guess=[18, 500,0.0001,20,1, 100,0.001])

# Alternate- Randles circuit with CPE
# circuit = Randles(initial_guess=[0.1, 10, .1, .9, .001, 200], CPE=True)

# Alternate- Randle circuit
# circuit = Randles(initial_guess=[100, 50, .1, .001, 200])


# Fit to circuit and write outputs
circuit.fit(frequencies, Z, global_opt=False)
print(circuit)
circuit.save('circuit.json')
file = open('out.txt', 'w')
file.write(str(circuit))
file.close()


# Plot Nyquist
fig, ax = plt.subplots(tight_layout=True)
plot_nyquist(ax, Z, fmt='o')
plot_nyquist(ax, circuit.predict(frequencies), fmt='-')
plt.legend(['Data', 'Fit'])
plt.title(filename)
plt.savefig('nyquist.png')
plt.close()


# Plot Bode
fig, ax = plt.subplots(2, 1, tight_layout=True)
plot_bode(ax, frequencies, Z, fmt='o')
plot_bode(ax, frequencies, circuit.predict(frequencies), fmt='-')
ax[0].set_title(filename)
ax[0].legend(['Data', 'Fit'])
ax[1].legend(['Data', 'Fit'])
plt.savefig('bode.png')
plt.close()
