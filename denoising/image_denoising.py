import cv2
import os

def denoise_image(image_path, denoise_method='fastNlMeansDenoisingColored'):
    image = cv2.imread(image_path)
    # denoised_image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

    if denoise_method == 'fastNlMeansDenoisingColored':
        denoised_image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    elif denoise_method == 'GaussianBlur':
        sigma = 1.5
        denoised_image = cv2.GaussianBlur(image, (5, 5), sigma)
    elif denoise_method == 'medianBlur':
        kernel_size = 3
        denoised_image = cv2.medianBlur(image, kernel_size)
    else:
        raise ValueError("Unknown denoising method")
    
    # Ensure the output path is in the media directory
    base_dir = os.path.dirname(image_path)
    output_filename = 'denoised_' + os.path.basename(image_path)
    output_path = os.path.join(base_dir, output_filename)
    
    cv2.imwrite(output_path, denoised_image)
    return output_filename  # Return the filename, not the full path