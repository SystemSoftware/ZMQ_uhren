## I'm a consumer. 

import zmq
import time
import datetime
import random
import argparse

parser = argparse.ArgumentParser(description='Worker')
parser.add_argument('--port', required=True, type=int,
help="Port for the worker, i.e. 5555 - Warning - reserves this port and port +1!")
args = parser.parse_args()

print("Worker: " + str(args.port))

# ZMQ Context erstellen
context = zmq.Context()
# Hoere auf Pull Verbindung vom Server
# auf Port, Verbindung um Ergebnisse zu pushen 
push_result = context.socket(zmq.PUSH)
push_result.bind("tcp://*:" + str(args.port))
# Hoere auf Push Verbindung vom Server
# auf Port + 1, Verbindung um Arbeit zu pullen 
pull_work = context.socket(zmq.PULL)
pull_work.bind("tcp://*:" + str(int(args.port)+1))
print("Wait for connection from coordinator")



lamp = 0


while True:
    ##entscheide, ob lokales Ereigniss eintritt oder nicht
    rnd_local = random.randint(0,1)
    if rnd_local == 1:
        print "Random Local Event!"
        lamp = lamp + 1


    ##verwalte Empfangs-Ereignisse
    rec_stamp = pull_work.recv_json()
    lamp = lamp +1
    print "Received Lampord:"+ rec_stamp
    print "Own Lampord:" + lamp
    lamp = max(rec_stamp, lamp)+1
    result = lamp

    ##Sende eigene Lamport-Zeit zurueck (und erhoehe um 1 wegen Sende-Ereignis)
    push_result.send_json(result)
    lamp = lamp + 1
        
