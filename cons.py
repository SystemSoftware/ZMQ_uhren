## I'm a consumer. I'm checking for right causality!

import zmq
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


while True:

    ##entscheide, ob lokales Ereigniss eintritt oder nicht
    rnd_local = random.randint(0,1)
    if rnd_local == 1:
        print "Random Local Event!"
        timestamp = datetime.datetime.now()
        print timestamp
    result = "No result yet..."  

    rec_stamp = pull_work.recv_json()
    own_stamp = datetime.datetime.now()
    ##ueberpruefe korrekte lokale Uhr
    if own_stamp < timestamp:
        result = "Something went wrong at consumer local"

    ##vergleiche den empfangenen timestamp mit dem lokalen timestamp
    ## um korrekte Kausualitaet zu pruefen
    print "Received stamp:"+ rec_stamp
    print "self-generated stamp:" + own_stamp
    if rec_stamp < own_stamp:
        result = "Causality OK!"
        print result
    else:
        result = "Something wrong..."

    push_result.send_json(result)
        
