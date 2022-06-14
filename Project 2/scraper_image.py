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
        image_name = image_name.replace('|','')
        image_name = image_name.replace(',','_')
        #image_name = image_name.replace('.','')
        
        img_data = requests.get(image_url).content
        
        with open('C:/Users/PaoloGouba/OneDrive - BeezUP/Documents/School/OC-DA-Python/Project 2/Images/' + image_name, 'wb') as handler:
            handler.write(img_data)
        return 
      
    def save_all_images(self,url):
        
        #make dir images
        directory = "Images"
        parent_dir = "C:/Users/PaoloGouba/OneDrive - BeezUP/Documents/School/OC-DA-Python/Project 2/"
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)
        print("Directory '% s' created" % directory)
        
        url = scraper.HOME_URL
        books_urls = scraper.oc_scraper.get_books_url(url)
        
        for book_url in books_urls : 
            book_url = 'https://books.toscrape.com/' + book_url
            product_data = scraper.oc_scraper.get_product_data(book_url)
            self.save_image(product_data,book_url)
        
        return print('ok!') 
      
      
new_scrapper = ScaperImage()

new_scrapper.save_all_images(scraper.HOME_URL)      