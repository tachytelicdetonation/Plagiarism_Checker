import os
import sys
import time
import json
import nltk
import nltk.data
from tqdm import tqdm 
from termcolor import colored
from difflib import SequenceMatcher
nltk.download('punkt')

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def removeEmptySentences(raw_lines):
    tmp = ''
    for line in raw_lines:
        if line != '':
            tmp += line + ' '
    return tmp


def preprocessLines(path_to_file):
    lines = []
    fp = open(path_to_file)
    data = fp.read()
    tokenized_lines = tokenizer.tokenize(data)
    for line in tokenized_lines:
        processed_line = line
        processed_line = processed_line.replace('\n',',')
        processed_line = processed_line.replace(' ',',')
        processed_line = processed_line.split(',')
        processed_line = removeEmptySentences(processed_line)
        lines.append(processed_line)
    return lines


def returnRatio(plagarised_obj, line):
    index = plagarised_obj['lines'].index(line)
    return plagarised_obj['reference_ratios'][index]

def getRatio(refernces, plagarised_obj):
    ratios = 0
    for r in plagarised_obj['reference_ratios']:
        ratios += r
    return ratios/len(refernces)

def plagarismCheck(references, path_to_originals):
    plagarism_checker = []
    orignals = os.listdir(path_to_originals)
    
    for orig in orignals:
        plagarised ={'orig_file': '' ,'ratio': [] ,'reference_ratios': [],'lines': []}
        plagarised['orig_file'] = orig
        orig_lines = preprocessLines(path_to_originals + orig)
        for line1 in tqdm(references):
            for line2 in orig_lines:
                seq = SequenceMatcher(None, line1, line2)
                r = seq.ratio()
                if r > 0.7:
                    plagarised['reference_ratios'].append(r)
                    plagarised['lines'].append(line1)
                    
        ratio = getRatio(references, plagarised)
        plagarised['ratio'].append(ratio)
        plagarism_checker.append(plagarised)
    return plagarism_checker

def checkPlagarismOffline(reference, plagarised_object, isjson = False):
    obj = {'line':[],'ratio':[], 'color':[],'orig':[]}
    for i in reference:
        tmp_obj = {'ratio':[],'color':[],'orig':[]}
        for j in range(len(plagarised_object)):
            if i in plagarised_object[j]['lines']:
                rr = returnRatio(plagarised_object[j],i)
                tmp_obj['ratio'].append(rr)
                tmp_obj['color'].append('red')
                tmp_obj['orig'].append(plagarised_object[j]['orig_file'])
            else:
                tmp_obj['ratio'].append(0)
                tmp_obj['color'].append('green')
                tmp_obj['orig'].append('None')
        
        obj['line'].append(i)
        obj['ratio'].append(tmp_obj['ratio'])
        obj['color'].append(tmp_obj['color'])
        obj['orig'].append(tmp_obj['orig'])

    if isjson:
        return json(obj)
    else:
        return obj
    

def showPlagarismOffline(obj):
    for i in range(len(obj['line'])):
        tmp = []
        for j in obj['ratio'][i]:
            if j != 0:
                for k in obj['orig'][i]:
                    if k != 'None':
                        tmp.append(str(j) + ' : ' + k)
        if 'red' in obj['color'][i]:
            print(colored(obj['line'][i],'red') + str(tmp))
        else:
            print(colored(obj['line'][i],'green'))
