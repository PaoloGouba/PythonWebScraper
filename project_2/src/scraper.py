import requests
from bs4 import BeautifulSoup
import csv
import unidecode
import os


PRODUCT_URL = 'https://books.toscrape.com/catalogue/chronicles-vol-1_462/index.html'
CATEGORY_URL = 'https://books.toscrape.com/catalogue/category/books/business_35/index.html'
HOME_URL = 'https://books.toscrape.com/index.html'
CSV_HEADER = ['product_page_url','universal_product_code','title','price_including_tax','price_excluding_tax','number_available','product_description','category','review_rating','image_url']
HEADER = "SEP=,"
DEFAULT_IMAGES_FOLDER_PATH = 'C:/Users/PaoloGouba/OneDrive - BeezUP/Documents/School/OC-DA-Python/project_2/Images/'


## -- Scraper

class Scraper():
    def __init__(self):
        
        return
    
    ## -- Tools --
    
    def clean_title(title):
        
        title = title.replace(' ','_')
        title = title.replace('|','_')
        title = title.replace(',','_')
        title = title.replace(':','_')
        title = title.replace('&','_and_')
        title = title.replace('...','_')
        title = title.replace('#','Number_')
        title = title.replace('(','')
        title = title.replace(')','')
        title = title.replace('*','xxx')
        title = title.replace('?','')
        title = title.replace('___','_')
        title = title.replace('_-_','_')
        title = title.replace('Vol.','Volume_')
        title = title.replace('/','_')
        title = title.replace('\\','_')
        title = title.replace('\'','-')
        title = title.replace('\"','')
        
        return title
    
    def create_folder(self):
        #make dir images
        directory = "Images"
        parent_dir = "C:/Users/PaoloGouba/OneDrive - BeezUP/Documents/School/OC-DA-Python/project_2/"
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)
        
        return print("Directory '% s' created" % directory)

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
    
    def change_url(self,endpoint,url=HOME_URL):
        
        
        page = requests.get(url)
        
        if page.status_code == 200:
            
            parsed_page = BeautifulSoup(page.content,'lxml')
            section = parsed_page.find('div',{'class':'container-fluid'}).find('div',{'class':'page_inner'}).find('div',{'class':'col-sm-8'}).find('section')
            next_button = section.find('li',{'class':'next'}).find('a')
            
            page_url = next_button['href']
            
            #endpoint = url.replace('index.html','')
            
            if 'index.html' in url :
                url = url.replace('index.html',str(page_url))   
                print('ciao')  
            else : 
                print('this is not the index page') 
                url = url.replace('index.html','')
                url = endpoint + page_url  
               


        
        return url
    
    def create_csv(self,category_name):
        
        file_name = category_name + '.csv' 
        with open(file_name, "a",newline='') as file:
            writer = csv.writer(file)
            #writer.writerow(HEADER)
            writer.writerow(CSV_HEADER)

        return
   
   
    ## -- Get Data --

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
            
            #title = self.clean_title(title)
           
            product_data.append(title)
            
            price_including_tax = table_list[2]
            product_data.append(price_including_tax.text)
            
            price_excluding_tax = table_list[3]
            product_data.append(price_excluding_tax.text)
            
            number_available = table_list[5]
            product_data.append(number_available.text)
            
            description_title = parsed_page.find('article',{'class':'product_page'}).find('div',{'class':'sub-header'})
            
            descrption = description_title.find_next_sibling('p')
            #if descrption is None : à tester avant 
            if descrption is None :
                product_data.append('Not available')  
            else : product_data.append(descrption.text)
            
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
    

