p2pnetwork
==========

Distributed Systems P2P Solution

PLEASE NOTE THAT THE PROGRAM USES A KILLALL PYTHON CODE TO CLOSE THE PROGRAM DUE TO THREADING

Changes to Specification provided: 
- No search results, dictionary instead "word": [(url,frequence)]
- Interface changed. 
- JOINING_NETWORK_RELAY_SIMPLIFIED carries joining nodes IP

Running: 

Runs on python 2.7
Run program by running: 
    python main.py

Things working: 
- When it recieves a packet that is not meant for itself, it passes it on 
- Responds and acts appropirately when receives a packet for itself including joining
- Program receives input from user via command line. 

Things not working: 
- Due to the way the program receives input from user, I wasn't able to get the program to open a terminal for each node. While I have tested all the response code seperately, I was not able to produce tests for more than one node due to this and thread complications. Therefore I used netcat to test the packets being sent and recieved with the command:
- nc -ul url port 
- Because of this, I have commented the section of the code in the joining method that waits until a routing info packet has been received from the gateway node. (routing.py) so that the input can be seen. 
