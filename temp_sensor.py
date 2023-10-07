import time
import adafruit_si7021
from message_handler import send_data

TIME_BETWEEN_TEMP_READINGS = 120


def get_temp_sensor(i2c):
    """ Method to read from the temp sensor """
    # Loop to read in temp/humidity
    success = False
    sensor = None
    # We can try to read from the sensor, but it doesn't always work. So just loop until it does.
    while not success:
        try:
            sensor = adafruit_si7021.SI7021(i2c)
            success = True
        except RuntimeError:
            pass

    return sensor


# def get_sensor_readings(temp_sensor, pm25_sensor):

#     data = {}

#     for _ in range(READINGS_TO_AVERAGE):
#         try:
#             # Read air quality sensor and append data
#             air_quality_data = pm25_sensor.read()

#             for key, value in air_quality_data.items():
#                 # print(f"{key} = {value}")

#                 if key not in data:
#                     data[key] = []

#                 data[key].append(value)

#             # - Read temp/humidity and append data
#             if 'temperature' not in data:
#                 data['temperature'] = []
#                 data['humidity'] = []

#             # Temp
#             data['temperature'].append(temp_sensor.temperature * 9 / 5 + 32)
#             data['humidity'].append(temp_sensor.relative_humidity)

#         except RuntimeError as e:
#             print(f"Error {e}")

#         # Pause
#         time.sleep(TIME_BETWEEN_READINGS)

#     return data


class TemperatureSensor:
    def __init__(self, i2c):
        self.last_sensor_send_time = 0
        # Create temp/humidity sensor object
        self.temp_sensor = get_temp_sensor(i2c)
        self.temp_f_str = ""
        self.hum_str = ""

    def update(self):
        now = time.time()
        if not self.last_sensor_send_time or now - self.last_sensor_send_time > TIME_BETWEEN_TEMP_READINGS:
            temp_f = self.temp_sensor.temperature * 9 / 5 + 32
            self.temp_f_str = f"{temp_f:.1f}"
            send_data("homeassistant/temperature", self.temp_f_str)

            self.hum_str = f"{self.temp_sensor.relative_humidity:.1f}"
            send_data("homeassistant/humidity", self.hum_str)

            print(self.temp_f_str, self.hum_str)

            self.last_sensor_send_time = now
