import paho.mqtt.publish as publish

from login_info import user
from login_info import password


def send_data(key: str):
    """ Publish to Home Assistant """

    state_topic = "homeassistant/macropad"

    publish.single(state_topic, key,
                   auth={'username': user,
                         'password': password},
                   hostname="homeassistant.local")
