import machine
from machine import Pin
import time
import sys


# Configuration of the receiving pin
RECEIVE_PIN = Pin(6, Pin.IN, Pin.PULL_DOWN)  # Replace 22 with the appropriate GPIO pin
MAX_DURATION = 0.1  # Maximum recording duration in seconds

# Use two separate lists
f = 45000
T = 1/f * 1000000

t = 0.2
n = int(t * f)
times = [0] * n
signals = [0] * n

def record_signal():
    start_time = time.ticks_us()  # Start time in microseconds
    old_time = start_time
    sys.stdout.write('**Started recording n:%d**\n' % n)
    
    idx = 0
    while idx < n:
        current_time = time.ticks_us()
        
        if current_time - old_time >= T:
            old_time = current_time
            times[idx] = current_time - start_time  # Time in microseconds
            signals[idx] = RECEIVE_PIN.value()
            idx = idx + 1
        
    sys.stdout.write('**Ended recording**\n')
    sys.stdout.write('%d samples recorded\n' % len(times))


def process_and_save_results():
    sys.stdout.write('**Processing results**\n')
    
    with open('6_off_raw.txt', 'w') as file:
        sys.stdout.write('**Saving results to file**\n')
        for time_stamp, signal in zip(times, signals):
            file.write('%d, %d\n' % (time_stamp, signal))

if __name__ == '__main__':
    record_signal()
    process_and_save_results()
