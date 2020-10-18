# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 16:27:40 2020

@author: giris
"""

# (1) Lexicographic compare -- check
# (2) Next word function -- check
# (3) Remove debug statements, edit init function, 
# (4) Saving and loading AVL trees

from PSR.WebsterClient import look_up_PoS
import random#, os

pos_expanded = {'Adj': 'adjective', 'N' : 'noun', 'Adv' : 'adverb', \
                'P' : 'preposition', 'D': 'determiner', 'V' : 'verb', \
                           'C' : 'conjunction', 'T' : 'auxiliary verb'}

def debug(error):
    if (0):
        print(error)

class TextMap():

    def __init__(self, args = []):
        # lex has each prev word once -- leads to a tuple ([following words], [pos])
        self.lex = {}
        
        if len(args) != 0: 
            self.array_insert(args)
            
    def array_insert(self, arr):
        debug(arr)
        if (type(arr[0]) != list):
            prev = "^"
            for i in arr:
                self.insert(i, prev)
                prev = i
        else:
            for i in arr:
                self.array_insert(i)

    def insert(self, key, prev = "^"):
        global pos_expanded
        debug(key)
        if prev in self.lex: 
            self.lex[prev][0].append(key)
        elif prev != "^":
            self.lex[prev] = ([key], look_up_PoS(prev, pos_expanded.values()))
    
    def next_random_word(self, prev, threshold = 1):
        choices_num = len(self.lex[prev])
        
        if (choices_num >= threshold):
            return random.choice(self.lex[prev])
        else:
            return self.random_word()
    
    def get_pos(self, current, target_pos):
        global pos_expanded
        follow_list = self.lex[current][0]
        target_check = []
        for word in follow_list:
            if (pos_expanded[target_pos] in self.lex[word][1]):
                target_check += word
        
        if (not target_check): return self.random_word()
        return random.choice(target_check)
    
    def random_word(self):
        return random.choice(list(self.lex.keys()))        
    
    def display(self, level=0, pref=''):
        '''
        Display the whole tree. Uses recursive def.
        TODO: create a better display using breadth-first search
        '''      
        print(self.lex)
# =============================================================================
#         self.update_heights()  # Must update heights before balances 
#         self.update_balances()
#         debug(self.node == None)
#         if(self.node != None): 
#             print ('-' * level * 2, pref, self.node.key, "[" + str(self.height) + ":" + str(self.balance) + "]", \
#                                                            'L' if self.is_leaf() else ' ', self.node.freq)
#             if self.node.left != None: 
#                 self.node.left.display(level + 1, '<')
#             if self.node.left != None:
#                 self.node.right.display(level + 1, '>')
# =============================================================================
