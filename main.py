
from machine import Pin, ADC
import time

# Pins and pin configs
ledBuiltIn = Pin(2,Pin.OUT)  # for onboard LED blink
led12 = Pin(12,Pin.OUT)
led14 = Pin(14,Pin.OUT)


def blink():
  ledBuiltIn.on()
  time.sleep_ms(1000)
  ledBuiltIn.off()
  time.sleep_ms(1000)
  led12.on()
  time.sleep_ms(1000)
  led14.on()

  led12.off()
  time.sleep_ms(1000)
  led14.off()

while True:
  blink()
