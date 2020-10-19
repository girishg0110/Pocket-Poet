# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 12:49:47 2020

@author: giris
"""

import GutenClient
#from PSR import PhraseGenerator
import random
from TextAdjacency import TextAdjacency

total_words = 140
queries = []
spot_query = input("Enter name of work (q to quit): ")
while (spot_query != 'q'):
    queries.append(spot_query)
    spot_query = input("Enter name of work (q to quit): ")

full_text = GutenClient.process_book_link(queries)[0]

adj_list = TextAdjacency(full_text)
seed = random.choice(full_text)
for i in range(total_words):
    if (i % 20==0): print("\n")
    print(adj_list.random_word(seed), end=" ")

# Structure
    # (1) Read in works --> use PSR rules with those words
    # (2) Read in works --> use freq blindly (random choice)
    # (3) Read in works --> use freq for next pos, then find random word with same pos
        # same sentence structure, diff words
        
# Next steps:
    # (1) PSRs uploaded so grammatically correct
    # (2) Use merriam-webster API to check which words fit (PoS), 
        # increment next_word count only when fits