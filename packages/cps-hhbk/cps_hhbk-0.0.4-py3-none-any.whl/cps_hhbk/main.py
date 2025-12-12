"""
Dieses Programm wird für die Steuerung des Gesamten Systems genutzt.
"""

import time
from . import ky001
from . import ky006
from . import led

def get_state():
    if ky001.read_temp() <= 25.0:
        return "GREEN"
    elif ky001.read_temp() <= 30.0:
        return "YELLOW"
    elif ky001.read_temp() <= 35.0:
        return "RED"
    elif ky001.read_temp() >= 35.0:
        return "REDPLUS"
    else:
        return "ERROR"
  
def act_on_state(state):
    if state == "GREEN":
        ky006.buzz_off()
        led.set_green("on")
        led.set_yellow("off")
        led.set_red("off")
    elif state == "YELLOW":
        led.set_yellow("on")
        led.set_green("off")
        led.set_red("off")
    elif state == "RED":
        led.set_red("on")
        led.set_green("off")
        led.set_yellow("off")
    elif state == "REDPLUS":
        ky006.buzz_on()
        led.set_red("on")
        led.set_green("off")
        led.set_yellow("off")
    else:
        print("Somethings broken.")



if __name__ == "__main__":
    while True:
        state = get_state()
        print("Current State:", state)
        act_on_state(state)
        time.sleep(1)
