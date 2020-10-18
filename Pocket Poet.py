# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 12:49:47 2020

@author: giris
"""

#import time
import GutenClient
#from PSR import PhraseGenerator
#from TextAVL import TextAVL
from TextMap import TextMap

total_words = 140 #int(input("How many words do you require? "))
total_sentences = 20
queries = ["romeo and juliet"]
spot_query = "q"#input("Enter name of work (q to quit): ")
while (spot_query != 'q'):
    queries.append(spot_query)
    spot_query = input("Enter name of work (q to quit): ")

full_text = GutenClient.process_book_link(queries)
limit = int(input("words "))
#if (0):
#print("Reading into AVL...")
#start1 = time.time()
#avl = TextAVL(poem_list)
#end1 = time.time()
#else:
print("Reading into HashMap...")
#start2 = time.time()
mapp = TextMap([full_text[0][0:limit]])
#end2 = time.time()

#print("AVL:", end1 - start1)
#print("Hash: ", end2 - start2)
#print("Hash is", (end1-start1)/(end2-start2), "times faster than AVL.")
# Generate seed word
#print (poem_list[0])
#for i in range(0,10):
    #print(avl.random_word())

#seed0 = mapp.random_word()

if (0):
    seed = seed0
    print("AVL...")
    linebreak_counter = 10
    for i in range(0, total_words):
        print(seed + " ", end="")
        seed = avl.next_word(seed)
        if (i%linebreak_counter == 0): print("\n")
if(1):
    seed = seed0
    print("Hash map...")
    linebreak_counter = 10
    for i in range(0, total_words):
        print(seed + " ", end="")
        seed = mapp.next_word(seed)
        if (i%linebreak_counter == 0): print("\n")
if(0):
    print("Hash map...")
    processed = PhraseGenerator.process_lexicon(full_text[0][0:limit])
    for j in range (0,total_sentences):
        print(PhraseGenerator.generate_phrase('TP', PhraseGenerator.ps_rules, processed))

# Structure
    # (1) Read in works --> use PSR rules with those words
    # (2) Read in works --> use freq blindly (random choice)
    # (3) Read in works --> use freq for next pos, then find random word with same pos
        # same sentence structure, diff words
        
# Next steps:
    # (1) PSRs uploaded so grammatically correct
    # (2) Use merriam-webster API to check which words fit (PoS), 
        # increment next_word count only when fits