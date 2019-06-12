#!/usr/bin/env python
import sys
import sqlite3
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
user = sys.argv[1]
camera = sys.argv[2]
f = open("LOG.txt", "a")
f.write(str(user) + " :  " + str(camera))
reader = SimpleMFRC522()
try:
	id, text = reader.read()
finally:
	GPIO.cleanup()
f.write(str(id))

conn = sqlite3.connect("~/RFID_Reader/rfid_web_interface/instance/flaskr.sqlite")
cur = conn.cursor()
sql = "UPDATE angajati SET id_tag = ? WHERE nume = ? and acces_camera = ?"
cur.execute(sql, (id, user, camera))
cur.commit()
cur.close()
conn.close()
f.close()
