import face_recognition
import cv2
import numpy as np
from datetime import datetime, timedelta
import os
import csv
import time  # Import time module for FPS calculation

# Directory for student images
image_directory = "student/"

# Initialize lists for face encodings and names
known_face_encodings = []
known_face_names = []

# Load all images and create encodings with names from filenames
print("Loading images...")
for filename in os.listdir(image_directory):
    if filename.endswith((".jpg", ".jpeg", ".png")):
        path = os.path.join(image_directory, filename)
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_face_encodings.append(encodings[0])
            name = os.path.splitext(filename)[0].capitalize()
            known_face_names.append(name)
            print(f"Loaded: {name}")

print("Image loading complete!")

# Initialize attendance tracking
attendance_file = "attendance.csv"
last_attendance_time = {}
attendance_log = set()  # Tracks recorded attendance to avoid duplicate prints

# Define the 1-hr attendance window
attendance_interval = timedelta(seconds=3600)

# Start video capture
video_capture = cv2.VideoCapture(0)
frame_processing_interval = 10
frame_count = 0
fps = 0
prev_time = time.time()  # Initialize FPS timer

try:
    with open(attendance_file, "a", newline="") as f:
        lnwriter = csv.writer(f)

        while True:
            start_time = time.time()  # Start time for FPS calculation
            ret, frame = video_capture.read()
            if not ret:
                break

            frame_count += 1

            # Process every nth frame
            if frame_count % frame_processing_interval == 0:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                for face_location, face_encoding in zip(face_locations, face_encodings):
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)

                    name = "Unknown"
                    color = (0, 0, 255)
                    display_message = ""

                    if matches and matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        color = (0, 255, 0)

                        current_time = datetime.now()
                        if name not in last_attendance_time or current_time - last_attendance_time[name] > attendance_interval:
                            last_attendance_time[name] = current_time
                            lnwriter.writerow([name, current_time.strftime("%Y-%m-%d"), current_time.strftime("%H:%M:%S")])
                            f.flush()  # Ensure data is written to the file

                            # Print attendance to terminal only once
                            if name not in attendance_log:
                                attendance_log.add(name)
                                print(f"Attendance recorded: {name} at {current_time.strftime('%H:%M:%S')}")

                            display_message = f"{name}: Present"

                    # Scale coordinates for bounding box
                    top, right, bottom, left = [coord * 4 for coord in face_location]
                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

                    # Display name and attendance status
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                    if display_message:
                        cv2.putText(frame, display_message, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

            # Calculate FPS
            end_time = time.time()
            fps = 1 / (end_time - start_time)

            # Display FPS on frame
            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Show video
            cv2.imshow("Camera", frame)

            # Exit loop on pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

except Exception as e:
    print(f"Error: {e}")

finally:
    video_capture.release()
    cv2.destroyAllWindows()
