import ntptime  # NTP library for time synchronization
import sys
import time

# Vienna timezone offset in hours
VIENNA_STANDARD_TIME_OFFSET = 1  # UTC+1
VIENNA_DST_OFFSET = 2  # UTC+2 during Daylight Saving Time (DST)

def is_dst_in_vienna():
    """
    Determines if daylight saving time (DST) is currently in effect in Vienna.
    
    Returns:
        bool: True if DST is in effect, False otherwise.
    """
    current_time = time.localtime(ntptime.time() + VIENNA_STANDARD_TIME_OFFSET * 3600)
    year, month, day, weekday = current_time[0], current_time[1], current_time[2], current_time[6]
    
    # DST starts last Sunday in March and ends last Sunday in October
    if month < 3 or month > 10:
        return False
    if month > 3 and month < 10:
        return True
    
    # Calculate the last Sunday of March or October
    last_sunday = day - weekday if day - weekday > 0 else day - weekday + 7

    # If it's March and after the last Sunday, DST is in effect
    if month == 3:
        return day >= last_sunday
    # If it's October and before the last Sunday, DST is in effect
    if month == 10:
        return day < last_sunday
    return False

def sync_time():
    """
    Synchronizes the local system time using an NTP server and adjusts it for Vienna timezone.
    """
    try:
        ntptime.settime()  # Set system time to UTC using the NTP server
        # Calculate Vienna time offset
        vienna_offset = VIENNA_DST_OFFSET if is_dst_in_vienna() else VIENNA_STANDARD_TIME_OFFSET
        adjusted_time = time.time() + vienna_offset * 3600  # Apply the offset
        time.localtime(adjusted_time)  # Set local time with Vienna adjustment
        sys.stdout.write('**Time synchronized with NTP server (Vienna Time)**\n')
    except Exception as e:
        sys.stdout.write(f'**Failed to sync time: {str(e)}**\n')
        
def get_time(raw=False):
    
    if raw:
        return time.time() + (VIENNA_DST_OFFSET if is_dst_in_vienna() else VIENNA_STANDARD_TIME_OFFSET) * 3600
    else:
        return time.localtime(time.time() + (VIENNA_DST_OFFSET if is_dst_in_vienna() else VIENNA_STANDARD_TIME_OFFSET) * 3600)

def is_night_time():
    """
    Determines if current Vienna time is between 00:00 and 07:00.
    
    Returns:
        bool: True if current time is between 00:00 and 07:00, False otherwise.
    """
    current_time = get_time()
    current_hour = current_time[3]
    current_minute = current_time[4]
    
    # Check if the current time is between 19:45 and 07:00
    if (current_hour > 0) and (current_hour < 7):
        return True
    return False

def is_weekend():
    """
    Determines if the current Vienna time is during the weekend.
    Weekend is defined as:
        - Friday after 17:00
        - Saturday (all day)
        - Sunday (all day)
    
    Returns:
        bool: True if current time is during the weekend, False otherwise.
    """
    current_time = get_time()  # Current local time in Vienna
    current_weekday = current_time[6]  # 0=Monday, 6=Sunday
    current_hour = current_time[3]
    current_minute = current_time[4]
    
    # Check if it is Friday after 17:00
    if current_weekday == 4 and (current_hour > 17 or (current_hour == 17 and current_minute == 0)):
        return True
    # Check if it is Saturday or Sunday
    elif current_weekday in [5, 6]:
        return True
    
    return False


def plot_daytime():
    """
    Prints a visual representation of daytime and nighttime as a bar adjusted to Vienna timezone.
    """
    current_time = get_time()
    current_hour = current_time[3]
    current_minute = current_time[4]

    # Define time blocks as 1-hour segments for simplicity
    daytime_hours = ["-" if 7 <= h < 19 else "*" for h in range(24)]
    
    # Mark the current hour with '|' to indicate the current time
    daytime_hours[current_hour] = "|"
    
    # Convert the list to a string and print it
    day_night_bar = "".join(daytime_hours)
    sys.stdout.write(f"\nCurrent Vienna time: {current_hour:02}:{current_minute:02}\n")
    sys.stdout.write("Day/Night Bar:\n")
    sys.stdout.write(day_night_bar + "\n")
    

if __name__ == '__main__':
    sync_time()

    while True:
        if is_night_time():
            sys.stdout.write("**Night time detected. Turning off**\n")
        else:
            sys.stdout.write("**Day time detected. Keeping on**\n")
        
        plot_daytime()  # Plot the day/night bar
        time.sleep(60)  # Check every 60 seconds
