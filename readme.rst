Home Assistant Client
---------------------

This is a project I use where I have a multi-function Raspberry Pi that
integrates with Home Assistant.

Major features:

* Read directly from a keyboard/macropad. This module might be useful for
  anyone wanting a pure Python way to read from the keyboard.
* Sends data to HA to trigger automations.
* Read temperature/humidity and send to HA.
* Update LED displays with time/temp/humidity.

Running in the background on a Raspberry Pi

.. code-block::
   :caption: /lib/systemd/system/update-ha.service

    [Unit]
    Description=Update Home Assistant
    After=multi-user.target

    [Service]
    Type=simple
    REstart=always
    ExecStart=/home/pi/Macropad/venv/bin/python /home/pi/Macropad/main.py

    [Install]
    WantedBy=multi-user.target

.. code-block::

    sudo systemctl daemon-reload
    sudo systemctl enable test.service
    sudo systemctl start test.service
