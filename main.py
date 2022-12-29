"""
Main event loop.

This can be set to autostart on Raspberry Pi boot by adding it to:
/etc/rc.local
"""
import struct
import sys
import keyboard
import time
import datetime

from busio import I2C
from board import SCL, SDA
from adafruit_ht16k33.segments import BigSeg7x4
from adafruit_ht16k33.segments import Seg14x4

from message_handler import send_data
from handle_keyboard_event import handle_keyboard_event
from temp_sensor import TemperatureSensor
from message_handler import send_data


def main():
    """ Main event loop """
    # Create keyboard handler
    keyboard_handler = keyboard.Keyboard(blocking=False)

    # Create i2c handler
    i2c = I2C(SCL, SDA, frequency=100000)

    # Create temperature handler
    temperature_handler = TemperatureSensor(i2c)

    # Create out displays
    display_1 = BigSeg7x4(i2c, address=0x70)
    display_1.brightness = 0.3
    display_1.colon = True
    time_string = ""

    display_2 = Seg14x4(i2c, address=0x71)
    display_2.brightness = 0.3

    display_3 = Seg14x4(i2c, address=0x72)
    display_3.brightness = 0.3

    done = False
    while not done:
        # Read and process keyboard events
        if event := keyboard_handler.get_event():
            handle_keyboard_event(event)

        # Read and display temp/humidity
        # Update method will read temp and update HA every x seconds.
        temperature_handler.update()
        display_2.print(f"{temperature_handler.temp_f_str:>5}")
        display_2.show()
        display_3.print(f"{temperature_handler.hum_str:>5}")
        display_3.show()

        # Create time string
        now = datetime.datetime.now()
        new_time_string = now.strftime("%I:%M")
        if new_time_string[0] == '0':
            new_time_string = ' ' + new_time_string[1:]

        # Update time string if needed
        if new_time_string != time_string:
            print(f"Time: {new_time_string}")
            display_1.print(new_time_string)
            time_string = new_time_string

        # Pause so we don't chew up the CPU
        time.sleep(0.2)

    keyboard_handler.close()


if "__main__" == __name__:
    main()
