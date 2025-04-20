import unittest
from unittest.mock import patch, mock_open, MagicMock
from scraping import fetch_website_content, parse_quotes_and_authors, save_to_csv
from requests.exceptions import RequestException


class TestWebScraping(unittest.TestCase):

    @patch('scraping.requests.get')
    def test_fetch_website_content_success(self, mock_get):
        """Test fetch_website_content with a successful response."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "<html><body>Test Content</body></html>"
        url = "https://example.com"
        result = fetch_website_content(url)
        self.assertEqual(result, "<html><body>Test Content</body></html>")
        mock_get.assert_called_once_with(url)

    @patch('scraping.requests.get')
    def test_fetch_website_content_failure(self, mock_get):
        """Test fetch_website_content with a failed response."""
        mock_get.side_effect = RequestException("Request failed")
        url = "https://example.com"
        result = fetch_website_content(url)
        self.assertIsNone(result)

    def test_parse_quotes_and_authors(self):
        """Test parse_quotes_and_authors with valid HTML content."""
        html_content = """
        <html>
            <body>
                <span class="text">Quote 1</span>
                <small class="author">Author 1</small>
                <span class="text">Quote 2</span>
                <small class="author">Author 2</small>
            </body>
        </html>
        """
        quotes, authors = parse_quotes_and_authors(html_content)
        self.assertEqual(len(quotes), 2)
        self.assertEqual(len(authors), 2)
        self.assertEqual(quotes[0].text, "Quote 1")
        self.assertEqual(authors[0].text, "Author 1")

    def test_parse_quotes_and_authors_empty(self):
        """Test parse_quotes_and_authors with no quotes or authors."""
        html_content = "<html><body></body></html>"
        quotes, authors = parse_quotes_and_authors(html_content)
        self.assertEqual(len(quotes), 0)
        self.assertEqual(len(authors), 0)

    @patch('builtins.open', new_callable=mock_open)
    @patch('scraping.csv.writer')
    def test_save_to_csv(self, mock_csv_writer, mock_open_file):
        """Test save_to_csv with valid quotes and authors."""
        mock_writer_instance = MagicMock()
        mock_csv_writer.return_value = mock_writer_instance

        quotes = [MagicMock(text="Quote 1"), MagicMock(text="Quote 2")]
        authors = [MagicMock(text="Author 1"), MagicMock(text="Author 2")]
        save_to_csv(quotes, authors, output_file="test.csv")

        mock_open_file.assert_called_once_with(
            "test.csv", 'w', newline='', encoding='utf-8')
        mock_writer_instance.writerow.assert_any_call(['Quote', 'Author'])
        mock_writer_instance.writerow.assert_any_call(['Quote 1', 'Author 1'])
        mock_writer_instance.writerow.assert_any_call(['Quote 2', 'Author 2'])


if __name__ == "__main__":
    unittest.main()
