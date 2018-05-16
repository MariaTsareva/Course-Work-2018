import re
import glob
import csv
from pymorphy2 import MorphAnalyzer
from pymystem3 import Mystem
import pandas as pd
import numpy as np


morph = MorphAnalyzer()
path = 'C://Put_txt/*.txt'  # note C:
files = glob.glob(path)
my_dict = {}
pos = []
file_wr = open("C://corp/verbs.csv", 'a', encoding='utf-8')
file_wr.close()
for name in files:
    with open(name, 'r', encoding='utf-8') as f:
        # file = open(name, "r", encoding='utf-8')
        text = f.read()
        text = re.split("[, \!?:;.()\\n]+", text)
        for t in text:
            ana = morph.parse(t)
            first = ana[0]
            if first.tag.POS == 'VERB' and first.tag.aspect is not None:

                # my_dict = first.word
                # pos.append(first.tag.voice)
                my_dict[first.word] = first.tag.aspect
                # my_dict[first.word].append(first.tag.tense)
                # print(my_dict)
                with open('C://corp/aspect.csv', 'w') as csv_file:
                    writer = csv.writer(csv_file)
                    try:
                        for key, value in my_dict.items():
                            writer.writerow([key, value])
                    except UnicodeEncodeError:
                        print(key, value)


