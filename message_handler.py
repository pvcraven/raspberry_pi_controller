import paho.mqtt.publish as publish

from login_info import user
from login_info import password


def send_data(topic: str,
              data: str):
    """ Publish to Home Assistant """

    publish.single(topic, data,
                   auth={'username': user,
                         'password': password},
                   hostname="192.168.1.202")
