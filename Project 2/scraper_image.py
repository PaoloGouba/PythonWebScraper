import scraper
import requests

class ScaperImage():
    def __init__(self):
        
        return
    
    def save_image(self,product_data):
        
        product_data = scraper.get_product_data()
        image_url = product_data[9]
        image_name = product_data[2] + '.jpg'
        image_name = image_name.replace(' ','_')
        image_name = image_name.replace('|','')
        image_name = image_name.replace(',','_')
        #image_name = image_name.replace('.','')
        
        img_data = requests.get(image_url).content
        
        with open(image_name, 'wb') as handler:
            handler.write(img_data)
        return 
      
    def save_all_images(self,url):
        pass 
      
      
new_scrapper = ScaperImage()

new_scrapper.save_image(scraper.product_data)      