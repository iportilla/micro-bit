from microbit import *
import radio

radio.on()
while True:
    msg = radio.receive()
    if msg == "ping":
        display.show(Image.YES)
    sleep(100)
