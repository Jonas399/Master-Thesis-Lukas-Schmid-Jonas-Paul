"""
transform_data.py

Scale Image and Target Data

Variables:

data:               Array | Numpy Array containing the data to be scaled. This can be the train data or its labels
mean_value          Float | Mean Value of the corresponding data to the data
standard_deviation  Float | Standard Deviation of the corresponding data

"""
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler



class transformData:

    # Z-Score Scaling
    def calc_standard_deviation_mean(self, data=None):
        mean_value = np.mean(data)
        standard_deviation = np.std(data)

        return mean_value, standard_deviation
    
    def scale_z_score(self, data=None, mean_value=None, standard_deviation=None):
        data = (data - mean_value) / standard_deviation

        return data

    def rescale_z_score(self, data=None, mean_value=None, standard_deviation=None):
        data = data + mean_value * standard_deviation

        return data
    
    # Min Max Scaling
    def calc_min_max(self, data=None):
        max_value = np.max(data)
        min_value = np.min(data)

        return min_value, max_value

    def scale_min_max(self, data=None, min_value=None, max_value=None):
        data = (data-min_value)/(max_value - min_value)

        return data

    # Does not work yet
    def rescale_min_max(self, data=None, min_value=None, max_value=None):
        #print("Max in Function:", data)
        data = (data+min_value)#*(max_value + min_value)
        #print(data)
        return data

