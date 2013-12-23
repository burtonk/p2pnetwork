import os 
import string
import json 
from routing import *
import thread
import sys
import os

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
interact = None
node_id = 0

class Input: 

	def to_hash (self, word):
		hash = 0 
		for i in range(0, len(word)): 
				hash = hash * 31 + ord(word[i])
		return hash

	def init(self, udp_socket): 
		pass

	def leaveNetwork(self, network_id):
		#send leave packet
		print "Leaving Network... "
		os.system("killall python")

	def indexPage (self, url, unique_words):
		pass

	def wait(self):
		while True: 
			request = raw_input("Please enter one of the following numbers: \n 1. Search \n 2. Index \n 3. Leave Network \n\t Input: ")
			if int(request) == 1: #SEARCH
				word = raw_input("\n Word: ")
				words = word.split()
				for word in words:
					to_h = self.to_hash(word)
					print "Searching for - "+word + " "+ str(to_h)

			elif int(request) == 2: #INDEX 
				word = raw_input("\n Word: ")
				url = raw_input("\n URL: ")
				self.indexPage(url, word)
				print "Indexing - "+ word +" - "+ url

			elif int(request) == 3: #LEAVE NETWORK
				self.leaveNetwork(node_id)
				print "Leaving Network..."

	def joinNetwork(self, bootstrap_node, identifier, target_identifier): 
		pass

	def __init__(self, bootstrap_node, target_id, node): #routing, node
		print node
		print type(node)
		node_id = self.to_hash(node)
		self.joinNetwork(bootstrap_node, node_id, target_id)
		interact = Routing(node_id)
		Thread(target=self.wait()) 
    	
