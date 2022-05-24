import csv
from ast import parse
from unicodedata import category
from numpy import product
import requests
from bs4 import BeautifulSoup

DEFAULT_URI = 'https://books.toscrape.com/catalogue/chronicles-vol-1_462/index.html'


class Scraper():
    def __init__(self):
        
        return
    
    def get_product_data(self,url=DEFAULT_URI):
        
        product_data = []
        
        page = requests.get(url)
        
        if page.status_code == 200:
            parsed_page = BeautifulSoup(page.content,'lxml')
            
            page_url = url
            product_data.append(page_url)
            
            table = parsed_page.find('table',{'class':'table'}).extract()
            table_list = table.find_all('td')
            
            upc = table_list[0]
            product_data.append(upc.text)
            
            title = parsed_page.title
            product_data.append(title.text)
            
            price_including_tax = table_list[2]
            product_data.append(price_including_tax.text)
            
            price_excluding_tax = table_list[3]
            product_data.append(price_excluding_tax.text)
            
            number_available = table_list[5]
            product_data.append(number_available.text)
            
            description_title = parsed_page.find('article',{'class':'product_page'}).find('div',{'class':'sub-header'})
            descrption = description_title.find_next_sibling('p')
            product_data.append(descrption.text)
            
            
            category = table_list[1]
            product_data.append(category.text)
            
            
            article_header = parsed_page.find('article',{'class':'product_page'}).find('div',{'class':'row'})
            review_rating_data = article_header.find('div',{'class':'product_main'}).find('p',{'class':'star-rating'}).extract()
            review_rating_data = review_rating_data['class']
            review_rating = review_rating_data[1]
            product_data.append(review_rating)

            
            
            img_url = parsed_page.find('article',{'class':'product_page'}).find('div',{'class':'row'}).find('div',{'class':'col-sm-6'}).find('img')
            img_url = img_url['src']
            img_url = img_url.replace('../../','https://books.toscrape.com/')
          
            
            product_data.append(img_url)
           
            #review_rating
            #image_url
            
        return product_data
    
    def export_product_data_csv(self,product_data):
        
        HEADER = ['product_page_url','universal_product_code','title','price_including_tax','price_excluding_tax','number_available','product_description','category','review_rating','image_url']
        
        product_data = self.get_product_data()
        
        row = []
        
        for data in product_data :
            data = data.replace('\n','')
            data = data.replace('   ','')
            row.append(str(data))
        
        with open("product.csv", "w") as file:
            writer = csv.writer(file)
            
            writer.writerow(HEADER)
            writer.writerow(row)
            
        #change delimiter
        
        reader = csv.reader(open("product.csv", "r"), delimiter=',')
        writer = csv.writer(open("output.csv", 'w'), delimiter='|')
        writer.writerows(reader)
            
         
        
        return
    
    def get_category_data(self,url):
        # count product, for each product get_product_data
        pass
    
    def export_category_data_csv(self,category_data):
        # get_category_data and write a csv with data
        pass
    
    def get_site_data(self,url):
        # for each category get get_category_data(self)
        pass
    
    
    
python = Scraper()    

pd = python.get_product_data()

python.export_product_data_csv(pd)