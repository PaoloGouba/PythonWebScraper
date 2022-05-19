from ast import parse
from numpy import product
import requests
from bs4 import BeautifulSoup


class Scraper():
    def __init__(self):
        
        return
    
    def get_product_data(self):
        
        product_data = []
        
        page = requests.get("https://books.toscrape.com/catalogue/chronicles-vol-1_462/index.html")
        
        if page.status_code == 200:
            pased_page = BeautifulSoup(page.content,'lxml')
            
            title = pased_page.title.extract()
 
            table = pased_page.find('table',{'class':'table-striped'}).extract()
            upc = table.td.extract()
            
            
            print(title)
            print(upc)
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