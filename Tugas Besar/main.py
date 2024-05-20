import time
import cv2
import mss
import numpy as np
import win32api
import mouse
import keyboard
from ultralytics import YOLO

# Inisialisasi model YOLOv8 dengan model yang telah Anda latih
model = YOLO('runs/detect/train/weights/best3.pt')  # Ganti dengan jalur model Anda

# Konfigurasi layar
screenHeight = win32api.GetSystemMetrics(1)
screenWidth = win32api.GetSystemMetrics(0)
width = 960
height = 540
# Definisikan area yang di-capture di pojok kanan bawah
gameScreen = {'top': screenHeight - height, 'left': screenWidth - width, 'width': width, 'height': height}

def checkBomb(bombs_path, object_path, object_width, object_height):
    for bomb_path in bombs_path:
        width_range = abs(bomb_path[0] - object_path[0])
        height_range = abs(bomb_path[1] - object_path[1])
        if height_range <= (object_height * 2.25):
            if width_range == object_width or width_range <= (object_width / 2):
                return True
    return False

def slice(x, y, height):
    """
    Simulates a slicing motion by moving and dragging the mouse.
    This function moves the mouse to the specified (x, y) coordinates and then performs a drag motion.
    """
    # Move to the start position
    mouse.move(x, y, absolute=True)
    
    # Perform the drag operation to simulate a slice
    # Adjusted the drag distance and duration for better slicing simulation
    mouse.drag(x, y, x, y - int(height * 2.25), absolute=True, duration=0.1)

def getRealCoord(center, y, heightObject):
    return (center + (screenWidth - width), y + heightObject)

with mss.mss() as sct:
    while True:
        # Screenshot
        screen = np.array(sct.grab(gameScreen))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
        
        # Resize image to reduce processing load
        small_screen = cv2.resize(screen, (width // 2, height // 2))

        # Object Detection
        start = time.time()
        results = model(small_screen, conf=0.4)
        end = time.time()

        bombs_path = []
        fruits_path = []

        for result in results:
            boxes = result.boxes
            for box in boxes:
                classid = int(box.cls[0])
                score = box.conf[0]
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                width_box = x2 - x1
                height_box = y2 - y1

                # Center Object
                center = x1 + int(width_box / 2)
                start_point = getRealCoord(center * 2, y1 * 2, height_box * 2)

                # Object Color
                color = (0, 255, 0) if classid == 0 else (0, 0, 255)
                label = "%s : %.2f" % (model.names[classid], score)

                # Draw Box Object Detection
                cv2.rectangle(screen, (x1 * 2, y1 * 2), (x2 * 2, y2 * 2), color, 2)
                cv2.putText(screen, label, (x1 * 2, y1 * 2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                # Bomb
                if classid == 1:
                    bombs_path.append(start_point)

                # Fruit
                if classid == 0:
                    fruits_path.append((x1 * 2, y1 * 2, width_box * 2, height_box * 2))

        # Slice Detected Object
        for fruit_path in fruits_path:
            center = fruit_path[0] + int(fruit_path[2] / 2)
            start_point = getRealCoord(center, fruit_path[1], fruit_path[3])
            nearBomb = checkBomb(bombs_path, start_point, fruit_path[2], fruit_path[3])
            if not nearBomb:
                slice(start_point[0], start_point[1], fruit_path[3])

        # Draw Result
        fps_label = "FPS: %.2f" % (1 / (end - start))
        cv2.putText(screen, fps_label, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('img', screen)

        # Update window and check for quit key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
