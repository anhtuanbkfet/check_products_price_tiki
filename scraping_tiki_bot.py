from time import sleep
import random
import xlwt

from web_driver import init_browser
from get_all_product_tiki import get_all_product_url


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

def get_product_id(url):
    pid = url.strip().split('?spid=')[-1]
    return int(pid)

def find_lowest_price_product(products):
    """
    find product have the lowest price
    """
    products = sorted(products, key=lambda d: d['seller_price']) 
    if len(products) == 1:
        p_min = products[0]
    else:
        p_min = products[1]
    return p_min

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
                pass

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

if __name__ == "__main__":

    browser = init_browser()
    item_list = get_all_product_url(browser, 'https://tiki.vn/cua-hang/thiet-bi-y-te-gia-dinh-hme')
    search_function(browser, item_list)
    browser.close()

    