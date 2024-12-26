import os
import sys
from loguru import logger
import cv2
import requests
import google.generativeai as genai

from Plant import *
import helpers.logger_config



def capture_picture(video_input = 0):
    camera = cv2.VideoCapture(video_input)
    if not camera.isOpened():
        logger.error("Error: Could not access the camera.")
        return None

    logger.info("Camera is ready. Press 's' to take a picture and save it.")
    while True:
        ret, frame = camera.read()
        if not ret:
            logger.error("Failed to capture image. Please try again.")
            break

        cv2.imshow("Camera", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            picture_path = "plant_picture.jpg"
            cv2.imwrite(picture_path, frame)
            logger.info(f"Picture saved as {picture_path}")
            break
        elif key == ord('q'):
            logger.info("Picture capture canceled.")
            picture_path = None
            break

    camera.release()
    cv2.destroyAllWindows()
    return 1

def identify_plant(picture_path):
    logger.info("Identifying plant type using Pl@ntNet API...")
    url = "https://my-api.plantnet.org/v2/identify/all"
    api_key = "2b10lSgnftz8kOa4tfxTU2LxO"  # Replace with your actual API key

    files = {"images": open(picture_path, "rb")}
    data = {"organs": "auto"}  
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        response = requests.post(url, files=files, data=data, headers=headers)
        response.raise_for_status()
        results = response.json()

        if "results" in results and results["results"]:
            plant_name = results["results"][0]["species"]["scientificNameWithoutAuthor"]
            logger.info(f"Plant identified as: {plant_name}")
            return plant_name
        else:
            logger.error("Could not identify the plant.")
            return None
    except Exception as e:
        logger.error(f"Error identifying plant: {e}")
        return None

# Function to create a Plant object from user input
def create_plant_from_input():
    print("Enter details to configure a new plant:")
    while True:
        try:
            sensor_pin = int(input("Sensor pin (integer): "))
            break
        except ValueError:
            print("Invalid input. Please enter an integer value.")

    while True:
        try:
            motor_pin = int(input("Motor pin (integer): "))
            break
        except ValueError:
            print("Invalid input. Please enter an integer value.")

    logger.info("Now capturing a picture for the plant...")
    # picture_path = capture_picture()
    name = identify_plant("src/planta.jpg")


    genai.configure(api_key="AIzaSyA3TwfeFqaU_23GhnQ19V3_mrrz6K_WEK8")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Give me humidity percentage that this plant needs {name}. Return just the number")
    humidity = response.text.replace('\r', '').replace('\n', '')

    return Plant(name, humidity, sensor_pin, motor_pin)