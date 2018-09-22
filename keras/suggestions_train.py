import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.preprocessing import sequence,text
from keras import metrics
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM, Bidirectional, BatchNormalization, Activation, Conv1D, MaxPooling1D, Flatten, GlobalMaxPooling1D
from keras.models import load_model
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from keras.utils.np_utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
np.random.seed(7)

df = pd.read_csv('data/suggestions_data.csv',encoding='latin1')
df2 = pd.read_csv('data/trial_data.csv',encoding='latin1')
df3 = pd.read_csv('data/tweets_data.csv',encoding='latin1')


maxlen = 25
batch_size = 128

tok = text.Tokenizer(num_words=200000)
tok.fit_on_texts(list(df['comments']))
x = tok.texts_to_sequences(df['comments'])
x = sequence.pad_sequences(x, maxlen=maxlen)
y = df['is_prompt_exists']
encoder = LabelEncoder()
encoder.fit(y)
y = encoder.transform(y)
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.1)
word_index = tok.word_index

#create a dictionary which stores embeddings for every word
embeddings_index = {}
f = open('data/glove.840B.300d.txt',encoding="utf8")
for line in f:
    values = line.split()
    word = values[0]
    try:
        coefs = np.asarray(values[1:], dtype='float32')
    except:
        pass
    embeddings_index[word] = coefs
f.close()

#create the embedding matrix mapping every index in the corpus to it's respective embedding_vector
embedding_matrix = np.zeros((len(word_index) + 1, 300))
for word, i in word_index.items():
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector

model1 = Sequential()
#model1.add(Embedding(len(word_index) + 1,300,weights=[embedding_matrix],input_length=maxlen,trainable=True))
model1.add(Embedding(len(word_index) + 1,100,input_length=maxlen))
model1.add(Dropout(0.5))
model1.add(LSTM(100,recurrent_dropout=0.5))
model1.add(Dropout(0.5))
#model1.add(Dense(128, activation='relu'))
#model1.add(Dropout(0.5))
model1.add(Dense(1, activation='sigmoid'))
model1.compile('adam', 'binary_crossentropy', metrics=['accuracy'])
model1_history = model1.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=5,
          validation_split=0.1)
score1, acc1 = model1.evaluate(x_test, y_test,
                            batch_size=batch_size)
print('Test accuracy for model 1:', acc1)
y_pred1 = model1.predict(x_test)
y_pred1 = (y_pred1 > 0.5)
print(classification_report(y_test, y_pred1))
print(confusion_matrix(y_test, y_pred1))

"""model3 = Sequential()
#model3.add(Embedding(len(word_index) + 1,300,weights=[embedding_matrix],input_length=maxlen,trainable=False))
model3.add(Embedding(len(word_index) + 1,100,input_length=maxlen))
model3.add(Dropout(0.3))
model3.add(Conv1D(350,3,padding='valid',activation='relu',strides=1))
model3.add(GlobalMaxPooling1D())
model3.add(Flatten())
model3.add(Dense(350, activation = 'relu'))
model3.add(Dropout(0.3))
model3.add(Dense(1, activation='sigmoid'))
model3.compile('adam', 'binary_crossentropy', metrics=['accuracy'])
model3_history = model3.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=5,
          validation_split=0.1)
score3, acc3 = model3.evaluate(x_test, y_test,
                            batch_size=batch_size)
print('Test accuracy for model 3:', acc3)
y_pred3 = model1.predict(x_test)
y_pred3 = (y_pred3 > 0.5)
print(classification_report(y_test, y_pred3))"""

tok2 = text.Tokenizer(num_words=200000)
tok2.fit_on_texts(list(df2['sentence']))
x2 = tok2.texts_to_sequences(df2['sentence'])
x2 = sequence.pad_sequences(x2, maxlen=maxlen)
y2 = df2['label']
encoder2 = LabelEncoder()
encoder2.fit(y2)
y2 = encoder2.transform(y2)

score2, acc2 = model1.evaluate(x2, y2,
                            batch_size=batch_size)
print('Test accuracy for model 2:', acc2)
y_pred2 = model1.predict(x2)
y_pred2 = (y_pred2 > 0.5)
print(classification_report(y2, y_pred2))
#print(confusion_matrix(y2, y_pred2))

tok3 = text.Tokenizer(num_words=200000)
tok3.fit_on_texts(list(df3['text']))
x3 = tok3.texts_to_sequences(df3['text'])
x3 = sequence.pad_sequences(x3, maxlen=maxlen)
y3 = df3['label']
encoder3 = LabelEncoder()
encoder3.fit(y3)
y3 = encoder3.transform(y3)

score3, acc3 = model1.evaluate(x3, y3,
                            batch_size=batch_size)
print('Test accuracy for model 3:', acc3)
y_pred3 = model1.predict(x3)
y_pred3 = (y_pred3 > 0.5)
print(classification_report(y3, y_pred3))




"""def plot_history(histories, key='acc'):
  plt.figure(figsize=(16,10))

  for name, history in histories:
    val = plt.plot(history.epoch, history.history['val_'+key],
                   '--', label=name.title()+' Validation')
    plt.plot(history.epoch, history.history[key], color=val[0].get_color(),
             label=name.title()+' Train')

  plt.xlabel('Epochs')
  plt.ylabel(key.replace('_',' ').title())
  plt.legend()

  plt.xlim([0,max(history.epoch)])
  plt.show()


plot_history([('model1', model1_history),('model2', model2_history)])"""
