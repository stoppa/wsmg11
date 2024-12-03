import machine
from machine import Pin
import time
import sys

# LED and sending pin configuration
LED_PIN = Pin("LED", Pin.OUT)
SEND_PIN = Pin(28, Pin.OUT)  # Replace 28 with the actual GPIO pin number


class Button:
    
    def __init__(self, button_number):
        """
        Initializes the Button class with the specific button number.
        This button number will be used to determine which file to read when sending signals.
        """
        self.button_number = str(button_number)  # Store the button number as a string
        self.button_state = False
    
    def _read_and_process_signal(self, state):
        """
        Reads the signal file based on the button's state ('on' or 'off') and processes the data.
        Each file contains timing and value information needed to send the signal.
        
        Args:
            state (str): The state of the button ("on" or "off").
        
        Returns:
            tuple: A list of toggle times and the starting value (either 0 or 1).
        """
        file_name = f"{self.button_number}_{state}_pi.txt"
        sys.stdout.write(f'**Reading signal file: {file_name}**\n')
        
        toggle_time = []  # Stores the times for toggling the signal
        value = []        # Stores the initial value (0 or 1)

        try:
            with open(file_name, "r") as file:
                for line in file:
                    # Strip any extra spaces or newlines and split the line by comma
                    line = line.strip()
                    values = line.split(',')
                    # Convert the values to float and append to the respective lists
                    toggle_time.append(float(values[0]))
                    value.append(float(values[1]))

        except FileNotFoundError:
            sys.stdout.write(f"**Error: File {file_name} not found**\n")
            return [], None
        
        return toggle_time, value[0] if value else None  # Return the toggle times and the first value

    def _send_signal(self, toggle_time, start_value):
        """
        Sends the signal based on the provided toggle times and initial value.
        The signal is toggled at each time interval specified in toggle_time.
        
        Args:
            toggle_time (list): List of time intervals for toggling the signal.
            start_value (int): The starting value of the signal (0 or 1).
        """
        if start_value == 1:
            SEND_PIN.off()
            LED_PIN.off()
        else:
            SEND_PIN.on()
            LED_PIN.on()
        
        start_time = time.ticks_us()  # Get the current time in microseconds
        old_time = start_time         # Track the last toggle time

        sys.stdout.write('**Started sending**\n')
        idx = 0
        
        # Loop through each toggle time and toggle the signal
        while idx < len(toggle_time):
            current_time = time.ticks_us()

            if current_time - old_time >= toggle_time[idx]:
                SEND_PIN.toggle()  # Toggle the send pin
                old_time = current_time  # Update the time of the last toggle
                idx += 1  # Move to the next toggle time
        
        sys.stdout.write('**Ended sending**\n')
        
    def get_button_state(self):
    
        return self.button_state
    
    def on(self):
        """
        Turns the button ON and sends the corresponding signal.
        Reads the 'on' signal file and sends the signal according to the timing values.
        """
        sys.stdout.write(f"**Turning Button {self.button_number} ON**\n")
        toggle_time, start_value = self._read_and_process_signal("on")
        
        if toggle_time:
            self._send_signal(toggle_time, start_value)
            SEND_PIN.on()  # Ensure that the send pin stays 'on' after sending the signal
            
        self.button_state = True
    def off(self):
        """
        Turns the button OFF and sends the corresponding signal.
        Reads the 'off' signal file and sends the signal according to the timing values.
        """
        sys.stdout.write(f"**Turning Button {self.button_number} OFF**\n")
        toggle_time, start_value = self._read_and_process_signal("off")
        
        if toggle_time:
            self._send_signal(toggle_time, start_value)
            SEND_PIN.off()  # Ensure that the send pin stays 'off' after sending the signal
        
        self.button_state = False
    def toggle(self):
        """
        Toggles the button between the ON and OFF states.
        """
        if self.button_state == True:
            self.off()  # If the current state is ON, turn it off
        else:
            self.on()   # If the current state is OFF, turn it on


# Example usage of the Button class
if __name__ == '__main__':
    
    # Create a Button object with number 1
    button1 = Button(5)
    
    time.sleep(3)
    
    # Turn Button 1 OFF
    button1.off()
    
    time.sleep(3)

    # Turn Button 1 ON
    button1.on()
    
    time.sleep(3)

    # Toggle Button 1's state
    button1.toggle()
    
    # This is a stupid test line
