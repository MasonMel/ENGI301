"""
--------------------------------------------------------------------------
LCD Shoot n Pull Display
--------------------------------------------------------------------------
License:   

Copyright 2021 Angelica Torres

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


This code was downloaded from the adafruit library for the LCD and edited.
https://learn.adafruit.com/character-lcds/python-circuitpython
Their licensing information is :
  - SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
  - SPDX-License-Identifier: MIT
--------------------------------------------------------------------------
Use the following hardware components:  
  - RGB backlight positive LCD 16x2  
Requirements:
  - Display messages on screen
Uses:
  - adafruit_character_lcd.character_lcd developed for LCD
  - time
  - board
  - digitalio
"""

"""Simple test for monochromatic character LCD on PocketBeagle"""
import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# Raspberry Pi Pin Config:
lcd_rs = digitalio.DigitalInOut(board.P2_18)
lcd_en = digitalio.DigitalInOut(board.P2_17)
lcd_d7 = digitalio.DigitalInOut(board.P2_20)
lcd_d6 = digitalio.DigitalInOut(board.P2_19)
lcd_d5 = digitalio.DigitalInOut(board.P2_24)
lcd_d4 = digitalio.DigitalInOut(board.P2_22)
button_pin = digitalio.DigitalInOut(board.P2_3)

# Initialise the lcd class
lcd = characterlcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

# Configure the button pin
button_pin.switch_to_input(pull=digitalio.Pull.UP)
lcd.clear() #Ensures Screen is blank on start

# Function to display blinking message until the button is pressed
def wait_for_button_press(message):
    while button_pin.value:
        lcd.message = message
        time.sleep(0.5)
        lcd.clear()
        time.sleep(0.5)

# Function to display countdown
def countdown(t, message):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        lcd.message = timer
        time.sleep(1)
        t -= 1
    lcd.clear()
    lcd.message = message
    time.sleep(1)
    lcd.clear()
    
def countdown_end(t, message):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        lcd.message = timer
        time.sleep(1)
        t -= 1
    lcd.clear()
    lcd.message = message
    time.sleep(3)
    lcd.clear()

# Function to display play again message
def play_again():
    while button_pin.value:
        lcd.message = "Press button\n to play again"
        time.sleep(0.5)
        lcd.clear()
        time.sleep(0.5)

# Wait for button press to start the game
wait_for_button_press("Press button\n to start")

while True:
    # Display countdown and "Begin!"
    countdown(5, "Begin!")

    # Display countdown and "Game over!"
    countdown_end(45, "Game over!")

    # Display play again message and wait for button press
    play_again()
