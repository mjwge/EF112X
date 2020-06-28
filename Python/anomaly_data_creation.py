import numpy as np
from scipy.io import loadmat
import os as os
import copy
import matplotlib.pyplot as plt

"""
Making the datasets used for the ANN, with artificially created anomalies. 
"""

dbg = False

def make_data(temp):
    """Make the original data vectors, where each day is one vector."""
    datasets = []
    directory = 'C:\\Users\\mjwge\\Documents\\kex\\Measurement_data\\datasets' + temp
    """'temp' chooses whether the data should be compensated ur unaltered."""
    print(directory)


    for filename in os.listdir(directory):
        """iterate through the directory."""

        if dbg: print(filename)
        data = loadmat('C:\\Users\\mjwge\\Documents\\kex\\Measurement_data\\datasets' + temp +'\\' +filename)
        inputdata = data['input']
        if dbg: print(len(inputdata), "length")

        datasets.append(inputdata)

    return datasets[3:]


def splitDataFull(datasets):
    """Split the data vectors to gain the structure and more training data."""

    ind1 = 1
    ind2 = 600
    """Set where the anomaly should be introduced."""

    print(ind1, ind2)
    newList = []
    newList.append(datasets[0])
    for i in range(1, len(datasets)):
        for j in range(len(newList[0])//2):



            tmp = copy.deepcopy(newList[-1])

            tmp[j] = datasets[i][j]
            """Replace measurement value with next timeslot."""

            tmp[j+len(datasets[0])//2-1] = datasets[i][j+len(datasets[0])//2-1]
            """Replace corresponding temperature reading. """

            newList.append(tmp)

            if j < 20 and dbg:
                """Debugging conditional"""
                print(j + (len(datasets) - 1) * (i - 1), "index")
                if j < 10:

                    print(newList[j+(len(datasets)-1)*(i-1)][0:j+3], "tempfunc")
                    print(i,j," i,j ")
                else:
                    print(newList[j+(len(datasets)-1)*(i-1)][j-10:j+3], "tempfunc")
                    print(i, j, " i,j ")

    newList[(ind1-1)*1439+ind2][ind2] = newList[(ind1-1)*1439+ind2][ind2]*(1-0.02)
    """Alter the value of the anomaly to, in this case, 1-0.02 = -2%"""

    plt.plot(newList[(ind1-1)*1439+ind2][0:1439])
    plt.show()
    """Plotting"""
    return newList

def splitDataKomp(datasets):
    """Does the same as splitDataFull but with compensated data, and will not be commented further since it was not used. """
    newList = []
    newList.append(datasets[0])
    for i in range(1, len(datasets)):
        for j in range(len(newList[0])):

            tmp = copy.deepcopy(newList[-1])
            tmp[j] = datasets[i][j]

            newList.append(tmp)

            if j < 20 and dbg and 1 == 0:
                print(j + (len(datasets) - 1) * (i - 1), "index")
                if j < 10:

                    print(newList[j+(len(datasets)-1)*(i-1)][0:j+3], "tempfunc")
                    print(i,j," i,j ")
                else:
                    print(newList[j+(len(datasets)-1)*(i-1)][j-10:j+3], "tempfunc")
                    print(i, j, " i,j ")
    return newList





def get_data(temp, full,anomaly):
    """Main function that gets called."""
    datasets = make_data(temp)

    if full and temp == "": datasets = splitDataFull(datasets)
    if full and temp == "_komp": datasets = splitDataKomp(datasets)
    """Decides whether compensated or raw data should be used. 'full' indicates if the data should be split into more datasets."""

    print(len(datasets))
    length = len(datasets[0])


    for i in range(len(datasets)):

        datasets[i][0:(length-1)//2] = (datasets[i][0:(length-1)//2]-np.min(datasets[i][0:(length-1)//2]) )/\
                                      (np.max(datasets[i][0:(length-1)//2])-np.min(datasets[i][0:(length-1)//2]))

        datasets[i][(length-1)//2:-1] = (datasets[i][(length-1)//2:-1]-np.min(datasets[i][(length-1)//2:-1]) )/\
                                     (np.max(datasets[i][(length-1)//2:-1])-np.min(datasets[i][(length-1)//2:-1]))

        """Normalize the inputs, with current measurements and temperature readings separated. """

    training = datasets[0:round(len(datasets)*0.8)]
    testing = datasets[round(len(datasets)*0.8):len(datasets)]
    """Divide the data in training and testing sets. """

    return training, testing


if __name__ == '__main__':
    training, testing = get_data("", True, True)
    print(len(training), len(testing))
    #plt.plot(training[0])
    #plt.show()
    #print(training, testing)

else:
    pass