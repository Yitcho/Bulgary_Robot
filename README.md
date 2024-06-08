# Bulgary_Robot

# Overview
This project is a face recognition security system built using a Raspberry Pi. The system captures video frames, identifies faces, and sends an email alert with a captured image if an unknown person is detected. Additionally, it includes remote control capabilities for DC motors using MQTT.

# Features
Real-Time Face Recognition: Uses face_recognition and OpenCV libraries to detect and recognize faces.
Email Alerts: Sends email notifications with an image attachment when an unknown person is detected.
Remote Motor Control: Controls DC motors via MQTT messages.
Custom I2C Driver: Developed a driver for the PCA9685 I2C DC motor driver.
Development Environment
Hardware: Raspberry Pi 3B
OS: Initially developed on Raspbian OS
Custom Image: Created using Yocto to include necessary requirements
Web Server: Flask
# Installation
# Prerequisites
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
 
