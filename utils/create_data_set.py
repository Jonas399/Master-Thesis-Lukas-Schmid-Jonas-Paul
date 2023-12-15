"""
create_data_set.py

Data Set Generator for the Preprocessing Algorithms used in the Jupyter Notebooks for Model Construction

Variables:

image_folder:   String  | Location where the unstructured Data is stored
target_folder:  String  | Location where the newly structured Data Set will be stored
image_amount:   Integer | Number of Images created during Dataaquisition per Measurement Value

"""

import os
import re
from PIL import Image

class CreateDataSet:
    def __init__(self, image_folder, target_folder, image_amount):
        self.image_folder = image_folder
        self.target_folder = target_folder
        self.image_amount = image_amount


        self.create_data_set(self.image_folder, self.target_folder, self.image_amount)

    # Define function to use the Integer Measurement Value as key for sorting both lists
    def get_key(self, item):
        return int(item[0])

    # Define function to Create a structured Data Set
    def create_data_set(self, image_folder_path, target_folder, image_amount_per_session):
        # Declare Image Path
        image_path = os.listdir(image_folder_path)
        image_list = []
        
        # Fill new List with renamed Filenames, where only the numbers remain
        for file in image_path:
            file = re.sub("image", "", file)
            file = re.sub(".jpg", "", file)
            image_list.append(file)

        # Connect the two Lists, 1. Filenames/ 2. Filenumbers and sort them based on their correspondive Integer Value
        image_path = [x for _,x in sorted(zip(image_list, image_path), key=self.get_key)]

        # Create new Folder for sorted Images
        os.mkdir("../Bilder/Manometer/{}".format(target_folder))
        
        # Iterate 101 Times to Create one Folder for each Measurement Value
        for number in range(20):
            os.mkdir("../Bilder/Manometer/{}/{}".format(target_folder, number))

            # Iterate X Times to add the same amount of Photos to the Measurement Photo Values
            for entry in range(image_amount_per_session):
            
                # Open the Images at their current Location and Place them in sorted Order within their new Location
                image = Image.open("{}/{}".format(image_folder_path, image_path[entry]))
                image.save("../Bilder/Manometer/{}/{}/{}.jpg".format(target_folder, number, entry))
            
            # Delete X names of the image_path list to continue sorting images with differing values
            del image_path[:image_amount_per_session]


path = "../Bilder/Manometer/Manometer0711 unlabeled"
target = "Manometer0711 Labeled"
image_amount = 50

CreateDataSet(path, target, image_amount)
