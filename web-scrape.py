# Scrape

from bs4 import BeautifulSoup
from requests import get
import datetime

# Define header to pass any blocks
headers = (
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'}
        )

# Pages with prices to scrape
urls = [
        'https://www.petcircle.com.au/product/royal-canin-kitten-instinctive-jelly-wet-cat-food-pouches/ac94bvo4x',
        ]

def get_html_soup(url, header):
    """ Returns soup object """
    response = get(url, headers=header)
    url_text = response.text
    html_soup = BeautifulSoup(url_text, 'html.parser')
    return(html_soup)

def get_price_container(soup_object, html_tag, tag_class):
    """ Contains prices for multiple sizes
    Returns bs4.element.ResultSet """
    price_container = soup_object.find_all(html_tag, class_=tag_class)
    return(price_container)

def make_data_row(item_name, scrape_datetime, soup_result_item):
    """ Returns dictionary """
    # Dates and times
    scrape_date = scrape_datetime.date().isoformat()
    scrape_weekday = scrape_datetime.strftime('%A')
    scrape_time = scrape_datetime.time().isoformat() 
    # Price data
    product_size = soup_result_item.get("data-displayname")
    sku_id = soup_result_item.get("data=sku")
    autodelivery_price = soup_result_item.get("data-adprice")
    standard_price = soup_result_item.get("data-price")
    sold_out = soup_result_item.get("data-issoldout")
    # Altogether
    data_row = {
            'scrape_date': scrape_date,
            'scrape_weekday': scrape_weekday,
            'scrape_time': scrape_time,
            'product_name': item_name,
            'product_size': product_size,
            'sku_id': sku_id,
            'autodelivery_price': autodelivery_price,
            'standard_price': standard_price,
            'sold_out': sold_out,
            }
    return(data_row)

def main():
    print(headers)
    print(urls)

    price_data = list()

    for u in urls:
        scrape_dt = datetime.datetime.now()
        url_soup = get_html_soup(url=u, header=headers)
        product_name = url_soup.find('input', id="pname").get("value").replace('-', ' ')
        price_container = get_price_container(soup_object = url_soup,
                                              html_tag = 'input',
                                              tag_class = "sku-option")

        for item in price_container:
            new_row = make_data_row(item_name = product_name,
                                    scrape_datetime = scrape_dt,
                                    soup_result_item = item)
            price_data.append(new_row)

    print(price_data)

main()
