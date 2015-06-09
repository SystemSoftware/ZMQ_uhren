##I'm the coordinator. I'm sending my timestamps to random consumers 

import zmq
import datetime
import random
import argparse

context = zmq.Context()
push_work = context.socket(zmq.PUSH)
pull_result = context.socket(zmq.PULL)


# CLI Arugmente parsen und uebernehmen (zum herausfinden der Teilnehmer)
parser = argparse.ArgumentParser(description='Cordinator')
parser.add_argument('--nodes', required=True, nargs='*',
help="Enter List of IP Adresses and Ports of Nodes, i.e. 127.0.0.1 5555 192.168.1.2 5555")
args = parser.parse_args()
 

prozesse = (len(args.nodes)/2)

final_print = "Everything fine so far.."


while True:
    timestamp = datetime.datetime.now()
    ##entscheide, ob lokales Ereigniss eintritt oder nicht
    rnd_local = random.randint(0,1)
    if rnd_local == 1:
        print "Random Local Event!"
        timestamp = datetime.datetime.now()
        print timestamp
    print "Checking who's turn it is..."
    turn = random.randint(1,prozesse)
    print turn
    print"Checking for the right address..."
    NodeIP = args.nodes[turn/2]
    NodePort = args.nodes[turn/2 +1]
    print "gettin current time..."
    ##ueberpruefe, ob lokale Zeit korrekt funktioniert
    if timestamp >= datetime.datetime.now():
        final_print = "Error in Causality happend local!"
        print final_print
    timestamp = datetime.datetime.now()
    print timestamp
    push_work.connect("tcp://" + NodeIP + ":" + NodePort)
    push_work.send_json(timestamp)
    print "The timestamp" + timestamp + "was send to tcp://" + NodeIP + ":" + NodePort
    ##senden an den entsprechenden prozess, der dran ist
    ## vorerst einfach eine print-anweisung
    print "Checking for any results..."
    pull_result.connect("tcp://" + NodeIP + ":" + NodePort)
    result = pull_result.recv_json()
    if result == "Causality OK!":
        print final_print
    else:
        final_print = "Error in Causality already happend!"
        print final_print
    
    




    
    

    
