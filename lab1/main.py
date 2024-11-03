import argparse 
from rich.progress import track 
import re 
from ascii_graph import Pyasciigraph 
from ascii_graph import colors  

import collections
from _collections_abc import Iterable 
collections.Iterable =  Iterable 

import os 


parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str, help='filename to process.')
parser.add_argument('--limit', '-l', type=int, default=10, help='number of words in the histogram.')
parser.add_argument('--minLength', '-ml', type=int, default=0, help='minimal length of analyzed words.')
parser.add_argument('--ignoredList', '-iL', nargs='*', default=[], help='list of words to ignore.')
parser.add_argument('--ignoredChars', '-iC', nargs='*', default=[], help='list of chars chains that cant be present in analized words.')
parser.add_argument('--requiredChars', '-rC', nargs='*', default=[], help='list of chars chains that have to be present in analized words.')
parser.add_argument('--dirname', '-dn', type=str, help='If given, all texts from txt files present in given directory will be analized.')
args = parser.parse_args()

def wordsFilter(word):
    if word in args.ignoredList:
        return False 
    if word == '':
        return False 
    if len(word) < args.minLength:
        return False 
    for chars in args.ignoredChars:
        if chars in word:
            return False     
    for chars in args.requiredChars:  ### I assume all chars chains have to be present in a word to be counted ### 
        if chars not in word:
            return False 
    return True 

if type(args.dirname) != str:
    dir_name = './'
    files_list = [args.filename]
else:
    dir_name = args.dirname + '/'    
    files_list = [] 
    for f in os.listdir(dir_name):
        if f.endswith(".txt"):
            files_list.append(f)

word_counts = {}
for file_name in track(files_list, description="Reading..."):
    file = open(dir_name + file_name, "r", encoding="utf-8")
    for line in file:
        tokens = re.split(r"[ .'\n]+", line)
        for word in tokens:
            if wordsFilter(word):
                if word.upper() in word_counts:
                    word_counts[word.upper()] += 1
                else:
                    word_counts[word.upper()] = 1
file.close()

word_counts = dict(sorted(word_counts.items(), key=lambda item: item[1], reverse=True))
items = list(word_counts.items())

hist_data = []
color_list = [colors.BBla, colors.BIGre, colors.BICya, colors.BYel, colors.BIRed,
              colors.BBlu, colors.BIPur, colors.BIWhi]

for i in range(min(args.limit, len(word_counts))):
    key, value = items[i]
    hist_data.append((key, value, color_list[i % len(color_list)]))    

for line in Pyasciigraph().graph('Words histogram', hist_data):
    print(line)  