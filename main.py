from ota import OTAUpdater
import main_task

from WIFI_CONFIG import SSID, PASSWORD

firmware_url = "https://raw.githubusercontent.com/stoppa/wsmg11/refs/heads/master"

files_to_update = [
    "button.py",
    "check_daytime.py",
    "main_task.py",
    "power.py",
    "receive.py",
    "telegram.py",
    "wifi.py",
    "WIFI_CONFIG.py"
    ]

for file in files_to_update:
    ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, file)
    ota_updater.download_and_install_update_if_available()
    
main_task.main()
    
    
  