from microbit import *
import radio

radio.on()
while True:
    if button_a.is_pressed():
        radio.send("ping")
    sleep(100)
