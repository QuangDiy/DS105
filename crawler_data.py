from urllib.parse import quote
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.service import Service

def search_product(keyword, driver):
    encoded_keyword = quote(keyword)
    url = f"https://www.thegioididong.com/may-doi-tra/search?key={encoded_keyword}"

    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    elements = soup.select('div.prdItem a')
    urls = [element['href'] for element in elements]

    # driver.quit()
    return f"https://www.thegioididong.com{urls[0]}"


def search_image(keyword, time_bh, driver):
    url = search_product(keyword, driver)

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    elements = soup.select('div.prdItem a')
    for element in elements:
        # print(element.select_one('.prdInfo span').text)
        if (float(element.select_one('.prdInfo span').text.split(' ')[0]) == time_bh):
            url_results = f"https://www.thegioididong.com{element['href']}"
            img = f"https:{element.select_one('.imgThumnb img')['src']}"
            price = element.select_one('.price strong').text
            return url_results, img, price
    return None


def search_image_base(keyword, driver):
    encoded_keyword = quote(keyword)
    url = f"https://www.thegioididong.com/tim-kiem?key={encoded_keyword}"
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    li_tag = soup.find('li', class_='item cat44')
    if li_tag is not None:
        img_src = li_tag.find('img', class_='thumb')['data-src']
    else:
        return None
    # driver.quit()
    return img_src

# keyword = "Laptop Lenovo IdeaPad 3 14ITL6"
# print(search_image_base(keyword, driver))