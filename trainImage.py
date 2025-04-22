import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time
from PIL import ImageTk, Image

# Train Image
def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(haarcasecade_path)
    faces, Id = getImagesAndLables(trainimage_path)
    recognizer.train(faces, np.array(Id))
    
    # Ensure that the output directory exists
    if not os.path.exists(trainimagelabel_path):
        os.makedirs(trainimagelabel_path)
    
    # Construct the full file path for the model
    trainer_file = os.path.join(trainimagelabel_path, "Trainer.yml")
    recognizer.save(trainer_file)  # Save the model to the file
    
    res = "Image Trained successfully"
    message.configure(text=res)
    text_to_speech(res)

def getImagesAndLables(path):
    newdir = [os.path.join(path, d) for d in os.listdir(path)]
    imagePath = [
        os.path.join(newdir[i], f)
        for i in range(len(newdir))
        for f in os.listdir(newdir[i])
    ]
    faces = []
    Ids = []
    for imagePath in imagePath:
        pilImage = Image.open(imagePath).convert("L")
        imageNp = np.array(pilImage, "uint8")
        Id = int(os.path.split(imagePath)[-1].split("_")[1])
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids
