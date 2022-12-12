import pandas as pa
import math as m
import os
from collections import defaultdict
import re

ham_paths_test = ['C:\\Users\\dimas\\PycharmProjects\\Bias_Classificator\\enron1\\ham']
spam_paths_test = ['C:\\Users\\dimas\\PycharmProjects\\Bias_Classificator\\enron1\\spam']
ham_paths_learn = ['C:\\Users\\dimas\\PycharmProjects\\Bias_Classificator\\enron3\\ham', 'C:\\Users\\dimas'
                                                                                         '\\PycharmProjects' +
                   '\\Bias_Classificator\\enron2\\ham', 'C:\\Users\dimas\\PycharmProjects\\Bias_Classificator\\enron3'
                                                        '\\ham']
spam_paths_learn = ['C:\\Users\\dimas\\PycharmProjects\\Bias_Classificator\\enron3\\spam', 'C:\\Users\\dimas'
                                                                                           '\\PycharmProjects' +
                    '\\Bias_Classificator\\enron2\\spam', 'C:\\Users\dimas\\PycharmProjects\\Bias_Classificator\\enron3'
                                                          '\\spam']


def remove_syms(s):
    s = s.lower()
    return set(re.findall(r'\w+', s))


def dic_update(abs_path, dic, k):
    """updates amount of words_in in dictionary"""
    for mes in os.listdir(abs_path):
        with open(abs_path + "\\" + mes, "r") as f:
            txt = f.read()
            words_in = remove_syms(str(txt))
            for token in words_in:
                if token in dic:
                    dic[token][k] += 1
                else:
                    if k == 0:
                        dic.update({token: [1, 0]})
                    elif k == 1:
                        dic.update({token: [0, 1]})


new_di = {}

for path in ham_paths_learn:
    dic_update(path, new_di, 0)

for path in spam_paths_learn:
    dic_update(path, new_di, 1)

ham_mes_count = 0
spam_mes_count = 0

for p in spam_paths_learn:
    spam_mes_count += len(os.listdir(p))
for p in ham_paths_learn:
    ham_mes_count += len(os.listdir(p))

new_dic = defaultdict(lambda: [0, 0])

for word in new_di:
    new_dic[word][0] = (new_di[word][0] + 1) / (ham_mes_count + 2)
    new_dic[word][1] = (new_di[word][1] + 1) / (spam_mes_count + 2)

spam_mes_count = len(os.listdir(spam_paths_test[0]))
ham_mes_count = len(os.listdir(ham_paths_test[0]))


def prob_count(dictionary, mes, u):
    t_prob = f_prob = 0
    for word_in in mes:
        if word_in in dictionary:
            t_prob += m.log(dictionary[word_in][0])
            f_prob += m.log(dictionary[word_in][1])
        else:
            t_prob += m.log(1 / (ham_mes_count + 2))
            f_prob += m.log(1 / (spam_mes_count + 2))
    t_prob += m.log(ham_mes_count / (ham_mes_count + spam_mes_count))
    f_prob += m.log(spam_mes_count / (ham_mes_count + spam_mes_count))
    return t_prob > f_prob


i = 0
right = 0
for path_l in spam_paths_test:
    for message in os.listdir(path_l):
        with open(path_l + "\\" + message, "r") as f:
            text = f.read()
            words = remove_syms(text)
            if prob_count(new_dic, words, i):
                right += 1
            i += 1

for path_l in ham_paths_test:
    for message in os.listdir(path_l):
        with open(path_l + "\\" + message, "r") as f:
            text = f.read()
            words = remove_syms(text)
            if prob_count(new_dic, words, i):
                right += 1
            i += 1

acc = right / (len(os.listdir(spam_paths_test[0])) + len(os.listdir(ham_paths_test[0])))

print(acc)
