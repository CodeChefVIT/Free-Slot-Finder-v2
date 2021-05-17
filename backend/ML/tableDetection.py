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

def fetch_data(image):
    gray = []
    print(image.shape)
    for i in range(0, image.shape[0]):
        ex = []
        for j in range(0, image.shape[1]):
            if 140 <= image[i][j][0] <= 255:
                if 220 <= image[i][j][1] <= 255:
                    if 239 <= image[i][j][2] <= 255:
                        ex.append(True)
                        continue
            ex.append(False)
        ex = np.asarray(ex)
        gray.append(ex)
    image = np.array(image)
    image = np.uint8(image)
    gray = np.asarray(gray)
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
        text = text.strip("\n")
        if text == "-" or text == "\f" or len(text)>5:
            continue
        else:
            text = fx(text)
            print(text)
            data.append(text)

    write_json(data)
    # returning data
    return {"Slots": data}
