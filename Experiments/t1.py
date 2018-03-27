DATA_PATH = "texts/" # The directory to look in for all the text files to be analyzed.

#The names (and locations) of the csv files that will be created:
WORD_FREQUENCY_CSV_FILENAME = "Frequencies.csv"
INVERSE_DOCUMENT_FREQUENCY_CSV_FILENAME = "InverseDocumentFrequencies.csv"
TF_IDF_CSV_FILENAME = "tfidf.csv"

import os

textdirs = os.listdir(DATA_PATH) # returns list
texts = []

#Loop over all of the files in the provided directory
for file in textdirs:
    
    #Ensure that only text files are included:
    if file.endswith(".txt"):
        text_dir = os.path.join(DATA_PATH, file)
        texts.append(text_dir)

print(texts)

import csv
import string
import re
import pandas as pd
from collections import defaultdict


num_lines = 0
num_words = 0
num_chars = 0

counts = defaultdict(int)
docs = {}

for text in texts:
    with open(text, 'r', encoding="utf-8") as f:
        for line in f:
            # Use Regex to remove punctuation and isolate words
            words = re.findall(r'\b\w[\w-]*\b', line.lower())
            for word in words:
                counts[word] += 1
            num_lines += 1
            num_words += len(words)
            num_chars += len(line)

    relativefreqs = {}
    for word, rawCount in counts.items():
        #relativefreqs[word] = rawCount #/ num_words
        # gather only words with alphabetical characters, discard ones with numbers
        if word.isalpha():
            relativefreqs[word] = rawCount / num_words
        counts[word] = 0
    # add this document's relative freqs to our dictionary
    docs[os.path.basename(text)] = relativefreqs

#output everything to a .csv file, using pandas as a go between.
df = pd.DataFrame(docs)
df = df.fillna(0)
df.to_csv(WORD_FREQUENCY_CSV_FILENAME, encoding="utf-8") # write out to CSV
print("Done.")


import csv
import math
import pandas as pd

idf = {}

with open(WORD_FREQUENCY_CSV_FILENAME, encoding="utf-8", newline='') as csvfile:
    wordsreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    
    #skip header information
    total_documents = len(next(wordsreader, None)) - 1
    for row in wordsreader:
        docsContainingWord = 0
        iterrow = iter(row)
        next(iterrow)
        for entry in iterrow:
            if (entry != '0.0') and (entry != '0'):
                docsContainingWord += 1
        idf[row[0]] = math.log(total_documents / (1 + docsContainingWord))
        
df = pd.DataFrame(idf, index=['Inverse Document Frequency'])
df2 = df.transpose()
df2.to_csv(INVERSE_DOCUMENT_FREQUENCY_CSV_FILENAME, encoding="utf-8")
print("Done.")


import csv

file1reader = csv.reader(open(WORD_FREQUENCY_CSV_FILENAME, encoding="utf-8"), delimiter=",")
file2reader = csv.reader(open(INVERSE_DOCUMENT_FREQUENCY_CSV_FILENAME, encoding="utf-8"), delimiter=",")

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#skip headers
header1 = next(file1reader) #header
header2 = next(file2reader) #header
with open(TF_IDF_CSV_FILENAME, 'w', encoding="utf-8", newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(header1)
    for row1, row2 in zip(file1reader, file2reader):
        rowOut = []
        iterrow1 = iter(row1)
        rowOut.append(next(iterrow1))
        for entry in iterrow1:
            entry = float(entry) * float(row2[1])
            rowOut.append(entry)
        writer.writerow(rowOut)
    
print("Done.")