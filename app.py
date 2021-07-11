import pandas as pd
import numpy as np
from flask import Flask,request,render_template
import scrape
import ranker



app=Flask(__name__)


@app.route('/')

def homepage():
    return render_template('home.html')



curr_product_list=0
@app.route('/products',methods=["POST","GET"])

def get_product_list():
    if request.method=='POST':
        query=str(request.form['query'])
        product_list,err_msg=scrape.get_product_details(query)

        if err_msg!="":
            return "Oops Error : "+err_msg

        global curr_product_list
        curr_product_list=product_list
        print(curr_product_list[2])
        
    

    return render_template('products.html',product_list=curr_product_list)





curr_df=0
@app.route('/reviews/<int:num>')

def show_reviews(num):
    
    single_product_details=curr_product_list[num]
    reviews_details=scrape.get_reviews(single_product_details)

    df=ranker.create_dataframe(reviews_details['review_list'])
    
    global curr_df
    curr_df=df
    review_sentiment=df[['body','sentiment']].values.tolist()    
  
    return render_template('reviews.html',product=single_product_details,review_sentiment=review_sentiment,criteria='default',num=num)




@app.route('/reviews/<int:num>/<criteria>')

def sort_df(num,criteria):
    
    df=ranker.sort_according_to(curr_df,criteria)
    single_product_details=curr_product_list[num]

    review_sentiment=df

    return render_template('reviews.html',product=single_product_details,review_sentiment=review_sentiment,criteria=criteria,num=num)



    
    




if __name__=="__main__":
    app.run(debug=True)



