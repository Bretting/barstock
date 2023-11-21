from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import os
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')


def search_products(query):
    driver = webdriver.Chrome(options=options)

#RIGHT SPIRITS
    try:
        # Open the search page
        driver.get(f"https://rightspirits.com/search?q={query}")
        print(f'searching: {query} at Right Spirits')

        # Wait for the page to load (adjust the timeout as needed)
        time.sleep(2)

        # Find all elements with the specified aria-label
        product_elements = driver.find_elements(By.CSS_SELECTOR, '[aria-label="Product pagina"]')

        # set up array
        right_spirits = []

        # Search the HTML code of each element
        for element in product_elements:
            outer = element.get_attribute("outerHTML")
            soup = BeautifulSoup(outer, 'html.parser')
            product = soup.find('div', {'class': 'text-primary'}).text.strip()
            price = soup.find('span', {'dusk': 'price'}).text.strip().split()
            size = soup.find('span', {'dusk': 'contents'}).text.strip().split()
            abv = soup.find('span', {'dusk': 'alcohol_percentage'}).text.strip().split()
            link = soup.find('a').get('href')
            image_link = soup.find('img').get('src')
            image = f"https://www.rightspirits.com{image_link}"

            right_spirits.append(
                {'product': product, 'price': price[1], 'size': size[1], 'abv': abv[1], 'image': image, 'link': link, })
            #  'instock':instock}

        for item in right_spirits:
            try:
                driver.get(item['link'])
                try:
                    driver.find_element(By.CSS_SELECTOR,
                                        'meta[itemprop="availability"][content="https://schema.org/InStock"]')
                    instock = 'In stock'
                except:
                    instock = 'Not in stock'

                item.update({'instock': instock})
            except Exception as e:
                print(f'Something went wrong with the Right Spirits stock search: {str(e)}')

    except Exception as e:
        print(f'Something went wrong with the Right Spirits search: {str(e)}')

    finally:
        print('Right Spirits search & loop done.')

#ANKER
    try:
        # Login
        print(f'searching: {query} at Anker')
        driver.get("https://www.ankeramsterdamspirits.nl/login")
        anker_login = driver.find_element(By.ID, 'login-email')
        anker_password = driver.find_element(By.ID, 'login-password')

        anker_login.send_keys(os.environ.get('ANKER_LOGIN'))
        anker_password.send_keys(os.environ.get('ANKER_PW'))
        anker_password.send_keys(Keys.RETURN)
        time.sleep(2)

        # Search
        driver.get(f"https://www.ankeramsterdamspirits.nl/zoek?query={query}")
        time.sleep(2)
        search = driver.find_elements(By.CLASS_NAME, 'product-tile__container')

        anker = []

        for item in search:
            soup = BeautifulSoup(item.get_attribute('outerHTML'), 'html.parser')
            product = soup.find('h3', {'class': 'product-tile__name'}).text.strip()
            price = soup.find('div', {'class': 'product-tile__price__excise'}).text.strip().split()
            link_partial = soup.find('a').get('href')
            link = f"https://www.ankeramsterdamspirits.nl{link_partial}"

            attribute_div = soup.find('div', {'class': 'product-tile__details__attributes'}).find_all('span')
            for span in attribute_div[0]:
                size = span.text.strip()
            for span in attribute_div[1]:
                abv = span.text.strip()

            if soup.find('span', {'class': 'fragment--label-badge'}):
                instock = 'Not in stock'
            else:
                instock = 'In stock'

            anker.append(
                {'product': product, 'price': price[1], 'size': size, 'abv': abv, 'instock': instock, 'link': link})
    except Exception as e:
        print(f'Something went wrong with the Anker search: {str(e)}')

    finally:
        print('Anker search & loop done.')


#HENK SMIT
    try:
        print(f'searching: {query} at Henk Smit')
        # Open the search page
        driver.get(f'https://drankdirect.nl/zoeken?full-search={query}')
        time.sleep(2)

        #Make page show all items
        show_all_on_page = Select(driver.find_element(By.CLASS_NAME, 'select_item_count'))
        show_all_on_page.select_by_visible_text("Alle")
        time.sleep(1)

        #Search
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


    except Exception as e:
        print(f'Something went wrong with the Henk Smit search: {str(e)}')
    finally:
        print('Henk Smit search & loop done.')



    if not right_spirits:
        right_spirits = 'Not found'
    if not anker:
        anker = 'Not found'
    if not henk_smit:
        henk_smit = 'Not found'

    spirits_search = [right_spirits, anker, henk_smit]

    return spirits_search
