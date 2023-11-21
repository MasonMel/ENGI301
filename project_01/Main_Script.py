"""
--------------------------------------------------------------------------
Main_Script
--------------------------------------------------------------------------
License:   
Copyright 2023 Mason Melendez

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
-------------------------------------------------------------------------- 
"""
# Import necessary libraries
import time
import threading
import digitalio
import board
import Adafruit_BBIO.PWM as PWM
import adafruit_character_lcd.character_lcd as characterlcd
from scoring_logic import scoring_logic_timer, bang_setup
from ht16k33_project import HT16K33
from BangNote import bang

# LCD setup
lcd_columns = 16
lcd_rows = 2
lcd_rs = digitalio.DigitalInOut(board.P2_18)
lcd_en = digitalio.DigitalInOut(board.P2_17)
lcd_d7 = digitalio.DigitalInOut(board.P2_20)
lcd_d6 = digitalio.DigitalInOut(board.P2_19)
lcd_d5 = digitalio.DigitalInOut(board.P2_24)
lcd_d4 = digitalio.DigitalInOut(board.P2_22)

lcd = characterlcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

# GPIO setup
button_pin = digitalio.DigitalInOut(board.P2_3)
ir_pin = digitalio.DigitalInOut(board.P2_2)
ir_pin.switch_to_input(pull=digitalio.Pull.UP)

# Initialize the HT16K33 Display
display = HT16K33(1, 0x70)


# Function to display blinking message until the button is pressed
def wait_for_button_press(message):
    lcd.clear()
    while button_pin.value:
        lcd.message = message
        time.sleep(0.5)
        lcd.clear()
        time.sleep(0.5)

# Function to display countdown on LCD
def countdown(t, message):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        lcd.message = timer
        time.sleep(1)
        t -= 1

    lcd.clear()  # Clear the LCD after the countdown is complete
    lcd.message = message
    time.sleep(1)
    lcd.clear()

# Start the main script
if __name__ == '__main__':
    # Wait for button press to start the game
    wait_for_button_press("Press button\n to start")

    # Initialize components
    bang_setup()

    # Start the score at 0
    score = 0

    # Event to signal the scoring logic to stop after 20 seconds
    stop_scoring_event = threading.Event()

    # Start the scoring logic in a separate thread
    scoring_thread = threading.Thread(target=scoring_logic_timer, args=(display, stop_scoring_event))
    scoring_thread.start()
    
    try:
        # Initial countdown of 5 seconds
        countdown(5, "Begin!")
    
        # Sets game timer to 20 seconds
        t = 20 
    
        while t>0 and not stop_scoring_event.is_set():
            mins, secs = divmod(t, 60)
            timer = '%02d:%02d' % (mins, secs)
            lcd.message = timer
            time.sleep(0.05) #Sets how long to wait in between checking if IR break beam is in tact
            t -= 0.05
    
            if ir_pin.value == False: 
                # Add score
                score += 2
                # Update Display
                display.update(score)
                # Play sound
                bang()
    
            if t == 0:
                # Signal the scoring thread to stop after 45 seconds
                stop_scoring_event.set()
                # Wait for the scoring thread to finish
                scoring_thread.join()
                break  # Exit the loop right before displaying "Game over!"
    
        lcd.clear()  # Clear the LCD after the countdown is complete
        lcd.message = "Game over!"
        time.sleep(3)  # Display "Game over!" for 3 seconds
        lcd.clear()
        display = HT16K33(1, 0x70)
    
    except KeyboardInterrupt:
        pass  # Handle KeyboardInterrupt (Ctrl+C) gracefully