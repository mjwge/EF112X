# EF112X
Relevant code for B.Sc. Project in machine learning by Martin Gelin &amp; Rikard Fridsén Skogsberg at KTH, Sweden

The project was aimed towards evaluating Artificial Neural Networks in the structure of an Autoencoder as a way of detecting anomalies
in the drinking water distribution network.  

Quick explanation of the files:

MATLAB: 


  Convert.m: Convert to an earlier version of .mat files that python can process easier. 
  
  datacomp_temp.m: Compensate and eliminate influence of temperature on the measurements, using linear estimator. 
  
  datacompilation.m: Make the input vectors used for the ANN. 
  
  misc_komp.m: Compensate and eliminate influences of all given factors in a simultaneous fashion. 
  
  sequential_komp.m: Compensate and eliminate influences of all given factors in a sequential fashion.
  
  tempkomp.m: Function used by other scripts for eliminating temperature influence. 
  
 
Python:

  AE_training.py: Main program where the Autoencoder is created, trained and the weights are saved for future use. 
  
  anomaly_data_creation.py: Create data with manually added anomalies. 
  
  anomaly_testing.py: Test the ANNs capability to detect anomalie, using deviation based anomaly detection. 
  
  autoencoder_2hidden.py: Contains the class of the Autoencoder which is used in the project, with related loss and train              functions.
  
  data_creation.py: Create all datasets used to train and test the ANN. No anomalies is added, all data is natural. 
  

