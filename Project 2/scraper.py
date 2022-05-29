import csv
from ast import parse
from unicodedata import category
from numpy import product
import requests
from bs4 import BeautifulSoup

DEFAULT_URI = 'https://books.toscrape.com/catalogue/chronicles-vol-1_462/index.html'
DEFAULT_URI_CATEGORY = 'https://books.toscrape.com/catalogue/category/books/business_35/index.html'

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
            title = title.text
            
            title = title.strip()
           
            product_data.append(title)
            
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
        
        books_link = self.find_books_url()
        
        product_data = self.get_product_data(books_link)
        
        row = []
        
        writer = csv.writer(file)
        writer.writerow(HEADER)
        
        for data in product_data :
            row.append(str(data))
        
        file_name = str(row[7]) + '.csv' 
        with open(file_name, "a",newline='') as file:
            writer.writerow(row)
            
        
        return
    
    def next_button_exist(self,url=DEFAULT_URI_CATEGORY):
        
        page = requests.get(url)
        
        if page.status_code == 200:
            parsed_page = BeautifulSoup(page.content,'lxml')
            
            section = parsed_page.find('div',{'class':'container-fluid'}).find('div',{'class':'page_inner'}).find('div',{'class':'col-sm-8'}).find('section')
            next_button = section.find('li',{'class':'next'})
            if next_button is None :
                print('false')
                return False
            else : 
                print('True')
                return True
            
            
        return            
        
    def find_books_url(self,url=DEFAULT_URI_CATEGORY):
        
        books_url = []
        
        page = requests.get(url)
                
        if page.status_code == 200:
            parsed_page = BeautifulSoup(page.content,'lxml')  
            
            section = parsed_page.find('div',{'class':'container-fluid'}).find('div',{'class':'page_inner'}).find('div',{'class':'col-sm-8'}).find('section')
                  
            books = section.find_all('h3')
            
        for book in books :
            
            book_url = book.find('a')
            book_url = book_url['href']
            book_url = 'https://books.toscrape.com/' + book_url
            books_url.append(book_url)
            print(books_url)
        
        return books_url
    
    def get_category_data(self,url=DEFAULT_URI_CATEGORY):
        
        books = self.find_books_url()
        
        for book in books : 
            print('ciao')
            print(book)
            product_data = self.get_product_data(book)
            self.export_product_data_csv(product_data) 
                
        return                
        
        
        
        
                          
                
    

    def get_site_data(self,url):
        # for category in categories :
        #   get_category_data
        pass
    
    def download_images(self,url):
        pass
    
python = Scraper()    

pd = python.get_product_data()

python.export_product_data_csv(pd)

url = 'https://books.toscrape.com/catalogue/category/books/music_14/index.html'

python.get_category_data(url)