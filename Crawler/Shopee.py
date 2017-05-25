# -*- coding:utf-8 -*-
import urllib
import Log
import Utilities
from bs4 import BeautifulSoup

shopee_url = 'https://shopee.tw'

def search_product(keyword):
    webdriver = Utilities.webdriver_create()
    previous_url, url = '', shopee_url + '/search/?keyword=' + urllib.quote(keyword)
    webdriver.get(url)
    products = []
    results = None
    while Utilities.wait_element_loaded(webdriver, '//div[@class="shopee-search-result-view__item-card"]'):
        current_url = webdriver.current_url
        if current_url == previous_url:
            results = products
            break
        previous_url = current_url
        Log.debug('Get URL ' + current_url)
        page = BeautifulSoup(webdriver.page_source, 'html.parser')
        for item in page.find_all('div', 'shopee-search-result-view__item-card'):
            name = item.find('div', class_='shopee-item-card__text-name')
            path = item.find('a', class_='shopee-item-card--link')
            products.append({'name': name.get_text(), 'path': path.get('href')})
        if Utilities.click_element(webdriver, '//div[@class="shopee-icon-button shopee-icon-button--right "]') is False:
            Log.debug('Call click_element failed(//div[@class="shopee-icon-button shopee-icon-button--right "])')
            break
    webdriver.quit()
    return results

def search_seller(keyword):
    webdriver = Utilities.webdriver_create()
    previous_url, url = '', shopee_url + '/search_user/?keyword=' + urllib.quote(keyword)
    webdriver.get(url)
    sellers = []
    results = None
    while Utilities.wait_element_loaded(webdriver, '//div[@class="shopee-search-user-item shopee-search-user-item--full"]'):
        current_url = webdriver.current_url
        if current_url == previous_url:
            results = sellers
            break
        previous_url = current_url
        Log.debug('Get URL ' + current_url)
        page = BeautifulSoup(webdriver.page_source, 'html.parser')
        for item in page.find_all('div', 'shopee-search-user-item shopee-search-user-item--full'):
            product_amount = item.find('span', 'shopee-search-user-seller-info-item__primary-text').get_text()
            if product_amount == '0':
                continue
            name = item.find('div', class_='shopee-search-user-item__username')
            path = item.find('a', class_='shopee-search-user-item__leading')
            sellers.append({'name': name.get_text(), 'path': path.get('href')})
        if Utilities.click_element(webdriver, '//div[@class="shopee-icon-button shopee-icon-button--right "]') is False:
            Log.debug('Call click_element failed(//div[@class="shopee-icon-button shopee-icon-button--right "])')
            break;
    webdriver.quit()
    return results

def load_products(seller_path):
    webdriver = Utilities.webdriver_create()
    previous_url, url = '', shopee_url + urllib.quote(seller_path) + '?tab=product'
    webdriver.get(url)
    products = []
    while previous_url != webdriver.current_url:
        Log.debug("Load " + webdriver.current_url)
        if Utilities.wait_element_loaded(webdriver, '//div[@class="shop-search-result-view__item col-xs-2"]') is False:
            Log.debug('Call wait_element_loaded failed(//div[@class="shop-search-result-view__item col-xs-2"])')
            break
        page = BeautifulSoup(webdriver.page_source, 'html.parser')
        for item in page.find_all('div', 'shop-search-result-view__item col-xs-2'):
            name = item.find('div', class_='shopee-item-card__text-name')
            path = item.find('a', class_='shopee-item-card--link')
            products.append({'name': name.get_text(), 'path': path.get('href')})
        previous_url = webdriver.current_url
        if Utilities.click_element(webdriver, '//div[@class="shopee-icon-button shopee-icon-button--right "]') is False:
            Log.debug('Call click_element failed(//div[@class="shopee-icon-button shopee-icon-button--right "])')
            break;
    webdriver.quit()
    return products

def load_product_details(product_path_list):
    webdriver = Utilities.webdriver_create()
    detail_list = []
    failed_list = []
    for product_path in product_path_list:
        url = shopee_url + urllib.quote(urllib.unquote(product_path), safe='/?&=')
        Log.debug("Load " + url)
        webdriver.get(url)
        details = None
        for _ in range(0, 1):
            xpath = '//div[@class="product-page"]//li[@class="shopee-tab-container__header-item"]'
            if Utilities.wait_element_loaded(webdriver, xpath) is False:
                Log.debug('Call wait_element_loaded failed(' + xpath + ')')
                break
            page = BeautifulSoup(webdriver.page_source, 'html.parser')
            evaluation_string = page.find('div', 'product-page').find_all('li', 'shopee-tab-container__header-item')[1].get_text()
            evaluation_number = int(evaluation_string.split('(')[1].split(')')[0])
            xpath = '//div[@class="shopee-product-info__header__real-price"]'
            if Utilities.wait_element_loaded(webdriver, xpath) is False:
                Log.debug('Call wait_element_loaded failed(' + xpath + ')')
                break
            page = BeautifulSoup(webdriver.page_source, 'html.parser')
            price = page.find('div', class_='shopee-product-info__header__real-price').get_text()
            if evaluation_number == 0:
                details = {'price': price, 'evaluations': []}
                break
            xpath = '//div[@class="product-page__tab-link"]'
            if Utilities.click_element(webdriver, xpath, 1) is False:
                Log.debug('Call click_element failed(' + xpath + ')')
                break
            evaluations = []
            previous_page = ''
            while Utilities.wait_element_loaded(webdriver, '//div[@class="shopee-tab-container__content"]//div[@class="shopee-product-rating"]'):
                xpath = '//div[@class="shopee-page-controller"]//div[@class="shopee-button-solid shopee-button-solid--primary "]'
                if Utilities.wait_element_loaded(webdriver, xpath) is False:
                    Log.debug('Call wait_element_loaded failed(' + xpath + ')')
                    break
                page = BeautifulSoup(webdriver.page_source, 'html.parser')
                current_page = page.find('div', 'shopee-page-controller').find('div', class_='shopee-button-solid shopee-button-solid--primary ').get_text()
                if current_page == previous_page:
                    details = {'price': price, 'evaluations': evaluations}
                    break
                previous_page = current_page
                for evaluation in page.find('div', class_='product-page').find_all('div', class_='shopee-product-rating'):
                    start_amount = evaluation.find_all('svg', class_='shopee-svg-icon icon-rating-solid icon-rating-solid--active')
                    rating_time = evaluation.find('div', class_='shopee-product-rating__time')
                    evaluations.append({'start': str(len(start_amount)), 'time': rating_time.get_text().split('|')[0]})
                xpath = '//div[@class="shopee-icon-button shopee-icon-button--right"]'
                xpath = '//div[@class="shopee-page-controller"]//div[@class="shopee-icon-button shopee-icon-button--right "]'
                if Utilities.click_element(webdriver, xpath) is False:
                    Log.debug('Call click_element failed(//div[@class="shopee-icon-button shopee-icon-button--right "])')
                    break
        if details is None:
            failed_list.append({'path': product_path})
        else:
            detail_list.append({'path': product_path, 'details': details})
    webdriver.quit()
    return detail_list, failed_list
