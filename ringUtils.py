#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import threading
import datetime

BUTTON = 4
BELL_RELAY = 27                         
RING_TRIGGER_LENGTH = .050
RING_COOLDOWN_LENGTH = 5

last_ring_time = time.time()

def initialize():
     GPIO.setwarnings(False)         # Disable warning mesages for GPIO
     GPIO.setmode(GPIO.BCM)          # Set to use  Boardcom markings, not pin position

     GPIO.setup(BELL_RELAY, GPIO.OUT, initial=GPIO.HIGH)      # Setup GPIO output port to relay for bell ringer, GPIO.HIGH means not triggered, relay off  
     GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Setup GPIO input port from button.

     GPIO.add_event_detect(BUTTON, GPIO.RISING, callback=button_callback)

def button_callback(channel):
    now = datetime.datetime.now()
    print("Button pressed!", now.strftime('%I:%M:%S %a, %b %d, %Y'))
    ringOnce()

def ringOnce():

     global last_ring_time

     now = time.time()
     time_since_last_ring = int(now - last_ring_time)

     if time_since_last_ring < RING_COOLDOWN_LENGTH:
          print("RING BLOCKED, still in cooldown period")
          return False

     last_ring_time = now

     GPIO.output(BELL_RELAY, GPIO.LOW)   # Set GPIO pin output to trigger relay
     time.sleep(RING_TRIGGER_LENGTH)     # Keep GPIO pin up in order to allow time to pull dinger
     GPIO.output(BELL_RELAY, GPIO.HIGH)  # Set GPIO pin out put to reset relay
     return True

def cleanup():
     GPIO.cleanup()                      # GPIO cleanup for a clean exit (reset ports used)

