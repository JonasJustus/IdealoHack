import simplejson
from textblob import TextBlob
import random
import logging
from gensim import corpora, models, similarities
from collections import defaultdict
from pprint import pprint   #pretty-printer
import json



good_offers = list()
bad_offers = list()
products = list()
data_file = open('data.json', 'r')
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
for p in range(0, 4):

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
good_final = list()
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
                        good_final.append(obj)
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
                        bad_final.append(obj)
    except KeyError:
        pass

new_data = []

for item in good_offers:
    s = json.dumps(item)
    print(s)
    print(type(s))
    index = s.index("categoryPaths")

    new_data.append(s[index + 16])
    print item
    print(new_data)

word_dict = dict()

for item in new_data:
    for thing in item:

        try:
            if len(item) > 0:
                blob = TextBlob(item)
                replacement = blob.translate(to="en")
                word_dict[item] = replacement
        except:
            pass

print(word_dict.values())

for item in categories:
    if item in word_dict:
        item = word_dict[item]



len_of_data = len(good_offers)

context_list = []

for i in range(8):
    index = random.randrange(0, len_of_data)
    if len(good_offers[index]["title"]) > 0:
        try:
            blob = TextBlob(good_offers[index]["title"])
            replacement = blob.translate(to="en")
            context_list.append(replacement)
        except:
            pass

final_data = []


context_list.insert(0, new_data[1])

print(context_list)


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



documents = [context_list]

stoplist = set('for a of the and to in'.split())

texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1
texts = [[token for token in text if frequency[token] > 1]
         for text in texts]
pprint(texts)

dictionary = corpora.Dictionary(texts)
dictionary.save('/tmp/deerwester.dict') # store the dictionary, for future reference
print(dictionary)
print(dictionary.token2id)

new_doc = "Human computer interaction"
new_vec = dictionary.doc2bow(new_doc.lower().split())
print(new_vec) # the word "interaction" does not appear in the dictionary and is ignored

corpus = [dictionary.doc2bow(text) for text in texts]
print(corpus)

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
doc = "Human computer interaction"
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow] # convert the query to LSI space
print(vec_lsi)

index = similarities.MatrixSimilarity(lsi[corpus])

sims = index[vec_lsi] # perform a similarity query against the corpus
print(list(enumerate(sims))) # print (document_number, document_similarity) 2-tuples
sims = sorted(enumerate(sims), key=lambda item: -item[1])
print(sims) # print sorted (document number, similarity score) 2-tuples
