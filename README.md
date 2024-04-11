# 📝 Text to 3D Model Conversion Web Application

This is a web application that allows users to create images from text prompts and convert those images into 3D models. It uses Hugging Face's text-to-image model for image generation and OpenAI's DPT model for depth estimation.

## ✨ Features

- Users can enter a text prompt.
- Upon clicking the "Generate" button, the application converts the text prompt into an image.
- The generated image is displayed to the user.
- Users can download the generated image.
- Users can view the depth map of the generated image.
- Users can download a 3D model of the image.

## 🛠️ Technologies Used

- Python (Flask framework)
- HTML
- CSS
- JavaScript

## 🚀 Installation

1. Clone this repository to your local machine.
2. Install the required Python packages using pip:
   - pip install -r requirements.txt
3. Run the Flask application:
   - python app.py
4. Access the application in your web browser at http://localhost:5000.

## 💡 Usage

1. Enter a text prompt in the input field.
2. Click the "Generate" button.
3. Wait for the image to be generated.
4. Once the image is generated, it will be displayed on the page.
5. You can download the generated image by clicking the "Download Generated Image" button.
6. To view the depth map of the image, click the "View Depth Map" button.
7. To download a 3D model of the image, click the "Download 3D Model" button.

## 🙌 Credits

- This project uses Hugging Face's text-to-image model for image generation.
- The depth estimation feature is powered by OpenAI's DPT model.
- Image to 3D conversion is achieved using depth estimation and point cloud generation techniques.
