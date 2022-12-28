
import struct
import sys
from datetime import datetime

import paho.mqtt.publish as publish

from login_info import user
from login_info import password

# /home/pi/Macropad/venv/bin/python /home/pi/Macropad/main3.py


def send_data(key: str):
    # Publish to HA
    state_topic = "homeassistant/macropad"

    publish.single(state_topic, key,
                   auth={'username': user,
                         'password': password},
                   hostname="homeassistant.local")


def get_keyboard_event_file(token_to_look_for):
    section = ""
    event_name = ""

    fp = open("/proc/bus/input/devices", "r")
    done = False
    while not done:
        line = fp.readline()
        if line:
            # print (line.strip())
            if "" == line.strip():
                # print ("\nFound Section:\n" + section)
                if -1 != section.find(token_to_look_for) and -1 == section.lower().find("mouse"):
                    # It is entirely possible there to be multiple devices
                    # listed as a keyboard. In this case, I will look for
                    # the word "mouse" and exclude anything that contains
                    # that. This section may need to be suited to taste
                    print("Found [" + token_to_look_for + "] in:\n" + section)
                    # Get the last part of the "Handlers" line:
                    lines = section.split('\n')
                    for section_line in lines:
                        # The strip() method is needed because there may be trailing spaces
                        # at the end of this line. This will confuse the split() method.
                        if -1 != section_line.strip().find("Handlers=") and "" == event_name:
                            print("Found Handlers line: [" + section_line + "]")
                            section_line_parts = section_line.strip().split(' ')
                            event_name = section_line_parts[-1]
                            print("Found eventName [" + event_name + "]")
                            done = True
                section = ""
            else:
                section = section + line
        else:
            done = True
    fp.close()

    if "" == event_name:
        raise Exception("No event name was found for the token [" + token_to_look_for + "]")

    return "/dev/input/" + event_name


def main():
    # Need to add code which figures out the name of this file from
    # /proc/bus/input/devices - Look for EV=120013
    # Per Linux docs, 120013 is a hex number indicating which types of events
    # this device supports, and this number happens to include the keyboard
    # event.

    keyboard_event_file = ""
    try:
        keyboard_event_file = get_keyboard_event_file("EV=120013")
    except Exception as err:
        print("Couldn't get the keyboard event file due to error [" + str(err) + "]")

    if "" != keyboard_event_file:
        try:
            k = open(keyboard_event_file, "rb")
            # The struct format reads (small L) (small L) (capital H) (capital H) (capital I)
            # Per Python, the structure format codes are as follows:
            # (small L) l - long
            # (capital H) H - unsigned short
            # (capital I) I - unsigned int
            struct_format = 'llHHI'
            event_size = struct.calcsize(struct_format)

            event = k.read(event_size)
            going_on = True
            while going_on and event:
                (seconds, microseconds, event_type, event_code, value) = struct.unpack(struct_format, event)

                # Per Linux docs at https://www.kernel.org/doc/html/v4.15/input/event-codes.html
                # Constants defined in /usr/include/linux/input-event-codes.h
                # EV_KEY (1) constant indicates a keyboard event. Values are:
                # 1 - the key is depressed.
                # 0 - the key is released.
                # 2 - the key is repeated.

                # The code corresponds to which key is being pressed/released.

                # Event codes EV_SYN (0) and EV_MSC (4) appear but are not used, although EV_MSC may
                # appear when a state changes.

                unix_time_stamp = float(str(seconds) + "." + str(microseconds))
                uts_date_time_obj = datetime.fromtimestamp(unix_time_stamp)
                friendly_dts = uts_date_time_obj.strftime("%B %d, %Y - %H:%M:%S.%f")

                if 1 == event_type:
                    # It is necessary to flush the print statement or else holding multiple keys down
                    # is likely to block *output*
                    print("Event Size [" + str(event_size) + "] Type [" + str(event_type) + "], code [" +
                          str(event_code) + "], value [" + str(value) + "] at [" + friendly_dts + "]", flush=True)

                    if event_code == 82 and value == 1:
                        print("Sending NUM_0")
                        send_data("NUM_0")

                    if event_code == 96 and value == 1:
                        print("Sending ENTER")
                        send_data("ENTER")

                    if event_code == 78 and value == 1:
                        print("Sending PLUS")
                        send_data("PLUS")

                if 1 == event_code:
                    print("ESC Pressed - Quitting.")
                    going_on = False
                # if 4 == eventType:
                # print ("-------------------- Separator Event 4 --------------------")
                event = k.read(event_size)

            k.close()
        except IOError as err:
            print("Can't open keyboard input file due to the error [" + str(err) + "]. Maybe try sudo?")
        except Exception as err:
            print("Can't open keyboard input file due to some other error [" + str(err) + "].")
    else:
        print("No keyboard input file could be found.")
    return 0


if "__main__" == __name__:
    main()
