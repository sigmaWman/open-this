import pygame
import cv2
import numpy as np
import sys

# Initialize Pygame
pygame.init()

# Open video file
video_path = "lagu.mp4"  # ← Replace with your video file
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    sys.exit(1)

# Get video info
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS) or 30  # Fallback if FPS unknown

# Create Pygame screen (match video size)
screen = pygame.display.set_mode((frame_width, frame_height))
pygame.display.set_caption("Embedded Video Player")
clock = pygame.time.Clock()

print(f"Playing video: {frame_width}x{frame_height} @ {fps:.2f} FPS")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Read frame
    ret, frame = cap.read()
    if not ret:
        print("End of video")
        break  # Exit when video ends

    # Convert frame from OpenCV BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Rotate and flip to match Pygame surface format
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    frame = pygame.transform.flip(frame, True, False)  # Flip Y axis

    # Display frame
    screen.blit(frame, (0, 0))
    pygame.display.flip()

    # Sync to video FPS
    clock.tick(fps)

# Cleanup
cap.release()
pygame.quit()