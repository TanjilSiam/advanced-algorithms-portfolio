import os
import time
import face_recognition
from PIL import Image
import numpy as np
import cv2
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

def load_rgb8_strict(path: str):
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

KNOWN_ENCODING = None

def init_worker(encoding):
    global KNOWN_ENCODING
    KNOWN_ENCODING = encoding

def check_image(filepath: str):
    filename = os.path.basename(filepath)

    try:
        img = load_rgb8_strict(filepath)
    except Exception as e:
        return ("error", filename, f"load failed: {e}")

    locs = face_recognition.face_locations(
        img,
        number_of_times_to_upsample=1,
        model="cnn"
    )

    encs = face_recognition.face_encodings(
        img,
        known_face_locations=locs
    )

    for enc in encs:
        if face_recognition.compare_faces([KNOWN_ENCODING], enc):return ("match", filename)

    return ("nomatch", filename)

if __name__ == "main":
    known_path = "dataset/task1_4/known_man.jpg"
    imageset = "dataset/task1_4/imageset/"

    t0 = time.time()

    known_image = load_rgb8_strict(known_path)

    known_locs = face_recognition.face_locations(
        known_image,
        number_of_times_to_upsample=2,
        model="cnn"
    )

    encs = face_recognition.face_encodings(
        known_image,
        known_face_locations=known_locs,
        num_jitters=1
    )

    if not encs:
        raise RuntimeError("No face found in known_man.jpg using CNN.")

    known_encoding = encs[0]

    filepaths = [str(p) for p in Path(imageset).iterdir() if p.is_file()]

    matches = []
    errors = []

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as ex:
        futures = {ex.submit(check_image, fp): fp for fp in filepaths}
        init_worker(known_encoding)

        for fut in as_completed(futures):
            status, filename, *rest = fut.result()

            if status == "match":
                print("Match found! in " + filename)
                matches.append(filename)
            elif status == "error":
                errors.append((filename, rest[0]))

    elapsed = time.time() - t0

    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)
    summary = out_dir / "matches.txt"

    with open(summary, "w") as f:
        f.write(f"Elapsed: {elapsed:.2f} sec\n\n")
        f.write("Matches:\n")
        for m in matches:
            f.write(m + "\n")
        f.write("\nErrors:\n")
        for fname, msg in errors:
            f.write(f"{fname} : {msg}\n")

    print("\nParallel done.")
    print("Matches:", len(matches))
    print("Time:", elapsed)
    print("Summary saved to output/matches.txt")