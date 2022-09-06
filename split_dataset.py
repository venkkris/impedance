"""
Author: Venkatesh Krishnamurthy
Script to split the EIS dataset based on non-monotonous change in frequency
"""

# Import modules
from glob import glob
import numpy as np
from os import makedirs
from pandas import DataFrame
from impedance.preprocessing import readCSV
from galvani.BioLogic import MPRfile

freq_order = 'descending'

# Convert data from mpr file into csv
filename = glob('*.mpr')[0]
print('Filename: {}'.format(filename))
data = DataFrame(MPRfile(filename).data)

freq = data['freq/Hz']
real_Z = data['Re(Z)/Ohm']
imag_Z = -1*data['-Im(Z)/Ohm']
np.savetxt('data.csv', np.column_stack((freq, real_Z, imag_Z)), delimiter=',')


# Read from csv file and pre-process
# freq, Z = readCSV('data.csv')

# Split the data into individual cycles based on non-monotonous change in frequency
# Find index where adjacent frequencies are ascending/descending
if freq_order == 'ascending':
    indices = np.where(np.diff(freq) < 0)
elif freq_order == 'descending':
    indices = np.where(np.diff(freq) > 0)

makedirs('split', exist_ok=True)

for i in range(len(indices[0])):
    print('Cycle: {}'.format(i))
    if i == 0:
        start = 0
        end = indices[0][i]
    else:
        start = indices[0][i-1] + 1
        end = indices[0][i]
    # Save the data
    makedirs('split/cycle_{}'.format(i), exist_ok=True)
    np.savetxt('split/cycle_{}/data.csv'.format(i), np.column_stack((freq[start:end], Z[start:end].real, Z[start:end].imag)), delimiter=',')