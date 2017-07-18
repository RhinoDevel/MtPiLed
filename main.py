# RhinoDevel, Marcel Timm, 2017.07.17

import RPi.GPIO as GPIO
import time
import threading

state_wait = 0
state_init = 1
state_done = 2

init_state_seconds = 3
done_flash_seconds = 1

pinmode = GPIO.BCM # GPIO.BOARD
inpinnr = 27 # BCM
outpinnr = 17 # BCM
bouncems = 200

lock = threading.Lock()
#
state = state_wait
init_seconds = 0

def on_press(pinnr):
    global state
    global init_seconds
    
    with lock:
        if state == state_wait:
    	    state = state_init
            return

        if state == state_init:
            state = state_wait
            init_seconds = 0
            return

def led_on_off(onseconds, offseconds):
    #print('Enabling LED..')
    GPIO.output(outpinnr, GPIO.HIGH)

    #print('Waiting '+str(onseconds)+' second(-s)..')
    time.sleep(onseconds)

    #print('Disabling LED..')
    GPIO.output(outpinnr, GPIO.LOW)

    #print('Waiting '+str(offseconds)+' second(-s)..')
    time.sleep(offseconds)

state_copy = -1
i = 0
j = 0

GPIO.setwarnings(False)
GPIO.setmode(pinmode)
GPIO.setup(outpinnr, GPIO.OUT)
GPIO.setup(
    inpinnr, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(
    inpinnr,
    GPIO.FALLING,
    callback=on_press,
    bouncetime=bouncems)

while True:
    with lock:
        state_copy = state

    if state_copy == state_wait:
        time.sleep(1) # Sleep for a second.
        continue

    if state_copy == state_init:
        led_on_off(0.6, 0.4) # "Sleep" for a second.
        with lock:
            if state == state_wait:
                continue
            init_seconds = init_seconds + 1
            if init_seconds == init_state_seconds:
                state = state_done
        continue

    if state_copy == state_done:
        break

# Do some fancy point-of-no-return flashing:
#
i = 0
while i < done_flash_seconds:
    j = 0
    while j < 10:
        led_on_off(0.05, 0.05)
        j = j + 1
    i = i + 1

#print('Cleaning up..')
GPIO.cleanup()

#print('Done.')
