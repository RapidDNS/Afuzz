from os import system
import sys

if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    filename = "url.txt"

with open(filename,"r", encoding='utf-8') as fp:
    for line in fp:
        line = line.strip()
        print("scan: " + line)
        system("python afuzz.py -t 50 -u " + line)
