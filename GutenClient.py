# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 21:31:52 2020

@author: giris
"""

import requests
from bs4 import BeautifulSoup

def debug(x):
    if (0): print(x)

def valid_text(full_tag, target_tag, target_match):
    try:
       return (target_match in full_tag[target_tag])
    except(KeyError):
        return False

def find_all(string, target):
    target_len = len(target)
    all_locations = []
    for i in range(len(string)):
        if string[i:i+target_len] == target:
            all_locations.append(i)
        
    return all_locations

def get_link(query):
    search_request = requests.get("http://www.gutenberg.org/ebooks/search/?query=" \
                                  + (query.replace(' ', '+')))
    search_results = BeautifulSoup(search_request.text, features='lxml')

    booklink_tags = search_results.find_all('li')
    right_link = ""
    for tag in booklink_tags:
        if (valid_text(tag, 'class', 'booklink')):
            right_link = tag
            break
    link_text = right_link.text.strip()
    newlines = find_all(link_text, "\n")
    author = link_text[newlines[0] + 1: newlines[1]]
    print(author)
    print("Reading from " + link_text.replace("\n", ', '))
    download_link = "http://www.gutenberg.org" + right_link.find('a')['href']
    return (download_link + ".txt.utf-8", author)
    
def process_book_link(query):
    print("Loading source...")
    all_text = []
    if (type(query) == list):
        for i in query:
            all_text.append(process_book_backend(i))
    else: 
        all_text = [process_book_backend(query)]
        
    return all_text

def process_book_backend(query):
    query_result = get_link(query)
    book = requests.get(query_result[0])
    text = BeautifulSoup(book.text, features='lxml')
    text = text.p.text
    
#    all_author_names = find_all(text, query_result[1])
#    text = text[all_author_names[1] + 1: all_author_names[2]]
    try: 
        startindex = text.index('***START')
    except(ValueError):
        startindex = text.index('*** START')
    
    try:
        endindex = text.index('***END')
    except(ValueError):
        endindex = text.index('*** END')
        
    text = text[startindex:endindex]
    
    for x in text:
        if ((not x.isalpha()) and x != "'"): text = text.replace(x, ' ')
    text = text.lower().split()
    
    return text

def process_poem_link(link):
    print("Loading source...")
    
    book = requests.get(link)
    text = BeautifulSoup(book.text, features='lxml')
    
    
    poem_list = text.find_all('p')
    poem_list[:] = [pTag.get_text() for pTag in poem_list if valid_text(pTag, 'p', 'poem')]
        
    # Generate AVL for words in selection and dictionary {following word : frequency }
        # Note: <br> tag is '\n'
    
    for i in range(0, len(poem_list)):
        for x in poem_list[i]:
            if ((not x.isalpha()) and x != "'"): poem_list[i] = poem_list[i].replace(x, ' ')
        poem_list[i] = poem_list[i].lower().split()
    
    return poem_list