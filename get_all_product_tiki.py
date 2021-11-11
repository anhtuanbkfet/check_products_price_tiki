from time import sleep
from web_driver import init_browser


def get_all_product_url(browser, shop_url):
    
    browser.get(shop_url+'?t=product')
    product_urls = []

    sleep(4)
    # auto click to expand all products:
    while True:
        try:
            browser.find_elements_by_class_name('ViewMoreBtn__Wrapper-sc-qs9ydg-0')[0].click()
        except:
            break
        print('Auto clicked to \'Expand\' button to view more items....')
        sleep(1)

    # find data
    print('Done, now get all items url....')
    counter = 0 
    try:
        products = browser.find_elements_by_class_name('Product__Wrapper-sc-n99tp2-0')
        for product in products:
            url = product.get_attribute("href")
            url = url.replace(' ', '').replace('\t', '')
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

    # browser.close()
