from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
from bs4 import BeautifulSoup

def get_html_of_elements_with_aria_label(query):
    # Replace 'path/to/chromedriver' with the path to your WebDriver executable
    
    try:
        # Open the search page
        driver.get(f'https://drankdirect.nl/zoeken?full-search={query}')
        time.sleep(2)

        show_all_on_page = Select(driver.find_element(By.CLASS_NAME, 'select_item_count'))
        show_all_on_page.select_by_visible_text("Alle")
        time.sleep(1)


        search = driver.find_elements(By.CLASS_NAME, 'product')

        henk_smit = []

        for item in search:
            soup = BeautifulSoup(item.get_attribute('outerHTML'), 'html.parser')
            product = soup.find_all('a')[-1].text.strip()
            price = soup.find('span', {'class' : 'price'}).text.strip().split()
            size = soup.find('span', {'class' : 'volume'}).text.strip().split()
            size = size[1]
            link_partial = soup.find_all('a')[-1].get('href')
            link = (f"https://drankdirect.nl/{link_partial}")
            image = soup.find('img').get('src')
            if soup.find('p', {'class':'niet-op-voorraad'}):
                instock = 'Not in stock'
            else:
                instock = 'In stock'

            henk_smit.append({'product': product, 'price': price[1], 'size': size, 'image': image, 'link': link,'instock' : instock })  


            print(henk_smit)
            print('')


    except Exception as e:
        print(f'Something went wrong with the Henk Smit search: {str(e)}')





        # search = driver.find_elements(By.CLASS_NAME,'product-tile__container')

        # for item in search:
        #     soup = BeautifulSoup(item.get_attribute('outerHTML'), 'html.parser')
        #     product = soup.find('h3',{'class':'product-tile__name'}).text.strip()
        #     price = soup.find('span',{'class':'product-tile__price__price'}).text.strip().split()

        #     attribute_div = soup.find('div',{'class':'product-tile__details__attributes'}).find_all('span')
        #     for span in attribute_div[0]:
        #         size = span.text.strip()
        #     for span in attribute_div[1]:
        #         abv = span.text.strip()


        #     print(f'Anker search for {query}')
        #     print(product)
        #     print(price[1])
        #     print(size)
        #     print(abv)
        #     print('')

    finally:
        # Close the browser window
        driver.quit()

# Example usage with the query "ocho"
get_html_of_elements_with_aria_label("ocho")

print("finished")