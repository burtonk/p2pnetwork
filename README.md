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
- Responds and acts appropirately when receives a packet for itself, not joining 

Things not working: 
-Joining
