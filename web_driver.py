from selenium import webdriver

def init_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    browser = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
    return browser