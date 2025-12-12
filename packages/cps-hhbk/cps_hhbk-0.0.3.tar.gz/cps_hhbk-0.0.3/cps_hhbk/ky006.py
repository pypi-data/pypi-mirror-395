"""
Helper zum Ansteuern des KY-006 Buzzer
"""

import time
from gpiozero import PWMOutputDevice

#Der GPIO Pin wird hier mit der ersten Zahl gesetzt.
buzzer = PWMOutputDevice(6, frequency=500, initial_value=0.0)

def buzz_on():
    """Turn the buzzer on."""
    buzzer.value = 0.5

def buzz_off():
    """Turn the buzzer off."""
    buzzer.value = 0.0

if __name__ == '__main__':
    buzz_on()
    time.sleep(1)
    buzz_off()
    time.sleep(1)

