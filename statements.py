# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    def __init__(self):
        self.list = []
         
    def add(self,stem,cat):
        self.list.append((stem,cat))
     
    def getAll(self,cat):
        output_list = []
        for i in self.list:
            if i[0] not in output_list and i[1] == cat:
                output_list.append(i[0])

        return output_list 

class FactBase:
    """stores unary and binary relational facts"""
    def __init__(self):
        self.Unary = []
        self.Binary = []
    def addUnary(self,sym,pred):
        self.Unary.append((sym,pred))
    
    def addBinary(self,sym,pred1,pred2):
        self.Binary.append((sym,pred1,pred2))
    
    def queryUnary(self,sym,pred):
        return (sym, pred) in self.Unary
    
    def queryBinary(self,sym,pred1,pred2):
        return (sym, pred1, pred2) in self.Binary

vb = []
vbz = []

import re
from nltk.corpus import brown

for (word, tag) in brown.tagged_words():
    if tag == "VB":
        vb.append(word)
    if tag == "VBZ":
        vbz.append(word)

def verb_stem(s):
    stem = ""
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    if re.match ("[a-z]*[^sxyzaeiou]s$", s) and s[-4:-2] != 'ch' and s[-4:-2] != 'sh':
        stem = s[:-1]
    elif re.match ("[a-z]*[aeiou]ys$", s):
        stem = s[:-1]
    elif re.match ("[a-z]+[^aeiou]ies$", s) and len(s) >= 3:
        stem = s[:-3] + "y"
    elif re.match ("[^aeiou]ies$", s):
        stem = s[:-1]
    elif re.match ("[a-z]*[ox]es$", s) or s[-4:] == "ches" or s[-4:] == "shes" or s[-4:] == "sses" or s[-4:] == "zzes":
        stem = s[:-2]
    elif (re.match ("[a-z]*ses$", s) or re.match("[a-z]*zes$", s)) and s[-3:] != "sses" and s[-3:] != "zzes":
        stem = s[:-1]
    elif s == "has":
        stem = "have"
    elif re.match ("[a-z]*[^iosxz]es$", s) and s[-4:-2] != 'ch' and s[-4:-2] != 'sh':
        stem = s[:-1]
    else:
        stem = ""

    if (stem in vb and s in vbz):
        return stem
    else:
        return ""

def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg
                        
# End of PART A.