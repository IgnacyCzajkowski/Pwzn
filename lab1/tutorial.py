import sys 
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str, help='filename to process')
parser.add_argument('--limit', '-l', type=int, help='minimum length of words', default=0)
parser.add_argument('--flag', '-f', action='store_true', help='just a flag')
parser.add_argument('--list', '-L', nargs='+', help='list of strings')
args = parser.parse_args()

print(args)
print(args.filename)
print(args.limit)
print(args.flag)
print(args.list)