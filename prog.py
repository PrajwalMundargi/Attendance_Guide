import cv2 as cv
import face_recognition
import numpy as np
import json
import os

def email_sender(receiver_email, subject, body, sender_email, sender_password):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import smtplib

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

# Function to display the menu
def display_menu():
    print("Welcome to attendance manager!")
    print("Please select from below options")
    print("1. Mark your Attendance")
    print("2. View Attendance")

def option1():
    with open('assessts/data/employees.students.json','r') as file:
        users_data = json.load(file)

    know_faces = []
    face_names=[]

    image = face_recognition.load_image_file('assessts/images/topg.jpg')
    samarth_encoding = face_recognition.face_encodings(image)[0]
    know_faces.append(samarth_encoding)
    face_names.append('samarth g')

    image = face_recognition.load_image_file('assessts/images/kothi.jpg')
    samarth_encoding = face_recognition.face_encodings(image)[0]
    know_faces.append(samarth_encoding)
    face_names.append('ramya g')

    image = face_recognition.load_image_file('assessts/images/me.jpg')
    samarth_encoding = face_recognition.face_encodings(image)[0]
    know_faces.append(samarth_encoding)
    face_names.append('prajwal')

    video_capture =cv.VideoCapture(0)

    recognized_faces = set()

    while True:
        ret, frame = video_capture.read()

        face_locations = face_recognition.face_locations(frame)
        face_encoding_in_frame = face_recognition.face_encodings(frame, face_locations)

        for(top, right, bottom, left), face_encoding in zip(face_locations, face_encoding_in_frame):
            matches = face_recognition.compare_faces(know_faces, face_encoding)
            name='unknown'

            if True in matches:
                first_match_index = matches.index(True)
                name = face_names[first_match_index]

                if name not in recognized_faces:
                    recognized_faces.add(name)

                    for users in users_data:
                        if(users['name'] == name):
                            print(f"welcome {name}, hope you have a good day!")
                            users["attendance"]+=1
                            print(f"your attendance is {users['attendance']}")
                            with open('assessts/data/employees.students.json','w') as file:
                                json.dump(users_data, file, indent=4)

            cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv.putText(frame, name, (left, top-10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        cv.imshow('video', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv.destroyAllWindows()

def option2():
    student_name = input('Enter your name: ')
    file_path = 'assessts/data/employees.students.json'

    with open(file_path) as file:
        users_data = json.load(file)

    user_found = False
    for user in users_data:
        if user['name'] == student_name:
            user_found = True
            if user['attendance'] > 20:
                print(f"WELL DONE {user['name']}!! Your attendance is above average")
            else:
                sender_email = 'attendanceguide@gmail.com'
                sender_password = 'ojuv gguu qnzs tjxp'
                receiver_email = user['email']

                subject = 'Attendance Reminder'
                body = f"Dear {user['name']}, Your biology attendance is very low. Please attend your classes properly."

                email_sender(receiver_email, subject, body, sender_email, sender_password)
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


    