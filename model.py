import pandas as pd
import numpy as np
from keras.layers import LSTM,Dense,Dropout,Input,Embedding
import pickle
from keras.models import Model


with open('static\embedd_matrix.npy','rb') as f:
    embedd_matrix=np.load(f)

vocab_size=embedd_matrix.shape[0]
maxlen=50

input=Input(shape=(50,))

embedd=Embedding(input_dim=vocab_size,output_dim=50,weights=[embedd_matrix],mask_zero=True,trainable=False)(input)

lstm1=LSTM(64,return_sequences=True)(embedd)

dropout1=Dropout(0.5)(lstm1)

lstm2=LSTM(32,return_sequences=True)(dropout1)

dropout2=Dropout(0.5)(lstm2)

lstm3=LSTM(32)(dropout2)

output=Dense(2,activation='softmax')(lstm3)

model=Model(inputs=input,outputs=output)



model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
model.load_weights("static\lstm1.h5")

with open('static/nb_classifier.pkl','rb') as f:
    nb=pickle.load(f)


def predict(tokenized_reviews,cv_reviews):

    y_pred=model.predict(tokenized_reviews)
    sent_1=np.argmax(y_pred,axis=1)

    sent_2=nb.predict(cv_reviews)

    sentiment=np.logical_and(sent_1,sent_2)

    return sentiment



    