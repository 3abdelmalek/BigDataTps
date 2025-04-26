import requests
from bs4 import BeautifulSoup
import csv
import time

# Base URL for Goodreads list (replace with a valid list URL)
base_url = "https://www.goodreads.com/list/show/1.Best_Books_Ever?page="

# Headers to mimic a real browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# Initialize a list to store the data
book_data = []

# Function to scrape a single page
def scrape_page(page_number):
    url = base_url + str(page_number)
    print(f"Scraping page {page_number}...")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if the request was successful

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all book items on the page
        books = soup.find_all('tr', {'itemtype': 'http://schema.org/Book'})

        for book in books:
            # Extract book title
            title = book.find('a', {'class': 'bookTitle'}).text.strip()

            # Extract book author
            author = book.find('a', {'class': 'authorName'}).text.strip()

            # Extract book rating
            rating = book.find('span', {'class': 'minirating'}).text.strip()

            # Extract book type (e.g., Hardcover, Paperback)
            book_type = book.find('span', {'class': 'greyText'})
            if book_type:
                book_type = book_type.text.strip()
            else:
                book_type = "Type not available"

            # Append the data to the list
            book_data.append([title, author, rating, book_type])

        print(f"Scraped {len(books)} books from page {page_number}.")
    except requests.exceptions.HTTPError as e:
        print(f"Error scraping page {page_number}: {e}")

# Loop through multiple pages to scrape 10,000 books
for page in range(1, 101):  # Scrape 100 pages (100 books per page)
    scrape_page(page)
    time.sleep(2)  # Add a delay to avoid overloading the server

    # Stop if we've reached 10,000 books
    if len(book_data) >= 10000:
        break

# Save the data to a CSV file
with open('goodreads_books_10k.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Author", "Rating", "Type"])  # Write header
    writer.writerows(book_data)  # Write book data

print(f"Total books scraped: {len(book_data)}")
print("Data saved to goodreads_books_10k.csv")