p2pnetwork
==========

Distributed Systems P2P Solution

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
- Due to time restraints, while I have tested all the response code seperately, I was not able to produce tests for more than one node due to thread complications. I used netcat to test the packets being sent and recieved with the command:
- nc -ul url port 
