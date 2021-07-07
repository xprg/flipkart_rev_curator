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
    print(len(links),len(imgs),len(names))
    product_details=[]
    for i in range(5):
        temp={}
        temp['link']=links[i]
        temp['img']=imgs[i]
        temp['name']=names[i]
        product_details.append(temp)
    

    
    return product_details                                                        # list of product details


def get_reviews(single_product_details):                      #pass product detail dict
    rlist=[]
    for i in range(1,5):
        link='https://www.flipkart.com'+single_product_details['link'].split('FLIPKART')[0]+"FLIPKART&page="+str(i)
        time.sleep(.250)
        print(link)
        result=requests.get(link)
        
        review_page=soup(result.content,'html.parser')                                       #returns a dic containing details along with reviews
        

        review_list=review_page.find_all('div',attrs={'class':"t-ZTKy"})
        
        
        for r in review_list:
            rlist.append(r.find('div').find('div').text)

        
    avg_rating=review_page.find('div',{'class':"_3LWZlK"}).text

    single_product_details['avg_rating']=avg_rating
    single_product_details['rlist']=rlist
        
                                                                     
    return single_product_details



    


    











   
    

    

    













    

    
    
    




