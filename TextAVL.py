# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 14:19:55 2020

@author: giris --> Adapted from Twoody (girish3) from github
"""

# (1) Lexicographic compare -- check
# (2) Next word function -- check
# (3) Remove debug statements, edit init function, 
# (4) Saving and loading AVL trees

import random#, os

class Node():
    def __init__(self, key):
        self.key = key
        self.left = None 
        self.right = None
        self.total_occurences = 0
        self.freq = {}

def debug(error):
    if (0):
        print(error)

class TextAVL():

    def __init__(self, args = []):
        self.node = None
        self.height = -1 
        self.balance = 0
        TextAVL.size = 0
        
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
        
    def height(self):
        if self.node: 
            return self.node.height 
        else: 
            return 0 
    
    def is_leaf(self):
        return (self.height == 0) 

    def frequency_adjust(self, key, prev):
        tree = self.node
        
        if prev < tree.key: 
            self.node.left.frequency_adjust(key, prev)
            
        elif prev > tree.key: 
            self.node.right.frequency_adjust(key, prev)
        
        else: 
            self.node.total_occurences += 1
            self.node.freq[key] = (self.node.freq[key] + 1) \
                                        if key in self.node.freq else 1
            debug("Key [" + str(key) + "] already in tree.")    
    # are we double adding? once for key, once for prev
    def insert(self, key, prev = "^"):
        TextAVL.size += self.insert_backend(key, prev)
        self.rebalance()
        if (prev != '^'): self.frequency_adjust(key, prev)

    def insert_backend(self, key, prev = "^"):
        debug(key)
        tree = self.node
        
        newnode = Node(key)
        
        if tree == None:
            debug("THERE" + key)
            self.node = newnode 
            self.node.left = TextAVL() 
            self.node.right = TextAVL()
            debug("Inserted key [" + str(key) + "]")
        
        elif key < tree.key: 
            self.node.left.insert_backend(key, prev)
            
        elif key > tree.key: 
            debug("HERE" + key + tree.key)
            self.node.right.insert_backend(key, prev)
        
        else: 
            return False
            debug("Key [" + str(key) + "] already in tree.")
        
        return True
    
    def next_word(self, prev):
        result = self.next_word_driver(prev)
        if (result == "^"): return self.random_word()
        return result
    
    def next_word_driver(self, prev):
        tree = self.node
        
        if prev < tree.key: 
            return self.node.left.next_word(prev)
            
        elif prev > tree.key: 
            return self.node.right.next_word(prev)
        
        else: 
            if (self.node.total_occurences == 0): 
                if (random.random() > 0.5): return "^"
                return "^"
            freq_select = random.randint(1, self.node.total_occurences + 1)
            counter = 0
            for i in self.node.freq.keys():
                counter += self.node.freq[i]
                if (counter >= freq_select):
                    return i;
        
        return prev
        
    def rebalance(self):
        ''' 
        Rebalance a particular (sub)tree
        ''' 
        # key inserted. Let's check if we're balanced
        self.update_heights(False)
        self.update_balances(False)
        while self.balance < -1 or self.balance > 1: 
            if self.balance > 1:
                if self.node.left.balance < 0:  
                    self.node.left.lrotate() # we're in case II
                    self.update_heights()
                    self.update_balances()
                self.rrotate()
                self.update_heights()
                self.update_balances()
                
            if self.balance < -1:
                if self.node.right.balance > 0:  
                    self.node.right.rrotate() # we're in case III
                    self.update_heights()
                    self.update_balances()
                self.lrotate()
                self.update_heights()
                self.update_balances()
 
    def rrotate(self):
        # Rotate left pivoting on self
        debug ('Rotating ' + str(self.node.key) + ' right') 
        A = self.node 
        B = self.node.left.node 
        T = B.right.node 
        
        self.node = B 
        B.right.node = A 
        A.left.node = T 

    
    def lrotate(self):
        # Rotate left pivoting on self
        debug ('Rotating ' + str(self.node.key) + ' left') 
        A = self.node 
        B = self.node.right.node 
        T = B.left.node 
        
        self.node = B 
        B.left.node = A 
        A.right.node = T 

    def update_heights(self, recurse=True):
        if not self.node == None: 
            if recurse: 
                if self.node.left != None: 
                    self.node.left.update_heights()
                if self.node.right != None:
                    self.node.right.update_heights()
            
            self.height = max(self.node.left.height,
                              self.node.right.height) + 1 
        else: 
            self.height = -1 

    def update_balances(self, recurse=True):
        if not self.node == None: 
            if recurse: 
                if self.node.left != None: 
                    self.node.left.update_balances()
                if self.node.right != None:
                    self.node.right.update_balances()

            self.balance = self.node.left.height - self.node.right.height 
        else: 
            self.balance = 0 

    def check_balanced(self):
        if self == None or self.node == None: 
            return True
        
        # We always need to make sure we are balanced 
        self.update_heights()
        self.update_balances()
        return ((abs(self.balance) < 2) and self.node.left.check_balanced() and self.node.right.check_balanced())  
    
    def random_word(self):
        count = [0]
        target = random.randint(1, TextAVL.size + 1)
        debug(target)
        return self.random_word_backend(target, count)
    
    def random_word_backend(self, target, count):
        if (self.node == None or self.node.key == None): return "^"
        count[0] += 1
        if (count[0] == target): 
            return self.node.key
        
        answer = self.node.left.random_word_backend(target, count)
        if (answer != '^'): return answer
        
        answer = self.node.right.random_word_backend(target, count)
        return answer
    
#    def saveAs(file_name, file_path = os.getcwd + "MiniAuthors"):
        
    
    def display(self, level=0, pref=''):
        '''
        Display the whole tree. Uses recursive def.
        TODO: create a better display using breadth-first search
        '''        
        self.update_heights()  # Must update heights before balances 
        self.update_balances()
        debug(self.node == None)
        if(self.node != None): 
            print ('-' * level * 2, pref, self.node.key, "[" + str(self.height) + ":" + str(self.balance) + "]", \
                                                           'L' if self.is_leaf() else ' ', self.node.freq)
            if self.node.left != None: 
                self.node.left.display(level + 1, '<')
            if self.node.left != None:
                self.node.right.display(level + 1, '>')

#        
#    def inorder_traverse(self):
#        if self.node == None:
#            return [] 
#        
#        inlist = [] 
#        l = self.node.left.inorder_traverse()
#        for i in l: 
#            inlist.append(i) 
#
#        inlist.append(self.node.key)
#
#        l = self.node.right.inorder_traverse()
#        for i in l: 
#            inlist.append(i) 
#    
#        return inlist 
# =============================================================================
#     def delete(self, key):
#         # debug("Trying to delete at node: " + str(self.node.key))
#         if self.node != None: 
#             if self.node.key == key: 
#                 debug("Deleting ... " + str(key))  
#                 if self.node.left.node == None and self.node.right.node == None:
#                     self.node = None # leaves can be killed at will 
#                 # if only one subtree, take that 
#                 elif self.node.left.node == None: 
#                     self.node = self.node.right.node
#                 elif self.node.right.node == None: 
#                     self.node = self.node.left.node
#                 
#                 # worst-case: both children present. Find logical successor
#                 else:  
#                     replacement = self.logical_successor(self.node)
#                     if replacement != None: # sanity check 
#                         debug("Found replacement for " + str(key) + " -> " + str(replacement.key))  
#                         self.node.key = replacement.key 
#                         
#                         # replaced. Now delete the key from right child 
#                         self.node.right.delete(replacement.key)
#                     
#                 self.rebalance()
#                 return  
#             elif key < self.node.key: 
#                 self.node.left.delete(key)  
#             elif key > self.node.key: 
#                 self.node.right.delete(key)
#                         
#             self.rebalance()
#         else: 
#             return 
# 
# 
# =============================================================================
#     def logical_predecessor(self, node):
#         ''' 
#         Find the biggest valued node in LEFT child
#         ''' 
#         node = node.left.node 
#         if node != None: 
#             while node.right != None:
#                 if node.right.node == None: 
#                     return node 
#                 else: 
#                     node = node.right.node  
#         return node 
# 
#     def logical_successor(self, node):
#         ''' 
#         Find the smallese valued node in RIGHT child
#         ''' 
#         node = node.right.node  
#         if node != None: # just a sanity check  
#             
#             while node.left != None:
#                 debug("LS: traversing: " + str(node.key))
#                 if node.left.node == None: 
#                     return node 
#                 else: 
#                     node = node.left.node  
#         return node         