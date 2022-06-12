# Copyright (c) 2015 Troy Dack
# Author: Troy Dack
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO
class MAX6675(object):
        def __init__(self, clk=None, cs=None, do=None,units = "c", spi=None, gpio=None):

                
                self._spi = None
                self.units = units
                # Handle hardware SPI
                if spi is not None:
                        self._spi = spi
                elif clk is not None and cs is not None and do is not None:
                        if gpio is None:
                                gpio = GPIO.RPiGPIOAdapter(RPi.GPIO)
                        self._spi = SPI.BitBang(gpio, clk, None, do, cs)
                else:
                        raise ValueError('Must specify either spi')
                self._spi.set_clock_hz(5000000)
                self._spi.set_mode(0)
                self._spi.set_bit_order(SPI.MSBFIRST)
                
        def get_temp(self):
                return getattr(self, "pass_" + self.units)(self.read())
            
        def read(self):
                #Return the thermocouple temperature value in degrees celsius.
                v = self._read16()
                # Check for error reading value.
                if v & 0x4:
                        return float('NaN')
                # Check if signed bit is set.
                if v & 0x80000000:
                        v >>= 3 # only need the 12 MSB
                        v -= 4096
                else:
                        # Positive value, just shift the bits to get the value.
                        v >>= 3 # only need the 12 MSB
                # Scale by 0.25 degrees C per bit and return value.
                return v * 0.25

        def _read16(self):
                # Read 16 bits from the SPI bus.
                raw = self._spi.read(2)
                if raw is None or len(raw) != 2:
                        raise RuntimeError('Did not read device!')
                value = raw[0] << 8 | raw[1]
                return value

        def pass_c(self, celsius):
            return celsius

        def pass_k(self, celsius):
            return celsius + 273.15

        def pass_f(self, celsius):
            return celsius * 9.0/5.0 + 32
