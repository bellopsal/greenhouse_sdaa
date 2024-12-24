from Plant import Plant
import os
import cv2
import requests
import google.generativeai as genai



class Plant:
    def __init__(self, name, humidity, sensor_pin, motor_pin):
        self.name = name
        self.humidity = humidity
        self.sensor_pin = sensor_pin
        self.motor_pin = motor_pin

    def __str__(self):
        return (f"Plant Name: {self.name}\n"
                f"Humidity Level: {self.humidity}\n"
                f"Sensor Pin: {self.sensor_pin}\n"
                f"Motor Pin: {self.motor_pin}\n")

# Function to capture a picture using the camera
def capture_picture():
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Error: Could not access the camera.")
        return None

    print("Camera is ready. Press 's' to take a picture and save it.")
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to capture image. Please try again.")
            break

        cv2.imshow("Camera", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            picture_path = "plant_picture.jpg"
            cv2.imwrite(picture_path, frame)
            print(f"Picture saved as {picture_path}")
            break
        elif key == ord('q'):
            print("Picture capture canceled.")
            picture_path = None
            break

    camera.release()
    cv2.destroyAllWindows()
    return 1

def identify_plant(picture_path):
    print("Identifying plant type using Pl@ntNet API...")
    url = "https://my-api.plantnet.org/v2/identify/all"
    api_key = "2b10lSgnftz8kOa4tfxTU2LxO"  # Replace with your actual API key
    files = {"images": open(picture_path, "rb")}
    data = {"organs": "leaf"}  # Adjust as needed, e.g., "flower", "fruit"
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        response = requests.post(url, files=files, data=data, headers=headers)
        response.raise_for_status()
        results = response.json()

        if "results" in results and results["results"]:
            plant_name = results["results"][0]["species"]["scientificNameWithoutAuthor"]
            print(f"Plant identified as: {plant_name}")
            return plant_name
        else:
            print("Could not identify the plant.")
            return None
    except Exception as e:
        print(f"Error identifying plant: {e}")
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

    print("Now capturing a picture for the plant...")
    # picture_path = capture_picture()
    name = identify_plant("src/planta.jpg")

    # if picture_path is None:
    #     print("No picture was taken. Plant creation aborted.")
    #     return None
    genai.configure(api_key="AIzaSyA3TwfeFqaU_23GhnQ19V3_mrrz6K_WEK8")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Give me humidity percentage that this plant needs {name}. Return just the number")
    print(response.text)
    humidity = response

    return Plant(name, humidity, sensor_pin, motor_pin)

# Example usage
if __name__ == "__main__":
    plant = create_plant_from_input()
    if plant:
        print("\nPlant created successfully!")
        print(plant)
