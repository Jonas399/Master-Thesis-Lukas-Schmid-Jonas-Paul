"""
preprocessing.py

Preprocessing for Image Data of Measurement Device

Variables:

folder:             String  | Location where the Data Set is stored
is_validation:      Boolean | Determins wether Data loaded is for Training or Validation
grey_scale:         Boolean | Determins wether Grey Scale should be applied
resize_image:       Boolean | Determins wether the Images schould be rescaled
new_size:   	    Touple  | Contains a Touple with the new Size of the Data Set
normalize_image:    Boolean | Determins wether the Data Set should be normalized
thresholding:       Boolean | Determins wether Thresholding should be applied to the Data Set
erosion:            Boolean | Determins wether Erosion should be applied to the Data Set
kernel:             Array   | Contains an array with the to be used Kernel Size
cut_image:          Boolean | Determins wether the Borders should be cut away
z_score_data:       Boolean | Determins wether Z-Score Scaling should be applied to the Image Data
z_score_targets:    Boolean | Determins wether Z-Score Scaling should be applied to the Image Labels

"""

import os
import cv2
import re
from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt


class preprocessImage:
    def __init__(self, folder=None, is_validation=None, grey_scale=None, resize_image=None, new_size=None, normalize_image=None, thresholding=None, erosion=None, kernel=None, cut_image=None, z_score_data=None, z_score_targets=None):
       
        self.folder = folder
        self.is_validation = is_validation
        self.grey_scale = grey_scale
        self.resize_image = resize_image
        self.new_size = new_size
        self.normalize_image = normalize_image
        self.thresholding = thresholding
        self.erosion = erosion
        self.kernel = kernel
        self.cut_image = cut_image
        self.z_score_data = z_score_data
        self.z_score_targets = z_score_targets

    def preprocess_image(self, image, grey_scale=None, resize_image=None, new_size=None, normalize_image=None, thresholding=None, erosion=None, kernel=None, cut_unimportant_stuff=None, turn_image=None):
        

        image = np.array(image)


        #Convert Image to grey scale 
        if grey_scale == True:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)                       
                
        if resize_image == True:
            image = cv2.resize(image, new_size, interpolation=3)
        
        # normalizing the image has to be postponed, to only normalize the train set
        #if normalize_image ==True:                
        #        image = cv2.normalize(image, None, 0, 1.0,cv2.NORM_MINMAX, dtype=cv2.CV_32F)  
        
        # Apply Thresholding
        if thresholding==True:
            ret, image = cv2.threshold(image, 80, 255, cv2.THRESH_TOZERO)
        

        # Apply erosion
        if erosion==True:
            image = cv2.erode(image, kernel, iterations=3)
            #image = cv2.dilate(image, kernel, iterations=1)


        # Cut Image to Further Focus on the scale, now obsolete
        if cut_unimportant_stuff == True:
            image = cv2.rectangle(image, (0, 0), 
                        (100, 225), 
                        (255, 255, 255), -1)

            image =  cv2.rectangle(image, (225, 0), 
                        (300, 225), 
                        (255, 255, 255), -1)
        

        #normalizing the image has to be postponed, to only normalize the train set
        #if normalize_image == True:
        #    image = image/255

        #Turn the Image in 90°
        if turn_image == True:
            image = np.rot90(image,axes=(1,0))

        return image



    
    def load_images(self, folder, is_validation, grey_scale=None, resize_image=None, new_size=None, normalize_image=None, thresholding=None, erosion=None, kernel=None, cut_unimportant_stuff=None, turn_image=None, z_score_data=None, z_score_targets=None):
        #Declare Variable to Hold Path of the Variables in each Folder
        imagePath = ""
        image_list = []
        label_list = []
        print("imageFolderPath: {}".format(folder))
        measurementLocation = os.listdir(folder) 
        
        #Get Structure of Image Folder
        if is_validation==False:
            #measurementLocation.pop()
            #measurementLocation.remove("93")
            
            for entry in measurementLocation:
                imageFolderPath = folder+"/{}".format(entry)
                imagePath = os.listdir(imageFolderPath) 
                print("Load in Data with Values {}".format(entry))
            
                #Iterate over all Images per Measurement Category
                for file in imagePath:
                    #Get Image Path
                    measurement = imageFolderPath + "/{}".format(file)

                    #Get Image
                    image = Image.open(measurement)
                    image = self.preprocess_image(image, grey_scale, resize_image, new_size, normalize_image, thresholding, erosion, kernel, cut_unimportant_stuff, turn_image)
                    
                    
                    #Comment in for Image Display
                    #cv2.imshow(' ',image)
                    #cv2.waitKey(0)
                    #cv2.destroyAllWindows()
                    
                    image_list.append(image)
                
                    #Get Label
                    label_list.append(float(entry))
                    
        else:
            for file in measurementLocation:

                #Get Image Path
                measurement = folder + "/{}".format(file)

                    #Get Image
                image = Image.open(measurement)

                image = self.preprocess_image(image, grey_scale, resize_image, new_size, normalize_image, thresholding, erosion, kernel, cut_unimportant_stuff, turn_image)

                #Comment in for Image Display
                #cv2.imshow(' ',image)
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()

                image_list.append(image)
                
                #Get Label
                #Delete .jpeg
                file = re.sub(".jpg", "", file)
                #Delete (x) Ocurrances
                file = re.sub("\(\d\)", "", file)
                #Delete White Spaces
                file = re.sub(" ", "", file)
                #Swap "," to "."
                file = re.sub(",", ".", file)
                label_list.append(float(file))
                
        image_np = np.asarray(image_list)
        label_np = np.asarray(label_list)
        """
        if z_score_data == True:
            mean_value = np.mean(image_np)
            standard_deviation = np.std(image_np)
            image_np = (image_np - mean_value) / standard_deviation

        if z_score_targets == True:
            mean_value = np.mean(label_np)
            standard_deviation = np.std(label_np)
            label_np = (label_np - mean_value) / standard_deviation
        """
        return image_np, label_np