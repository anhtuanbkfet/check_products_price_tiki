import sys
import argparse

from web_driver import init_browser
from get_all_product_tiki import get_all_product_url
from scraping_tiki_bot import search_function



# def parse_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--file', default= None,
#                     help='txt file store the products url')
#     return parser.parse_args()

def do_work(args):
    browser = init_browser()

    if len(args) == 1:
        item_list = get_all_product_url(browser, 'https://tiki.vn/cua-hang/thiet-bi-y-te-gia-dinh-hme')
        with open('product_list.txt', 'w') as wFile:
            for item in item_list:
                wFile.write(item+'\n')
            wFile.close()
    else:
        with open(args[-1], 'r') as rFile:
            item_list = rFile.readlines()
            rFile.close()

    search_function(browser, item_list)
    browser.close()


if __name__ == "__main__":
    args = sys.argv
    do_work(args)
    