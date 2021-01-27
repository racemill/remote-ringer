#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import threading
import datetime
import logging

BUTTON = 4
BELL_RELAY = 27                         
RING_TRIGGER_LENGTH = .050
RING_COOLDOWN_LENGTH = 5

last_ring_time = time.time()

def initialize():
     GPIO.setwarnings(False)         # Disable warning mesages for GPIO
     GPIO.setmode(GPIO.BCM)          # Set to use  Boardcom markings, not pin position

     # Configure GPIO port 27 as Output to use as relay trigger, initial value set to not triggered
     # Hardware: Connect jumper from GPIO port 27 to Relay board signal pin
     GPIO.setup(BELL_RELAY, GPIO.OUT, initial=GPIO.HIGH)     

     # Configure GPIO port 4 as Input for Hardware button, Use built in pull Up resistor
     # Hardware: Connect Button leads to GPIO port4 and GPIO ground pin
     GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

     # Detect Button pushes and then do callback to ring function
     GPIO.add_event_detect(BUTTON, GPIO.FALLING, callback=button_callback)

def button_callback(channel):
    logging.info('Button on Bell-Ringer box pressed at    ')
    print("Button pressed!")
    ringOnce()

def ringOnce():

     global last_ring_time

     now = time.time()
     time_since_last_ring = int(now - last_ring_time)

     if time_since_last_ring < RING_COOLDOWN_LENGTH:
          print("RING BLOCKED, still in cooldown period")
          return False

     last_ring_time = now

     GPIO.output(BELL_RELAY, GPIO.LOW)   # Set GPIO output to trigger the relay
     time.sleep(RING_TRIGGER_LENGTH)     # Keep GPIO output triggered the needed time to pull clapper
     GPIO.output(BELL_RELAY, GPIO.HIGH)  # Set GPIO output to reset/relax the relay
     return True

def cleanup():
     GPIO.cleanup()                      # GPIO cleanup for a clean exit (reset ports used)

