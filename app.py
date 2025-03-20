from flask import Flask, render_template, request, send_from_directory, jsonify
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import os
import uvicorn

# Flask + FastAPI combo server
flask_app = Flask(__name__)
fast_api = FastAPI()

# CORS Enable
fast_api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Kahin bhi host kar sakta hai
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static folder
UPLOAD_FOLDER = "static"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
flask_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Flask route for HTML page
@flask_app.route('/')
def index():
    return render_template('index.html')

# FastAPI route for cropping image
@fast_api.post("/crop")
async def crop_image(
    file: UploadFile = File(...), 
    x: int = 0, y: int = 0, 
    w: int = 200, h: int = 200
):
    try:
        image = Image.open(file.file)
        cropped = image.crop((x, y, x + w, y + h))

        save_path = os.path.join(UPLOAD_FOLDER, f"cropped_{file.filename}")
        cropped.save(save_path)

        return {"message": "Image cropped successfully", "image_url": f"/static/cropped_{file.filename}"}

    except Exception as e:
        return {"error": str(e)}

# Server start
def start_servers():
    import threading
    threading.Thread(target=lambda: uvicorn.run(fast_api, host="0.0.0.0", port=8000)).start()
    flask_app.run(debug=True, port=5000)

if __name__ == '__main__':
    start_servers()
