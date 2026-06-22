# 🍽️ Hostel Mess Attendance System

A Flask-based web application that automates hostel mess attendance tracking using real-time face recognition. The system captures student faces through a webcam, identifies registered students using a CNN-based face recognition model, and records attendance meal-wise (Breakfast, Lunch, and Dinner).

---

## 🚀 Features

- Hostel registration with password-protected login
- Student registration with:
  - Name
  - USN/Roll Number
  - Student Mobile Number
  - Parent Mobile Number
- Automatic capture of 50 face images per student using webcam
- CNN-based face recognition model training using TensorFlow/Keras
- Real-time face detection using OpenCV Haar Cascade Classifier
- Meal-wise attendance tracking:
  - Breakfast
  - Lunch
  - Dinner
- Dashboard displaying:
  - Total registered students
  - Present students
  - Absent students
- Absentee management with:
  - Student contact numbers
  - Parent contact numbers
  - Date-wise filtering
  - Meal-wise filtering
- Attendance records stored as daily CSV files

---

## 🛠️ Technology Stack

| Layer | Technology |
|---------|------------|
| Backend | Python, Flask |
| Face Detection | OpenCV, Haar Cascade |
| Face Recognition | TensorFlow, Keras (CNN) |
| Machine Learning Utilities | scikit-learn, joblib |
| Data Processing | pandas, NumPy |
| Database Storage | CSV Files |
| Frontend | HTML, Jinja2, Bootstrap 5 |
| Desktop Packaging | PyInstaller, FlaskWebGUI |

---

## 📂 Project Structure

```text
Hostel-Mess-Attendance-System/
│
├── app.py
├── requirements.txt
├── init.sh
├── exec.sh
│
├── static/
│   ├── haarcascade_frontalface_default.xml
│   │
│   └── data/
│       ├── faces/
│       ├── Attendance/
│       ├── face_recognition_model.pkl
│       ├── login.info
│       └── ftype
│
└── templates/
    ├── signup.html
    ├── login.html
    ├── dashboard.html
    ├── adduser.html
    ├── attn.html
    └── absents.html
```

### Directory Description

| Path | Description |
|--------|------------|
| `app.py` | Main Flask application containing all routes and logic |
| `requirements.txt` | Python dependencies |
| `init.sh` | Environment setup script |
| `exec.sh` | PyInstaller build script |
| `static/data/faces/` | Student face image dataset |
| `static/data/Attendance/` | Daily attendance CSV files |
| `face_recognition_model.pkl` | Trained CNN recognition model |
| `login.info` | Hostel name and password data |
| `ftype` | Current active meal type |
| `templates/` | HTML templates |

---

## 🌐 Application Routes

| Route | Method | Description |
|---------|---------|------------|
| `/` | GET | Redirects to signup or login page |
| `/signup` | POST | Creates hostel account |
| `/login` | POST | Authenticates user |
| `/dashboard` | GET | Displays dashboard statistics |
| `/adduser` | GET | Student registration form |
| `/add` | POST | Captures face data and trains model |
| `/startattn` | GET | Attendance page |
| `/start` | GET | Starts webcam attendance process |
| `/updateftype` | GET | Changes active meal type |
| `/absentees` | GET / POST | Displays absentee list |

---

## 👨‍🎓 Student Registration Format

Each student is stored in a separate folder:

```text
static/data/faces/
└── Name_USN_StudentMobile_ParentMobile/
```

Example:

```text
static/data/faces/
└── John_USN001_9876543210_9123456789/
```

---

## 📋 Attendance Data Format

Attendance records are stored in:

```text
static/data/Attendance/
```

Each day generates a CSV file containing:

| Column | Description |
|----------|------------|
| Name | Student Name |
| Roll | USN / Roll Number |
| StudentNo | Student Mobile Number |
| Time | Attendance Timestamp |
| ParentNo | Parent Mobile Number |

---

## ⚙️ Installation

### Prerequisites

- Python 3.8 or above
- Webcam
- Git (optional)

### Windows Setup

```bash
bash init.sh
```

### macOS / Linux Setup

```bash
python -m venv pyvenv
source pyvenv/bin/activate
pip install -r requirements.txt
```

---

## ▶️ Running the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

On first launch:

1. Register the hostel name
2. Create a password
3. Login to access the dashboard

---

## 🧠 Face Recognition Workflow

### Student Registration

1. Enter student details
2. Webcam captures 50 face images
3. Images are stored in the student's folder
4. CNN model is retrained automatically
5. Updated model is saved as:

```text
static/data/face_recognition_model.pkl
```

### Attendance Process

1. Select meal type
2. Start attendance
3. Webcam detects faces
4. CNN predicts student identity
5. Attendance is recorded automatically
6. Duplicate attendance for the same meal is prevented

---

## 📊 Dashboard Features

The dashboard provides:

- Total Registered Students
- Present Students
- Absent Students
- Meal-wise attendance tracking
- Quick access to:
  - Add Student
  - Take Attendance
  - View Absentees

---

## 📞 Absentee Management

The absentee module allows administrators to:

- View absent students
- Filter by date
- Filter by meal type
- Access student mobile numbers
- Access parent mobile numbers

This helps hostel management quickly identify students who missed meals.

---

## 📦 Build Standalone Executable

For Windows:

```bash
bash exec.sh
```

This uses **PyInstaller** to generate a standalone executable.

> **Warning:** The build script removes the `static/data` directory before packaging. Back up important attendance and student data before building.

---

## 📚 Major Dependencies

```text
Flask==2.3.2
opencv-python==4.7.0.72
tensorflow
scikit-learn==1.2.2
pandas==2.0.2
numpy==1.24.3
joblib==1.2.0
flaskwebgui==1.0.6
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔮 Future Enhancements

- Database integration (MySQL/PostgreSQL)
- Parent SMS notifications for absentees
- Improved recognition using FaceNet or MobileFaceNet
- Multi-hostel support
- Cloud deployment
- Attendance analytics and reports
- QR-code based backup attendance

---

## 📄 License

This project is intended for educational and hostel management purposes. Feel free to modify and extend it according to your requirements.

---

## 👨‍💻 Author

Developed using **Flask, OpenCV, TensorFlow, and Keras** to automate hostel mess attendance through facial recognition technology.
