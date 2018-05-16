import re
import operator
import glob
from pymystem3 import Mystem
import pandas as pd
import numpy as np

def open_file():
    path = 'C://Put_txt/*.txt'  # note C:
    files = glob.glob(path)
    text11 = ''
    for name in files:
        with open(name, encoding='utf-8') as f:
            # file = open(name, "r", encoding='utf-8')
            text = f.read().lower()
            f.close()
        text11 += text
    return text11


def from_str_to_list(text11):
    # print(text11)
    m = Mystem()
    d = re.split("[, \!?:;.()\\n]+", text11)
    dd = ' '.join(d)
    lemmas = m.lemmatize(dd)
    text1 = ' '.join(lemmas)
    text1 = re.sub(r'[A-z&=;]+', r'', text1).strip()
    return text1


def count_text(text1):
    words = re.findall(r"(\w+)", text1, re.UNICODE)
    stats = {}
    count_1 = 0
    for word in words:
        count_1 += 1
        stats[word] = stats.get(word, 0) + 1
    print('Количество слов: ', count_1)
    return words, count_1


def del_part(words):
    from pymorphy2 import MorphAnalyzer
    morph = MorphAnalyzer()
    clean_words = []
    # print('3.1')
    words1 = [item for item in words if not item.isdigit()]
    # print('3.2')
    for word in words1:
        ana = morph.parse(word)
        #print('3.3')
        first = ana[0]
        if first.tag.POS == 'PREP' or first.tag.POS == 'CONJ'or first.tag.POS == 'PRCL' :
            # print('3.4')
            continue
        else:
            if first.word in 'abcdefghijklmnopqrsuvwxyzóáéíã':
                # print('3.5')
                continue
            else:
                clean_words.append(first.word)
    # print(clean_words)
    return clean_words


def clean_words1(clean_words, count_1):
    word_ = []
    count_ = []
    ipm_ = []
    stats = {}
    count = 0
    for word in clean_words:
        count += 1
        stats[word] = stats.get(word, 0) + 1
    stats_list = sorted(stats.items(), key=operator.itemgetter(1), reverse=True)
    for word, count in stats_list:
        if count > 50:
            ipm_fr = count*1000000/count_1
            ipm_fr = float(ipm_fr)
            word_.append(word)
            count_.append(count)
            ipm_.append(ipm_fr)
            # print("%-32s %d %.2f" % (word, count, ipm_fr))
    my_words = pd.DataFrame(
        {'word': word_,
         'my ipm': ipm_})
    print(type(my_words['word']))
    return my_words


def dict_pd():
    a = pd.read_csv('C://Put_txt/freqrnc2011.csv', sep='\t')
    a['Lemma'].str.lower()
    print(len(a))
    # print(a)
    return a


def comparison(my_words, a):
    col = my_words[my_words.word.isin(a.Lemma)]
    not_col = my_words[~my_words.word.isin(a.Lemma)]
    not_col.reset_index(drop=True)
    not_col.sort_values('word')
    not_col.to_csv('C://Put_txt/words_not_in_list.csv', index=None)
    col = col.reset_index(drop=True)
    col = col.sort_values('word')
    col1 = a[a.Lemma.isin(my_words.word)]
    print(len(col))
    col1 = col1.drop_duplicates('Lemma')
    col1 = col1.reset_index(drop=True)
    col1 = col1.sort_values('Lemma')
    col1 = col1.rename(index=str, columns={"Lemma": "word"})
    print(len(col1))
    col2 = col.merge(col1, how='left', on='word')
    col2 = col2.drop(['PoS', 'R', 'D', 'Doc'], axis=1, inplace=False)
    print(col2)
    col2.to_csv('C://Put_txt/my_database.csv', index=None)
    return col2


def lexicon(col2):
    my_list = pd.DataFrame(np.where(col2['my ipm'] > col2['Freq(ipm)'], col2['word'], np.nan))
    my_list = my_list.rename(index=str, columns={0: "word"})
    my_list = my_list.dropna()
    my_list.to_csv('C://Put_txt/top_words.csv', index=None)
    return my_list


new_file = open_file()
print('1')
converce = from_str_to_list(new_file)
print('2')
counting, my_count = count_text(converce)
print('3')
delin = del_part(counting)
print('4')
cleaning = clean_words1(delin, my_count)
frec2011 = dict_pd()
my_compare = comparison(cleaning, frec2011)
lex = lexicon(my_compare)