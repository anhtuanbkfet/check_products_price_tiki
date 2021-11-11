from web_driver import init_browser
from get_all_product_tiki import get_all_product_url
from scraping_tiki_bot import search_function

if __name__ == "__main__":

    browser = init_browser()
    item_list = get_all_product_url(browser, 'https://tiki.vn/cua-hang/thiet-bi-y-te-gia-dinh-hme')
    search_function(browser, item_list)
    browser.close()