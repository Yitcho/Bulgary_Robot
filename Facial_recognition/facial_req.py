#!/usr/bin/python3.11
"""
Author: Mahdi Kaffel

Description: This script uses a Raspberry Pi with a Picamera and Flask to detect faces. Known faces are identified using pre-trained encodings. 
             When an unknown face is detected, an email alert is sent with an image attachment of the unknown person. 
"""
# import the necessary packages
from flask import Flask, Response
from picamera2 import Picamera2, Preview
import face_recognition
import imutils
import pickle
import time
import cv2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

app = Flask(__name__)

# Initialize 'currentname' to trigger only when a new person is identified.
currentname = "unknown"
# Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "encodings.pickle"

# Load the known faces and embeddings
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())

# Initialize the Picamera2
picam2 = Picamera2()

# Configure the camera
config = picam2.create_preview_configuration(main={"size": (640,480)})
picam2.configure(config)

# Start the camera
picam2.start()
time.sleep(2.0)  # Allow the camera sensor to warm up

def send_email(frame):
    toaddr = "your_email@example.com"
    fromaddr = "raspberry_pi_email@example.com"
    password = "your_email_password"

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Unknown Person Detected"

    body = "An unknown person has been detected."
    msg.attach(MIMEText(body, 'plain'))

    # Attach the frame image
    filename = "intruder.jpg"
    cv2.imwrite(filename, frame)
    attachment = open(filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= {filename}")
    msg.attach(part)

    # Send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

    # Remove the image file after sending the email
    os.remove(filename)

def generate_frames():
    global currentname
    # Loop over frames from the camera stream
    while True:
        # Capture a frame from the camera
        frame = picam2.capture_array()

        # Convert the frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Resize the frame to 500px (to speed up processing)
        frame_rgb = imutils.resize(frame_rgb, width=500)

        # Detect face locations
        boxes = face_recognition.face_locations(frame_rgb)

        # Compute facial embeddings for each face bounding box
        encodings = face_recognition.face_encodings(frame_rgb, boxes)
        names = []

        # Loop over the facial embeddings
        for encoding in encodings:
            # Attempt to match each face in the input image to our known encodings
            matches = face_recognition.compare_faces(data["encodings"], encoding)
            name = "Unknown"  # If face is not recognized, then print Unknown

            # Check to see if we have found a match
            if True in matches:
                # Find the indexes of all matched faces then initialize a dictionary to count the total number of times each face was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # Loop over the matched indexes and maintain a count for each recognized face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # Determine the recognized face with the largest number of votes
                name = max(counts, key=counts.get)

                # If someone in your dataset is identified, print their name on the screen
                if currentname != name:
                    currentname = name
                    print(currentname)
            else:
                # If the detected person is unknown, send an email
                if currentname != name:
                    currentname = name
                    print(currentname)
                    send_email(frame)

            # Update the list of names
            names.append(name)

        # Loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
            # Draw the predicted face name on the image - color is in BGR
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 225), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 255, 255), 2)

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame
        yield (b'--frame\r\n'
               b'Content-Type:image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
