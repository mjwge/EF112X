import tensorflow as tf
print("Hello ")
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image
from autoencoder_2hidden import *
from data_creation import *


"""
Program for training the ANN
"""

dbg = False
plotta = False

if __name__ == '__main__':

    date = datetime.now()
    if date.month in range(1,10) and date.day in range(1,10):
        date = "" + str(date.year) + "0" + str(date.month) +"0" + str(date.day)
    elif date.month in range(1,10) and date.day not in range(1,10):
        date = "" + str(date.year) + "0" + str(date.month) + str(date.day)
    elif date.month not in range(1,10) and date.day in range(1,10):
        date = "" + str(date.year) + str(date.month) + "0" + str(date.day)
    else:
        date = "" + str(date.year) + str(date.month) + str(date.day)
    print(date)
    '''
    plt.close()

    a = tf.constant([1,2])
    b = tf.constant([3,4])
    print(a+b)
    '''
    #np.random.seed(1)                               # Osäker på vad seed i tf och np gör, ska kolla upp det.
    #tf.random.set_seed(1)
    batch_size = 256
    epochs = 100
    learning_rate = 0.002
    training_data, testing_data = get_data("", full=True, anomaly=False)
    """Put "" for raw data, "_komp" for preprocessed data."""


    testing = testing_data
    original_dim = len(training_data[0])
    hidden_dim = [round(original_dim*0.5), round(original_dim*0.15), round(original_dim*0.1)] # Set dimensions for the Autoencoder

    print(len(training_data), "Amount of training data. ")



    training_data = training_data/np.max([0,1])
    testing_data = testing_data / np.max([0, 1])
    ''' Making the training/testing data to a np structure, so it can be reshaped.'''


    training_data = training_data.reshape(training_data.shape[0],1 , training_data.shape[1])
    '''Give the data "new shape", instead of [60000, 28, 28] -> 60000, 28*28,
    to be able to feed it to the ANN as a columnvector. 
    https://www.tensorflow.org/api_docs/python/tf/reshape'''

    print('-----------')

    training_features = training_data.astype('float32')
    '''Make the features to floats, unsure if this really is necessary. '''
    print(type(training_features[0][0]), "type of training_features")
    print('------------------')


    autoencoder = Autoencoder(hidden_dim=hidden_dim, original_dim=original_dim)
    """Create the autoencoder"""



    optimizer = tf.optimizers.Adam(learning_rate=learning_rate)
    """Make an optimizer"""

    autoencoder.compile(optimizer, loss=tf.keras.losses.MeanSquaredError())
    """Compile the autoencoder, .compile is a built in function"""

    autoencoder.fit(training_features, training_features, batch_size, epochs, 2)
    """The actual training of the network. .fit is also a biult in model """

    #print("wöö", flush=True)

    #writer = tf.summary.create_file_writer('runs\\runs' + date)
    """Writes to file that can be viwed in tesorboard. Was used for MNIST, not our actual data."""


    weights = optimizer.get_weights()
    autoencoder.save_weights('saves\\50-15-15-50_all_data_new')
    """Save the weigths to be able to use them at any time.  """

    autoencoder.summary()
    """Print some info about the structure"""

    #print(weights[0])

    """All below is in case of testing, can be ignored. """
    if dbg:
        newAutoencoder = Autoencoder(hidden_dim=hidden_dim, original_dim=original_dim)
        newAutoencoder.load_weights('saves\\50-25-10-25-50_komp_more_data')

        im_ind = 0

        testdata = testing_data[im_ind].reshape(testing_data[im_ind].shape[1], testing_data[im_ind].shape[0])

        rec = newAutoencoder(tf.constant(testdata))
        rec = rec.numpy()
        rec = rec.reshape(rec.shape[1], rec.shape[0])

        plt.plot(rec)
        plt.show()
        plt.plot(testing_data[im_ind])
        plt.show()
    else:
        pass
else:
    pass

