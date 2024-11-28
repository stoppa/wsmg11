import network
import time
import sys
from WIFI_CONFIG import SSID, PASSWORD

def connect_to_wifi():
    """
    Connects the Raspberry Pi Pico W to the specified Wi-Fi network.
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        sys.stdout.write('**Connecting to Wi-Fi**\n')
        wlan.connect(SSID, PASSWORD)

        # Wait until the connection is established
        while not wlan.isconnected():
            time.sleep(1)

    sys.stdout.write(f"**Connected to Wi-Fi, IP address: {wlan.ifconfig()[0]}**\n")
