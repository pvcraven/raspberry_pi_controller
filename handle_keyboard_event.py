import keyboard
import time
from message_handler import send_data

state_topic = "homeassistant/macropad"


lookup = {
    96: "ENTER",
    78: "PLUS",
    1: "ESC",
    82: "NUM_0",
    79: "NUM_1",
    80: "NUM_2",
    81: "NUM_3",
    75: "NUM_4",
    76: "NUM_5",
    77: "NUM_6",
    71: "NUM_7",
    72: "NUM_8",
    73: "NUM_9",
    74: "NUM_MINUS",

}
def handle_keyboard_event(event: keyboard.KeyboardEvent):

    if event.event_type != keyboard.EV_KEY:
        return

    elif event.value != keyboard.KEY_DOWN:
        return

    elif event.event_code == 69:
        return

    elif event.event_code in lookup:
        val = lookup[event.event_code]
        print(f"Sending {val}")
        send_data(state_topic, val)

    elif event.event_code == 1:
        print("ESC Pressed")

    else:
        print(f"Event code [{event.event_code}] at [{event.get_friendly_dts()}]", flush=True)
