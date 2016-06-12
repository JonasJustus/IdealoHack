import json
from pprint import pprint


good_offers = list()
bad_offers = list()
products = list()

data_file = open('./idealo/data.json', 'r')
content = data_file.readlines()

for line in content:

	#load good offers
	j_obj = json.loads(line)
	for i in range(0, len(j_obj['offers_ok'])):
		good_offers.append(j_obj['offers_ok'][i])

	#load bad offers
	for i in range(0, len(j_obj['offers_error'])):
		bad_offers.append(j_obj['offers_error'][i])

	#load products
	products.append(j_obj['product'])


#get categories
categories = set()
category_strings = set()
top_dict = {}

delimeters = ["->", ">", "/"]

top_options = open("top.txt","w")

for obj in good_offers:
	try:
		#for each category string
		for i in range(0, len(obj["categoryPaths"])):
			
			#add this to the category strings for full strings
			category_strings.add(obj["categoryPaths"][i])

			#for each delimiter, search for the delimiter to split by
			for p in range(0, len(delimeters)):

				#if that delimeter is used, split by it
				if delimeters[p] in obj["categoryPaths"][i] :	
					temp_split_data = obj["categoryPaths"][i].split(delimeters[p])
					split = list()	

					#remove ending/starting spaces to ensure uniqueness
					for s in temp_split_data:
					
						if len(s) is 0 or len(s) is 1:
							continue

						if s[0].isspace():
							s = s[1:]

						if s[len(s) - 1].isspace():
							s = s[:(len(s)-1)]

						split.append(s)

					#add these new entries to split data
					for i in range(0, len(split) - 1):
						if split[i] in categories:
							top_dict[split[i]] += 1
						else:
							top_dict.update({split[i]: 1})

					categories.update(split)
					break;

	except KeyError:
		pass

for obj in bad_offers:
	try:
		#for each category string
		for i in range(0, len(obj["categoryPaths"])):
			
			#add this to the category strings for full strings
			category_strings.add(obj["categoryPaths"][i])
			
			#for each delimiter, search for the delimiter to split by
			for p in range(0, len(delimeters)):

				#if that delimeter is used, split by it
				if delimeters[p] in obj["categoryPaths"][i] :	
					temp_split_data = obj["categoryPaths"][i].split(delimeters[p])
					split = list()

					#remove ending/starting spaces to ensure uniqueness
					for s in temp_split_data:
					
						if len(s) is 0 or len(s) is 1:
							continue

						if s[0].isspace():
							s = s[1:]

						if s[len(s) - 1].isspace():
							s = s[:(len(s)-1)]

						split.append(s)

					#add these new entries to split data
					for i in range(0, len(split) - 1):
						if split[i] in categories:
							top_dict[split[i]] += 1
						else:
							top_dict.update({split[i]: 1})

					categories.update(split)
					break;

	except KeyError:
		pass

new_list = []
good_list = []

for k in top_dict:
	new_list.append([k, top_dict[k]])

for p in range(0, 50):
	
	max_num = 0;
	max_dex = 0;

	for i in range(0, len(new_list) - 1):
		if new_list[i][1] >= max_num:
			max_num = new_list[i][1]
			max_dex = i

	good_list.append([new_list[max_dex][0],new_list[max_dex][1]])
	new_list[max_dex][1] = 0


#======================================================================
# Get what we need
#======================================================================
raw_txt = open("raw.txt", "w")

for obj in good_offers:
	try:
		#for each category string
		for i in range(0, len(obj["categoryPaths"])):
			
			#for each delimiter, search for the delimiter to split by
			for p in range(0, len(delimeters)):

				#if that delimeter is used, split by it
				if delimeters[p] in obj["categoryPaths"][i] :	
					temp_split_data = obj["categoryPaths"][i].split(delimeters[p])
					split = list()	


					#remove ending/starting spaces to ensure uniqueness
					for s in temp_split_data:
					
						if len(s) is 0 or len(s) is 1:
							continue

						if s[0].isspace():
							s = s[1:]

						if s[len(s) - 1].isspace():
							s = s[:(len(s)-1)]

						split.append(s)

					#compare with top 500
					
					safe = 0

					for word in split:
						safe = 0	
						for good_word in good_list:
							
							if good_word[0] == word:
								safe = 1

						if safe == 0:
							
							break
					
					if safe == 1:
						raw_txt.write((obj["categoryPaths"][i] + "\n").encode("UTF-8"))


	except KeyError:
		pass

#======================================================================
# Get what we need
#======================================================================

bad_final = list()

for obj in bad_offers:
	try:
		#for each category string
		for i in range(0, len(obj["categoryPaths"])):
			
			#for each delimiter, search for the delimiter to split by
			for p in range(0, len(delimeters)):

				#if that delimeter is used, split by it
				if delimeters[p] in obj["categoryPaths"][i] :	
					temp_split_data = obj["categoryPaths"][i].split(delimeters[p])
					split = list()	


					#remove ending/starting spaces to ensure uniqueness
					for s in temp_split_data:
					
						if len(s) is 0 or len(s) is 1:
							continue

						if s[0].isspace():
							s = s[1:]

						if s[len(s) - 1].isspace():
							s = s[:(len(s)-1)]

						split.append(s)

					#compare with top 500
					
					safe = 0

					for word in split:
						safe = 0	
						for good_word in good_list:
							
							if good_word[0] == word:
								safe = 1

						if safe == 0:
							
							break
					
					if safe == 1:
						raw_txt.write((obj["categoryPaths"][i] + "\n").encode("UTF-8"))


	except KeyError:
		pass

#print(len(bad_final))
#print(len(good_final))