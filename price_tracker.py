# ============================================================
#  Price Tracker — by Hussain Farhan
#  Scrapes book titles, prices & ratings from books.toscrape.com
#  Saves results to price_data.csv
# ============================================================

import requests
from bs4 import BeautifulSoup
import csv
from datetime import date

BASE_URL = "https://books.toscrape.com/catalogue/"
START_URL = "https://books.toscrape.com/catalogue/page-1.html"

def get_page(url):
    """Fetch a page and return a BeautifulSoup object."""
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

def scrape_books(max_pages=5):
    """Scrape book data across multiple pages."""
    all_books = []
    url = START_URL

    for page_num in range(1, max_pages + 1):
        print(f"Scraping page {page_num}...")
        soup = get_page(url)

        # Find all book items on the page
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text.strip()
            rating = book.p["class"][1]  # e.g. "Three", "Four"
            availability = book.find("p", class_="instock availability").text.strip()

            all_books.append({
                "title": title,
                "price": price,
                "rating": rating,
                "availability": availability,
                "date_scraped": date.today()
            })

        # Find the next page link
        next_btn = soup.find("li", class_="next")
        if next_btn:
            url = BASE_URL + next_btn.a["href"]
        else:
            print("No more pages found.")
            break

    return all_books

def save_to_csv(books, filename="price_data.csv"):
    """Save scraped data to a CSV file."""
    if not books:
        print("No data to save.")
        return

    keys = books[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(books)

    print(f"\n✅ Done! Saved {len(books)} books to {filename}")

if __name__ == "__main__":
    print("=== Price Tracker by Hussain Farhan ===\n")
    books = scrape_books(max_pages=5)
    save_to_csv(books)

    # Preview first 3 results
    print("\nSample results:")
    for book in books[:3]:
        print(f"  📖 {book['title'][:40]}... | {book['price']} | {book['rating']} stars")
