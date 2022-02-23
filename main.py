from listingToEbay import create_listing
from imagesInFile import get_img_paths
from cropImage import crop_card
from imageToEbay import uploadPictureFromFilesystem

import os
import shutil
import pandas as pd

# TODO: Threading can likely make this much faster

# Settings
debug = True
crop_images = False
# Path Variables, IDs, etc.
EXCEL_SHEET_PATH = "EXCEL_SHEET_PATH"  # Must have columns: name, price, column
IMGS_PATH = "UNLISTED_IMAGES_PATH"  # Path to the folder containing the unedited, unlisted images
# Must be in the same order as the excel sheet
LISTED_IMGS_PATH = "LISTED-IMAGES_PATH"  # Path to folder where the listed images will be sorted into sub-folders

# Get list of each image path from path of images file
img_paths = get_img_paths(IMGS_PATH)
if crop_images:
    # Crop Each Image
    list(map(crop_card, img_paths))

# Upload each image to eBay Picture Service (EPS) get a list of all the links
links = list(map(uploadPictureFromFilesystem, img_paths))
# TODO: Catch eBay internal error #10007 and just try again - means error on their side

# Unpack the unlisted card data
data = pd.read_excel(EXCEL_SHEET_PATH)
num_cards = len(data)


# Make sure there are 2 images per card listing (front & back)
if len(links) != 2 * num_cards:
    print("There are {} images".format(len(links)))
    print("There are {} cards".format(num_cards))
    raise ValueError("There are 2 not images per card listing.")

# TODO: Ensure titles are all less than 80 characters before beginning to list

# Post the listings to eBay, move the images to the Listed cards file
for n in range(num_cards):
    # Get the data for the current card
    name, price, title = data.loc[n]
    title = title.replace("&", "&amp;")  # Replace & or xml will try to execute logic
    img_urls = links[:2]
    del links[:2]
    # Create the listing
    if debug:
        print("Now listing: \n{}\n".format(title))

    create_listing(title, price, img_urls)
    
    # Move images to Listed cards area
    new_fold_name = name.replace('/', '.')
    destination = LISTED_IMGS_PATH + "\\" + new_fold_name
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    for _ in range(2):
        source = img_paths[0]
        shutil.move(source, destination)
        del img_paths[0]


# Move the listed card data to the "Listed" excel sheet
listed_data = pd.read_excel(EXCEL_SHEET_PATH, sheet_name="Listed")
listed_data = listed_data.append(data, ignore_index=True)
empty_data = pd.DataFrame(columns=listed_data.columns)
with pd.ExcelWriter(EXCEL_SHEET_PATH) as writer:
    empty_data.to_excel(writer, sheet_name="Unlisted", index=False)
    listed_data.to_excel(writer, sheet_name="Listed", index=False)

#"""