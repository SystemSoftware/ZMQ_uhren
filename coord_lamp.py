##I'm the coordinator. I'm sending my timestamps to random consumers 

import zmq
import time
import datetime
import random
import argparse

context = zmq.Context()
push_work = context.socket(zmq.PUSH)
pull_result = context.socket(zmq.PULL)

##irgendwie rausfinden wie viele prozesse beteiligt sind

# CLI Arugmente parsen und uebernehmen 
parser = argparse.ArgumentParser(description='Cordinator')
parser.add_argument('--nodes', required=True, nargs='*',
help="Enter List of IP Adresses and Ports of Nodes, i.e. 127.0.0.1 5555 192.168.1.2 5555")
args = parser.parse_args()
 
lamp = 0

prozesse = (len(args.nodes)/2)

final_print = "Everything fine so far.."

while True:
    ##entscheide, ob lokales Ereigniss eintritt oder nicht
    rnd_local = random.randint(0,1)
    if rnd_local == 1:
        print "Random Local Event!"
        lamp = lamp + 1

    ## Sende Lamport-Zeit an zufaelligen Teilnehmer
    print "Checking who's turn it is..."
    turn = random.randint(1,prozesse)
    print turn
    print"Checking for the right address..."
    NodeIP = args.nodes[turn/2]
    NodePort = args.nodes[turn/2 +1]
    print "gettin current Lampord-Time..."
    lamp = lamp +1
    print lamp
    push_work.connect("tcp://" + NodeIP + ":" + NodePort)
    push_work.send_json(lamp)
    print "The Lampord-Time" + str(lamp) + "was send to tcp://" + NodeIP + ":" + NodePort

    ## Verwalte zurueckgelieferte Ergebnisse
    print "Checking for any results..."
    pull_result.connect("tcp://" + NodeIP + ":" + NodePort)
    result = pull_result.recv_json()
    lamp = max(lamp, result) + 1
    print "New Lampord-Time: "+ lamp
    
    




    
    

    
