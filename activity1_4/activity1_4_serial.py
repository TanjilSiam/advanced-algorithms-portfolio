import os
import time
import face_recognition
from PIL import Image
import numpy as np
import cv2

def load_rgb8_strict(path: str):
    """
    Load image in RGB, uint8, contiguous form.
    Falls back to OpenCV if Pillow cannot decode.
    """
    try:
        img = Image.open(path).convert("RGB")
        arr = np.asarray(img, dtype=np.uint8)
        return np.ascontiguousarray(arr)
    except Exception:
        bgr = cv2.imread(path)
        if bgr is None:
            raise FileNotFoundError(f"Cannot load: {path}")
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        return np.ascontiguousarray(rgb, dtype=np.uint8)

start = time.time()

# Load known face
known_path = "dataset/task1_4/known_man.jpg"
known_image = load_rgb8_strict(known_path)

# Use CNN detector for tiny faces
known_locs = face_recognition.face_locations(
    known_image,
    number_of_times_to_upsample=2,
    model="cnn"
)

known_encs = face_recognition.face_encodings(
    known_image,
    known_face_locations=known_locs,
    num_jitters=1
)

if not known_encs:
    raise RuntimeError("No face found in known_man.jpg using CNN.")

known_encoding = known_encs[0]

# Scan images
folder = "dataset/task1_4/imageset/"
filenames = [f.name for f in os.scandir(folder) if f.is_file()]

for filename in filenames:
    img_path = folder + filename

    try:
        unknown_image = load_rgb8_strict(img_path)
    except Exception as e:
        print(f"Skipping {filename}: {e}")
        continue

    unknown_locs = face_recognition.face_locations(
        unknown_image,
        number_of_times_to_upsample=1,
        model="cnn"
    )

    unknown_encs = face_recognition.face_encodings(
        unknown_image,
        known_face_locations=unknown_locs
    )

    for enc in unknown_encs:
        if face_recognition.compare_faces([known_encoding], enc):
            print("Match found! in " + filename)
            break

print("Elapsed seconds:", time.time() - start)