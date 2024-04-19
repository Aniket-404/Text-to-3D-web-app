import base64
from multiprocessing import process
from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
from transformers import DPTImageProcessor, DPTForDepthEstimation
import torch
import numpy as np
from PIL import Image, UnidentifiedImageError
import open3d as o3d
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load API key from environment variable
HUGGINGFACE_API_KEY = os.environ.get('key', None)
if not HUGGINGFACE_API_KEY:
    raise ValueError('HUGGINGFACE_API_KEY environment variable is not set')

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
STATIC_FOLDER = os.path.join(os.getcwd(), 'static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    data = request.json
    input_text = data['input']
    image_bytes = query_api({"inputs": input_text})
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    return jsonify({'image': encoded_image})

@app.route('/generate_depth', methods=['POST'])
def generate_depth():
    data = request.json
    input_text = data['input']
    
    # Generate image
    image_bytes = query_api({"inputs": input_text})
    image_path = os.path.join(STATIC_FOLDER, 'generated_image.jpg')
    with open(image_path, 'wb') as f:
        f.write(image_bytes)
    
    try:
        image = Image.open(image_path)
    except UnidentifiedImageError:
        return jsonify({'error': 'UnidentifiedImageError', 'message': 'Cannot identify image file. Please try again.'}), 500
    
    # Perform depth estimation
    processor = DPTImageProcessor.from_pretrained("Intel/dpt-beit-large-512")
    model = DPTForDepthEstimation.from_pretrained("Intel/dpt-beit-large-512")
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        predicted_depth = outputs.predicted_depth
    prediction = torch.nn.functional.interpolate(
        predicted_depth.unsqueeze(1),
        size=image.size[::-1],
        mode="bicubic",
        align_corners=False,
    )
    output = prediction.squeeze().cpu().numpy()
    formatted = (output * 255 / np.max(output)).astype("uint8")
    depth = Image.fromarray(formatted)
    
    # Save depth map
    depth_path = os.path.join(STATIC_FOLDER, 'generated_depth.jpg')
    depth.save(depth_path)
    
    # Generate point cloud
    depth_map = np.array(depth)
    color_image = np.array(image)
    fx = 1000
    fy = 1000
    cx = color_image.shape[1] / 2
    cy = color_image.shape[0] / 2
    point_cloud = []
    colors = []
    for v in range(depth_map.shape[0]):
        for u in range(depth_map.shape[1]):
            Z = depth_map[v, u]
            X = (u - cx) * Z / fx
            Y = (v - cy) * Z / fy
            point_cloud.append([X, Y, Z])
            colors.append(color_image[v, u])
    colors = np.array(colors) / 255.0
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(point_cloud)
    pcd.colors = o3d.utility.Vector3dVector(colors)
    output_file_path = os.path.join(STATIC_FOLDER, 'output.ply')
    o3d.io.write_point_cloud(output_file_path, pcd)
    
    # Convert .ply to .obj
    mesh = o3d.io.read_triangle_mesh(output_file_path)
    obj_output_file_path = os.path.join(STATIC_FOLDER, 'output.obj')
    o3d.io.write_triangle_mesh(obj_output_file_path, mesh)
    
    return jsonify({'image': 'generated_image.jpg', 'depth': 'generated_depth.jpg', 'point_cloud': 'output.ply', 'obj_file': 'output.obj'})

def query_api(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.content

@app.route('/images/<path:filename>')
def download_image(filename):
    return send_from_directory(STATIC_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