## -- Save and Export Data --

    def export_product_data_csv(self,product_data,url=PRODUCT_URL):
        
        product_data = self.get_product_data(url)
        
        row = []
        for data in product_data :
            data = unidecode.unidecode(data)
            row.append(str(data))
        
        file_name = str(row[7]) + '.csv' 
        with open(file_name, "a",newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)
        
        return
    
    def save_image(self,product_data,url,folder_path ='C:/Users/PaoloGouba/OneDrive - BeezUP/Documents/School/OC-DA-Python/project_2/Images/'):
        
        product_data = self.get_product_data(url)
        image_url = product_data[9]
        image_name = product_data[2] + '.jpg'

        image_name = image_name.replace(' ','_')
        image_name = image_name.replace('|','_')
        image_name = image_name.replace(',','_')
        image_name = image_name.replace(':','_')
        image_name = image_name.replace('&','_and_')
        image_name = image_name.replace('...','_')
        image_name = image_name.replace('#','Number_')
        image_name = image_name.replace('(','')
        image_name = image_name.replace(')','')
        image_name = image_name.replace('*','xxx')
        image_name = image_name.replace('?','')
        image_name = image_name.replace('___','_')
        image_name = image_name.replace('_-_','_')
        image_name = image_name.replace('Vol.','Volume_')
        image_name = image_name.replace('/','_')
        image_name = image_name.replace('\\','_')
        image_name = image_name.replace('\'','-')
        image_name = image_name.replace('\"','')
        
        img_data = requests.get(image_url).content
        
        with open(folder_path + image_name, 'wb') as handler:
            handler.write(img_data)
        return 
      
    def store_images(self,url=HOME_URL):
        
        endpoint = 'https://books.toscrape.com/catalogue/'
        
        url = HOME_URL
        
        
        if self.next_button_exist(url) is True :
            
            while self.next_button_exist(url) is True :
        
                #url = scraper.HOME_URL
                books_urls = self.get_books_url(url)
                
                for book_url in books_urls : 
                    if 'catalogue' in book_url :
                        book_url = 'https://books.toscrape.com/' + book_url
                    else : book_url = 'https://books.toscrape.com/catalogue/' + book_url    
                    product_data = self.get_product_data(book_url)
                    self.save_image(product_data,book_url,DEFAULT_IMAGES_FOLDER_PATH)
                    
                url = self.change_url(endpoint,url)  
        else :
            books_urls = self.get_books_url(url)
            for book_url in books_urls : 
                if 'catalogue' in book_url :
                    book_url = 'https://books.toscrape.com/' + book_url
                else : book_url = 'https://books.toscrape.com/catalogue' + book_url    
                product_data = self.get_product_data(book_url)
                self.save_image(product_data,book_url,DEFAULT_IMAGES_FOLDER_PATH)
        
        return ('Images are created !') 
    
    def get_category_data(self,url=CATEGORY_URL):
        
        if 'index.html' in url :
            endpoint = url.replace('index.html','')
        elif 'page-2.html' in url :
            endpoint = url.replace('page-2.html','')  
        elif 'page-3.html' in url :
            endpoint = url.replace('page-3.html','') 
        elif 'page-4.html' in url :
            endpoint = url.replace('page-4.html','')                           
        elif 'page-5.html' in url :
            endpoint = url.replace('page-5.html','') 
        elif 'page-6.html' in url :
            endpoint = url.replace('page-6.html','') 
        elif 'page-7.html' in url :
            endpoint = url.replace('page-7.html','') 
        elif 'page-8.html' in url :
            endpoint = url.replace('page-8.html','') 
        elif 'page-9.html' in url :
            endpoint = url.replace('page-9.html','') 
        elif 'page-10.html' in url :
            endpoint = url.replace('page-10.html','')                                                             
            
            
            
                    
        if self.next_button_exist(url) is True :
            
            while self.next_button_exist(url) is True :
        
                book_url_list = self.get_books_url(url)
                i_book = 0
                book_url_list_len = len(book_url_list)
                category_name = self.get_category_name(self.get_product_data(book_url_list[0]))
                self.create_csv(category_name)
                    
                while book_url_list_len > i_book :
                    book_url = book_url_list[i_book]
                    product_data = self.get_product_data(book_url)
                    self.export_product_data_csv(product_data,book_url)
                    self.save_image(product_data,book_url)
                    i_book +=1
                    
                    
                #change url
            
                url = self.change_url(endpoint,url)
                    
        if self.next_button_exist(url) is False :
            book_url_list = self.get_books_url(url)
            i_book = 0
            book_url_list_len = len(book_url_list)
            category_name = self.get_category_name(self.get_product_data(book_url_list[0]))
            self.create_csv(category_name)
                
            while book_url_list_len > i_book :
                book_url = book_url_list[i_book]
                product_data = self.get_product_data(book_url)

                self.export_product_data_csv(product_data,book_url)
                self.save_image(product_data,book_url)
                i_book +=1
 
        
 
        
        return
    
    def get_site_data(self):
        
        categories_urls = self.get_categories_urls()
        i_cat = 0
        categories_urls_len = len(categories_urls)
        
        while categories_urls_len > i_cat :
            cat_url = categories_urls[i_cat]
            self.get_category_data(cat_url)
            
            i_cat += 1 
            


        return
    



## -- Main program

def start_scraper():
    
    oc_scraper = Scraper()  

    # 1) Get product data and store in csv   

    product_data = oc_scraper.get_product_data()
    category_name = oc_scraper.get_category_name(product_data)
    oc_scraper.create_csv(category_name)
    oc_scraper.export_product_data_csv(product_data)
    oc_scraper.create_folder()
    oc_scraper.save_image(product_data,PRODUCT_URL)

    # 2) get business book informations and store in a csv
    
    oc_scraper.get_category_data()

    # 3) Get all site data and store in differents CSV files
    oc_scraper.get_site_data()

    # now I store images when I get books, so I've commented the function store_images
    # 4) store all images in a folder
    #oc_scraper.store_images('https://books.toscrape.com/catalogue/page-1.html')    
    
    return
    


start_scraper()