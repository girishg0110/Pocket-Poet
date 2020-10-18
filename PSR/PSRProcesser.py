# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 15:03:10 2020

@author: giris
"""

# =============================================================================
# Key (Dictionary):
#     8b69ae94-7edc-4404-99f0-4f2d0d93ccb2
# Key (Elementary Dictionary):
#     313ee166-4784-4268-b18a-6865aec2b85f
# =============================================================================

def psr_part_tuple(fragment, option):
    slash_index = -1
    try:
        slash_index = fragment.index('/')
    except(ValueError):
        if (fragment[-1] == '+'): return (fragment[:-1], option, True)
        else: return (fragment, option, False)
    
    choice_list = []
    try: 
        while (len(fragment) > 0):
            choice_list.append(fragment[0:slash_index])
            fragment = fragment[slash_index + 1:]
            slash_index = fragment.index('/')
    except(ValueError):
        if (len(fragment) > 0): choice_list.append(fragment)
    
    return (choice_list, option, False)

def parse_psr(rule):
    #print(rule, end="")
    parsed_list = []
    current = ""
    for i in rule:
        if ((i == ' ' and len(current) == 0) or i == '('):
            continue
        elif (i.isalpha() or i == '/' or i == '+'):
            current += i
        else:
            if (len(current) > 0):
                parsed_list.append(psr_part_tuple(current, (i==')')))
            current = ""
    
    return parsed_list

def get_rules_from_file(path):
    psr_file = open(path, "r")
    psr_dictionary = {}
    for line in psr_file:
        if (line == "\n"): break
        equation = line.split('=')
        psr_dictionary[equation[0]] = parse_psr(equation[1])
    
    psr_file.close()
    return psr_dictionary