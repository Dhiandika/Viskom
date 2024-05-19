import cv2
import os

# Define the video path
video_path = "2024-05-18 23-27-05.mp4"

# Define the directory to save the screenshots
screenshot_dir = "savefoto"

# Create the directory if it doesn't exist
os.makedirs(screenshot_dir, exist_ok=True)

# Open the video
video = cv2.VideoCapture(video_path)

# Get the frame rate of the video
fps = 5

# Calculate the interval between frames to capture
interval = int(fps)

# Initialize the frame counter
frame_counter = 0

# Loop through the video
while True:
    # Read the next frame
    ret, frame = video.read()

    # Check if the frame was successfully read
    if not ret:
        break

    # Check if the frame counter is a multiple of the interval
    if frame_counter % interval == 0:
        # Save the frame as a screenshot
        cv2.imwrite(os.path.join(screenshot_dir, f"frame_{frame_counter}.jpg"), frame)

    # Increment the frame counter
    frame_counter += 1

# Release the video capture object
video.release()
