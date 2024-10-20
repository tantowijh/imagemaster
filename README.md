# Image Restoration and Denoising

This project is a Django-based web application that allows users to upload images, draw masks on them, and perform image restoration and denoising. The application uses OpenCV for image processing and provides a user-friendly interface for interacting with the images.

## Features

- **Image Upload**: Users can upload images for processing.
- **Mask Drawing**: Users can draw masks on the uploaded images using a canvas.
- **Image Restoration**: The application can restore images using the drawn masks.
- **Image Denoising**: The application provides various denoising methods to improve image quality.
- **Session Management**: The application manages user sessions to keep track of uploaded and processed images.
- **Media Cleanup**: The application can delete all media files and clear sessions when triggered.

## Requirements

- Python 3.x
- Django 5.1.2
- Django Tailwind 3.8.0
- OpenCV 4.10.0.84
- Pillow 11.0.0
- Django Widget Tweaks 1.5.0
- Node.js 14.x or higher
- npm 6.x or higher

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/tantowijh/imagerestoration.git
    cd imagerestoration
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt

4. **Install Tailwind CSS**:
    ```sh
    python manage.py tailwind install
    ```

5. **Build the CSS**:
    ```sh
    python manage.py tailwind build
    ```

6. **Apply migrations**:
    ```sh
    python manage.py migrate
    ```

7. **Run the development server**:
    ```sh
    python manage.py runserver
    ```

## Usage

1. **Upload Image**: Navigate to the upload page and upload an image.
2. **Draw Mask**: Draw a mask on the uploaded image using the canvas.
3. **Restore Image**: Click the "Start Restoring" button to restore the image using the drawn mask.
4. **Denoise Image**: Select a denoising method and apply it to the image.
5. **Cleanup Media**: Click on the navigation menu to delete all media files and clear sessions.

## Project Structure

- `imagerestoration/`: Main project directory.
- `denoising/`: App for image denoising.
- `restoration/`: App for image restoration.
- `templates/`: Directory for HTML templates.
- `static/`: Directory for static files (CSS, JS, images).
- `media/`: Directory for uploaded and processed images.
- `requirements.txt`: List of project dependencies.
- `README.md`: Project documentation.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [OpenCV](https://opencv.org/)
- [Pillow](https://python-pillow.org/)
- [Django Tailwind](https://django-tailwind.readthedocs.io/)
- [Django Widget Tweaks](https://github.com/jazzband/django-widget-tweaks)