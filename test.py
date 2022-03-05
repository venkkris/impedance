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

# data.to_csv('data.csv', columns=['freq/Hz', 'Re(Z)/Ohm', '-Im(Z)/Ohm'], header=False, index=False)


frequencies, Z = preprocessing.readCSV('data.csv')
frequencies, Z = preprocessing.ignoreBelowX(frequencies, Z)


# Define impedance model
circuit = 'R0-p(R1,C1)-p(R2,C2)'
initial_guess = [100, 10, 10, .1, 100]
circuit = CustomCircuit(circuit, initial_guess=initial_guess)

circuit.fit(frequencies, Z)
print(circuit)
Z_fit = circuit.predict(frequencies)

fig, ax = plt.subplots()
plot_nyquist(ax, Z, fmt='o')
plot_nyquist(ax, Z_fit, fmt='-')

plt.legend(['Data', 'Fit'])
# plt.show()
plt.savefig('plot.png')
