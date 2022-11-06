import json
from datetime import datetime, timezone
import socket
import ipaddress

"""
name, cpu a memory usage, created_at, status 
a všechny přiřazené IP adresy. Datumová pole převeďte na UTC timestamp.
"""

class DataParse:

	def __init__(self, file):
		self.file = file


	# https://stackoverflow.com/questions/9807634/find-all-occurrences-of-a-key-in-nested-dictionaries-and-lists
	# function for searching in nested dictionary
	@staticmethod
	def gen_dict_extract(key, var):
	    if hasattr(var,'items'): # if is a dict
	        for k, v in var.items(): # for each key: val
	            if k == key:
	                yield v    
	            if isinstance(v, dict):  # value is nested dict
	                for result in DataParse.gen_dict_extract(key, v):  # recursion
	                    yield result
	            elif isinstance(v, list):    # val is list
	                for d in v:  
	                    for result in DataParse.gen_dict_extract(key, d):
	                        yield result

	# https://thispointer.com/check-if-a-string-is-a-valid-ip-address-in-python/
	# checking if the given string represents ip address
	@staticmethod
	def is_valid_IPAddress(sample_str):
	    result = True
	    try:
	        ipaddress.ip_network(sample_str)
	    except:
	        result = False
	    return result


	# open json file
	def go_through_data(self):
		with open(self.file, 'r') as opened_file:  # json
			data = json.load(opened_file) 						 # list of dicts
			list_of_keys = ['name', 'cpu', 'memory', 'created_at', 'status', 'address']   # list of keys
			for item in data:  								# iterating through servers dict
				# item_json = json.dumps(item, indent=3) 

				for key in list_of_keys:
					val = list(DataParse.gen_dict_extract(key, item))

					if key == list_of_keys[0]:   # name list
						try:
							val.remove('eth0')
							print(f"{key} : {val[0]}")
						except:
							print('Something wrong...')
			
					elif key == list_of_keys[1]:   # cpu 
						try:
							cpu_usage = val[0]['usage']
							print(f"{key} : {cpu_usage}")
						except:
							print('Something wrong...')

					elif key == list_of_keys[2]:
						try:
							memory_usage = val[0]['usage']
							print(f"{key} : {memory_usage}")
						except:
							print('Something wrong...')

					elif key == list_of_keys[3]: 
						try:
							date_iso = val[0]
							date = datetime.fromisoformat(date_iso)
							utc_time = date.replace(tzinfo=timezone.utc)
							utc_timestamp = utc_time.timestamp()
							print(f"{key} : {utc_timestamp}")
						except:
							print('Something wrong...')

					elif key == list_of_keys[4]:
						try:
							status = val[0]
							print(f"{key} : {status}")
						except:
							print('Something wrong...')

					else:
						try:
							addresses = val
							ip_addr = []
							for addr in addresses:
								if DataParse.is_valid_IPAddress(addr):
								    ip_addr.append(addr)
								
							print(f"{key} : {ip_addr}")
						except:
							print('Something wrong...')	




if __name__ == '__main__':
	parsing = DataParse('sample-data.json')
	parsing.go_through_data()






