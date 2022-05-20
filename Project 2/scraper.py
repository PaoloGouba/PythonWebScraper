from ast import parse
from numpy import product
import requests
from bs4 import BeautifulSoup


class Scraper():
    def __init__(self):
        
        return
    
    def get_product_data(self):
        
        product_data = []
        
        DEFAULT_URI = 'https://books.toscrape.com/catalogue/chronicles-vol-1_462/index.html'
        
        page = requests.get(DEFAULT_URI)
        
        if page.status_code == 200:
            parsed_page = BeautifulSoup(page.content,'lxml')
            
            title = parsed_page.title.extract()
            title_text = title.get_text()
            
            product_data.append(title_text)
 
            table = parsed_page.find('table',{'class':'table-striped'}).extract()
            
            upc = table.td.extract().get_text()
            product_data.append(upc)
            
            print(title_text)
            print(upc)
            print(product_data)
        return
    
    def export_product_data_csv(self,product_data):
        # get_product_data and write csv with data
        pass
    
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

python.get_product_data()