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
                f"Motor Pin: {self.motor_pin}")

