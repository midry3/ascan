import os
import sys

import cv2
import numpy as np
from PIL import Image

def extract_black_lines(input_path, output_path, canvas_size):
    image = cv2.imread(input_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    binary = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV, 15, 10
    )
    alpha = binary.copy()
    line_img = np.zeros((binary.shape[0], binary.shape[1], 4), dtype=np.uint8)
    line_img[:, :, 0] = 0
    line_img[:, :, 1] = 0
    line_img[:, :, 2] = 0
    line_img[:, :, 3] = alpha
    pil_img = Image.fromarray(line_img)
    canvas = Image.new("RGBA", canvas_size, (255, 255, 255, 0))
    img_w, img_h = pil_img.size
    offset = ((canvas_size[0] - img_w) // 2, (canvas_size[1] - img_h) // 2)
    canvas.paste(pil_img, offset, pil_img)
    canvas.save(output_path)
    print(f"saved: {output_path}")

def main():
    if "-h" in sys.argv or "--help" in sys.argv or len(sys.argv) == 1:
        print("""Usage:
    ascan [input] [output] [width] [height]""")
    else:
        dst = sys.argv[2]
        if os.path.splitext(dst)[1] != ".png":
            dst = dst.rstrip(".") + ".png"
        extract_black_lines(sys.argv[1], dst, canvas_size=(int(sys.argv[3]), int(sys.argv[4])))

if __name__ == "__main__":
    main()