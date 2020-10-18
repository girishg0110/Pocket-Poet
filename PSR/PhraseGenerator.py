# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 00:22:40 2020

@author: giris
"""

import PSRProcesser, random, WebsterClient, os

pos_expanded = {'Adj': 'adjective', 'N' : 'noun', 'Adv' : 'adverb', \
                'P' : 'preposition', 'D': 'determiner', 'V' : 'verb', \
                           'C' : 'conjunction', 'T' : 'auxiliary verb'}


def debug(x):
    if (0): print(x)

def generate_phrase(phrase_type, psr_dict, lexicon, prob_threshold = 0.7):
    final_phr = ""
    current_rule = psr_dict[phrase_type]
    for i in current_rule:
        if (not i[1] or random.random() > prob_threshold):
            # (1) One-Or-Other --> choose one if 1OrOther
            mini_phrase = i[0]
            debug(mini_phrase)
            if (type(mini_phrase) == list):
                mini_phrase = random.choice(mini_phrase)#[random.randint(0, len(mini_phrase))]

            if (mini_phrase in psr_dict.keys()):  
                # (2) Phrase --> choose one if 1OrOther
                final_phr += generate_phrase(mini_phrase, psr_dict, lexicon, prob_threshold + 0.1)
                # (3) Multiplicity
                while (random.random()*i[2] > prob_threshold):
                    final_phr += generate_phrase(mini_phrase, psr_dict, lexicon, prob_threshold + 0.1)
                # make a current thing (phrase/word) - choose, if /
                # repeat potentially if +
                # /, +, phrase vs word
            else:
                # (2) Word --> if word, just pop one in
                final_phr += generate_word(mini_phrase, lexicon)
                # (3) Multiplicity
                while (random.random()*i[2] > prob_threshold):
                    final_phr += generate_phrase(mini_phrase, lexicon)
    
    return final_phr

def generate_word(word_type, proc_lex):
    global pos_expanded
    debug("Generating " + word_type + "...")
    #print(word_type + ' ', end = "")
    pos_choices = proc_lex[pos_expanded[word_type]]
    if (len(pos_choices) > 0):
        return random.choice(proc_lex[pos_expanded[word_type]]) + " "
    else:
        return ""


def process_lexicon(lexicon):
    # Nouns and pronouns (2) May have to have master list of C and T (not even use them if
    #   none found)
    global pos_expanded
  
    processed_lex = {}
    for x in pos_expanded.values():
        processed_lex[x] = []
    for word in lexicon:
        total_pos = WebsterClient.look_up_PoS(word, pos_expanded.values())
        for part in total_pos:
            processed_lex[part].append(word)
    
    return processed_lex
        
def process_phrase(phrase_type, phrase, rules):
    global pos_expanded
    
    possible_pos = []
    words = phrase.split()
    for p in words:
        possible_pos += [WebsterClient.look_up_PoS(p, pos_expanded.values())]
    
    phr_rule = ""
    try: 
        phr_rule = rules[phrase_type]
    except:
        phr_rule = phrase_type
    
    
    print(possible_pos)
    print(phr_rule)
    return 0

def generate_lexicon(keywords, depth = 3, spread = 3):
    lex = []
    for i in keywords:
        lex += WebsterClient.related_words(i, depth, spread)
    
    return process_lexicon(lex)

ps_rules = PSRProcesser.get_rules_from_file("PSR Text.txt")

sonnet_cliv = ['the', 'little', 'love', 'god', 'lying', 'once', 'asleep', 'laid', 'by', \
               'his', 'side', 'his', 'heart', 'inflaming', 'brand', 'whilst', 'many', \
               'nymphs', 'that', "vow'd", 'chaste', 'life', 'to', 'keep', 'came', \
               'tripping', 'by', 'but', 'in', 'her', 'maiden', 'hand', 'the', 'fairest', \
               'votary', 'took', 'up', 'that', 'fire', 'which', 'many', 'legions', 'of', \
               'true', 'hearts', 'had', "warm'd", 'and', 'so', 'the', 'general', 'of', \
               'hot', 'desire', 'was', 'sleeping', 'by', 'a', 'virgin', 'hand', "disarm'd", \
               'this', 'brand', 'she', 'quenched', 'in', 'a', 'cool', 'well', 'by', 'which', \
               'from', "love's", 'fire', 'took', 'heat', 'perpetual', 'growing', 'a', 'bath', \
               'and', 'healthful', 'remedy', 'for', 'men', "diseas'd", 'but', 'i', 'my', \
               "mistress'", 'thrall', 'came', 'there', 'for', 'cure', 'and', 'this', 'by',\
               'that', 'i', 'prove', "love's", 'fire', 'heats', 'water', 'water', 'cools', \
               'not', 'love']

road_less_traveled = ['Two',
 'roads',
 'diverged',
 'in',
 'a',
 'yellow',
 'wood', 'And',
 'sorry',
 'I',
 'could',
 'not',
 'travel',
 'both', 'And',
 'be',
 'one',
 'traveler,',
 'long',
 'I',
 'stood', 'And',
 'looked',
 'down',
 'one',
 'as',
 'far',
 'as',
 'I',
 'could', 'To',
 'where',
 'it',
 'bent',
 'in',
 'the',
 'undergrowth', 'Then',
 'took',
 'the',
 'other,',
 'as',
 'just',
 'as',
 'fair', 'And',
 'having',
 'perhaps',
 'the',
 'better',
 'claim', 'Because',
 'it',
 'was',
 'grassy',
 'and',
 'wanted',
 'wear', 'Though',
 'as',
 'for',
 'that',
 'the',
 'passing',
 'there', 'Had',
 'worn',
 'them',
 'really',
 'about',
 'the',
 'same', 'And',
 'both',
 'that',
 'morning',
 'equally',
 'lay', 'In',
 'leaves',
 'no',
 'step',
 'had',
 'trodden',
 'black', 'Oh,',
 'I',
 'kept',
 'the',
 'first',
 'for',
 'another',
 'day', 'Yet',
 'knowing',
 'how',
 'way',
 'leads',
 'on',
 'to',
 'way', 'I',
 'doubted',
 'if',
 'I',
 'should',
 'ever',
 'come',
 'back', 'I',
 'shall',
 'be',
 'telling',
 'this',
 'with',
 'a',
 'sigh', 'Somewhere',
 'ages',
 'and',
 'ages',
 'hence', 'Two',
 'roads',
 'diverged',
 'in',
 'a',
 'wood,',
 'and',
 'I',
 'took',
 'the',
 'one',
 'less',
 'traveled',
 'by', 'And',
 'that',
 'has',
 'made',
 'all',
 'the',
 'difference.']

simple_list = ['cat', 'the', 'bat', 'cute', 'hit', 'fast', 'limp', 'clock']
basic_sentence = "the cat likes the bat and my dog is in a house".split()

full_path = os.getcwd() + r"\Processed Lexicons\CLIV.txt"

sentence_rule = ps_rules['TP']
#processed = process_lexicon(road_less_traveled[0:10])
if (0):
    f = open(full_path, "w")
    f.write(str(processed))
    f.close()
    print("")

determiners = ['a', 'the']
basic_verbs = ['is', 'be']

elements = ['fire', 'water', 'earth', 'sky', 'warm', 'happy', 'comfort', 'sleep']
amma = ['blind', 'emperor', 'clothes', 'courtier', 'robes', 'purple', 'king', 'court', 'ego', 'vanity', 'flatter']
grace_hat = ['hat', 'cap', 'on', 'head', 'stay', 'hide', 'clothing', 'fashion', 'rest']
grace_bf = ['Benjamin', 'Frank', 'electricity', 'statesman', 'science', 'politics', 'wit', 'funny']

if (0):
    for i in range (1, 2):
        processed = generate_lexicon(grace_bf)
        sonnet = ""
        for j in range (0,20):
            sonnet += (generate_phrase('TP', ps_rules, processed) + "\n")
        print(sonnet)
#        full_path = os.getcwd() + r"\Sonnets" + r"\Sonnet " + str(i) + ".txt"
#        f = open(full_path, "w")
#        f.write(sonnet)
#        f.close()



# Verb tenses
# Keywords --> makes its own lexicon
# Take themes and title from Poetry Foundation or Goodreads, use as keywords

# =============================================================================
# # Stats on changing prob_threshold and effect on avg length
# length = 0
# count = 2
# for i in range (0, count):
#     new_sentence = generate_phrase('TP', ps_rules, sonnet_cliv, 0.7)
#     print(new_sentence)
#     length += new_sentence.count(" ")
# print("Length:", str(length/count))
# =============================================================================
    
# =============================================================================
#  Hash table for frequency lists (buckets by PoS)
#  Occurence for each PoS maintained (length of individual linked list)
#  Multiple parts of speech though??
#  First X results chosen from search page
#  Multiple sources in query set
#  GovTrack, Justia/Oyez, Genius (rap)
#  Get structure of phrase from words (PoS function of words)
#        
#  https://www.dictionaryapi.com/api/v3/references/collegiate/json/that?key=KEY
#  https://www.dictionaryapi.com/api/v3/references/school/json/that?key=KEY
# 
# Key (Collegiate Dictionary):
# 8b69ae94-7edc-4404-99f0-4f2d0d93ccb2
# Key (School Dictionary):
# 313ee166-4784-4268-b18a-6865aec2b85f
# =============================================================================