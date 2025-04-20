from bs4 import BeautifulSoup
import requests
import csv
import logging

# set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s -%(message)s')


def fetch_website_content(url):
    """Fetch The HTML content of a website"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.info(f'Successfully fetched the content for {url}')
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching content from {url}:{e}")
        return None


# using BeautifulSoup
def parse_quotes_and_authors(html_content):
    """Parse quotes and authos from the HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    qoutes = soup.find_all('span', class_='text')
    authors = soup.find_all('small', class_='author')
    if not qoutes or not authors:
        logging.warning('No quotes or authors found on the page.')
    return qoutes, authors


# Saving to CSV
def save_to_csv(quotes, authors, output_file='quotes.csv'):
    """Save quotes and authors to a CSV file."""
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Quote', 'Author'])
            for quote, author in zip(quotes, authors):
                writer.writerow([quote.text.strip(), author.text.strip()])
        logging.info(f"Data successfully written to {output_file}")
    except IOError as e:
        logging.error(f'Error writing to file {output_file}: {e}')


def main():
    """Main function to orchestrate the web scraping."""
    website = "https://quotes.toscrape.com/"
    html_content = fetch_website_content(website)
    if html_content:
        quotes, authors = parse_quotes_and_authors(html_content)
        if quotes and authors:
            save_to_csv(quotes, authors, output_file="new_scraping.csv")


if __name__ == "__main__":
    main()
