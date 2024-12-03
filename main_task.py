import network
import time
from machine import RTC, Pin
import sys

from button import Button
import wifi
import check_daytime as cd
import telegram as tg
import power as pw

from WIFI_CONFIG import SSID, PASSWORD

BT_TV = Button(1)
BT_WIFI = Button(2)
BT_BATH = Button(5)

LED = Pin("LED", Pin.OUT)

        
def main():
    
    BT_WIFI.on()

    for file in files_to_update:
        ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, file)
        ota_updater.download_and_install_update_if_available()

    
    
    # Connect to Wi-Fi
    wifi.connect_to_wifi()

    # Synchronize time from the NTP server
    cd.sync_time()

#     bt_tv.off()
    
    if cd.is_night_time():
        day = False
    else:
        day = True
    
    use_times = pw.get_cheapest_hours(2, False)
    
    last_update_id = None
    
    while True:
        
        use_time = pw.get_cheapest_hours(2, False)
        
        last_update_id = tg.handle_messages(last_update_id, use_time)
        
        current_time = cd.get_time(raw=True)

        if use_time["next_10h"]["led_on"]:
            
            LED.on()
            
        else:
            LED.off()

            

#         
#         if (cd.is_weekend() or cd.is_night_time) and BT_WIFI.get_button_state():
#             
#             BT_WIFI.off()
#             
#         elif not cd.is_weekend() and not BT_WIFI.get_button_state() and not cd.is_night_time():
#             
#             BT_WIFI.on()
#             
        
      


