import cv2
import numpy as np

def is_water_pixel(hsv_pixel):
    # Water typically has a hue in the blue range (~90-140 in HSV)
    h, s, v = hsv_pixel
    return 90 <= h <= 140 and s > 30 and v > 30

def detect_waterline_and_mask(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    height, width = hsv.shape[:2]
    waterline = np.zeros(width, dtype=int)

    for col in range(width):
        for row in range(height):
            if is_water_pixel(hsv[row, col]):
                waterline[col] = row
                break
        else:
            waterline[col] = height  # No water detected, keep all

    # Create mask: everything above waterline is black
    mask = np.zeros((height, width), dtype=np.uint8)
    for col in range(width):
        mask[waterline[col]:, col] = 255

    # Apply mask
    result = cv2.bitwise_and(image, image, mask=mask)
    return result

# Load and process image
image = cv2.imread("/Users/abdullahasif/Documents/University/Sem_6/dl/proj/FloW_IMG/new_test/images/000002.jpg")
masked = detect_waterline_and_mask(image)
cv2.imwrite("masked_water_only.jpg", masked)
