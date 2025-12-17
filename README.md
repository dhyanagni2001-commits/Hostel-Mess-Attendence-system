# 🍽️ Hostel Mess Attendance System (OpenCV)

## Overview
The **Hostel Mess Attendance System** is an automated attendance solution that uses **computer vision** to mark student attendance in a hostel mess. The system detects faces using **OpenCV and Haar Cascade classifiers** and **automatically notifies guardians if a student is absent**.

---

## Features
- 📸 Real-time face detection using Haar Cascade  
- 🧠 Automated attendance marking  
- 📂 Student face dataset management  
- 📄 Digital attendance records  
- 📩 Auto message to guardian for absentees  
- ⚡ Fast, contactless, and reliable system  

---

## Tech Stack
- Python  
- OpenCV  
- Haar Cascade Classifier  
- NumPy  
- CSV 
- Email API (for guardian notifications)

---

## Working
1. Camera captures live video feed  
2. Faces are detected using Haar Cascade  
3. Attendance is marked automatically  
4. Absentees are identified  
5. **Automatic email is sent to the guardian**  
6. Records are stored digitally  

---

## Setup
```bash
pip install opencv-python numpy
python main.py
