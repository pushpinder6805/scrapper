import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape product details from a given URL
def scrape_product_details(url):
    # Send a GET request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all product details
    product_details = soup.find_all("div", class_="product-details")

    # List to store all product information
    products_info = []

    # Loop through each product detail
    for product in product_details:
        # Extract relevant information such as product name, price, etc.
        product_name = product.find("h2").text.strip()
        product_price = product.find("span", class_="price").text.strip()
        product_description = product.find("p", class_="description").text.strip()

        # Store product information in a dictionary
        product_info = {
            "Name": product_name,
            "Price": product_price,
            "Description": product_description
        }
        
        # Append product information to the list
        products_info.append(product_info)

    return products_info

# Main function to scrape all products from the website
def scrape_all_products():
    # URL of the website to scrape
    base_url = "https://panelook.com/bramodlist.php?brands[]=124"
    # List to store all product information
    all_products_info = []

    # Hypothetical loop to iterate over multiple pages of products
    for page_number in range(1, 6):  # Assume there are 5 pages of products
        url = f"{base_url}?page={page_number}"
        products_info = scrape_product_details(url)
        all_products_info.extend(products_info)

    return all_products_info

# Function to save scraped product details to a CSV file
def save_to_csv(products_info, filename):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Name", "Price", "Description"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for product in products_info:
            writer.writerow(product)

# Scrape all products and save to CSV file
all_products_info = scrape_all_products()
save_to_csv(all_products_info, "panelook_products.csv")
