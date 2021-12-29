# Price check
Scrape prices from Pet Circle to monitor prices of cat food and kitty litter.

## How the script runs
- You provide a list of webpages from Pet Circle to scrape prices from
  (currently part of python script)
- It will output list to local csv
### Automating scraping
- The script runs from a Anaconda python environment, so the `auto-scrape-pet-circle.bat` is a batch file will switch the environment accordingly

## Google sheets API

- If running the `scrape-pet-circle-sheets.py` this will interface with the Google Sheets API.

sources:
https://towardsdatascience.com/looking-for-a-house-build-a-web-scraper-to-help-you-5ab25badc83e
https://towardsdatascience.com/scraping-multiple-amazon-stores-with-python-5eab811453a8
https://medium.com/analytics-vidhya/scraping-car-prices-using-python-97086c30cd65


---

## Pre-reqs
- Anaconda install of python (not necessary, but preferred for batch script)

## Installing
- In anaconda prompt `conda env create --name price-check --file environment.yml`

## Export environment
- `conda env export --name price-check --file environment.yml`

## Setup for Google Sheets

- See [OAuth stuff here](https://developers.google.com/workspace/guides/configure-oauth-consent#choose-scopes) and [Google Sheets API stuff here](https://developers.google.com/sheets/api/guides/authorizing)

---

## Todo
- Add error handling
- Add some input csv list thingo
- Combine the output csv and google sheets into one big script
- Work out how to do the OAuth stuff in a secure way
- Long term plan - move from local output to SqlLite
