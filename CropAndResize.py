import cv2
import os
import sys
from pathlib import Path

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def process_images(input_folder, output_folder):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    ensure_dir(output_folder)

    for subdir, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(subdir, file)
                img = cv2.imread(img_path)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    # Expand the crop area to include some hair above the face
                    expansion = int(h * 0.2)
                    x_new, y_new = max(0, x), max(0, y - expansion)
                    w_new, h_new = w, h + expansion

                    # Adjust coordinates to maintain 2:3 aspect ratio
                    if h_new * 2 / 3 > w_new:
                        w_new = int(h_new * 2 / 3)
                        x_new = max(0, x + w // 2 - w_new // 2)
                    else:
                        h_new = int(w_new * 3 / 2)
                        y_new = max(0, y + h // 2 - h_new // 2)

                    crop_img = img[y_new:y_new + h_new, x_new:x_new + w_new]
                    final_img = cv2.resize(crop_img, (600, 900))  # Resize to standard size

                    # Prepare output path
                    rel_path = os.path.relpath(subdir, input_folder)
                    output_subdir = os.path.join(output_folder, rel_path)
                    ensure_dir(output_subdir)
                    cv2.imwrite(os.path.join(output_subdir, file), final_img)
                    break  # Process only the first detected face

if __name__ == "__main__":
    input_dir = sys.argv[1]
    output_dir = 'Output_' + input_dir
    process_images(input_dir, output_dir)
