from datetime import datetime
import struct
import os
from dataclasses import dataclass


EV_SYN = 0x00
EV_KEY = 0x01
EV_REL = 0x02
EV_ABS = 0x03
EV_MSC = 0x04
EV_SW = 0x05
EV_LED = 0x11
EV_SND = 0x12
EV_REP = 0x14
EV_FF = 0x15
EV_PWR = 0x16
EV_FF_STATUS = 0x17
EV_MAX = 0x1f
EV_CNT = (EV_MAX+1)

KEY_DOWN = 1
KEY_REPEAT = 2
KEY_UP = 0


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
        raise Exception(f"ERROR: No event name was found for '{token_to_look_for}'. Is there a keyboard plugged in?")

    return "/dev/input/" + event_name


@dataclass
class KeyboardEvent:
    seconds: int = 0
    microseconds: int = 0
    event_type: int = 0
    event_code: int = 0
    value: int = 0

    def get_friendly_dts(self):

        unix_time_stamp = float(str(self.seconds) + "." + str(self.microseconds))
        uts_date_time_obj = datetime.fromtimestamp(unix_time_stamp)
        friendly_dts = uts_date_time_obj.strftime("%B %d, %Y - %H:%M:%S.%f")
        return friendly_dts


class Keyboard:
    def __init__(self, blocking: bool = True):
        self.keyboard_event_file = get_keyboard_event_file("EV=120013")

        self.k = open(self.keyboard_event_file, "rb")

        os.set_blocking(self.k.fileno(), blocking)

        # The struct format reads (small L) (small L) (capital H) (capital H) (capital I)
        # Per Python, the structure format codes are as follows:
        # (small L) l - long
        # (capital H) H - unsigned short
        # (capital I) I - unsigned int
        self.struct_format = 'llHHI'
        self.event_size = struct.calcsize(self.struct_format)

    def get_event(self):
        event_struct = self.k.read(self.event_size)

        if event_struct is None:
            return None

        (seconds, microseconds, event_type, event_code, value) = struct.unpack(self.struct_format, event_struct)
        event_obj = KeyboardEvent(seconds=seconds,
                                  microseconds=microseconds,
                                  event_type=event_type,
                                  event_code=event_code,
                                  value=value)
        return event_obj

    def close(self):
        self.k.close()
