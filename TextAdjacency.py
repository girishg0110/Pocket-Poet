# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 00:25:33 2020

@author: giris
"""

import random

class TextAdjacency:
    
    def __init__(self, full_text = []):
        self.vocab=set(full_text)
        self.toWord = {i:j for i,j in enumerate(self.vocab)}
        self.toNumber = {j:i for i,j in enumerate(self.vocab)}
        
        self.freq_distribution(full_text)
    
    def freq_distribution(self, full_text):
        self.adj = [[] for i in self.vocab]
        prev_word = self.toNumber[full_text[0]]
        for i in range(1,len(full_text)):
            current_word = self.toNumber[full_text[i]]
            self.adj[prev_word].append(current_word)
            prev_word = current_word
            
    def random_word(self, word):
        candidates = self.adj[self.toNumber[word]]
        return self.toWord[random.choice(candidates)] if len(candidates)>1 \
            else self.toWord[random.randint(0,len(self.adj)-1)]