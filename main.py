import requests
from bs4 import BeautifulSoup
import send_mail


def get_amazon_web_page():
    url = "https://www.amazon.co.uk/dp/B083KM6BZS?tag=camelproducts-21&linkCode=ogi&th=1&psc=1&language=en_GB"
    data_file = "./data/amazon_instant_pot.html"

    try:
        open(data_file)
    except FileNotFoundError:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
            "Accept-Language": "en",
        }
        params = {}

        response = requests.get(url, headers=headers, params=params)
        print(f'response:\n{response}\n\n, response.text:\n{response.text}')
        response.raise_for_status()
        data = response.text

        with open(data_file, mode="w", encoding="utf-8") as fp:
            fp.write(data)

    with open(data_file, mode="r") as fp:
        content = fp.read()
    return BeautifulSoup(content, "lxml")


soup = get_amazon_web_page()

# Get price of item
string_price = soup.find(name='span', attrs={"id": "priceblock_ourprice"}).getText()
float_price = float(string_price.split("£")[1])
target_price = 100.00

if float_price <= target_price:
    send_mail.send_mail(
        header="Your item is below the target price.",
        description=f'Target price = £{target_price} \n'
                    f'Current price : £{float_price} \n'
                    f'Go to \n'
                    f'https://www.amazon.co.uk/dp/B083KM6BZS?tag=camelproducts-21&linkCode=ogi&th=1&psc=1&language=en_GB \n'
                    f'to see this item.'
    )
