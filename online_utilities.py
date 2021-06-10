from googlesearch import search
from termcolor import colored
from tqdm import tqdm

def searchGoogle(lines):
    count = 0
    tmp = {'line':[],'url':[]}
    for line in tqdm(lines):
        count += 2
        pause = 60  
        for item in search(line, num = 1, stop = 1, pause = pause):
            tmp['line'].append(line)
            tmp['url'].append(item)
            
    return tmp

def getSearchLines(lines):
    tmp = []
    tmp_str = '' 
    for line in lines:
        tmp_str += line
        if len(tmp_str) > 100:
            tmp.append(tmp_str)
            tmp_str = ''
            
        else:
            tmp_str += line
    
    return tmp

def returnUrl(obj, line):
    index = obj['line'].index(line)
    return obj['url'][index]

def showPlagarismOnline(search_lines,online_plagrism_object):
    for i in search_lines:
        if i in online_plagrism_object['line']:
            url = returnUrl(online_plagrism_object,i)
            print(colored(i,'red') + '[' + str(url) + ']')
        else:
            print(colored(i,'green'))