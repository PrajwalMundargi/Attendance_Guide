# Face Recognition Attendance Manager

This project is a Face Recognition Attendance Manager using Python. It captures live video feed, recognizes known faces, marks attendance, and sends email notifications if attendance is below a certain threshold.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [License](#license)

## Features

- **Face Recognition:** Detects and recognizes faces from live video input.
- **Attendance Management:** Marks attendance for recognized users.
- **Email Notification:** Sends reminder emails to users with low attendance.
- **JSON Data Handling:** Stores and retrieves user data, including attendance records, from a JSON file.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/attendance-manager.git
   cd attendance-manager
   ```

2. Install required Python packages:
   Make sure you have Python installed on your system. Then, install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure you have a webcam connected, as this project uses it for face recognition.

4. Set up the JSON data:
   - Create a folder named `assets/data` and add the `rampraj.json` file in it.
   - The JSON file should contain user data with fields like name, email, and attendance.
   - Example JSON (`rampraj.json`):
     ```json
     [
       {
         "name": "samarth g",
         "email": "samarth@example.com",
         "attendance": 15
       },
       {
         "name": "ramya g",
         "email": "ramya@example.com",
         "attendance": 5
       }
     ]
     ```

## Usage

Run the application:

```bash
python face.py
```

Options in the menu:

1. **Mark your Attendance**: Opens the webcam, detects your face, and marks your attendance in the JSON file.
2. **View Attendance**: Check your attendance and receive email alerts if attendance is below average.

Exit: You can exit the program by pressing `q` while the webcam window is active, or by selecting 'q' from the main menu.

## Project Structure

```
face_recognition/
├── assessts/
│   ├── images/           # Folder containing known face images (e.g., topg.jpg, kothi.jpg)
│   ├── data/             # Folder containing the JSON file with user data (e.g., rampraj.json)
├── face.py               # Main script for running the face recognition attendance system
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
```

## Dependencies

- **OpenCV**: For video capture and displaying frames.
- **face_recognition**: For face detection and recognition.
- **NumPy**: For numerical operations.
- **smtplib**: To send email notifications using Gmail's SMTP server.
- **email.mime**: To format email messages.

Install all dependencies using:

```bash
pip install -r requirements.txt
```

## Configuration

### Email Configuration:

In `face.py`, update the `sender_email` and `sender_password` with valid Gmail credentials (enable "less secure apps" access for the sender email or set up an app-specific password).

### Image Data:

Place images of known users in the `assets/images/` folder. The filenames should match the names in the JSON data.

## License
