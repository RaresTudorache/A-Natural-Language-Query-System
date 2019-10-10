# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    singular = []
    plural = []
    same_form = []
    with open("sentences.txt", "r") as f:
        for line in f:
            for tag2 in line.split():
                w,tag = tag2.split('|')
                if tag == "NNS":
                    plural.append(w)
                elif tag == "NN":
                    singular.append(w)
    for s in singular:
        if s in plural and s not in same_form:         
            same_form.append(s)
    return same_form

unchanging_plurals_list = unchanging_plurals()

def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""    
    stem = ""
    if s in unchanging_plurals_list:
        stem = s
    elif re.match("[a-z]*men$",s):
        stem = s[:-3] + "man"
    else: 
        if s[-4:-2] != 'ch' and s[-4:-2] != 'sh' and re.match("[a-z]*[^sxyzaeiou]s$", s):
            stem = s[:-1]
        elif re.match("[a-z]*[aeiou]ys$",s):
            stem = s[:-1]
        elif re.match("[a-z]+[^aeiou]ies$",s) and len(s) >= 3:
            stem = s[:-3] + "y"
        elif re.match("[^aeiou]ies$",s):
            stem = s[:-1]
        elif re.match("[a-z]*[ox]es$",s) or s[-4:] == "ches" or s[-4:] == "shes" or s[-4:] == "sses" or s[-4:] == "zzes":
            stem = s[:-2]
        elif (re.match ("[a-z]*ses$", s) or re.match("[a-z]*zes$", s)) and s[-4:] != "sses" and s[-4:] != "zzes": 
            stem = s[:-1]
        elif s == "has":
            stem = "have"
        elif re.match ("[a-z]*[^iosxz]es$", s) and s[-4:-2] != "ch" and s[-4:-2] != "sh":
            stem = s[:-1]
        else:
            stem = ""
    return stem

def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    output = []

    if wd in function_words:
        for tag in function_words_tags:
            if tag[0] == wd:
                output.append(tag[1])

    if wd in lx.getAll("P"):
        output.append("P")

    if wd in lx.getAll("A"):
        output.append("A")
    
    if wd in lx.getAll("T"):
        if verb_stem(wd) == "":
            output.append("T" + "p")
        else:
            output.append("T" + "s")
    if verb_stem(wd) in lx.getAll("T"):
        output.append("T" + "s")
    for i in lx.getAll("T"):
        if verb_stem(i) == wd:
            output.append("T" + "p")
            break

    if wd in lx.getAll("I"):
        if verb_stem(wd) == "":
            output.append("I" + "p")
        else:
            output.append("I" + "s")
    if verb_stem(wd) in lx.getAll("I"):
        output.append("I" + "s")
    for i in lx.getAll("I"):
        if verb_stem(i) == wd:
            output.append("I" + "p")
            break

    if wd in lx.getAll("N"):
        if wd in unchanging_plurals_list:
            output += ["Np", "Ns"]
        elif noun_stem(wd) == "":
            output.append("Ns")
        else:
            output.append("Np")
    if noun_stem(wd) in lx.getAll("N"):
        output.append("Np")
    for i in lx.getAll("N"):
        if noun_stem(i) == wd:
            output.append("Ns")
            break

    output = list(set(output))
    return output

def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.