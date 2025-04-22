import pandas as pd
from glob import glob
import os
import tkinter as tk
from tkinter import *
import csv

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get().strip()
        if Subject == "":
            t = 'Please enter the subject name.'
            text_to_speech(t)
            return
        
        # Define the folder path where attendance CSV files are stored
        folder_path = f"D:\\Pr\\Attendance-system\\Attendance-Management-system-using-face-recognition-master\\Attendance\\{Subject}"
        
        # Get all CSV files for the subject using a pattern
        filenames = glob(os.path.join(folder_path, f"{Subject}*.csv"))
        # Exclude the merged file (attendance.csv) if it exists to avoid merging it again.
        filenames = [f for f in filenames if os.path.basename(f) != "attendance.csv"]

        if not filenames:
            t = 'No attendance records found for this subject.'
            text_to_speech(t)
            return
        
        # Merge all CSV files based on common columns "Enrollment" and "Name"
        df_list = [pd.read_csv(f) for f in filenames]
        newdf = df_list[0]
        for i in range(1, len(df_list)):
            newdf = pd.merge(newdf, df_list[i], on=["Enrollment", "Name"], how="outer")
        newdf.fillna(0, inplace=True)
        
        # Convert all columns (except Enrollment and Name) to show "Present" if value is 1; else blank.
        for col in newdf.columns:
            if col not in ["Enrollment", "Name"]:
                newdf[col] = newdf[col].apply(lambda x: "Present" if x == 1 else "")
                
        # Save the merged attendance to a CSV file in the same folder
        csv_path = os.path.join(folder_path, "attendance.csv")
        newdf.to_csv(csv_path, index=False)
        
        # Create a new Tkinter window to display the attendance sheet
        root = tk.Tk()
        root.title("Attendance of " + Subject)
        root.configure(background="black")
        
        # Read and display the CSV file as a grid of labels
        with open(csv_path, newline='') as file:
            reader = csv.reader(file)
            r = 0
            for row in reader:
                c = 0
                for cell in row:
                    label = tk.Label(root, text=cell, width=15, height=1,
                                     fg="yellow", font=("times", 15, "bold"),
                                     bg="black", relief=tk.RIDGE)
                    label.grid(row=r, column=c, padx=2, pady=2)
                    c += 1
                r += 1
        root.mainloop()
        print(newdf)

    # Main subject selection window
    subject = Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")
    
    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)
    titl = tk.Label(subject, text="Which Subject Attendance?", 
                    bg="black", fg="green", font=("arial", 25))
    titl.place(x=100, y=12)

    # Function to open the folder containing attendance sheets
    def Attf():
        sub = tx.get().strip()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            folder_path = f"D:\\Pr\\Attendance-system\\Attendance-Management-system-using-face-recognition-master\\Attendance\\{sub}"
            if os.path.exists(folder_path):
                os.startfile(folder_path)
            else:
                t = "Attendance folder not found for the subject."
                text_to_speech(t)

    attf = tk.Button(subject, text="Check Sheets", command=Attf, bd=7,
                     font=("times new roman", 15), bg="black", fg="yellow",
                     height=2, width=10, relief=RIDGE)
    attf.place(x=360, y=170)

    sub = tk.Label(subject, text="Enter Subject", width=10, height=2,
                   bg="black", fg="yellow", bd=5, relief=RIDGE,
                   font=("times new roman", 15))
    sub.place(x=50, y=100)

    tx = tk.Entry(subject, width=15, bd=5, bg="black", fg="yellow",
                  relief=RIDGE, font=("times", 30, "bold"))
    tx.place(x=190, y=100)

    fill_a = tk.Button(subject, text="View Attendance", command=calculate_attendance,
                       bd=7, font=("times new roman", 15), bg="black", fg="yellow",
                       height=2, width=12, relief=RIDGE)
    fill_a.place(x=195, y=170)
    
    subject.mainloop()
