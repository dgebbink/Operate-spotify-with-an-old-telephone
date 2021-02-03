#!/usr/bin/env python
from __future__ import print_function

import RPi.GPIO as GPIO
import time
import sys
import requests
import os
from threading import Timer
from subprocess import call

PULSEINTERVAL = 0.18

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP) #draaischijf
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #aardpin
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP) #haak
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) #haak
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP) # draaienbegonnen

# https://pcmweb.nl/artikelen/programmeren/bouw-je-eigen-sommentelefoon-met-een-raspberry-pi/?article-page=1

state = 'IDLE'
pulses = 0
antwoord = 0
check1 = False

def executeCommand(command):
  #https://github.com/jishi/node-sonos-http-api
  print ("executeCommand " + str(command))
  option1 = 'playpause'
  option2 = 'groupVolume/+5'
  option3 = 'groupVolume/+10'
  option4 = 'groupVolume/-10'
  option5 = 'groupVolume/-5'
  option6 = 'say/mummer 6 niet in gebrui/nl-nl'
  option7 = 'say/mummer 7 niet in gebruik/nl-nl'
  option8 = 'shuffle'
  option9 = 'say/Bedankt voor het luisteren, tot de volgende keer, ik schakel mijzelf nu uit./nl-nl'
  option10 = 'say/Zoals aangegeven is het ten strengste verboden 0 te draaien! Ik overweeg nu om de politie in te schakelen/nl-nl'
  option11 = 'play'
  option12 = 'pause'
  option13 = 'next'

  if command == 1:
    urltoget = "http://localhost:5005/Werkkamer/" + option1
  if command == 2:
    urltoget = "http://localhost:5005/Werkkamer/" + option2
  if command == 3:
    urltoget = "http://localhost:5005/Werkkamer/" + option3
  if command == 4:
    urltoget = "http://localhost:5005/Werkkamer/" + option4
  if command == 5:
    urltoget = "http://localhost:5005/Werkkamer/" + option5
  if command == 6:
    urltoget = "http://localhost:5005/Werkkamer/" + option6
  if command == 7:
    urltoget = "http://localhost:5005/Werkkamer/" + option7
  if command == 8:
    urltoget = "http://localhost:5005/Werkkamer/" + option8
  if command == 9:
    urltoget = "http://localhost:5005/Werkkamer/" + option9
    call("sudo nohup shutdown -h now", shell=True)
  if command == 10:
    urltoget = "http://localhost:5005/Werkkamer/" + option10
  if command == 11:
    urltoget = "http://localhost:5005/Werkkamer/" + option11
  if command == 12:
    urltoget = "http://localhost:5005/Werkkamer/" + option12
  if command == 13:
    urltoget = "http://localhost:5005/Werkkamer/" + option13
#  else:
#    urltoget = "http://localhost:5005/Werkkamer/pause" 

  try:
    print (urltoget)
    r = requests.get(urltoget)
  except:
    print ("failed to coneect to Sonos API at http://localhost")
  if r.status_code != 200:
    print ("Error code returned from Sonos API")

def check(answer):
    print ("check answer" + str(answer))
    global check1
    if answer == 1  and check1 == False:
      # print ("1 en check is false")
      # answer = 1, but next time, print 
      check1 = True
      print ("Het  nummer is nu:", answer)
    elif check1 == True:
      # anwer = 1 and it's the 2nd time. so print 1
      print ("Het gedraaide nummer is:", answer)
      check1 = False
      executeCommand(answer)

def settozero():
    #print("check zero and execute" + str(pulses))
    global pulses
    global state

    state = 'IDLE'
    #check(pulses)
    executeCommand(pulses)
    pulses = 0

def my_callback(channel):
    #print("check callback")
    global state
    global pulses
    global timer

    if state == 'IDLE':
      state = 'COUNTING'
      timer = Timer(PULSEINTERVAL, settozero)
      timer.start()
    else:
      timer.cancel()
      timer = Timer(PULSEINTERVAL, settozero)
      timer.start()

    pulses+=1
    sys.stdout.flush()



def my_callbackxx(channel):
  print ("hallo 16 / aardping ingedrukt")
  option = 'next'
  urltoget = "http://localhost:5005/Werkkamer/" + option
  try:
    print (urltoget)
    r = requests.get(urltoget)
  except:
    print ("failed to coneect to Sonos API at http://localhost")
  if r.status_code != 200:
    print ("Error code returned from Sonos API")

def my_callbackAardpin(channel):
  print ("Aardpin ingedrukt")
  executeCommand(13)

def my_callbackHoorn(channel):
  #print ("hallo hoorn")
  if GPIO.input(18) == GPIO.HIGH:
    print ("Hoorn op de haak")
    executeCommand(11)
  else:
    print ("Hoorn van de haak")
    executeCommand(12)
#def my_callbackHoorn2(channel):
#  print ("hallo hoorn2")


GPIO.add_event_detect(16, GPIO.RISING, callback=my_callbackAardpin, bouncetime=800) #aardpin
GPIO.add_event_detect(18, GPIO.BOTH, callback=my_callbackHoorn, bouncetime=800) #hoorn
#GPIO.add_event_detect(23, GPIO.BOTH, callback=my_callbackHoorn2, bouncetime=800)



#GPIO.add_event_detect(21, GPIO.FALLING, callback=my_callback, bouncetime=80)
#GPIO.add_event_detect(14, GPIO.FALLING, callback=my_callback, bouncetime=80)

try:
  print ("Hier ben ik")
  while True:
#    global teller
    if GPIO.input(21) == GPIO.HIGH:
      my_callback(21)
      #print("21 is activated!")
#      print ("ik heb " + str(teller) + "geteld.")
    time.sleep(0.1)
    #print ('door')
    #check1 =  False
    #print ("check weer op False")
except KeyboardInterrupt:
  GPIO.cleanup()
  raise

GPIO.cleanup()


