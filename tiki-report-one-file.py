import os
import sys
import urllib.request
from tqdm import tqdm
from time import sleep
import random
import xlwt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chrome_excute_file = '.\chromedriver.exe'
url_download = "https://github.com/anhtuanbkfet/check_products_price_tiki/raw/main/chromedriver.exe"
our_name = 'Thiết bị y tế Gia Đình HME'

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)

def init_browser():
    # check chrome is existed:
    if not os.path.isfile(chrome_excute_file):
        print('Chrome excuter driver file is not found, now download from: {}'.format(url_download))
        download_url(url_download, chrome_excute_file)

    options = webdriver.ChromeOptions()
    # options.add_argument("--start-maximized")
    options.add_argument("--headless")
    options.add_argument('--disable-logging')

    browser = webdriver.Chrome(executable_path=chrome_excute_file, options=options)
    return browser


"""
CRALW ITEMS URL FUNCTIONS

"""

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
        products = browser.find_elements_by_xpath('//*[@class="Product__Wrapper-sc-n99tp2-0 Product___StyledWrapper-sc-n99tp2-1 gMgInl"]')
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


"""
CRALW ITEMS PRICE FUNCTIONS

"""

def save_to_xls_file(products):
     # save to excel sheet:
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Tiki-Report')

    ws.write(0,0,"Product name")    
    ws.write(0,1,"My price")
    ws.write(0,2,"Other-seller price")
    ws.write(0,3,"Other-seller name")
    ws.write(0,4,"My Url")
    ws.write(0,5,"Other-seller Url")

    for i, product in enumerate(products):
        
        ws.write(i+1, 0, product['product_name'])
        ws.write(i+1, 1, product['our_price'])
        ws.write(i+1, 2, product['seller_price'])
        ws.write(i+1, 3, product['seller_name'])
        ws.write(i+1, 4, product['our_url'])
        ws.write(i+1, 5, product['seller_url'])

    #close excel file:
    wb.save('tiki_report.xls')

def find_lowest_price_product(products):
    """
    find product have the lowest price
    """
    products = sorted(products, key=lambda d: d['seller_price'])    
    for product in products:
        if product['seller_name'] != our_name:
            return product
    return products[0]

def tiki_search_sililiar_products(browser, my_url):
    
    p_string = my_url.split('tiki.vn/')[-1].split('.html')[0]
    p_id = my_url.split('?spid=')[-1]
    url = 'https://tiki.vn/so-sanh-gia/{}?spid={}'.format(p_string, p_id)

    browser.get(url)

    # delay web
    # sleep(random.randint(4, 8))

    products = []

    # find data
    try:
        m_product = browser.find_elements_by_class_name('styles__Wrapper-sc-1ypfr1f-0')[0]
        p_name = m_product.find_element_by_class_name('product-title')
        p_name = p_name.text
        p_name = p_name.split('So sánh giá ')[-1]

        p_price = m_product.find_element_by_class_name('final-price')
        p_price = p_price.text.replace("₫", "")
        p_price = p_price.replace(".", "").replace(' ', '')
        p_price = int(p_price)


        print('Searching similiar products of: \n{}\nPrice: {}₫'.format(p_name, p_price))
        # book_list = browser.find_elements_by_class_name("product-item")
        book_list = browser.find_elements_by_class_name('styles__BaseRow-sc-15nb5z1-1')

        count = 1
        for book in book_list:
            try:
                # ----------------
                seller_name = book.find_element_by_class_name("styles__SellerName-sc-18tylfc-3")
                seller_name = seller_name.text
                # ----------------
                price = book.find_element_by_class_name("styles__PriceValue-sc-1pqr4qd-1")
                price = price.text.replace("₫", "")
                price = price.replace(".", "").replace(' ', '')
                price = int(price)

                # -----------------
                url = book.find_element_by_class_name("styles__StyledButtonLink-sc-1agqv8o-0")
                url = url.get_attribute("href")
                url = url.replace(' ', '').replace('\t', '')
                # ----------------
                print('{}. A similiar products found: \n-Seller: {}\n-Price: {} ₫ \n-Url: {}'.format(count, seller_name, price, url))

                product = {"product_name": p_name, "our_price": p_price, "seller_price": price, "seller_name": seller_name, "our_url": my_url, "seller_url": url}
                products.append(product)

                count+=1
                # if count > 2:
                #     break
            except:
                continue

    except:
        print('Can not find the element data of our product, process have been denied!')
   
    return products

def search_function(browser, url_list):
    total = len(url_list)
    print('Starting to scrap product data, total our products: {}'.format(total))

    results = []
    for i, url in enumerate(url_list):
        print('\n{}/{}: scraping product url: {}'.format(i, total, url))
        products = tiki_search_sililiar_products(browser, url.strip())
        if len(products) is not 0:
            lowest_price_product = find_lowest_price_product(products)
            results.append(lowest_price_product)

    #In the end, sve to xls file:
    print('Scraping process have been completed, save the result to xls file...')

    save_to_xls_file(results)

    print('All done!')


"""
MAIN FUNCTION

"""
def do_work(args):
    browser = init_browser()
    if len(args) == 1:
        url_file = None
        delay = 3
    else:
        try:
            delay = int(args[1])
            url_file = None
        except:
            url_file = args[1]
            delay = 3
    if url_file is None:
        item_list = get_all_product_url(browser, 'https://tiki.vn/cua-hang/thiet-bi-y-te-gia-dinh-hme', delay)
        with open('product_list.txt', 'w') as wFile:
            for item in item_list:
                wFile.write(item+'\n')
            wFile.close()
    else:
        print('read urls from: {}'.format(url_file))
        with open(url_file, 'r') as rFile:
            item_list = rFile.readlines()
            rFile.close()

    search_function(browser, item_list)
    browser.close()


if __name__ == "__main__":
    args = sys.argv
    do_work(args)

    # url = 'https://tiki.vn/may-do-huyet-ap-dien-tu-bap-tay-sinoheart-ba-801-duc-p41523006.html?spid=111708894'
    # browser = init_browser()
    # products = tiki_search_sililiar_products(browser, url.strip())
    # if len(products) is not 0:
    #     print(products)
    #     lowest_price_product = find_lowest_price_product(products)
    #     print(lowest_price_product)
