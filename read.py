#!/usr/bin/env python

import signal
import time
import sys
import requests
import uuid
import json
import ast

from pirc522 import RFID
from tinydb import TinyDB, Query
from ast import literal_eval

# https://tinydb.readthedocs.io/en/latest/getting-started.html
# https://pcmweb.nl/artikelen/programmeren/bouw-je-eigen-sommentelefoon-met-een-raspberry-pi/?article-page=1
db = TinyDB ('/home/pi/test/db.json')
db.all()

for item in db:
  print str((item))

Card = Query()
search = db.search(Card.tag == 70246357)
names = [r['name'] for r in search]
names = ast.literal_eval(json.dumps(names))

#print (names[0])
#names.encode("utf-8")

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

signal.signal(signal.SIGINT, end_read)

print("Starting")
while run:
    rdr.wait_for_tag()

    (error, data) = rdr.request()
    #if not error:
        #print("\nDetected card ")

    (error, uid) = rdr.anticoll()
    if not error:
        #print ("\nCard read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
	CardU = str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
	#print ("\nCardU is set to: "+str(CardU))
	Card = Query()
	search = db.search(Card.tag == int(CardU))
	names = [r['name'] for r in search]
	names = ast.literal_eval(json.dumps(names))
	#print (names[0])

	#print ("wtf: "+ CardU)
        #print("Setting tag")
        #util.set_tag(uid)
        #print("\nAuthorizing")
        #util.auth(rdr.auth_a, [0x12, 0x34, 0x56, 0x78, 0x96, 0x92])
        #util.auth(rdr.auth_b, [0x74, 0x00, 0x52, 0x35, 0x00, 0xFF])
        #print("\nReading")
        #util.read_out(4)
        #print("\nDeauthorizing")
        #util.deauth()

        time.sleep(1)
	if  CardU == prevCardU:
	  print ("already detected. CardU is:" + CardU + "Fetching URL: " + names[0])
	else:
	  print ("new card and we set prevCardU to CardU: "+ CardU + "\nFetching URL: " + names[0])
	  prevCardU = CardU
	  #check Sonos API is responding
	  try:
	    r = requests.get("http://localhost:5005")
	  except:
	    print ("Failed to connect to Sonos API at http://localhost")
	    #return True

	  #clear the queue for every service request type except commands
	  #if servicetype != "command":
	  print ("Clearing Sonos queue")
	  r = requests.get("http://localhost:5005/clearqueue")
	  time.sleep(2)
	  #r = requests.get("http://localhost:5005/Werkkamer/say/sorry, ik zal er mee stoppen/nl-nl")

	  #use the request function to get the URL built previously, triggering the sonos
	  try:
            urltoget = "http://localhost:5005/Werkkamer/" + names[0] 
            r = requests.get(urltoget)
          except:
            print ("failed to coneect to Sonos API at http://localhost")
	  print ("Fetching URL via HTTP: "+ urltoget)

	  if r.status_code != 200:
	    print ("Error code returned from Sonos API")
	    #return True

