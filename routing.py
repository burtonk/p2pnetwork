#class to determine whether it is meant 
#for this node or another. spools thread of project if for this node. . 

import json 
import socket 
import datetime
import time
import threading

class Routing: 

	join = {"type": "JOINING_NETWORK_SIMPLIFIED", "node_id": None, "target_id": None, "ip_address": None }
	join_relay = {"type": "JOINING_NETWORK_RELAY_SIMPLIFIED", "node_id": None, "target_id": None, "gateway_id": None }
	routing = {"type": "ROUTING_INFO", "gateway_id": None, "node_id": None, "ip_address": None, "routing_table" : []}
	leaving = {"type": "LEAVING_NETWORK", "node_id": None} 
	index = {"type": "INDEX", "target_id": None, "sender_id": None, "keyword": None, "link": []}
	search = {"type": "SEARCH","word": None, "node_id": None, "sender_id": None }
	search_response = {"type": "SEARCH_RESPONSE","word": None, "node_id": None, "sender_id": None, "response":[]}
	ping = {"type": "PING", "target_id": None, "sender_id": None, "ip_address": None}
	ack = {"type": "ACK", "node_id": None, "ip_address": None}
	ack_index = {"type": "ACK_INDEX", "node_id": None, "keyword": None}

	routing_table = {}
	information = {}
	conditions = {}
	polling = {}
	wait_time = 10
	node_id = 0

	def get_time():
		ts = time.time()
		return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

	def to_hash (word): # to hash a given word according to spec
		hash = 0 
		for i in range(0, len(word)): 
				hash = hash * 31 + ord(word[i])
		return hash

	def send (json_file, ip_address): 
		mess = json.dumps(json_file)
		try: 
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			sock.sendto(mess, (ip_address, 5005))
			print get_time() + " -- PACKET SENT TO "+ ip_address
		except: 
			raise
			#pass #handle exceptions 

	def closest (target_node): #calcalate closest to but not greater than node. 
		closest_node = 0
		above_node = 0 
		for node in routing_table: 
			if node > closest_node: 
				if int(node) <= target_node:
					closest_node = node
		if closest_node == 0: 
			pass
		return routing_table[closest_node]

	def wait_for_response (event, sender_id): 
		event.wait(wait_time)
		if event.isSet() == False: #didn't recieve in time, pinging target node
			print "failed"
			temp = ping
			temp["target_id"] = sender_id
			temp["sender_id"] = node_id
			temp["ip_address"] = ip_address
			ip = closest(sender_id)
			send(temp, ip)
			polling[sender_id] = threading.Event() #creates a waiting thread 
			polling_node(polling[sender_id], sender_id) # continues with theread?

	def polling_node (event, sender_id): 
		event.wait(wait_time)
		if event.isSet() == False:
			try: #delete from routing table. 
				del routing_table[sender_id]
			except KeyError, e:
				pass # not in routing table

	# need to work out which are replys if it is to itself. 
	def receive (received_packet): 
		#wait for packets
		json_file = json.dumps(received_packet)
		packet =  json.loads(json_file)
		index = packet["type"]
		if index == "JOINING_NETWORK_SIMPLIFIED": 
			if packet["target_id"] == node_id: 
				pass# add to index and reply. 
			elif int(packet["gateway_id"]) == node_id: 
				pass
			else: 
				new_ip = closest(packet["target_node"])
				send(packet, new_ip)

		elif index == "JOINING_NETWORK_RELAY_SIMPLIFIED": 
			if int(packet["target_id"]) == node_id: 
				pass
			elif int(packet["gateway_id"]) == node_id: 
				pass #shouldn't be recieving this if you are the gateway node. 
			else: 
				new_ip = closest(packet["target_node"])
				send(packet, new_ip)
				
		elif index == "ROUTING_INFO": ###########################################DONE 
			if int(packet["node_id"]) == node_id: 
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
			if int(packet["target_id"]) == node_id:
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
			if int(packet["node_id"]) == node_id: 
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

		elif index == "SEARCH_RESPONSE": 
			if int(packet["node_id"]) == node_id: 
				try:
					pass # need to set one in other class and print results
					#insert into information
				except Exception, e:
					raise e
			else: 
				new_ip = closest(packet["node_id"])
				send(packet, new_ip)

		elif index == "PING": ###########################################DONE
			if int(packet["target_id"]) == node_id: 
				new_packet = ack
				new_packet["node_id"] = node_id
				new_packet["ip_address"] = ip_address
				send(new_packet, packet["ip_address"])
			else: 
				new_ip = closest(packet["target_id"])
				packet["ip_address"] = ip_address #change the IP to this node
				send(packet, new_ip)

		elif index == "ACK": 
			if int(packet["node_id"]) == node_id: 
				try:
					conditions[("PING", packet["node_id"])].set() #???
				except Exception, e:
					raise e #not waiting for packet, possiby already timed out. 
			else: 
				new_ip = closest(packet["target_id"])
				packet["ip_address"] = ip_address
				send(packet, new_ip)

		elif index == "ACK_INDEX": 
			if int(packet["node_id"]) == node_id: 
				pass #set input flas
			else: 
				new_ip = closest(packet["target_id"])
				packet["ip_address"] = ip_address
				send(packet, new_ip)
		else: 
			raise ("Not a valid packet")

	def __init__(routing, node):
	    self.data = []
	    routing_table = routing
		node_id = node
	    main()

	def main(): 
		print node_id
		ip_address = "127.0.0.3"
		#wait_for_response(conditions["test"], 5)
		print information
		receive(index)
		print information
		receive(index)
		#send(routing, "127.0.0.1")
		print information
		receive(search)
		print information
		while True: 
			packet = ack # listen to port
			receive(packet) #new thread
