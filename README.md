# Image Restoration and Denoising

This project is a Django-based web application that allows users to upload images, draw masks on them, and perform image restoration and denoising. The application uses OpenCV for image processing and provides a user-friendly interface for interacting with the images. Additionally, it leverages Google Colab for running GPU-intensive tasks like Stable Diffusion and Real-ESRGAN.

## Features

- **Image Upload**: Users can upload images for processing.
- **Mask Drawing**: Users can draw masks on the uploaded images using a canvas.
- **Image Restoration**: The application can restore images using the drawn masks.
- **Image Denoising**: The application provides various denoising methods to improve image quality.
- **Stable Diffusion**: Leverages Google Colab for running Stable Diffusion tasks.
- **Real-ESRGAN**: Leverages Google Colab for running Real-ESRGAN tasks.
- **Session Management**: The application manages user sessions to keep track of uploaded and processed images.
- **Media Cleanup**: The application can delete all media files and clear sessions when triggered.

## Requirements

- Python 3.12.x
- Django 5.1.2
- Django Tailwind 3.8.0 (or django-tailwind[reload])
- OpenCV 4.10.0.84
- Pillow 11.0.0
- Django Widget Tweaks 1.5.0
- Requests 2.32.3
- Python Dotenv 1.0.1
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
    source venv/bin/activate    # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Copy the environment variables**:
    ```sh
    cp .env.example .env    # On Windows use `copy .env.example .env`
    ```

5. **See the usage section to set up the Google Colab API**.
    ```sh
    # Add the provided URL to the .env file:
    COLAB_API_URL=<your_colab_api_url>
    ```

6. **Install Tailwind CSS**:
    ```sh
    python manage.py tailwind install
    ```

7. **Build the CSS**:
    ```sh
    python manage.py tailwind build
    ```

8. **Apply migrations**:
    ```sh
    python manage.py migrate
    ```

9. **Run the development server**:
    ```sh
    python manage.py runserver
    ```

## Google Colab API Setup

To use the Google Colab API for running Stable Diffusion and Real-ESRGAN tasks, follow these steps:

1. **Open the provided Jupyter notebook**:
    - The notebook file is located in the project directory. Open it in Google Colab.
    - Make sure to run the notebook with Google Colab's GPU runtime.

2. **Run the notebook**:
    - Follow the instructions in the notebook to set up the API. This will provide you with a URL.

3. **Update the `.env` file**:
    - Add the provided URL to the `.env` file in the project directory:
    ```env
    COLAB_API_URL=<your_colab_api_url>
    ```

4. **Restart the Django server**:
    - Restart the Django development server to apply the changes.

## Usage

1. **Upload Image**: Navigate to the upload page and upload an image.
2. **Draw Mask**: Draw a mask on the uploaded image using the canvas.
3. **Restore Image**: Click the "Start Restoring" button to restore the image using the drawn mask.
4. **Denoise Image**: Select a denoising method and apply it to the image.
5. **Run Stable Diffusion**: Use the provided interface to run Stable Diffusion tasks via the Google Colab API.
6. **Run Real-ESRGAN**: Use the provided interface to run Real-ESRGAN tasks via the Google Colab API.
7. **Cleanup Media**: Click on the navigation menu to delete all media files and clear sessions.

## Project Structure

- `imagerestoration/`: Main project directory.
  - `__init__.py`: Initialization file for the project.
  - `asgi.py`: ASGI configuration for the project.
  - `settings.py`: Settings and configuration for the project.
  - `urls.py`: URL routing for the project.
  - `wsgi.py`: WSGI configuration for the project.
- `denoising/`: App for image denoising.
  - `__init__.py`: Initialization file for the app.
  - `admin.py`: Admin configuration for the app.
  - `apps.py`: App configuration.
  - `forms.py`: Forms used in the app.
  - `image_denoising.py`: Image denoising logic.
  - `migrations/`: Database migrations.
  - `models.py`: Database models.
  - `templates/`: HTML templates for the app.
  - `tests.py`: Unit tests for the app.
  - `urls.py`: URL routing for the app.
  - `views.py`: Views for the app.
- `enhancement/`: App for image enhancement.
  - Similar structure to `denoising/`.
- `restoration/`: App for image restoration.
  - Similar structure to `denoising/`.
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
- [Stable Diffusion](https://github.com/CompVis/stable-diffusion)
- [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN)