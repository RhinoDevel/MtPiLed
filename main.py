# RhinoDevel, Marcel Timm, 2017.07.17

import RPi.GPIO as GPIO
import time

pinmode = GPIO.BCM # GPIO.BOARD
inpinnr = 27 # BCM
outpinnr = 17 # BCM
bouncems = 200

done = False

def on_press(pinnr):
    global done
    
    done = True
    GPIO.remove_event_detect(pinnr)

def led_on_off(onseconds, offseconds):
    print('Enabling LED..')
    GPIO.output(outpinnr, GPIO.HIGH)

    print('Waiting '+str(onseconds)+' second(-s)..')
    time.sleep(onseconds)

    print('Disabling LED..')
    GPIO.output(outpinnr, GPIO.LOW)

    print('Waiting '+str(offseconds)+' second(-s)..')
    time.sleep(offseconds)


#GPIO.setwarnings(False)
GPIO.setmode(pinmode)
GPIO.setup(outpinnr, GPIO.OUT)
GPIO.setup(
    inpinnr, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(
    inpinnr,
    GPIO.FALLING,
    callback=on_press,
    bouncetime=bouncems)

#while GPIO.input(inpinnr)==0:
while not done:
    led_on_off(1, 1)

#print('Waiting for button release..')
#GPIO.wait_for_edge(inpinnr, GPIO.RISING)

#print('Waiting for button press..')
#GPIO.wait_for_edge(inpinnr, GPIO.FALLING)
#time.sleep(0.2)

print('Cleaning up..')
GPIO.cleanup()

print('Done.')
