import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

portTrig = 23
portEcho = 24

GPIO.setup(portTrig, GPIO.OUT)
GPIO.setup(portEcho, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

pulse_start= time.time()

def process_pulse(channel):
    global pulse_start
    
    if GPIO.input(portEcho):
        pulse_start = time.time()
        pulse_end = pulse_start
    else:
        pulse_end = time.time()
        calculate(pulse_start, pulse_end)
    
def calculate(start, end):
    pulse_duration = end - start

    if pulse_duration  < 0.023:  # otherwise timeout
        #distance = (duration / 2) * speed_of_sound
        #speed_of_sound = 343 m/s = 34300 cm/s = 1125 ft/s = 13504 in/s
        distance = (pulse_duration / 2) * 13504

        print "Distance: {:0.2f} ({})".format(distance, pulse_duration)
    
    
GPIO.add_event_detect(portEcho, GPIO.BOTH, callback=process_pulse)

#reset Trigger and let settle
GPIO.output(portTrig, False)
time.sleep(0.5)

#Start ranging
try:
    while True:
        GPIO.output(portTrig, True)
        time.sleep(0.00001)
        GPIO.output(portTrig, False)

        time.sleep(0.2)
        
except KeyboardInterrupt:
    pass
    
finally:
    GPIO.cleanup()

