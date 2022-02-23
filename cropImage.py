import numpy as np
import matplotlib.pyplot as plt

from skimage import io, filters, feature


def crop_card(img_path, debug=False, sigma=4, new_path=None):
    """
    Crops the card image from path provided (img_path) using skimage's sobel filter to identify corners.
    This process requires the background of the image to be a mostly solid color.

    Set debug to True to see a chart of the steps and understand potential failures. Afterwards adjust sigma to fix.
    """
    image = io.imread(img_path)
    filtered = filters.sobel(image)
    filtered = np.sum(filtered, axis=2)
    filtered /= np.max(filtered)

    # Compute the Canny filter given sigma
    edges = feature.canny(filtered, sigma=sigma)

    # Get the min & max indices where an edge is detected
    edge_indices = np.array(np.nonzero(edges))
    y_min, x_min = np.min(edge_indices, axis=1)
    y_max, x_max = np.max(edge_indices, axis=1)

    margin = 80
    cropped = image[y_min-margin:y_max+margin, x_min-margin:x_max+margin]

    if cropped.shape[1] > cropped.shape[0]:
        cropped = np.rot90(cropped)

    # Initialize a variable saying the operation has not failed - will be switched if debugging sigma does not work
    # Needed to skip plotting
    failed = False
    if new_path is None:
        io.imsave(img_path, cropped)
    else:
        try:
            io.imsave(new_path, cropped)
        except IndexError:  # When iterating upon sigma sometimes the cropped image is nothing and throws error
            failed = True  # Skip the faulty sigma value

    if debug and not failed:
        fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(16, 9))

        ax[0, 0].imshow(filtered, cmap='gray')
        ax[0, 0].set_title('Filtered Image', fontsize=20)

        ax[0, 1].imshow(edges, cmap='gray')
        ax[0, 1].set_title(r'Canny Filter, $\sigma={}$'.format(sigma), fontsize=20)

        ax[1, 0].imshow(image, cmap='gray')
        ax[1, 0].set_title('Starting Image', fontsize=20)

        ax[1, 1].imshow(cropped, cmap='gray')
        ax[1, 1].set_title('Cropped Image', fontsize=20)

        for a in ax.flatten():
            a.axis('off')

        fig.tight_layout()
        plt.show()
