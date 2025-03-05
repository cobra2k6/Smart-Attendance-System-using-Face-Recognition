# Smart Attendance System using Face Recognition

## Overview
The **Smart Attendance System** is a real-time facial recognition application that automates attendance tracking using a webcam. It recognizes students based on stored images and logs their attendance, ensuring efficiency and accuracy.

## Features
- Real-time face detection and recognition using OpenCV and face_recognition library.
- Automatically records attendance in a CSV file.
- Prevents duplicate entries within a specified time interval (default: 1 hour).
- Displays attendance status and FPS (frames per second) on-screen.
- Works with pre-stored student images for recognition.

## Requirements
Ensure you have the following dependencies installed:

```bash
pip install opencv-python numpy face-recognition
```

### Additional Requirements:
- Python 3.x
- Webcam or external camera
- CSV support for attendance logging

## Installation
1. Clone the repository or download the script:
   ```bash
   git clone https://github.com/yourusername/smart-attendance-system.git
   cd smart-attendance-system
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a directory named `student/` and add images of students (JPEG/PNG format) with filenames as their names.
4. Run the script:
   ```bash
   python attendance_system.py
   ```

## How It Works
1. The program loads stored student images and encodes their facial features.
2. It continuously captures video frames from the webcam.
3. If a recognized face appears, it logs their attendance in `attendance.csv`.
4. Each student’s attendance is recorded once per hour to prevent multiple entries.
5. Press 'q' to exit the program.

## Attendance Logging
The system logs attendance in a CSV file (`attendance.csv`) with the following format:
```
Name, Date, Time
John Doe, 2025-03-05, 10:30:15
Jane Smith, 2025-03-05, 10:35:20
```

## Customization
- Adjust `attendance_interval = timedelta(seconds=3600)` to change the attendance window.
- Modify `frame_processing_interval = 10` for faster or slower frame processing.
- Tune `tolerance=0.5` in `face_recognition.compare_faces()` for stricter or looser face matching.

## Future Enhancements
- Add GUI for better user interaction.
- Implement cloud storage for attendance records.
- Enable email or SMS notifications for attendance updates.
- Enhance security with multi-factor authentication.

## License
This project is open-source and available under the MIT License.

---
Feel free to modify this file to fit your project needs!


