import os 
import string
import json 
#import routing.py

class Input: 

	join = {"type": "JOINING_NETWORK_SIMPLIFIED", "node_id": None, "target_id": None, "ip_address": None }
	join_relay = {"type": "JOINING_NETWORK_RELAY_SIMPLIFIED", "node_id": None, "target_id": None, "gateway_id": None }
	routing = {"type": "ROUTING_INFO", "gateway_id": None, "node_id": None, "ip_address": None, "routing_tale" : []}
	leaving = {"type": "LEAVING_NETWORK", "node_id": None} 
	index = {"type": "INDEX", "target_id": None, "sender_id": None, "keyword": None, "link": []}
	search = {"type": "SEARCH","word": None, "node_id": None, "sender_id": None }
	search_response = {"type": "SEARCH_RESPONSE","word": None, "node_id": None, "sender_id": None, "response":[]}
	ping = {"type": "PING", "target_id": None, "sender_id": None, "ip_address": None}
	ack = {"type": "ACK", "node_id": None, "ip_address": None}
	ack_index = {"type": "ACK", "node_id": None, "keyword": None}

	node_id = 0

	def to_hash (word):
		hash = 0 
		for i in range(0, len(word)): 
				hash = hash * 31 + ord(word[i])
		return hash

	def init(udp_socket): 
		pass

	def joinNetwork(bootstrap_node, identifier, target_identifier): 
		pass

	def leaveNetwork(network_id):
		pass

	def indexPage (url, unique_words):
		pass

	def search (words): 
		for word in words:
			hash = to_hash(word)
			#search_for_word(word, hash) need to send

	def wait():
		while True: 
			request = raw_input("Please enter one of the following numbers: \n 1. Search \n 2. Index \n 3. Leave Network \n\t Input: ")
			if int(request) == 1: #SEARCH
				word = raw_input("\n Word: ")
				words = word.split()
				search(words) 
				print "Searching for - "+word

			elif int(request) == 2: #INDEX 
				word = raw_input("\n Word: ")
				url = raw_input("\n URL: ")
				indexPage(url, word)
				print "Indexing - "+ word +" - "+ url

			elif int(request) == 3: #LEAVE NETWORK
				leaveNetwork(node_id)
				print "Leaving Network..."

	def __init__(self, bootstrap_node, target_id, keyword): #routing, node
		node_id = int(to_hash(keyword))
		joinNetwork(bootstrap_node, node_id, target_id)
		#create receiving node
    	wait() #receiver = new Routing(routing, node)
