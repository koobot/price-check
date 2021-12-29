# Scrapes from Pet Circle
# But writes to google sheets instead of csv
from __future__ import print_function

# Scraping
from bs4 import BeautifulSoup
from requests import get
import datetime
import csv
import os

# API
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


#################################################################################
# Define header to pass any blocks for scraping
HEADERS = (
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'}
        )

# Pages with prices to scrape
# CHANGE TO CSV OR EXTERNAL LIST IN FUTURE
URLS = [
        'https://www.petcircle.com.au/product/royal-canin-kitten-instinctive-jelly-wet-cat-food-pouches/ac94bvo4x',
        'https://www.petcircle.com.au/product/royal-canin-kitten-instinctive-gravy-wet-cat-food-pouches/rcvp031',
        'https://www.petcircle.com.au/product/rufus-and-coco-wee-kitty-clumping-corn-litter/rcclcl8ms',
        ]

# Output
# CHANGE TO EXTERNAL LIST IN FUTURE
csv_output_path = "D:/Documents/Python/price-check/output/pet-circle.csv"

# API params
SPREADSHEET_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1gj5P6t7cNqUdmbR5qQ8SKg3jMI02hbJhQgtbYyzt5eU'
SPREADSHEET_RANGE = 'Sheet1!A:J'

#################################################################################
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

def make_data_row(url, item_name, scrape_datetime, soup_result_item):
    """ Returns dictionary """
    # Dates and times
    scrape_date = scrape_datetime.date().isoformat()
    scrape_weekday = scrape_datetime.strftime('%A')
    scrape_time = scrape_datetime.time().isoformat() 
    # Price data
    product_size = soup_result_item.get("data-displayname")
    sku_id = soup_result_item.get("data-sku")
    autodelivery_price = soup_result_item.get("data-adprice")
    standard_price = soup_result_item.get("data-price")
    sold_out = soup_result_item.get("data-issoldout")
    # Altogether
    data_row = {
            'url': url,
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

def get_sheets_creds(scopes=SPREADSHEET_SCOPES):
    """ Get credentials for Google Sheets API.
    Uses OAuth 2.0.
    Expects the 'credentials.json' and 'token.json' to be in same
    working directory as script.
    Returns: credentials object
    """
    creds = None

    current_script_path = os.path.dirname(os.path.abspath(__file__))

    token_path = os.path.join(current_script_path, 'token.json')
    creds_path = os.path.join(current_script_path, 'credentials.json')
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes=scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_path, scopes=scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    return(creds)

#################################################################################

def main():
    print(HEADERS)
    print(URLS)

    price_data = list()

    for u in URLS:
        scrape_dt = datetime.datetime.now()
        url_soup = get_html_soup(url=u, header=HEADERS)
        product_name = url_soup.find('input', id="pname").get("value").replace('-', ' ')
        price_container = get_price_container(soup_object = url_soup,
                                              html_tag = 'input',
                                              tag_class = "sku-option")

        for item in price_container:
            new_row = make_data_row(url = u,
                                    item_name = product_name,
                                    scrape_datetime = scrape_dt,
                                    soup_result_item = item)
            price_data.append(new_row)

    print(price_data)

    # Get data ready for Google Sheets API ------------------------
    # List
    sheets_values = list()

    for row in price_data:
        sheets_values.append(list(row.values()))
    
    # JSON format
    sheets_body = {'values': sheets_values}

    # Get credentials for Google Sheets API
    sheets_creds = get_sheets_creds(scopes=SPREADSHEET_SCOPES)

    try:
        service = build('sheets', 'v4', credentials=sheets_creds)

        # Call the Sheets API
        sheet = service.spreadsheets()

        # Appends the data
        result = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=SPREADSHEET_RANGE,
            valueInputOption='USER_ENTERED',
            body=sheets_body
        ).execute()

        print('{0} cells appended.'.format(result
                                    .get('updates')
                                    .get('updatedCells')))
    except HttpError as err:
        print(err)

main()
