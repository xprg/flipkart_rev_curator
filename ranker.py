import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import model
import preprocess


def create_dataframe(reviews):
    
    tokenized_reviews,cv_reviews,real_reviews=preprocess.preprocess(reviews)
    
    sentiment=model.predict(tokenized_reviews,cv_reviews)
    
    print(len(sentiment))
    

    dic={'body':real_reviews,'sentiment':sentiment,'default':[x for x in range(len(reviews))]}          
    df=pd.DataFrame(dic) 

    tfidf=TfidfVectorizer()
    td_matrix=tfidf.fit_transform(reviews)
    idx_word=tfidf.get_feature_names()

    word_idx={}
    for i in range(len(idx_word)):
        word_idx[idx_word[i]]=i
    

    td_matrix=td_matrix.toarray()
    special=['performance','camera','display','battery','cost']
    

    for word in special:
        if word_idx.get(word) is not None:
            index=word_idx[word]
            tf_idf_scores=td_matrix[:,index]
            df[word]=tf_idf_scores
    

    return df


def sort_according_to(criteria,df):
    if criteria!='default':
        if(criteria in list(df.columns)):
            ans=df.sort_values(by=criteria,ascending=False)
        
        else:
            ans=df
    
    return list(ans[['body','sentiment']])
                                                                    
        
    
    
        
    








    





    


    


def sort_according_to(criteria):
    pass

    
