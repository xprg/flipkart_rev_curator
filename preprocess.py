import re
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import pickle




with open('static/tokenizer.pkl','rb') as f:
    tokenizer=pickle.load(f)

    



stopwords = [ "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", 
             "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down", "during",
             "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", 
             "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into",
             "is", "it", "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or",
             "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", 
             "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's",
             "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up",
             "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's",
             "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've",
             "your", "yours", "yourself", "yourselves" ]

dict_stopwords={}
for s in stopwords:
  dict_stopwords[s]=True



def clean_text(sentence):                           
  sentence=sentence.lower()
  sentence=re.sub("[^a-z]"," ",sentence)
  sentence=sentence.split()

  sentence=" ".join(sentence)

  return sentence





def preprocess(review):
    for i in range(len(review)):
        review[i]=" ".join([word for word in review[i].split() if dict_stopwords.get(word,False)==False])     #stopword removal
    
    for i in range(len(review)):
        review[i]=clean_text(review[i])
    
    reviews=[]
    for i in range(len(review)):
        if len(review[i].split())<75:
            reviews.append(review[i])
    

    tokenized_reviews=tokenizer.texts_to_sequences(reviews)  
    tokenized_reviews=pad_sequences(tokenized_reviews,maxlen=50,padding='post')
    
    return tokenized_reviews


    


    
