# scoring_logic.py

import Adafruit_BBIO.GPIO as GPIO
import time
import digitalio
from BangNote import setup as bang_setup, bang
from ht16k33_project import HT16K33

def scoring_logic_timer(display, stop_event):
    bang_setup()
    
    score = 0

    ir_pin = digitalio.DigitalInOut(board.P2_2)
    ir_pin.switch_to_input(pull=digitalio.Pull.UP)
    
    while not stop_event.is_set():
        if ir_pin.value == False:
            # A basket is made, increment the score by 2
            score += 2
            # Update the HT16K33 Display with the new score
            display.update(score)
            # Play sound or perform other actions for a made basket
            bang()                
            time.sleep(0.0001)
        else:
            time.sleep(0.0001)
