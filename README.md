# Bulgary_Robot
Overview
This project is a face recognition security system built using a Raspberry Pi. The system captures video frames, identifies faces, and sends an email alert with a captured image if an unknown person is detected. Additionally, it includes remote control capabilities for DC motors using MQTT.

Features
Real-Time Face Recognition: Uses face_recognition and OpenCV libraries to detect and recognize faces.
Email Alerts: Sends email notifications with an image attachment when an unknown person is detected.
Remote Motor Control: Controls DC motors via MQTT messages.
Custom I2C Driver: Developed a driver for the PCA9685 I2C DC motor driver.
Development Environment
Hardware: Raspberry Pi 3B
OS: Initially developed on Raspbian OS
Custom Image: Created using Yocto to include necessary requirements
Web Server: Flask
Installation
Prerequisites
Raspberry Pi 3B
Raspberry Pi Camera Module
PCA9685 I2C DC Motor Driver
Email account for sending alerts
Software Requirements
Python 3.11
Flask
OpenCV
face_recognition
smbus
paho-mqtt
Setup Instructions
Clone the Repository

sh
Copy code
git clone https://github.com/yourusername/facerecognition-security-system.git
cd facerecognition-security-system
Install Dependencies

sh
Copy code
sudo apt-get update
sudo apt-get install python3-opencv python3-pip
pip3 install flask face_recognition smbus paho-mqtt
Load Face Encodings

Ensure you have an encodings.pickle file generated from training your model using face_recognition. This file should be placed in the root directory of the project.

Configure Email Alerts

Update the email settings in the send_email function in app.py with your email address and password.

Run the Application

sh
Copy code
python3 app.py
Access the Video Feed

Open a web browser and navigate to http://<your_raspberry_pi_ip>:5000/video_feed to view the video feed.

MQTT Configuration
Set Up MQTT Broker

Install and configure an MQTT broker on your Raspberry Pi (e.g., Mosquitto).

sh
Copy code
sudo apt-get install mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
Publish MQTT Messages

Use an MQTT client to send control messages to the topic motor/control. For example, to move the motors forward, send the message {"action": "forward"}.

Systemd Service Configuration
To ensure the application runs as a service on startup, create a systemd service file.

Create Service File

sh
Copy code
sudo nano /etc/systemd/system/facerecognition.service
Add the Following Configuration

ini
Copy code
[Unit]
Description=Face Recognition Security System
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/your/app.py
WorkingDirectory=/path/to/your/project
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
Enable and Start the Service

sh
Copy code
sudo systemctl enable facerecognition.service
sudo systemctl start facerecognition.service
Limitations
The Raspberry Pi 3B faces CPU overload issues during face recognition processing. For smoother video streaming, consider using a board with a GPU.
Future Improvements
Optimize face recognition code for better performance.
Explore hardware acceleration options for face recognition.
Contributing
Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

License
This project is licensed under the MIT License.
