# coding=utf-8
from io import BytesIO
from PIL import Image
import os
import json
import numpy as np
position = [39, 38, 48, 49, 41, 40, 46, 47, 35, 34, 50, 51, 33, 32, 28, 29, 27, 26, 36, 37, 31, 30, 44, 45, 43, 42, 12, 13, 23, 22, 14, 15, 21, 20, 8, 9, 25, 24, 6, 7, 3, 2, 0, 1, 11, 10, 4, 5, 19, 18, 16, 17]
tracks_path = os.path.join(os.path.dirname(__file__), "tracks.json")
with open(tracks_path, "r") as f:
    tracks = json.load(f)

def get_standard_img(content):
    image = Image.open(BytesIO(content))
    standard_img = Image.new("RGBA", (260, 160))
    s, u = 80, 10
    for c in range(52):
        a = position[c] % 26 * 12 + 1
        b = s if position[c] > 25 else 0
        im = image.crop(box=(a, b, a + 10, b + 80))
        standard_img.paste(im, box=(c % 26 * 10, 80 if c > 25 else 0))
    return standard_img


def get_gap_position(image):
    """横向连续40个像素点像素值小于100，100，100"""
    array = np.delete(np.array(image), -1, 2)
    height, width, _ = array.shape
    for threshold in range(40, 120, 10):
        for y in range(height - 40):
            for x in range(60, width - 40):
                if np.all(array[y:y + 1][x:x + 15] < threshold) and np.all(array[y:y + 15, x:x + 1] < threshold):
                    return x, y
    return False

def get_track(offset):
    for track in tracks:
        if offset == track[-1][0]:
            return track