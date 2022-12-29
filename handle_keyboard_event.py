import keyboard
import time
from message_handler import send_data

state_topic = "homeassistant/macropad"


def handle_keyboard_event(event: keyboard.KeyboardEvent):

    if event.event_type != keyboard.EV_KEY:
        return

    elif event.value != keyboard.KEY_DOWN:
        return

    elif event.event_code == 69:
        return

    elif event.event_code == 82:
        print("Sending NUM_0")
        send_data(state_topic, "NUM_0")

    elif event.event_code == 96:
        print("Sending ENTER")
        send_data(state_topic, "ENTER")

    elif event.event_code == 78:
        print("Sending PLUS")
        send_data(state_topic, "PLUS")

    elif event.event_code == 1:
        print("ESC Pressed")

    else:
        print(f"Event code [{event.event_code}] at [{event.get_friendly_dts()}]", flush=True)
