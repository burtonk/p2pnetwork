#class to determine whether it is meant 
#for this node or another. spools thread of project if for this node. . 

import json 
import socket 
import datetime
import time
from threading import Thread
import threading
import thread
import os

join = {"type": "JOINING_NETWORK_SIMPLIFIED", "node_id": None, "target_id": None, "ip_address": None }
join_relay = {"type": "JOINING_NETWORK_RELAY_SIMPLIFIED", "node_id": None, "target_id": None, "gateway_id": None, "ip_address" : None}
routing = {"type": "ROUTING_INFO", "gateway_id": None, "node_id": None, "ip_address": None, "routing_table" : []}
leaving = {"type": "LEAVING_NETWORK", "node_id": None} 
index = {"type": "INDEX", "target_id": None, "sender_id": None, "keyword": None, "link": []}
search = {"type": "SEARCH","word": None, "node_id": None, "sender_id": None }
search_response = {"type": "SEARCH_RESPONSE","word": None, "node_id": None, "sender_id": None, "response":[]}
ping = {"type": "PING", "target_id": None, "sender_id": None, "ip_address": None}
ack = {"type": "ACK", "node_id": None, "ip_address": None}
ack_index = {"type": "ACK_INDEX", "node_id": None, "keyword": None}

routing_table = {"7": "127.0.0.1","4": "127.0.0.2"}
information = {}
conditions = {}
polling = {}
wait_time = 10
ip_address = "127.0.0.3"
returned= {}
	
