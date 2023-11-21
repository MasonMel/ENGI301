# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Skittle Dispenser
--------------------------------------------------------------------------
License:   
Copyright 2018 Nicholas Lester

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

Use IR breakbeam to detect a made basket. Then, play a note with a piezo element. Finally, add two points to the scoreboard. 

Requirements:
    - Play a note when the ir beam is broken.
    - Display score, that increases by two for each made basket

"""



"""
This sets the path to find the python file ht16k33_i2c_base. This may need to
change depending on where ht16k33_i2c_base is located.
"""
import sys
import time
import math
import random

import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from ht16k33_project import HT16K33

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------
servo_pin = "P1_36"
piezo_pin = "P2_3"
FSR_pin = "AIN5"
ir_pin = "P2_2"


# ------------------------------------------------------------------------
# Note Library
# ------------------------------------------------------------------------
NOTE_F5  = 698
NOTE_C7  = 2093


# ------------------------------------------------------------------------
# Main Tasks
# ------------------------------------------------------------------------

def setup():
    """Sets up the hardware components."""
    ADC.setup()
    GPIO.setup(ir_pin, GPIO.IN)
    """ HT16K33.display_setup() 
    HT16K33.display_clear() """
    
# end def

def play_note(Note, Length):
    """Plays a given note for a given length."""
    PWM.start(piezo_pin, 50, Note)
    time.sleep(Length)
    PWM.stop(piezo_pin)
    PWM.cleanup() #Stops continuous tone after function runs

# end def

    
def bang():
    """Plays a sound for a made basket"""
    play_note(NOTE_F5, 0.1)  # Play the first note
    time.sleep(0.1)  # Add a short pause between the notes
    play_note(NOTE_C7, 0.2)  # Play the final note with a longer duration
   # end def


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    setup()
    
    display = HT16K33(1, 0x70)

    bang()
    
    score = 0

    while True:
        if GPIO.input("P2_2") == 0:
            #Basket is made
            print("basket")
            score += 2
            #Update display
            display.update(score)
            bang()
            time.sleep(0.05)
        else:
            pass
        time.sleep(0.1)
