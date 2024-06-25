# Smart Pillow IoT Project

# One day project!- power of design thinking

![Project Logo](images/logo1.png)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Classes and Threads](#classes-and-threads)
- [Contributing](#contributing)
- [License](#license)

## Introduction
This project implements a smart pillow using IoT technologies to monitor various aspects such as pressure, emergency alerts, and timer-based operations. It utilizes Raspberry Pi GPIO pins, sensors, and Telegram bot integration to provide real-time notifications and interactions.

## Features
- **Pressure Sensing:** Monitors pressure on the pillow using a Force-Sensitive Resistor (FSR).
- **Fan Activation:** Turns on a fan when pressure is detected, promoting airflow.
- **Emergency Alert:** Sends emergency notifications via Telegram to predefined contacts.
- **Timer Functionality:** Allows setting and triggering a buzzer alarm after a specified duration.
- **Interactive Buttons:** Control functionalities like emergency alerts and timer settings via GPIO buttons.

## Hardware Requirements
- Raspberry Pi (tested on Raspberry Pi 3 Model B+)
- Force-Sensitive Resistor (FSR)
- MOSFET (for fan control)
- Buzzer
- GPIO Push Buttons
- Connecting wires and breadboard

## Software Requirements
- Raspbian OS
- Python 3
- Required Python Libraries:
  - `RPi.GPIO`
  - `telebot`

## Setup and Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/smart-pillow-iot.git
   cd smart-pillow-iot
# Hardware Setup:

- Connect the FSR to GPIO pin 17.
- Connect the MOSFET to GPIO pin 18 for fan control.
- Connect the Buzzer to GPIO pin 21.
- Connect GPIO push buttons (IDs 20, 21, 22, 23) as per your setup.
  
# Telegram Bot Setup:

- Create a Telegram bot and obtain the bot token.
- Update the TOKEN variable in the script with your bot token.
- Update the CHAT_ID list with your Telegram chat IDs for receiving alerts.
 
# Classes and Threads
## FSR
- Monitors the Force-Sensitive Resistor (FSR) to detect pressure on the pillow.
## Button
- Manages GPIO buttons for controlling pillow functionalities and timer settings.
  
# Contributing
- Contributions are welcome! Fork the repository and submit pull requests to contribute new features, improvements, or bug fixes.


