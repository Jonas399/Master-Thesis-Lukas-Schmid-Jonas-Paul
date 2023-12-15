"""
image_display.py

Display Images after Preprocessing and Data Augmentation

Variables:

images: 	List    | Arrays of Image Data
labels: 	List    | Measurement Values of Image Data
grey_scale: Boolean | Determines wether Grey Scale Preprocessing was applied

"""

import matplotlib.pyplot as plt

class imageDisplay:
    def __init__(self, images, labels, grey_scale) -> None:
        self.images = images
        self.labels = labels
        self.grey_scale = grey_scale

        self.display_images(self.images, self.labels, self.grey_scale)

    def display_images(self, images_test, labels_test, grey_scale):
        if grey_scale == False:

            # Show graphics
            fig=plt.figure(figsize=(16, 16))
            columns = 4
            rows = 4
            for i in range(1, columns*rows +1):
                ax = fig.add_subplot(rows, columns, i)
                ax.title.set_text(labels_test[(i-1)])

                # Pre-process input for display (invert)
                image_test = images_test[(i-1)]
                mean = [100, 100, 100]
                for idx in range(3):
                    image_test[:, :, idx] = (image_test[:, :, idx] + mean[idx]) / 255
                image_test = image_test[..., ::-1]

                plt.axis('off')
                plt.imshow(image_test)
            plt.tight_layout()
            plt.show()
        
        else:

            # Show graphics
            fig=plt.figure(figsize=(16, 16))
            columns = 4
            rows = 4
            for i in range(1, columns*rows +1):
                ax = fig.add_subplot(rows, columns, i)
                ax.title.set_text(labels_test[(i-1)])

                # Pre-process input for display (invert)
                image_test = images_test[(i-1)]
                mean = [1, 1, 1]
                for idx in range(1):
                    image_test[:, :, idx] = (image_test[:, :, idx] + mean[idx]) #/ 255
                image_test = image_test[..., ::-1]

                plt.axis('off')
                plt.imshow(image_test)
            plt.tight_layout()
            plt.show()
        return