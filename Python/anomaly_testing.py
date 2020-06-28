import numpy as np
from scipy.io import loadmat
import os as os
import copy
import matplotlib.pyplot as plt
from anomaly_data_creation import *
from autoencoder_2hidden import *

from datetime import datetime

"""
Test the structure for anomaly detection, by introducing an anomaly in 'anomaly_data_creation' and using deviation based anomaly detection. 
"""

date = datetime.now()
if date.month in range(1,10) and date.day in range(1,10):
    date = "" + str(date.year) + "0" + str(date.month) +"0" + str(date.day)
elif date.month in range(1,10) and date.day not in range(1,10):
    date = "" + str(date.year) + "0" + str(date.month) + str(date.day)
elif date.month not in range(1,10) and date.day in range(1,10):
    date = "" + str(date.year) + str(date.month) + "0" + str(date.day)
else:
    date = "" + str(date.year) + str(date.month) + str(date.day)

training_data, testing_data = get_data("", True, False)


original_dim = len(training_data[0])
print(original_dim)

testing_data = testing_data / np.max([0,1])
"""Make numpy vector of testing data"""


testing_data = testing_data.reshape(testing_data.shape[0], testing_data.shape[2], testing_data.shape[1])
"""Reshape input data for testing data"""


training_data = training_data/ np.max([0,1])
training_data = training_data.reshape(training_data.shape[0], training_data.shape[2], training_data.shape[1])
"""Make data to numpy vector and reshape it, for training dataset. """

hidden_dim = [round(original_dim*0.7), round(original_dim*0.3)]


newAutoencoder = Autoencoder(hidden_dim=hidden_dim, original_dim=original_dim)
newAutoencoder.load_weights('saves\\70-30-30-70_all_data')
"""Create autoencoder and load the previously trained weights. """

variance = []
mse = []
falseAlarms = 0
"""Initiate some variables."""


maxVar = 7*0.00017293528 + 0.00016897997
"""Determining the threshold level as k*Var + mean"""

for i in range(round(len(training_data)//9)):

    variance.append(np.var(np.subtract(training_data[i], newAutoencoder(training_data[i]))))

    #tmp = abs(np.subtract(training_data[i], newAutoencoder(training_data[i]))).mean()
    tmp2 = np.square(np.subtract(training_data[i], newAutoencoder(training_data[i]))).mean()
    """Compute variance and mean square error of one input. """

    mse.append(tmp2)
    """Append it for plotting in the end."""
    if i%1440 == 0:
        print(i)
    if i == 1350:
        """Only used to verify the anomaly reconstruction error. The 1350 can be swapped to whichever is used in 'anomaly_data_creation'. """
        print(tmp2, " Rec error")
    if tmp2 > maxVar:
        """Raise alarm if MSE is over threshold. """
        falseAlarms = falseAlarms + 1
        print("Anomaly detected at time ", i//60, "h ", round((i/60-i//60)*60), "min, timestamp ", i)
        """Alert user that an anomaly is detected at certain timepoint"""

        plott = training_data[i][0:1439]
        plott = plott.reshape(plott.shape[1], plott.shape[0])
        plott2 = newAutoencoder(training_data[i])
        plott2 = plott2.numpy()
        plott2 = plott2.reshape(plott2.shape[1], plott2.shape[0])
        print(i, " sample")
        og = plt.plot(plott[0:1439], label="Input")
        rec = plt.plot(plott2[0:1439], label="Reconstruction")
        plt.ylabel("Normalized value")
        plt.xlabel("Time, [minutes]")
        plt.legend()
        plt.title("Comparision between input and reconstruction")
        plt.show()
        print(tmp2)
        """Only used for plotting"""


mean_var = np.mean(variance)

print("Mean of MSEs: ",np.mean(mse)," Mean of variences: ", mean_var)
line = plt.axhline(maxVar, color = "r", label = "Threshold level")
mseplot = plt.plot(mse, label = "MSE")
plt.ylabel("Mean square error")
plt.xlabel("Time, [minutes]")
plt.legend(loc='top right')
plt.title("Reconstruction errors")
plt.show()

plt.plot(variance)
plt.show()

print("False alarms: ", falseAlarms)
"""Ploting and some prints that give information about the run."""
