import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape product details from a given URL
def scrape_product_details(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Find product details
        product_details = soup.find("div", class_="dewrapB")

        # Extract additional information from definition lists
        additional_info = product_details.find_all("dl")

        # Dictionary to store product details
        product_info = {}

        # Loop through each dl element and extract key-value pairs
        for dl in additional_info:
            # Get the text from dt and dd elements
            key = dl.find("dt").text.strip()
            value = dl.find("dd").text.strip()
            # Add key-value pair to the product_info dictionary
            product_info[key] = value

        return product_info
    except Exception as e:
        print(f"An error occurred while scraping {url}: {e}")
        return {}

# Main function to scrape all products from the website
def scrape_all_products():
    # URL of the website to scrape
    base_url = "https://www.panelook.com/"
    # List to store all product information
    all_products_info = []

    try:
        # Hypothetical loop to iterate over multiple pages of products
        for page_number in range(1, 6):  # Assume there are 5 pages of products
            url = f"{base_url}?page={page_number}"
            product_info = scrape_product_details(url)
            all_products_info.append(product_info)
    except Exception as e:
        print(f"An error occurred while scraping products: {e}")

    return all_products_info

# Function to save scraped product details to a CSV file
def save_to_csv(products_info, filename):
    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = products_info[0].keys() if products_info else []
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for product in products_info:
                writer.writerow(product)
        print(f"Product details successfully saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving to {filename}: {e}")

# Scrape all products and save to CSV file
all_products_info = scrape_all_products()
save_to_csv(all_products_info, "panelook_products.csv")
