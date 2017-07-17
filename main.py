# RhinoDevel, Marcel Timm, 2017.07.17

import RPi.GPIO as GPIO
import time

done = False

def on_press(pinnr):
    global done
    
    done = True
    GPIO.remove_event_detect(pinnr)

#GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # GPIO.BOARD

GPIO.setup(17, GPIO.OUT)
GPIO.setup(
    27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(
    27,
    GPIO.FALLING,
    callback=on_press,
    bouncetime=200)

#while GPIO.input(27)==0:
while not done:
    print('Enabling LED..')
    GPIO.output(17, GPIO.HIGH)

    print('Waiting one second..')
    time.sleep(1)

    print('Disabling LED..')
    GPIO.output(17, GPIO.LOW)

    print('Waiting one second..')
    time.sleep(1)

#print('Waiting for button release..')
#GPIO.wait_for_edge(27, GPIO.RISING)

#print('Waiting for button press..')
#GPIO.wait_for_edge(27, GPIO.FALLING)
#time.sleep(0.2)

print('Cleaning up..')
GPIO.cleanup()

print('Done.')
