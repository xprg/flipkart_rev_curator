from bs4 import BeautifulSoup as soup
import re
import requests
import csv
import pandas as pd
import time


def flipkart(search_query):
    url="https://www.flipkart.com/search?q="+search_query+"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    print(url)
    page=requests.get(url)
    if page.status_code==200:
        return page                                                       #flipkart search //no need to call this
    else:
        return "error"


def get_product_details(search_query):
    search_query='%20'.join(search_query.split())
    response=flipkart(search_query)
    page=soup(response.content,'html.parser')  
                                                                                 #get product links and details based on query//call this
    links=[]
    for a in page.find_all('a',{'class':"_1fQZEK"},limit=5):
        links.append(a['href'])
    
    imgs=[]
    for a in page.find_all('img',{'class':"_396cs4 _3exPp9"},limit=5):                        # get product image
        imgs.append(a['src'])
    
    names=[]
    for a in page.find_all('div',{'class':"_4rR01T"},limit=5):                                  # get product name
        names.append(a.text)
    
    rating=[]
    for a in page.find_all('div',{'class':'_3LWZlK'},limit=5):
        rating.append(a.text)

    print(len(links),len(imgs),len(names))
    product_details=[]
    for i in range(5):
        temp={}
        temp['link']=links[i]
        temp['img']=imgs[i]
        temp['name']=names[i]
        temp['rating']=rating[i]
        product_details.append(temp)
    

    
    return product_details                                                        # list of product details


def get_reviews(single_product_details):                      #pass product detail dict
    review_list=[]
    for i in range(1,5):
        link='https://www.flipkart.com'+single_product_details['link'].split('/p/')[0]+'/product-reviews/'+single_product_details['link'].split('/p/')[1].split('FLIPKART')[0]+"FLIPKART&page="+str(i)
        time.sleep(.200)
        print(link)
        result=requests.get(link)
        
        review_page=soup(result.content,'html.parser')                                       #returns a dic containing details along with reviews
        

        r_list=review_page.find_all('div',attrs={'class':"t-ZTKy"})
        
        
        for r in r_list:
            review_list.append(r.find('div').find('div').text)

        
    

    single_product_details['review_list']=review_list
        
                                                                     
    return single_product_details



    


    











   
    

    

    













    

    
    
    




