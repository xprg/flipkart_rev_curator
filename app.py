import pandas as pd
import numpy as np
from types import MethodType
from flask import Flask,request,render_template,redirect
from requests.api import post
import model
import preprocess
import scrape
import ranker



app=Flask(__name__)


@app.route('/')

def homepage():
    return render_template('home.html')



curr_product_list=0
@app.route('/products',methods=["POST"])


def get_product_list():
    query=str(request.form['query'])
    product_list=scrape.get_product_details(query)
    global curr_product_list
    curr_product_list=product_list
        

    return render_template('products.html',product_list=product_list)


curr_df=0
@app.route('/reviews/<int:num>')

def show_reviews(num):
    
    single_product_details=curr_product_list[num]
    reviews_details=scrape.get_reviews(single_product_details)

    
    print(len(reviews_details['review_list']))
    print(reviews_details['review_list'][-5:])
    df=ranker.create_dataframe(reviews_details['review_list'])
    
    global curr_df
    curr_df=df
    review_sentiment=df[['body','sentiment']].values.tolist()    
  
    return render_template('reviews.html',product=single_product_details,review_sentiment=review_sentiment,criteria='default')


@app.route('/reviews/<int:num>/<criteria>')

def sort_df(num,criteria):
    
    df=curr_df.sort_values(by=criteria,ascending=False)
    single_product_details=curr_product_list[num]

    review_sentiment=df[['body','sentiment']].values.tolist()

    return render_template('reviews.html',product=single_product_details,review_sentiment=review_sentiment,criteria=criteria)



    
    




if __name__=="__main__":
    app.run(debug=True)



