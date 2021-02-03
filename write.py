#!/usr/bin/env python

import signal
import time
import sys
import requests
import uuid
import json
import ast

from pirc522 import RFID
from tinydb import TinyDB, Query, where
from tinydb.operations import delete
import tinydb.operations
db = TinyDB('/home/pi/test/db.json')

# throw away all data to start with an empty database:
# db.truncate()
#db.insert({'tag': 744205122, 'name': 'playpause'})
#db.insert({'tag': 70246357, 'name': 'spotify/now/spotify:album:4baa3THO8wKLMrASaem2Ri'})
#db.insert({'tag': 1364217220, 'name': 'spotify/now/spotify:album:1yIqauTni1V7l7djYAKSsZ'})

db.all()

for item in db:
  print str((item))
#db.close()

Card = Query()
run = True
rdr = RFID()
util = rdr.util()
util.debug = True
CardU = 00000000
prevCardU = CardU

def end_read(signal,frame):
    global run
    print("\nCtrl+C captured, ending read.")
    run = False
    rdr.cleanup()
    sys.exit()
    db.close()

def yes_or_no(question):
    reply = str(raw_input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no("Uhhhh... please enter ")

while run:
  rdr.wait_for_tag()
  (error, data) = rdr.request()
  #if not error:
  #print("\nDetected card ")
  (error, uid) = rdr.anticoll()
  if not error:
    #print ("\nCard read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
    CardU = str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
    print ("\nCardU is set to: "+str(CardU))
    Card = Query()
    search = db.search(Card.tag == int(CardU))
    if (search):
      #print search
      names = [r['name'] for r in search]
      names = ast.literal_eval(json.dumps(names))
      print (names[0])
      question = "update card from db?"
      if (yes_or_no(question)):
        db.remove(where('tag') == int(CardU))
        db.all
        for item in db:
          print str((item))

    else:
      print ("bestaat niet?")
      g = raw_input("Enter Spotify URL (eg. spotify/now/spotify:playlist:1khZWzUAbIqQalUSiB66y0 : ")
      print g
      url= "spotify/now/" + g
      print url

      #insert = 'tag': 1364217220, 'name': 'spotify/now/spotify:album:1yIqauTni1V7l7djYAKSsZ'

      db.insert({'tag': int(CardU), 'name': url })
      db.all
      for item in db:
        print str((item))
      #names = [r['name'] for r in search]
      #names = ast.literal_eval(json.dumps(names))
      #print (names[0])

    time.sleep(1)
