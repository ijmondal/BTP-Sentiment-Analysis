"""Identify CMI distributions"""
import re
import json
import pdb
from operator import itemgetter
from numpy import linspace
from matplotlib.pyplot import scatter, show
import matplotlib.pyplot as plt
import pickle
import numpy as np
import sys

def calculate_cmi(sentence):
    """Calculate CMI for a sentence."""
    hi_regex = r'([.]*\\HI)'
    en_regex = r'([.]*\\EN)'
    cmi = 0
    hi_words = re.findall(hi_regex, sentence)
    en_words = re.findall(en_regex, sentence)
    sentence_len = len(hi_words+en_words)
    if sentence_len:
       cmi = float(max(len(en_words),len(hi_words)))/sentence_len
    return cmi



def read_data(filepath):
    """Read data into a python dictionary."""
    f = open(filepath, 'r')
    data = json.load(f)
    return data

def load_pickle(file_name):
    return pickle.load(open(file_name,"rb"))

def write_data(filepath, data):
    """Write the data into the file."""
    string = "\n".join(data)
    f = open(filepath, 'w')
    f.write(string)
    f.close()


def get_cmi_buckets(data):
    """Return positive, neutral and negative accuracies for cmi buckets."""
    predicted = load_pickle(sys.argv[1])
    cmi_list = list()
    cmi=0
    for i, obj in enumerate(data):
        lang_text = obj["lang_tagged_text"]
        if type(lang_text) is float:
            continue
        cmi = calculate_cmi(lang_text)
        cmi_list.append([cmi, predicted[i], obj["sentiment"] ])

    ## dividing based on cmi
    buckets = [list() for i in range(10)]
    for each in cmi_list:
        buckets[9 if each[0]==1.0 else int(each[0]*10)].append([each[2], int(each[1]==each[2])])

    ## calculating accuracies. if accuracy saved as -1, then len(that bucket) = 0.
    bucket_accuracy = list()
    for bucket in buckets:
        bucket = np.array(bucket)
        pos_acc = neg_acc = neu_acc = 0
        if len(bucket)!=0:
            positive =(bucket[:,0]==1).nonzero()[0]
            negative = (bucket[:,0]==-1).nonzero()[0]
            neutral = (bucket[:, 0]==0).nonzero()[0]
            if len(positive)!=0:
                pos_t = len((bucket[positive, 1]==1).nonzero()[0])
                pos_f = len((bucket[positive, 1]==0).nonzero()[0])
                pos_acc = pos_t

            if len(negative)!=0:
                neg_t = len((bucket[negative, 1]==1).nonzero()[0])
                neg_f = len((bucket[negative, 1]==0).nonzero()[0])
                neg_acc = neg_t

            if len(neutral)!=0:
                neu_t = len((bucket[neutral, 1]==1).nonzero()[0])
                neu_f = len((bucket[neutral, 1]==0).nonzero()[0])
                neu_acc = neu_t

        print(bucket)
        if bucket.size != 0:
            bucket_accuracy.append(float(pos_acc + neg_acc + neu_acc)/(positive.size + negative.size + neutral.size))
        else:
            bucket_accuracy.append(0.0)
    return bucket_accuracy



if __name__ == "__main__":
    data = read_data(sys.argv[2])
    cmi_list = get_cmi_buckets(data)
    print(cmi_list)
