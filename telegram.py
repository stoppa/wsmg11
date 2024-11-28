import urequests
import ujson
import time
import sys
from button import Button
import power as pw
import check_daytime as cd

# Replace these with your own values
TOKEN = '7618490180:AAGpcvNP2l72WugC3a7y1K-3DeVJn6jC6a4'  # Your Telegram bot token
CHAT_ID = '1556894786'  # Your chat ID with the bot
API_URL = f'https://api.telegram.org/bot{TOKEN}'

BT_TV = Button(1)
BT_WIFI = Button(2)
BT_BATH = Button(5)

# Function to send a message to Telegram
def send_message(chat_id = CHAT_ID, text="empty"):
    
    print(text)
    
    url = f"{API_URL}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = urequests.post(url, headers=headers, data=ujson.dumps(payload))
        
        if response.status_code == 200:
            
            print("Message sent successfully!")
            
        else:
            
            print("Failed to send message:", response.text)
            
        response.close()
        
    except Exception as e:
        print("Error:", e)

# Function to check for new messages

def check_for_messages(last_update_id=None):

    unread_messages = []
    url = f"{API_URL}/getUpdates?timeout=1"
    
    if last_update_id:
        url += f"&offset={last_update_id + 1}"
    
    try:
        response = urequests.get(url)
        
        if response.status_code == 200:
            messages = response.json().get("result", [])
            
            if messages:  
                for message in messages:
                    update_id = message.get("update_id")
                    
                    if "message" in message:
                        chat_id = message["message"]["chat"]["id"]
                        text = message["message"]["text"]
                        
                        unread_messages.append({
                            "chat_id": chat_id,
                            "text": text,
                            "update_id": update_id
                        })
                
                # Letzten Update-ID aktualisieren, um Doppelte zu vermeiden
                last_update_id = update_id

        response.close()
    
    except Exception as e:
        sys.print_exception(e)
        print("Error while fetching messages:", e)
    
    return unread_messages, last_update_id


def answer_messages(messages, use_time):
    
    for message in messages:
        
        command = message["text"]
        
        chat_id = message["chat_id"]
        
        if command == "/tvon":
        
            BT_TV.on()
            
            send_message(chat_id, "Turned TV power ON")
            
        if command == "/tvoff":
        
            BT_TV.off()
            
            send_message(chat_id, "Turned TV power OFF")
            
        if command == "/bathon":
            
            BT_BATH.on()
            
            send_message(chat_id, "Turned BATHROOM power ON")
            
        if command == "/bathoff":
            
            BT_BATH.off()
            
            send_message(chat_id, "Turned BATHROOM power OFF")
            
        if command == "/wash":
            
            start_10 = use_time["next_10h"]["time_until_start"]
            start_full = use_time["full_period"]["time_until_start"]
    
            send_message(chat_id, f"Waschmaschine:\nNaechster Start in {start_10[0]}:{start_10[1]} Stunden\nGuenstigster Start in {start_full[0]}:{start_full[1]} Stunden")
            
#         if cd.is_night_time() and day:
#             
#             sys.stdout.write("**Night time detected. Turning button  OFF**\n")
#             
#             bt_tv.off()
#             bt_wifi.off()
#             
#             day = False
# 
#         if not cd.is_night_time() and not day
#         
#             sys.stdout.write("**Night time detected. Turning button  ON**\n")
#             
#             bt_wifi.on()

def handle_messages(last_update_id=None, use_time=None):

    messages, last_update_id = check_for_messages(last_update_id)

    if messages:
        answer_messages(messages, use_time)
        
    return last_update_id    
   
