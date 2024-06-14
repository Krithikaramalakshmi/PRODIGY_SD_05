import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_page_content(url):
    """Fetch the content of the web page."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to retrieve content: {response.status_code}")
        return None

def parse_html(html_content):
    """Parse the HTML content and extract product information."""
    soup = BeautifulSoup(html_content, "html.parser")
    products = []

    product_elements = soup.find_all("article", class_="product_pod")
    
    for product in product_elements:
        try:
            name = product.find("h3").find("a")["title"].strip()
        except AttributeError:
            name = None

        try:
            price = product.find("p", class_="price_color").text.strip()
        except AttributeError:
            price = None

        try:
            availability = product.find("p", class_="instock availability").text.strip()
        except AttributeError:
            availability = None

        products.append({"name": name, "price": price, "availability": availability})

    return products

def save_to_csv(products, filename="products.csv"):
    """Save the product information to a CSV file."""
    df = pd.DataFrame(products)
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    url = "http://books.toscrape.com/catalogue/category/books/science_22/index.html"
    html_content = get_page_content(url)
    if html_content:
        products = parse_html(html_content)
        if products:
            save_to_csv(products)
            print(f"Saved {len(products)} products to 'products.csv'")
        else:
            print("No products found.")
    else:
        print("Failed to retrieve web page content.")
