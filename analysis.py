""" Author: Venkatesh Krishnamurthy. Copyright 2022."""

from galvani.BioLogic import MPRfile
from impedance.models.circuits import CustomCircuit, Randles
from pandas import DataFrame
import matplotlib.pyplot as plt
from impedance.visualization import plot_nyquist, plot_bode, plot_residuals
import glob
from impedance import preprocessing
import numpy as np


# Convert data from mpr file into csv
filename = glob.glob('*.mpr')[0]
data = DataFrame(MPRfile(filename).data)

freq = np.array(data['freq/Hz'])
real_Z = np.array(data['Re(Z)/Ohm'])
imag_Z = -1*np.array(data['-Im(Z)/Ohm'])
np.savetxt('data.csv', np.column_stack((freq, real_Z, imag_Z)), delimiter=',')
# np.savetxt('data.csv', np.column_stack((data['freq/Hz'], data['Re(Z)/Ohm'], data['-Im(Z)/Ohm'])), delimiter=',')


# Read from csv file and pre-process
frequencies, Z = preprocessing.readCSV('data.csv')
frequencies, Z = preprocessing.ignoreBelowX(frequencies, Z)

# mask = frequencies < 1000
# frequencies = frequencies[mask]
# Z = Z[mask]

# Define circuit with iniital values
# With CPE
circuit = CustomCircuit('R0-p(R1,C1,CPE0)-p(R2,C2)', initial_guess=[18, 500,0.0001,20,1.0, 100,0.001])

# With Gerisher element
# circuit = CustomCircuit('R0-p(R1,C1,G0)-p(R2,C2)', initial_guess=[18, 500,0.0001,20,1, 100,0.001])

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


# Compute residuals
res_real = (Z - circuit.predict(frequencies)).real/np.abs(Z)
res_imag = (Z - circuit.predict(frequencies)).imag/np.abs(Z)


# Plot Nyquist
fig, ax = plt.subplots(tight_layout=True)
plot_nyquist(ax, Z, fmt='o', units='\Omega', label='Data')
plot_nyquist(ax, circuit.predict(frequencies), fmt='-', units='\Omega', label='Fit')
plt.legend()
plt.title(filename)
plt.savefig('nyquist.png')
plt.close()


# Plot Bode
fig, ax = plt.subplots(2, 1, tight_layout=True)
plot_bode(ax, frequencies, Z, fmt='o', units='\Omega', label='Data')
plot_bode(ax, frequencies, circuit.predict(frequencies), fmt='-', units='\Omega', label='Fit')
ax[0].set_title(filename)
ax[0].legend()
ax[1].legend()
plt.savefig('bode.png')
plt.close()


# Plot residuals
fig, ax = plt.subplots(tight_layout=True)
plot_residuals(ax, frequencies, res_real, res_imag, y_limits=(-10,10))
plt.savefig('residuals.png')
plt.close()
