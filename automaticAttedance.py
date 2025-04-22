import tkinter as tk
from tkinter import *
import os
import cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.ttk as tkk
import tkinter.font as font

# File paths
haarcasecade_path = r"D:\Pr\Attendance-system\Attendance-Management-system-using-face-recognition-master\haarcascade_frontalface_alt.xml"
trainimagelabel_path = r"D:\Pr\Attendance-system\Attendance-Management-system-using-face-recognition-master\TrainingImageLabel"
trainimage_path = r"D:\Pr\Attendance-system\Attendance-Management-system-using-face-recognition-master\Training Image"
studentdetail_path = r"D:\Pr\Attendance-system\Attendance-Management-system-using-face-recognition-master\StudentDetails\studentdetails.csv"
attendance_path = r"D:\Pr\Attendance-system\Attendance-Management-system-using-face-recognition-master\Attendance"


def subjectChoose(text_to_speech):
    def FillAttendance():
        # Get the subject name from the entry widget
        subject_name = tx.get().strip()
        now = time.time()
        future = now + 20  # Run attendance for 20 seconds

        if subject_name == "":
            msg = "Please enter the subject name!!!"
            text_to_speech(msg)
            return

        try:
            # Create the face recognizer instance
            recognizer = cv2.face.LBPHFaceRecognizer_create()

            # Build the model path and check if the Trainer file exists
            model_path = os.path.join(trainimagelabel_path, "Trainer.yml")
            if not os.path.exists(model_path):
                error_msg = "Model not found, please train model first!"
                Notifica.configure(
                    text=error_msg,
                    bg="black",
                    fg="yellow",
                    width=33,
                    font=("times", 15, "bold")
                )
                Notifica.place(x=20, y=250)
                text_to_speech(error_msg)
                return

            # Load the trained model and the Haar Cascade
            recognizer.read(model_path)
            faceCascade = cv2.CascadeClassifier(haarcasecade_path)

            # Load student details from CSV
            df = pd.read_csv(studentdetail_path)

            # Start video capture
            cam = cv2.VideoCapture(0)
            cv_font = cv2.FONT_HERSHEY_SIMPLEX
            col_names = ["Enrollment", "Name"]
            attendance = pd.DataFrame(columns=col_names)

            while True:
                ret, im = cam.read()
                if not ret:
                    continue

                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(gray, 1.2, 5)

                for (x, y, w, h) in faces:
                    # Predict the face using the recognizer
                    Id, conf = recognizer.predict(gray[y:y + h, x:x + w])

                    if conf < 70:
                        # Recognized face
                        ts = time.time()
                        date_str = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                        
                        # Lookup student details in the CSV
                        student_info = df.loc[df["Enrollment"] == Id]["Name"].values
                        if student_info.size == 0:
                            # No matching student details found: log and skip this face
                            print(f"No student details found for ID: {Id}")
                            continue

                        student_name = student_info[0]
                        label_text = f"{Id}-{student_name}"
                        
                        # Record attendance
                        attendance.loc[len(attendance)] = [Id, student_name]

                        # Draw rectangle and label around the face
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                        cv2.putText(im, label_text, (x + w, y), cv_font, 1, (255, 255, 0), 4)
                    else:
                        # Face not recognized (low confidence)
                        label_text = "Unknown"
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                        cv2.putText(im, label_text, (x + w, y), cv_font, 1, (0, 25, 255), 4)

                # Check for timeout or user exit
                if time.time() > future:
                    break

                cv2.imshow("Filling Attendance...", im)
                key = cv2.waitKey(30) & 0xFF
                if key == 27:  # Exit if ESC key is pressed
                    break

            # Add the date column to the attendance DataFrame
            attendance[date_str] = 1

            # Release resources
            cam.release()
            cv2.destroyAllWindows()

            # Create directory for the subject if it doesn't exist and save the CSV file
            save_path = os.path.join(attendance_path, subject_name)
            os.makedirs(save_path, exist_ok=True)
            fileName = f"{save_path}/{subject_name}_{date_str}_{timeStamp.replace(':', '-')}.csv"
            attendance.drop_duplicates(["Enrollment"], keep="first", inplace=True)
            attendance.to_csv(fileName, index=False)

            success_msg = f"Attendance Filled Successfully for {subject_name}"
            Notifica.configure(
                text=success_msg,
                bg="black",
                fg="yellow",
                width=33,
                font=("times", 15, "bold")
            )
            Notifica.place(x=20, y=250)
            text_to_speech(success_msg)

        except Exception as e:
            print(f"Error: {str(e)}")
            error_audio = "No Face found for attendance"
            text_to_speech(error_audio)
            cv2.destroyAllWindows()

    # Build the main subject chooser window
    subject = Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")

    # Title label at the top
    title_lbl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    title_lbl.pack(fill=X)

    title_txt = tk.Label(
        subject,
        text="Enter the Subject Name",
        bg="black",
        fg="green",
        font=("arial", 25)
    )
    title_txt.place(x=160, y=12)

    # Notification label to display messages
    Notifica = tk.Label(
        subject,
        text="Attendance filled Successfully",
        bg="yellow",
        fg="black",
        height=2,
        font=("times", 15, "bold")
    )

    def Attf():
        # Open the attendance sheets directory
        sub_text = tx.get().strip()
        if sub_text == "":
            text_to_speech("Please enter the subject name!!!")
        else:
            os.startfile(r"D:\Pr\Attendance-system")

    # Button to check sheets
    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=10,
        relief=RIDGE,
    )
    attf.place(x=360, y=170)

    # Label for subject entry
    sub_lbl = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="black",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 15),
    )
    sub_lbl.place(x=50, y=100)

    # Entry widget to type the subject name
    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="black",
        fg="yellow",
        relief=RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    # Button to fill attendance
    fill_a = tk.Button(
        subject,
        text="Fill Attendance",
        command=FillAttendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
    )
    fill_a.place(x=195, y=170)

    subject.mainloop()


# Example text_to_speech function for testing
def text_to_speech(message):
    # For example purposes, we just print the message.
    # Replace this function with your TTS implementation.
    print("TTS:", message)


# To run the subject chooser window, uncomment the following line:
# subjectChoose(text_to_speech)
