import csv
import requests
from bs4 import BeautifulSoup

PRODUCT_URL = 'https://books.toscrape.com/catalogue/chronicles-vol-1_462/index.html'
CATEGORY_URL = 'https://books.toscrape.com/catalogue/category/books/music_14/index.html'
HOME_URL = 'https://books.toscrape.com/index.html'
CSV_HEADER = ['product_page_url','universal_product_code','title','price_including_tax','price_excluding_tax','number_available','product_description','category','review_rating','image_url']
HEADER = "SEP=,"

class Scraper():
    def __init__(self):
        
        return
    
    def get_product_data(self,url=PRODUCT_URL):
        
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
            
            header_nav = parsed_page.find('div',{'class':'container-fluid'}).find('div',{'class':'page_inner'}).find('ul',{'class':'breadcrumb'})
            category_tag = header_nav.find_all('li')
            category_pas = category_tag[2]
            category = category_pas.find('a')
            
            #category = table_list[1]
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
    def get_category_name(self,product_data):
        category_name = product_data[7]
        return category_name
    
    def create_csv(self,category_name):
        
        file_name = category_name + '.csv' 
        with open(file_name, "a",newline='') as file:
            writer = csv.writer(file)
            #writer.writerow(HEADER)
            writer.writerow(CSV_HEADER)

        return
    
    
    def export_product_data_csv(self,product_data,url):
        
        product_data = self.get_product_data(url)
        
        row = []
        for data in product_data :
            row.append(str(data))
        
        file_name = str(row[7]) + '.csv' 
        with open(file_name, "a",newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)
        
        return
    
    def next_button_exist(self,url=CATEGORY_URL):
        
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
        
    
    def get_books_url(self,url=CATEGORY_URL):

        page = requests.get(url)
                
        if page.status_code == 200:
            parsed_page = BeautifulSoup(page.content,'lxml')  
            
            section = parsed_page.find('div',{'class':'container-fluid'}).find('div',{'class':'page_inner'}).find('div',{'class':'col-sm-8'}).find('section')
                  
            books = section.find_all('h3')
            books_url = []
            for book in books :
                book_url = book.find('a')
                book_url = book_url['href']
                book_url = book_url.replace('../..','https://books.toscrape.com/catalogue')
                book_url = book_url.replace('../','')
                books_url.append(book_url)
            
            print(books_url)
        
            #if next_button_exist(url) is true :
            #   while next_button_exist(url) is true :
            #       for book in books :
            #           dynamic_link = create link
            #           product_data = get_product_data(dynamic_link)
            #           export_product_data_csv(product_data)
            #else : 
            #    for book in books :
            #           dynamic_link = create link
            #           product_data = get_product_data(dynamic_link)
            #           export_product_data_csv(product_data)
            
            
        
        return books_url
    
    def get_categories_urls(self,url=HOME_URL):
        
        
        page = requests.get(url)
        
        if page.status_code == 200:
            parsed_page = BeautifulSoup(page.content,'lxml')
            
        categories_urls = []    
        
        side_bar_list = parsed_page.find('div',{'class':'container-fluid'}).find('div',{'class':'page_inner'}).find('div',{'class':'row'}).find('ul',{'class':'nav'}).find('li').find_all('li')
        
        for item in side_bar_list :
            category_url = item.find('a')
            category_url = category_url['href']
            category_url = 'https://books.toscrape.com/' + category_url
            categories_urls.append(category_url)
        
        print(categories_urls)
        return categories_urls
    
    def get_category_data(self,url=CATEGORY_URL):
        
        if self.next_button_exist(url) is True :
            
            while self.next_button_exist(url) is True :
        
                book_url_list = self.get_books_url(url)
                i_book = 0
                book_url_list_len = len(book_url_list)
                pd_create = self.get_product_data(book_url_list[0])
                category_name = self.get_category_name(pd_create)
                self.create_csv(category_name)
                    
                while book_url_list_len > i_book :
                    book_url = book_url_list[i_book]
                    product_data = self.get_product_data(book_url)

                    self.export_product_data_csv(product_data,book_url)
                    i_book +=1
                    
                    
                #change url
            
                page = requests.get(url)
                
                if page.status_code == 200:
                    parsed_page = BeautifulSoup(page.content,'lxml')
                    
                    section = parsed_page.find('div',{'class':'container-fluid'}).find('div',{'class':'page_inner'}).find('div',{'class':'col-sm-8'}).find('section')
                    next_button = section.find('li',{'class':'next'}).find('a')
                    page = next_button['href']
                    url = url.replace('index.html',str(page))
                    
        elif self.next_button_exist(url) is False :
            book_url_list = self.get_books_url(url)
            i_book = 0
            book_url_list_len = len(book_url_list)
            pd_create = self.get_product_data(book_url_list[0])
            category_name = self.get_category_name(pd_create)
            self.create_csv(category_name)
                
            while book_url_list_len > i_book :
                book_url = book_url_list[i_book]
                product_data = self.get_product_data(book_url)

                self.export_product_data_csv(product_data,book_url)
                i_book +=1
 
        
        return

    def get_site_data(self,url=HOME_URL):
        
        categories_urls = self.get_categories_urls()
        i_cat = 0
        categories_urls_len = len(categories_urls)
        
        while categories_urls_len > i_cat :
            cat_url = categories_urls[i_cat]
            self.get_category_data(cat_url)
            
            i_cat += 1 
            


        return
    
    
    
oc_scraper = Scraper()    

#product_data = oc_scraper.get_product_data()
#category_name = oc_scraper.get_category_name(product_data)
#oc_scraper.create_csv(category_name)
#oc_scraper.export_product_data_csv(product_data)

#oc_scraper.next_button_exist()

#oc_scraper.get_books_url()

#oc_scraper.get_categories_urls()

#oc_scraper.get_category_data()

oc_scraper.get_site_data()