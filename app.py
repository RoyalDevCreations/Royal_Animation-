from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from PIL import Image
import os

# FastAPI app
app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static folder setup
UPLOAD_FOLDER = "static/cropped"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML route
@app.get("/", response_class=HTMLResponse)
async def index():
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read())

# Crop API
@app.post("/crop")
async def crop_image(
    file: UploadFile = File(...),
    x: int = Form(...),
    y: int = Form(...),
    w: int = Form(...),
    h: int = Form(...)
):
    try:
        image = Image.open(file.file)

        # Crop
        cropped = image.crop((x, y, x + w, y + h))

        # Save the cropped image
        save_path = os.path.join(UPLOAD_FOLDER, f"cropped_{file.filename}")
        cropped.save(save_path)

        return JSONResponse(content={"message": "Cropped successfully", "image_url": f"/static/cropped/cropped_{file.filename}"})
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
