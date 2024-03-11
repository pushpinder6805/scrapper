import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape product details from a given URL
def scrape_product_details(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the product details section
        product_details_section = soup.find("div", class_="cent clearfix")

        # Extract specific product details
        brand = product_details_section.find("dt", text="Brand").find_next_sibling("dd").text.strip()
        model_number = product_details_section.find("dt", text="Model P/N").find_next_sibling("dd").text.strip()
        diagonal_size = product_details_section.find("dt", text="Diagonal Size").find_next_sibling("dd").text.strip()
        panel_type = product_details_section.find("dt", text="Panel Type").find_next_sibling("dd").text.strip()
        resolution = product_details_section.find("dt", text="Resolution").find_next_sibling("dd").text.strip()
        active_area = product_details_section.find("dt", text="Active Area").find_next_sibling("dd").text.strip()

        # Store product information in a dictionary
        product_info = {
            "Brand": brand,
            "Model Number": model_number,
            "Diagonal Size": diagonal_size,
            "Panel Type": panel_type,
            "Resolution": resolution,
            "Active Area": active_area
        }

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
            if product_info:
                all_products_info.append(product_info)
    except Exception as e:
        print(f"An error occurred while scraping products: {e}")

    return all_products_info

# Function to save scraped product details to a CSV file
def save_to_csv(products_info, filename):
    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["Brand", "Model Number", "Diagonal Size", "Panel Type", "Resolution", "Active Area"]
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
