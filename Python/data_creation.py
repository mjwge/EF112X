import numpy as np
from scipy.io import loadmat
import os as os
import copy
import matplotlib.pyplot as plt

"""
Creation of data sets without added anomalies. Same code as 'anomaly_data_creation', except this is shuffled before the last return. 
For more detailed comments, check 'anomaly_data_creation.py'.
"""

dbg = False

def make_data(temp):

    datasets = []
    directory = 'C:\\Users\\mjwge\\Documents\\kex\\Measurement_data\\datasets' + temp
    print(directory)

    for filename in os.listdir(directory):
        if dbg: print(filename)
        data = loadmat('C:\\Users\\mjwge\\Documents\\kex\\Measurement_data\\datasets' + temp +'\\' +filename)
        inputdata = data['input']
        if dbg: print(len(inputdata), "length")

        datasets.append(inputdata)

    return datasets[3:]


def splitDataFull(datasets):
    newList = []
    newList.append(datasets[0])
    for i in range(1, len(datasets)):
        for j in range(len(newList[0])//2):

            tmp = copy.deepcopy(newList[-1])
            tmp[j] = datasets[i][j]


            tmp[j+len(datasets[0])//2-1] = datasets[i][j+len(datasets[0])//2-1]


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
def splitDataKomp(datasets):
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
    datasets = make_data(temp)
    if anomaly == True:
        ind = round(1440*np.random.random())
        datasets[0][ind:ind+6] = datasets[0][ind+6]*1.05
        datasets[1][ind:ind + 6] = datasets[1][ind + 6] * 1.025
        datasets[2][ind:ind + 6] = datasets[2][ind + 6] * 1.01
        print(ind, "anomaly index")
        if True:

            ploting = datasets[0][0:1439]

            ploting = np.append(ploting, datasets[1][0:1439])
            ploting = np.append(ploting, datasets[2][0:1439])

            print(datasets[0].shape, "  ", ploting.shape)
            plt.plot(ploting)

            plt.show()
        else:
            pass
    else:
        pass

    if full and temp == "": datasets = splitDataFull(datasets)
    if full and temp == "_komp": datasets = splitDataKomp(datasets)

    print(len(datasets))
    length = len(datasets[0])


    for i in range(len(datasets)):

        datasets[i][0:(length-1)//2] = (datasets[i][0:(length-1)//2]-np.min(datasets[i][0:(length-1)//2]) )/\
                                      (np.max(datasets[i][0:(length-1)//2])-np.min(datasets[i][0:(length-1)//2]))

        datasets[i][(length-1)//2:-1] = (datasets[i][(length-1)//2:-1]-np.min(datasets[i][(length-1)//2:-1]) )/\
                                     (np.max(datasets[i][(length-1)//2:-1])-np.min(datasets[i][(length-1)//2:-1]))


    np.random.shuffle(datasets)
    """Shuffle the datasets to avoid any unnecessary correlation that may influence the training. """


    training = datasets[0:round(len(datasets)*0.8)]

    testing = datasets[round(len(datasets)*0.8):len(datasets)]

    return training, testing


if __name__ == '__main__':
    training, testing = get_data("", True, True)
    print(len(training), len(testing))

else:
    pass