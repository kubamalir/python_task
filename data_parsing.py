import json

"""
name, cpu a memory usage, created_at, status 
a všechny přiřazené IP adresy. Datumová pole převeďte na UTC timestamp.
"""


# https://stackoverflow.com/questions/9807634/find-all-occurrences-of-a-key-in-nested-dictionaries-and-lists
# function for searching in nested dictionary
def gen_dict_extract(key, var):
    if hasattr(var,'items'): # if is a dict
        for k, v in var.items(): # for each key: val
            if k == key:
                yield v    
            if isinstance(v, dict):  # value is nested dict
                for result in gen_dict_extract(key, v):  # recursion
                    yield result
            elif isinstance(v, list):    # val is list
                for d in v:  
                    for result in gen_dict_extract(key, d):
                        yield result


# open json file
with open('sample-data.json', 'r') as opened_file:  # json
	data = json.load(opened_file)  # list of dicts
	list_of_keys = ['name', 'cpu', 'memory', 'created_at', 'status', 'address']
	for item in data:  # dict
		# item_json = json.dumps(item, indent=3) 

		for key in list_of_keys:
			val = list(gen_dict_extract(key, item))
			print(f"{key} : {val}")





