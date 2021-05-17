"""Importing necessary modules"""

import json

import cv2
import numpy as np
import pytesseract as pt
from utils.difFixer import fix_string as fx

def write_json(data, filename="data.json"):
    """ Function to write a json file"""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def fetch_data(img):
    image = np.array(img)
    image = np.uint8(image)
    gray = np.bitwise_or(image == (164,239,249), image == (204,255,255))
    gray = np.all(gray!= (0,255,0),2)
    gray = gray.astype(np.uint8) * 255
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    gray = cv2.threshold(blur, 140, 255, cv2.THRESH_BINARY)[1]
    cv2.imwrite('bleh.png', gray)
    cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
    boxes = []
    cnts.reverse()
    data = list()
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        boxes.append([x, y, x + w, y + h])
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        crop = gray[y: y + h, x: x + w]
        text = pt.image_to_string(crop)
        if text == "-" or text == "\f":
            continue
        else:
            text = fx(text)
            print(text)
            data.append(text)

    write_json(data)
    # returning data
    return {"Slots": data}
