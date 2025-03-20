from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from PIL import Image
import os
import datetime

# FastAPI app
app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static folder
UPLOAD_FOLDER = "static/cropped"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML route
@app.get("/", response_class=HTMLResponse)
async def index():
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read())

# Function to generate unique filename
def generate_unique_filename(filename):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    name, ext = os.path.splitext(filename)
    return f"cropped_{timestamp}_{name}{ext}"

# Image crop API
@app.post("/crop")
async def crop_image(
    file: UploadFile = File(...),
    x: int = Form(...),
    y: int = Form(...),
    w: int = Form(...),
    h: int = Form(...),
    rotate: int = Form(0),
    flip: bool = Form(False)
):
    try:
        # If file is missing, create a dummy white image
        if file is None or file.filename == "":
            width, height = 800, 600
            image = Image.new("RGB", (width, height), color="white")
        else:
            image = Image.open(file.file)

        # Rotate if requested
        if rotate:
            image = image.rotate(rotate, expand=True)

        # Flip image if requested
        if flip:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)

        # Crop image
        cropped = image.crop((x, y, x + w, y + h))

        # Save cropped image with unique filename
        unique_filename = generate_unique_filename(file.filename if file else "dummy.jpg")
        save_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        cropped.save(save_path)

        return {
            "message": "Cropped successfully",
            "image_url": f"/static/cropped/{unique_filename}"
        }

    except Exception as e:
        return {"error": str(e)}
