import argparse

from web_driver import init_browser
from get_all_product_tiki import get_all_product_url
from scraping_tiki_bot import search_function



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default= None,
                    help='txt file store the products url')
    return parser.parse_args()

def do_work(args):
    browser = init_browser()

    if args.file is not None:
        with open(args.file, 'r') as rFile:
            item_list = rFile.readlines()
            rFile.close()
    else: 
        item_list = get_all_product_url(browser, 'https://tiki.vn/cua-hang/thiet-bi-y-te-gia-dinh-hme')
        with open('product_list.txt', 'w') as wFile:
            for item in item_list:
                wFile.write(item+'\n')
            wFile.close()
        search_function(browser, item_list)
    browser.close()


if __name__ == "__main__":
    args = parse_args()
    do_work(args)
    