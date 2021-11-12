from selenium import webdriver
import os.path
import urllib.request
import urllib.request
from tqdm import tqdm


chrome_excute_file = 'chromedriver.exe'
url_download = "https://github.com/anhtuanbkfet/check_products_price_tiki/raw/main/chromedriver.exe"


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
    # options.add_argument('--disable-logging')

    browser = webdriver.Chrome(executable_path=chrome_excute_file, options=options)
    return browser