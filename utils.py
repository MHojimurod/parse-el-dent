import time
import requests
from bs4 import BeautifulSoup
from upload.models import Product, Urls


url = "https://el-dent.ru"

cache = {}
counter = 0


def fetch(url: str):

    if url in cache:
        return cache[url]

    try:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.text
            cache[url] = content
            return content
    except requests.exceptions.Timeout:
        # A re-request is sent when the request timed out
        print('sleep')
        time.sleep(2)
        fetch(url)


def parse_products_link(category_id, category_url: str):

    full_url = url + category_url
    response = fetch(full_url)
    if response:
        soup = BeautifulSoup(response, 'html.parser')
        if soup.find('div', class_='navi'):
            full_url = url + category_url.replace('.html', '-ALL.html')
            response = fetch(full_url)
            if response:
                soup = BeautifulSoup(response, 'html.parser')

        uls = soup.find_all('div', class_='about')
        links = []
        for ul in uls:
            links.append(
                Urls(
                    category_id=category_id,
                    url=ul.find('a', class_='tit')['href']
                )
            )
        Urls.objects.bulk_create(links)


def parse_product_detail(product_url: str, category_id):

    full_url = url + product_url
    response = fetch(full_url)
    try:

        soup = BeautifulSoup(response, 'html.parser')
        title = soup.find("h1").get_text()
        price = soup.find("span", class_='price').get_text()

        manufacturer_divs = soup.find_all(
            'div', class_='product-manufacturer-logo-block')
        if manufacturer_divs:
            logo = manufacturer_divs[0].find('img')
            country = manufacturer_divs[1].find_all('span')[-1].get_text()
            company = logo['title']
            logo = f'{url}{logo["src"]}'
        else:
            logo = None
            country = None
            company = None

        code = soup.find(
            'div', style='line-height:22px').get_text().split(":")[-1].strip()
        vendor_code = soup.find('div', class_='floatleft w60 --article').get_text(
        ).replace("\n", '').split('Артикул')[-1].strip()

        images = [
            f"{url}{ul['href']}" for ul in soup.find_all('a', class_='put_image')]
        desc = parse_description(soup)
        Product.objects.create(
            title=title,
            images=str(images),
            price=price,
            company=company,
            country=country,
            manufacturer_logo=logo,
            manufacturer_code=code,
            vendor_code=vendor_code,
            description=desc,
            category_id=category_id
        )
        print('done')
        return True
    except Exception as e:
        print("Something error", e)
    return False


def parse_description(soup: BeautifulSoup):

    parsed_data = []

    # Get the main content div
    description_div = soup.find('div', itemprop="description")

    # Helper function to clean text
    def clean_text(text):
        return text.strip()

    # Parse the elements and organize them in the desired format
    for element in description_div.find_all(['h2', 'h4', 'p', 'ul', 'img']):
        if element.name == 'h2':

            # Clean and check if not empty
            text = clean_text(element.get_text())
            if text:
                parsed_data.append({
                    "h2": text
                })
        elif element.name == 'h4':

            # Clean and check if not empty
            text = clean_text(element.get_text())
            if text:
                parsed_data.append({
                    "h4": text
                })
        elif element.name == 'p':

            # Clean and check if not empty
            text = clean_text(element.get_text())
            if text:
                if parsed_data and "p" in parsed_data[-1]:
                    parsed_data[-1]["p"].append(text)
                else:
                    parsed_data[-1]["p"] = [text]
        elif element.name == 'ul':

            # Clean and add list items, but only non-empty ones
            list_items = [clean_text(li.get_text()) for li in element.find_all(
                'li') if clean_text(li.get_text())]
            if list_items:
                parsed_data[-1]["ul"] = list_items
        elif element.name == 'img':
            img_src = element.get('src', '').strip()
            if img_src:
                if parsed_data and "img" in parsed_data[-1]:
                    parsed_data[-1]["img"].append(
                        f'{url}{img_src}')
                else:
                    parsed_data[-1]["img"] = [f'{url}{img_src}']

    return parsed_data