class Routing: 

	node_id = 0

	def get_time(self):
		ts = time.time()
		return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

	def to_hash (self, word): # to hash a given word according to spec
		hash = 0 
		for i in range(0, len(word)): 
				hash = hash * 31 + ord(word[i])
		return hash


	def send (self, json_file, ip_address, typ): #function that sends the packets to the specific addresss and reports to user 
		mess = json.dumps(json_file)
		try: 
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			sock.sendto(mess, (ip_address, 5005))
			print self.get_time() + " "+ typ+" -- PACKET SENT TO "+ ip_address
		except: 
			raise
			#pass #handle exceptions 

	def send_join(self, packet, ip):
		packet["ip_address"] = ip_address
		self.send(packet, ip, "JOIN")
		conditions[("JOIN", ip)] = threading.Event()
		resp = self.wait_for_response(conditions[("JOIN", ip)], ip)
		'''if resp == True: #commented bit so that you are able to see it running as explained in readme
			return "Connected."
		else: 
			print "Unable to Connect to Network"
			os.system("killall python")'''
		return "Connected"

	def closest (self, target_node): #calcalate closest to but not greater than node. 
		closest_node = 0
		above_node = 0 
		for node in routing_table: 
			if node > closest_node: 
				if int(node) <= target_node:
					closest_node = node
		if closest_node == 0: 
			return 4 #this should not occur as it would be for this node or go to the local set, as this is the simplified version, i am ignoring it 
			#raise ("No valid option")
		return routing_table[closest_node]

	def wait_for_response (self, event, sender_id): #method to ensure that packets are returned
		event.wait(wait_time)
		if event.isSet() == False: #didn't recieve in time, pinging target node
			print "No response received"
			temp = ping
			temp["target_id"] = sender_id
			temp["sender_id"] = str(self.node_id)
			temp["ip_address"] = ip_address
			ip = self.closest(sender_id)
			self.send(temp, ip, "PING")
			polling[sender_id] = threading.Event() #creates a waiting thread 
			self.polling_node(polling[sender_id], sender_id) # continues with theread?
			return False
		else: return True

	def polling_node (self, event, sender_id): #waiting for ping response, has different actions than wait_for_response
		event.wait(wait_time)
		if event.isSet() == False:
			try: #delete from routing table. 
				del routing_table[sender_id]
			except KeyError, e:
				pass # not in routing table

	def get_info(self, word): #allows the input to receive the information
		#need to wait until it happens
		response = returned[word]
		del returned[word]
		return response

	def index(self, packet): #used to send a index request
		ip = self.closest(packet["target_id"])
		self.send(packet, ip, "INDEX")
		conditions[("INDEX", packet["keyword"])] = threading.Event()
		resp = self.wait_for_response(conditions[("INDEX", packet["keyword"])], packet["target_id"])

	def search_word(self, word): #used to send and receive a send request from the input
		temp = search
		temp["word"] = word
		temp["sender_id"] = str(self.node_id)
		temp["node_id"] = self.to_hash(word)
		ip = self.closest(temp["node_id"])
		self.send(temp, ip, "SEARCH")
		conditions[("SEARCH", word)] = threading.Event()
		resp = self.wait_for_response(conditions[("SEARCH", word)], temp["node_id"])
		if resp == True: 
			return self.get_info(self, word)
		else: 
			return "No Information was returned"

	# need to work out which are replys if it is to itself. 
	def receive (self, received_packet): #deciefers the packet recieved. 
		#wait for packets
		json_file = json.dumps(received_packet)
		packet =  json.loads(json_file)
		index = packet["type"]
		if index == "JOINING_NETWORK_SIMPLIFIED": ###########################################DONE
			if int(packet["gateway_id"]) == self.node_id: 
				#pass on to others in the network
				temp = join_relay
				temp["node_id"] = packet["node_id"]
				temp["target_id"] = packet["target_id"]
				temp["ip_address"] = packet["ip_address"]
				temp["gateway_id"] = str(self.node_id)
				ip = self.closest(packet["target_id"])
				self.send(temp, ip)
				#add to routing table
				routing_table[packet["node_id"]] = packet["ip_address"]
				#send pack routing table
				temp = routing
				temp["gateway_id"] = str(self.node_id)
				temp["node_id"] = packet["node_id"]
				temp["ip_address"] = ip_address
				temp["route_table"] = []
				for key in routing_table: 
					temp["route_table"].append({"node_id": key, "ip_address": routing_table[key]})
				ip = self.closest(packet["node_id"])
				self.send(temp, ip)

			else: 
				new_ip = closest(packet["target_node"])
				send(packet, new_ip)

		elif index == "JOINING_NETWORK_RELAY_SIMPLIFIED": ###########################################DONE
			if int(packet["target_id"]) == node_id: 
				#send routing table
				temp = routing
				temp["gateway_id"] = packet["gateway_id"]
				temp["node_id"] = packet["node_id"]
				temp["ip_address"] = ip_address
				temp["route_table"] = []
				for key in routing_table: 
					temp["route_table"].append({"node_id": key, "ip_address": routing_table[key]})
				ip = self.closest(packet["gateway_id"])
				self.send(temp, ip)
				#add to routing table
				routing_table[packet["node_id"]] = packet["ip_address"]

			elif int(packet["gateway_id"]) == self.node_id: 
				pass #shouldn't be recieving this if you are the gateway node. 
			else: 
				#add to routing table 
				routing_table[packet["node_id"]] = packet["ip_address"]
				#pass back routing table
				temp = routing
				temp["gateway_id"] = packet["gateway_id"]
				temp["node_id"] = packet["node_id"]
				temp["ip_address"] = ip_address
				temp["route_table"] = []
				for key in routing_table: 
					temp["route_table"].append({"node_id": key, "ip_address": routing_table[key]})
				ip = self.closest(packet["gateway_id"])
				self.send(temp, ip)
				#pass on the message
				new_ip = closest(packet["target_node"])
				send(packet, new_ip)
				
		elif index == "ROUTING_INFO": ###########################################DONE 
			if int(packet["node_id"]) == self.node_id: 
				try:
					conditions[("JOIN", packet["ip_address"])].set()
				except Exception, e:
					pass # should only react for first gateway noe. 
				for node in packet["routing_table"]:
					routing_table[node["node_id"]] = str(node["ip_address"])
			elif int(packet["gateway_id"]) == node_id: 
				new_ip = closest_node(packet["node_id"]) # send to joining node 
				send(packet, new_ip)
			else: 
				new_ip = closest(packet["gateway_id"])
				send(packet, new_ip)

		elif index == "LEAVING_NETWORK": ###########################################DONE
			try:
				del routing_table[packet["node_id"]]
			except KeyError, e:
				pass #entry not in routing table. 

		elif index == "INDEX":  ###########################################DONE 
			if int(packet["target_id"]) == self.node_id:
				keyword = packet["keyword"] 
				if keyword in information.keys(): #keyword already exists 
					the_list = information[keyword]
					for link in packet["link"]:
						seen = False
						for url, frequency in the_list: 
							if url == link:
								where =  information[keyword].index((url, frequency)) 
								frequency +=1 
								information[keyword][where] = (url, frequency)
								seen = True
						if seen == False: 
							information[keyword].append((link, 1))
				else: 
					information[keyword] = []
					for link in packet["link"]: 
						information[keyword].append((link, 1))
			else: 
				new_ip = closest(packet["target_id"])
				send(packet, new_ip)

		elif index == "SEARCH": ###########################################DONE
			if int(packet["node_id"]) == self.node_id: 
				try:
					new_packet = search_response
					links = information[packet["word"]]
					for link, frequency in links: 
						new_packet["response"].append({"url" : link, "rank" : frequency})
					new_packet["word"] = packet["word"]
					new_packet["node_id"] = packet["sender_id"]
					new_packet["sender_id"] = node_id
					ip = closest(packet["sender_id"])
					send(new_packet, ip )
				except KeyError, e:
					raise e
				except Exception, e: 
					raise e 
			else: 
				new_ip = closest(packet["node_id"])
				send(packet, new_ip)

		elif index == "SEARCH_RESPONSE": ###########################################DONE??
			if int(packet["node_id"]) == self.node_id: 
				try:
					returned[packet["word"]] = packet["response"] # need to set one in other class and print results
					conditions[("SEARCH", packet["word"])].set()
				except Exception, e:
					raise e
			else: 
				new_ip = closest(packet["node_id"])
				send(packet, new_ip)

		elif index == "PING": ###########################################DONE
			if int(packet["target_id"]) == self.node_id: 
				new_packet = ack
				new_packet["node_id"] = str(self.node_id)
				new_packet["ip_address"] = ip_address
				send(new_packet, packet["ip_address"])
			else: 
				new_ip = closest(packet["target_id"])
				packet["ip_address"] = ip_address #change the IP to this node
				send(packet, new_ip)

		elif index == "ACK": ###########################################DONE
			if int(packet["node_id"]) == self.node_id: 
				try:
					polling[packet["node_id"]].set() #??? or polling?
				except Exception, e:
					raise e #not waiting for packet, possiby already timed out. 
			else: 
				new_ip = closest(packet["target_id"])
				packet["ip_address"] = ip_address
				send(packet, new_ip)

		elif index == "ACK_INDEX": ###########################################DONE
			if int(packet["node_id"]) == self.node_id: 
				conditions[("INDEX", packet["keyword"])].set()
			else: 
				new_ip = closest(packet["target_id"])
				packet["ip_address"] = ip_address
				send(packet, new_ip)
		else: 
			raise ("Not a valid packet")

	def __init__(self,  node):
			self.node_id = node 
			Thread(target=self.main).start()			

	def main(self): #always running
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   		sock.bind((ip_address, 5005))
		while True: 
			packet, addr = sock.recvfrom(1024)
			Thread(target=self.receive, args=packet) #new thread to deal with the packet.
