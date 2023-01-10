#!/bin/bash

read -p " Execute script? (y/n): " response
if [[ $response == y ]]; then

    printf " Starting the Nodes....\\n"
        printf " Starting Replica0 \\n"
	
        osascript -e 'tell application "Terminal" to do script "conda activate bcr && cd Desktop/bcr/src && python -m da -r  --message-buffer-size=1280000 --logfile --logfilename logdirect/replica0.log --logfilelevel info -n ReplicaNode0  -D replica.da "' >/dev/null
    
        printf " Starting Replica1 \\n"
        osascript -e 'tell application "Terminal" to do script "conda activate bcr && cd Desktop/bcr/src && python -m da -r  --message-buffer-size=1280000 --logfile --logfilename logdirect/replica1.log --logfilelevel info -n ReplicaNode1  -D replica.da "' >/dev/null
    
        printf " Starting Replica2 \\n"
        osascript -e 'tell application "Terminal" to do script "conda activate bcr && cd Desktop/bcr/src && python -m da -r  --message-buffer-size=1280000 --logfile --logfilename logdirect/replica2.log --logfilelevel info -n ReplicaNode2  -D replica.da"' >/dev/null
    
        printf " Starting Replica3 \\n"
        osascript -e 'tell application "Terminal" to do script "conda activate bcr && cd Desktop/bcr/src && python -m da -r  --message-buffer-size=1280000 --logfile --logfilename logdirect/replica3.log --logfilelevel info -n ReplicaNode3  -D replica.da"' >/dev/null
   
        printf " Starting Replica4 \\n"
        osascript -e 'tell application "Terminal" to do script "conda activate bcr && cd Desktop/bcr/src && python -m da -r  --message-buffer-size=1280000 --logfile --logfilename logdirect/replica4.log --logfilelevel info -n ReplicaNode4  -D replica.da"' >/dev/null
  
        printf " Strating Client Node\\n"
        osascript -e 'tell application "Terminal" to do script "conda activate bcr && cd Desktop/bcr/src && python -m da -r  --message-buffer-size=1280000 --logfile --logfilename logdirect/client.log --logfilelevel info  -n ClientNode   -D client.da "' >/dev/null
   
        printf " Starting Olympus Node\\n"
        osascript -e 'tell application "Terminal" to do script "conda activate bcr && cd Desktop/bcr/src && python -m da -r  --message-buffer-size=1280000 --logfile --logfilename logdirect/olympus.log --logfilelevel info  -n OlympusNode  -D olympus.da "' >/dev/null
    
    python -m da -r --message-buffer-size=1280000 --logfile --logfilename logdirect/master.log --logfilelevel 'info' -n MasterNode bcr.da
fi