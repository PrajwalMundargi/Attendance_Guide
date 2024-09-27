import cv2 as cv
import face_recognition
import numpy as np
import json
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def email_sender(receiver_email, subject, body, sender_email, sender_password):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        print('Email sent successfully!')
    except Exception as e:
        print(f'Failed to send email: {e}')
    finally:
        server.quit()

def display_menu():
    print("Welcome to attendance manager!")
    print("Please select from below options")
    print("1. Mark your Attendance")
    print("2. View Attendance")

def option1():
    try:
        with open('assessts/data/rampraj.json', 'r') as file:
            users_data = json.load(file)
    except FileNotFoundError:
        print("Data file not found.")
        return
    except json.JSONDecodeError:
        print("Error decoding JSON from file.")
        return

    know_faces = []
    face_names = []

    try:
        # Load and encode sample images
        for image_path, name in [
            ('assessts/images/topg.jpg', 'samarth g'),
            ('assessts/images/kothi.jpg', 'ramya g'),
            ('assessts/images/me.jpg', 'prajwal mundargi')
        ]:
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            
            if face_encodings:
                know_faces.append(face_encodings[0])
                face_names.append(name)
    except FileNotFoundError:
        print("One or more image files not found.")
        return
    except IndexError:
        print("No faces found in one or more image files.")
        return

    video_capture = cv.VideoCapture(0)
    recognized_faces = set()

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture image")
            break

        # Convert the image from BGR to RGB
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings_in_frame = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings_in_frame):
            matches = face_recognition.compare_faces(know_faces, face_encoding)
            name = 'unknown'

            if True in matches:
                first_match_index = matches.index(True)
                name = face_names[first_match_index]

                if name not in recognized_faces:
                    recognized_faces.add(name)

                    for user in users_data:
                        if user.get('name') == name:
                            print(f"Welcome {name}, hope you have a good day!")
                            user["attendance"] += 1
                            print(f"Your attendance is {user['attendance']}")
                            try:
                                with open('assessts/data/rampraj.json', 'w') as file:
                                    json.dump(users_data, file, indent=4)
                            except IOError:
                                print("Error writing to data file.")
                            break

            # Draw a rectangle around the face
            cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Display the name of the person
            cv.putText(frame, name, (left, top-10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Display the resulting image
        cv.imshow('Video', frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close any OpenCV windows
    video_capture.release()
    cv.destroyAllWindows()

def option2():
    student_name = input('Enter your name: ')
    file_path = 'assessts/data/rampraj.json'

    try:
        with open(file_path) as file:
            users_data = json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        return

    user_found = False
    for user in users_data:
        if isinstance(user, dict) and 'name' in user:
            if user['name'] == student_name:
                user_found = True
                if user.get('attendance', 0) > 20:
                    print(f"WELL DONE {user['name']}!! Your attendance is above average")
                else:
                    sender_email = 'attendanceguide@gmail.com'
                    sender_password = 'ojuv gguu qnzs tjxp'
                    receiver_email = user.get('email')

                    if receiver_email:
                        subject = 'Attendance Reminder'
                        body = f"Dear {user['name']}, Your biology attendance is very low. Please attend your classes properly."

                        email_sender(receiver_email, subject, body, sender_email, sender_password)
                    else:
                        print(f"Email address not found for {user['name']}")

                break

    if not user_found:
        print(f"No record found for {student_name}")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-2) or 'q' to quit: ")

        if choice == '1':
            option1()
        elif choice == '2':
            option2()
        elif choice.lower() == 'q':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
