from time import sleep
import random
from web_driver import init_browser


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_product_id(url):
    pid = url.strip().split('?spid=')[-1]
    return int(pid)

def get_all_product_url(browser, shop_url, delay_time = 3):
    
    browser.get(shop_url+'?t=product')
    product_urls = []

    sleep(6)

    # auto click to expand all products:
    counter = 1
    while True:    
        try:
            element = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@class="ViewMoreBtn__Wrapper-sc-qs9ydg-0 cFmjcu"]')))
            element.click()
            print('{}. Auto clicked to \'ViewMore\' button to view more items....'.format(counter))
            counter+=1
            sleep(delay_time)
        except:
            break
   
    # find all items data
    print('Done, now get all items url....')
    counter = 0 
    try:
        products = browser.find_elements_by_xpath('//*[@class="Product__Wrapper-sc-n99tp2-0 gKQGzQ"]')
        # products = browser.find_elements_by_class_name('Product__Wrapper-sc-n99tp2-0')
        print ('Find out {} products, now duplicate checking...'.format(len(products)))
        for product in products:
            url = product.get_attribute("href").strip()
            if url in product_urls:
                print('url is duplicated:\n{}'.format(url))
                continue
            product_urls.append(url)     
     
            counter+=1
            print('[{}] url found: {}'.format(counter, url))
    except:
        pass
    print('Cralwing products completed, total found: {}'.format(counter))
    return product_urls

if __name__ == "__main__":
    
    shop_url = 'https://tiki.vn/cua-hang/thiet-bi-y-te-gia-dinh-hme'

    browser = init_browser()
    product_urls = get_all_product_url(browser, shop_url)
    browser.close()
