# check_products_price_tiki
check and report product on tiki.vn that have lower price than your shop

# Process:
1. Get all your product items by cralw data from your home page -> show all products.
2. Compare these products with other seller, then add lowest price seller to list.
3. Save this list to xls file.

# How to use:
1. Install python 3.6.8 (with pip)
2. Install all package as requirements.txt file defined:<br />
    <code>
    pip install -r requirements.txt --user
    </code>
3. Change your shop home page url on 'run.py' file:<br />
    <code>
    item_list = get_all_product_url(browser, 'https://tiki.vn/cua-hang/thiet-bi-y-te-gia-dinh-hme')
    </code>
4. To run scraping auto tool, run:<br />
    <code>
    python run.py
    </code>
    <br />
    The results will be saved to 'tiki_report.xls' file on current directory.<br />

All information, please kindly to contact: anhtuan.bkfet.k55@gmail.com
