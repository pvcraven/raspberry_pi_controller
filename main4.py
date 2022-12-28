import struct
import sys
from keyboard import Keyboard
from message_handler import send_data


def main():
    keyboard = Keyboard()

    event = keyboard.get_event()
    going_on = True
    while going_on and event:

        if 1 == event.event_type:
            # It is necessary to flush the print statement or else holding multiple keys down
            # is likely to block *output*
            print(f"Event Type [{event.event_type}], code [{event.event_code}], value [{event.value}] at [{event.get_friendly_dts()}]", flush=True)

            if event.event_code == 82 and event.value == 1:
                print("Sending NUM_0")
                send_data("NUM_0")

            if event.event_code == 96 and event.value == 1:
                print("Sending ENTER")
                send_data("ENTER")

            if event.event_code == 78 and event.value == 1:
                print("Sending PLUS")
                send_data("PLUS")

        if 1 == event.event_code:
            print("ESC Pressed - Quitting.")
            going_on = False

        event = keyboard.get_event()

    keyboard.close()


if "__main__" == __name__:
    main()
