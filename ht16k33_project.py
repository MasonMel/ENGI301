# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
HT16K33 I2C Library
--------------------------------------------------------------------------
License:
Copyright 2018-2023 <NAME>

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

import os
import time

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

# ... (Your existing constants)

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------
# Constants
HEX_DIGITS                  = [0x3f, 0x06, 0x5b, 0x4f,     # 0, 1, 2, 3
                               0x66, 0x6d, 0x7d, 0x07,     # 4, 5, 6, 7
                               0x7f, 0x6f, 0x77, 0x7c,     # 8, 9, A, b
                               0x39, 0x5e, 0x79, 0x71]     # C, d, E, F

LETTERS                     = { "a" : 0x77, "A" : 0x77,    # "A"
                                "b" : 0x7c, "B" : 0x7c,    # "b"
                                "c" : 0x58, "C" : 0x39,    # "c", "C"
                                "d" : 0x5e, "D" : 0x5e,    # "d"
                                "e" : 0x79, "E" : 0x79,    # "E"
                                "f" : 0x71, "F" : 0x71,    # "F"
                                "g" : 0x6F, "G" : 0x6F,    # "g"
                                "h" : 0x74, "H" : 0x76,    # "h", "H"
                                "i" : 0x04, "I" : 0x30,    # "i", "I"
                                "j" : 0x0e, "J" : 0x0e,    # "J"
# Cannot be implemented         "k" : None, "K" : None,    
                                "l" : 0x38, "L" : 0x38,    # "L"
# Cannot be implemented         "m" : None, "M" : None,    
                                "n" : 0x54, "N" : 0x54,    # "n"
                                "o" : 0x5c, "O" : 0x3f,    # "o", "O"
                                "p" : 0x73, "P" : 0x73,    # "P"
                                "q" : 0x67, "Q" : 0x67,    # "q"
                                "r" : 0x50, "R" : 0x50,    # "r"
                                "s" : 0x6D, "S" : 0x6D,    # "S"
                                "t" : 0x78, "T" : 0x78,    # "t"
                                "u" : 0x1c, "U" : 0x3e,    # "u", "U"
# Cannot be implemented         "v" : None, "V" : None,    
# Cannot be implemented         "w" : None, "W" : None,    
# Cannot be implemented         "x" : None, "X" : None,    
                                "y" : 0x6e, "Y" : 0x6e,    # "y"
# Cannot be implemented         "z" : None, "Z" : None,    
                                " " : 0x00,                # " "
                                "-" : 0x40,                # "-"
                                "0" : 0x3f,                # "0"
                                "1" : 0x06,                # "1"
                                "2" : 0x5b,                # "2"
                                "3" : 0x4f,                # "3"
                                "4" : 0x66,                # "4"
                                "5" : 0x6d,                # "5"
                                "6" : 0x7d,                # "6"
                                "7" : 0x07,                # "7"
                                "8" : 0x7f,                # "8"
                                "9" : 0x6f,                # "9"
                                "?" : 0x53                 # "?"
                              }                               

CLEAR_DIGIT                 = 0x7F
POINT_VALUE                 = 0x80

DIGIT_ADDR                  = [0x00, 0x02, 0x06, 0x08]
COLON_ADDR                  = 0x04

HT16K33_BLINK_CMD           = 0x80
HT16K33_BLINK_DISPLAYON     = 0x01
HT16K33_BLINK_OFF           = 0x00
HT16K33_BLINK_2HZ           = 0x02
HT16K33_BLINK_1HZ           = 0x04
HT16K33_BLINK_HALFHZ        = 0x06

HT16K33_SYSTEM_SETUP        = 0x20
HT16K33_OSCILLATOR          = 0x01

HT16K33_BRIGHTNESS_CMD      = 0xE0
HT16K33_BRIGHTNESS_HIGHEST  = 0x0F
HT16K33_BRIGHTNESS_DARKEST  = 0x00

# Maximum decimal value that can be displayed on 4 digit Hex Display
HT16K33_MAX_VALUE           = 9999




class HT16K33():
    """ Class to manage a HT16K33 I2C display """
    # Class variables
    bus = None
    address = None
    command = None
    def __init__(self, bus, address=0x70, blink=HT16K33_BLINK_OFF, brightness=HT16K33_BRIGHTNESS_HIGHEST):
        """ Initialize class variables; Set up display; Set display to blank """
        # Initialize class variables
        self.bus = bus
        self.address = address
        self.command = f"/usr/sbin/i2cset -y {bus} {address}"

        # Set up display
        self._setup(blink, brightness)
        # Set display to blank
        self.blank()

    def _setup(self, blink, brightness):
        """Initialize the display itself"""
        if self.command:
            os.system(f"{self.command} {HT16K33_SYSTEM_SETUP | HT16K33_OSCILLATOR}")
            os.system(f"{self.command} {HT16K33_BLINK_CMD | blink | HT16K33_BLINK_DISPLAYON}")
            os.system(f"{self.command} {HT16K33_BRIGHTNESS_CMD | brightness}")

    def encode(self, data, double_point=False):
        """Encode data to TM1637 format."""
        ret_val = 0
        try:
            if data != CLEAR_DIGIT:
                ret_val = HEX_DIGITS[data] + POINT_VALUE if double_point else HEX_DIGITS[data]
        except ValueError:
            raise ValueError("Digit value must be between 0 and 15.")
        return ret_val

    def set_digit(self, digit_number, data, double_point=False):
        """Update the given digit of the display."""
        if self.command:
            os.system(f"{self.command} {DIGIT_ADDR[digit_number]} {self.encode(data, double_point)}")

    def set_colon(self, enable):
        """Set the colon on the display."""
        if self.command:
            os.system(f"{self.command} {COLON_ADDR} {0x02 if enable else 0x00}")
    
    def set_digit_raw(self, digit_number, data):
        """Update the given digit of the display using raw data value"""
        if self.command:
            os.system(f"{self.command} {DIGIT_ADDR[digit_number]} {data}")

    def blank(self):
        """Clear the display to read nothing"""
        if self.command:
            self.set_colon(False)
            for i in range(4):
                self.set_digit_raw(i, 0x00)

    def clear(self):
        """Clear the display to read '0000'"""
        if self.command:
            self.set_colon(False)
            self.update(0)

    def update(self, value):
        """This function will clear the display and then set the appropriate digits."""
        if not 0 <= value <= HT16K33_MAX_VALUE:
            raise ValueError("Value is not between 0 and 9999")
        self.set_digit(3, value % 10)
        self.set_digit(2, (value // 10) % 10)
        self.set_digit(1, (value // 100) % 10)
        self.set_digit(0, (value // 1000) % 10)