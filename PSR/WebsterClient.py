# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 09:51:12 2020

@author: giris
"""

import requests

dict_key = '8b69ae94-7edc-4404-99f0-4f2d0d93ccb2'
thes_key = 'da3b1a46-9cb5-426d-8944-dca5e2bb84c2'

def look_up(word):
    print("Looking up " + word + "...")
    global dict_key
    link = 'https://www.dictionaryapi.com/api/v3/references/collegiate/json/' \
        + word + '?key=' + dict_key
    merriam_response = requests.get(link)
    wordJSON = merriam_response.json()
#    print(wordJSON[0]
#    print(wordJSON[0][0])
    
    try:
        #if (type(wordJSON[0][0]) == str):
            print("\tRedirecting... searching for " + wordJSON[0] + "...")
            link = 'https://www.dictionaryapi.com/api/v3/references/collegiate/json/' \
                + wordJSON[0][0] + '?key=' + dict_key
            merriam_response = requests.get(link)
            wordJSON = merriam_response.json()
            return wordJSON
    except(TypeError):
        return wordJSON
    
def thesaurus_entry(word):
    print("Searching thesaurus for " + word + "...")
    global thes_key
    link = 'https://www.dictionaryapi.com/api/v3/references/thesaurus/json/' \
        + word + '?key=' + thes_key
    merriam_response = requests.get(link)
    wordJSON = merriam_response.json()
#    print(wordJSON[0]
#    print(wordJSON[0][0])
    
    try:
        #if (type(wordJSON[0][0]) == str):
            print("\tRedirecting... searching for " + wordJSON[0] + "...")
            link = 'https://www.dictionaryapi.com/api/v3/references/thesaurus/json/' \
                + wordJSON[0][0] + '?key=' + thes_key
            merriam_response = requests.get(link)
            wordJSON = merriam_response.json()
            return wordJSON
    except(TypeError):
        return wordJSON
    
def look_up_PoS(word, targetPOS):
    wordJSON = look_up(word)
    parts = []
    for i in wordJSON:
        try:
            pos = i['fl']
            if (not pos in parts): 
                if ('article' in pos): parts.append('determiner')    
                elif pos in targetPOS: parts.append(pos)
                break
        except(KeyError):
            continue
    return parts

def related_words(word, depth = 3, spread = 3):
    rel = [word]
    if (depth == 0): return rel
    wordJSON = thesaurus_entry(word)
    meta = wordJSON[0]["meta"]
    
    rel += rel_category(meta, "syns", word, depth, spread)
    rel += rel_category(meta, "ants", word, depth, spread)
            
    return rel

def rel_category(meta, cat, word, depth, spread):
    if (len(meta[cat]) == 0): return []
    for j in range(0, min(len(meta[cat][0]), spread)): #
        return related_words(meta[cat][0][j], depth - 1, spread)

elements = ['fire', 'water', 'earth', 'sky', 'warm', 'happy', 'comfort', 'sleep']
element_lexicon = ['fire', 'conflagration', 'fire', 'conflagration', 'impassiveness', 'peace', 'peacefulness', 'war', 'impassiveness', 'affectlessness', 'apathy', 'emotion', 'emotion', 'chord', 'impassiveness', 'water', 'bathe', 'lap', 'leg', 'dehydrate', 'castrate', 'brace', 'dehydrate', 'castrate', 'damp', 'brace', 'brace', 'buttress', 'earth', 'globe', 'ball', 'globe', 'mite', 'chicken feed', 'chump change', 'big buck(s)', 'big buck(s)', 'bomb', 'mite', 'sky', 'blue', 'bawdy', 'blue', 'clean', 'clean', 'antiseptic', 'besmirched', 'Gehenna', 'agony', 'Gehenna', 'heaven', 'heaven', 'above', 'Gehenna', 'warm', 'heated', 'agitated', 'excited', 'collected', 'chilled', 'nipped', 'feeling', 'chilled', 'nipped', 'chilled', 'feeling', 'feeling', 'chord', 'callousness', 'happy', 'fluky', 'fortuitous', 'fluky', 'hapless', 'hapless', 'hard-luck', 'fortunate', 'hapless', 'hard-luck', 'hapless', 'fortunate', 'fortunate', 'fluky', 'hapless', 'comfort', 'cheer', 'cheerfulness', 'cheer', 'booing', 'hissing', 'acclamation', 'burden', 'cargo', 'burden', 'sleep', 'bed', 'bunk', 'bed', 'consciousness', 'advertence', 'consciousness', 'advertence', 'advertency']

pos_expanded = {'Adj': 'adjective', 'N' : 'noun', 'Adv' : 'adverb', \
                           'P' : 'preposition', 'D': 'determiner', \
                           'C' : 'conjunction', 'T' : 'auxiliary verb'}
#print(look_up("vow'd"))
#print(look_up("the"))

# =============================================================================
# pos_expanded = {'Adj': 'adjective', 'N' : 'noun', 'Adv' : 'adverb', \
#                            'P' : 'preposition', 'D': 'determiner', \
#                            'C' : 'conjunction', 'T' : 'auxiliary verb'}
# 
# =============================================================================
