from microbit import *

while True:
    if button_a.is_pressed():
        temp = temperature()
        light = display.read_light_level()
        print("TEMP:{},LIGHT:{}".format(temp, light))

        reply = uart.read()
        if reply:
            display.scroll(str(reply, "utf-8"))
    sleep(100)
