# Web Scrapper


## Installation:

### Clone repository 
git clone https://github.com/PaoloGouba/OC-DA-Python.git

### Install and activate virtual environment 
#### Installation
Windows :
python -m venv venv

Mac :
pvirtualenv env

#### Activation
Windows : 
venv/Scripts/activate

Mac :
env/bin/activate


### Install the dependencies 
with the command "pip install -r requirements.txt"

## Execution of the script

- Go to folder OC-DA-Python/project_2/src in your terminal
- Type python main.py and hit enter to run the program

The different data, reported in the script characteristics will be recovered, cleaned and sorted



### Script features : 

- Get the following data from the page https://books.toscrape.com/catalogue/chronicles-vol-1_462/index.html : 
    - product_page_url
    - universal_ product_code (upc)
    - title
    - price_including_tax
    - price_excluding_tax
    - number_available
    - product_description
    - category
    - review_rating
    - image_url
- Create a CSV file using previews data has header
- Get all 'Business' books data and store previews informations in a new CSV file (app have to change page if necessary)
- Get all informations from the website http://books.toscrape.com/
- Store informations in differents CSV for categories 
    - the name of the file have to contain the category name
- get all images


