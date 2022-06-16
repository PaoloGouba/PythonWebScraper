import scraper
import requests
import os

class ScaperImage():
    def __init__(self):
        
        return
    
    def save_image(self,product_data,url):
        

        
        
        product_data = scraper.oc_scraper.get_product_data(url)
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
        
        img_data = requests.get(image_url).content
        
        with open('C:/Users/PaoloGouba/OneDrive - BeezUP/Documents/School/OC-DA-Python/Project 2/Images/' + image_name, 'wb') as handler:
            handler.write(img_data)
        return 
      
    def save_all_images(self,url):
        
        endpoint = 'https://books.toscrape.com/catalogue/'
        
        #make dir images
        directory = "Images"
        parent_dir = "C:/Users/PaoloGouba/OneDrive - BeezUP/Documents/School/OC-DA-Python/Project 2/"
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)
        print("Directory '% s' created" % directory)
        
        
        url = scraper.HOME_URL
        
        
        if scraper.oc_scraper.next_button_exist(url) is True :
            
            while scraper.oc_scraper.next_button_exist(url) is True :
        
                #url = scraper.HOME_URL
                books_urls = scraper.oc_scraper.get_books_url(url)
                
                for book_url in books_urls : 
                    if 'catalogue' in book_url :
                        book_url = 'https://books.toscrape.com/' + book_url
                    else : book_url = 'https://books.toscrape.com/catalogue/' + book_url    
                    product_data = scraper.oc_scraper.get_product_data(book_url)
                    self.save_image(product_data,book_url)
                    
                url = scraper.oc_scraper.change_url(endpoint,url)  
        else :
            books_urls = scraper.oc_scraper.get_books_url(url)
            for book_url in books_urls : 
                if 'catalogue' in book_url :
                    book_url = 'https://books.toscrape.com/' + book_url
                else : book_url = 'https://books.toscrape.com/catalogue' + book_url    
                product_data = scraper.oc_scraper.get_product_data(book_url)
                self.save_image(product_data,book_url)
        
                      
        
        return print('ok!') 
      
      
new_scrapper = ScaperImage()

new_scrapper.save_all_images('https://books.toscrape.com/catalogue/page-1.html')      