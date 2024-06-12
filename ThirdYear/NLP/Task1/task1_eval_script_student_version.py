import sys
import csv
from itertools import groupby
import itertools
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
if len(sys.argv) != 3:
    print("Usage: python task1_eval_script.py <predictions_file> <validation_file>")
    sys.exit(1)
    
pred_f_name = sys.argv[1]
gold_f_name = sys.argv[2]

import gensim
from gensim.models import Word2Vec

def process_data(data):
    """sort by word pairs ids and then remove ids"""
    data = sorted(data, key=lambda i: int(i[0]))
    data = [row[1:] for row in data]
    data = [row[:-1]+[float(row[-1])] for row in data]
    return data

def read_file(file_name):
    """Read a csv file as a list and sort it"""
    with open(file_name) as f:
        reader = csv.reader(f)
        data = list(reader)
    data = process_data(data)
    return data

gold_standards = read_file(gold_f_name)
predictions = read_file(pred_f_name)
# Attach text word pairs to prediction similarity scores
predictions = [[gold_standards[i][0],gold_standards[i][1], predictions[i][0]] for i in range(len(gold_standards))]

# Group words pairs that have common words
gold_std_grouped = [list(it) for k, it in groupby(gold_standards, lambda p:p[0])]  
pred_grouped = [list(it) for k, it in groupby(predictions, lambda p:p[0])]
val = 0
for i in gold_std_grouped:
    val += len(i)
value = 0
print('The following similarity scores may need checking:')
for idx in range(len(gold_std_grouped)):
    preds = pred_grouped[idx]
    gold_std = gold_std_grouped[idx]
    # Get all possible permutations between word pairs that have common words
    pred_pairs_ = list(itertools.combinations(preds, 2))
    gold_pairs_ = list(itertools.combinations(gold_std, 2))
    # Get the relative order of word pairs' similarity scores in each permutation
    pred_pairs = map(lambda x:1 if x[0][2]-x[1][2] > 0 else 0, pred_pairs_)
    gold_pairs = map(lambda x:1 if x[0][2]-x[1][2] > 0 else 0, gold_pairs_)
    # Check if your prediction gives the same relative order as the gold standard
    out_arr = np.subtract(np.array(list(pred_pairs)), np.array(list(gold_pairs)))
    incorr = np.nonzero(out_arr)
    for item in incorr[0]:
        print("({},{}) similarity score: {}, gold ranking: {}".format(pred_pairs_[item][0][0], pred_pairs_[item][0][1], pred_pairs_[item][0][2], gold_pairs_[item][0][2]))
        print("({},{}) similarity score: {}, gold ranking: {}".format(pred_pairs_[item][1][0], pred_pairs_[item][1][1], pred_pairs_[item][1][2], gold_pairs_[item][1][2]))
        print("----------------------------")
        value += 1
print(f"Incorrect count: {value}")
print(f"All gold_pairs: {val}")
accuracy = ((val-value) / val) * 100
print(f"Accuracy: {accuracy}")

model = gensim.models.Word2Vec(sentences = [t.split() for t in training_data['preprocessed_text'].to_list()], size = 200, window=10, min_count=3)


from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense

max_words = 12000  
max_len = round(average_word_count(X_train))

# Tokenizing and padding the text data
tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(X_train)

X_train_seq = tokenizer.texts_to_sequences(X_train)
X_test_seq = tokenizer.texts_to_sequences(X_test)

X_train_pad = pad_sequences(X_train_seq, maxlen=max_len)
X_test_pad = pad_sequences(X_test_seq, maxlen=max_len)

# Defining the LSTM model architecture
embedding_dim = 100 
model = Sequential()
model.add(Embedding(input_dim=max_words, output_dim=embedding_dim, input_length=max_len))
model.add(Bidirectional(LSTM(64)))
model.add(Dense(9, activation='sigmoid'))

# Compiling the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])