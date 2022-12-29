import struct
import sys
import keyboard
import time

from busio import I2C
from board import SCL, SDA
# from adafruit_ht16k33.segments import BigSeg7x4
# from adafruit_ht16k33.segments import Seg14x4
# from adafruit_pm25.i2c import PM25_I2C
#
# import paho.mqtt.publish as publish
# import adafruit_si7021
# import adafruit_ht16k33.segments

from message_handler import send_data
from handle_keyboard_event import handle_keyboard_event
from temp_sensor import TemperatureSensor
from message_handler import send_data


def main():
    # Create keyboard handler
    keyboard_handler = keyboard.Keyboard(blocking=False)

    # Create i2c handler
    i2c = I2C(SCL, SDA, frequency=100000)

    # Create temperature handler
    temperature_handler = TemperatureSensor(i2c)

    last_sensor_send_time = 0

    done = False
    while not done:
        event = keyboard_handler.get_event()
        if event:
            handle_keyboard_event(event)
        else:
            time.sleep(0.2)

        temperature_handler.update()

    keyboard_handler.close()


if "__main__" == __name__:
    main()
