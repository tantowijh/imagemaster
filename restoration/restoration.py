import base64
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
import cv2
import os



def perform_restoration(image_filename, mask_data):
    format, imgstr = mask_data.split(';base64,')
    fs = FileSystemStorage()
    mask_data = ContentFile(base64.b64decode(imgstr), name='mask_' + image_filename)
    mask_filename = fs.save(mask_data.name, mask_data)

    # Perform restoration here
    restored_image_filename = restore_image(image_filename, mask_filename)
    return restored_image_filename



def restore_image(image_filename, mask_filename):
    fs = FileSystemStorage()

    # Open the image.
    img = cv2.imread(fs.path(image_filename))
    
    # Load the mask.
    mask = cv2.imread(fs.path(mask_filename), 0)
    
    # Inpaint.
    dst = cv2.inpaint(img, mask, 3, cv2.INPAINT_NS)

    # Ensure the output path is in the media directory
    base_dir = os.path.dirname(fs.path(image_filename))
    output_filename = 'restored_' + os.path.basename(fs.path(image_filename))
    output_path = os.path.join(base_dir, output_filename)
    
    cv2.imwrite(output_path, dst)
    return output_filename
    
