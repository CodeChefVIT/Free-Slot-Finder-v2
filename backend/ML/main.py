"""Import necessary modules"""

import cv2
import numpy as np
import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from starlette.middleware.cors import CORSMiddleware
from tableDetection import fetch_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def testing():
    """Check if server is working"""
    return "Ok! Working!"


@app.post("/uploadfile/")
async def predict_api(file: UploadFile = File(...)):
    """Upload timetable"""
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png", "JPG", "PNG")
    if not extension:
        raise HTTPException(
            status_code=400, detail="File must be an image, in jpg or png format!"
        )

    image = await file.read()
    nparr = np.fromstring(image, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    data = fetch_data(img)
    return data


if __name__ == "__main__":
    uvicorn.run(app, debug=True)
