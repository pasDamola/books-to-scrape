# Books-to-Scrape CLI Scraper

This is a Python CLI tool to scrape book data from [Books to Scrape](https://books.toscrape.com). It extracts Title, Price, Star rating, and the product URL for each book, up to a specified number of pages. The tool uses Playwright for browser automation with anti-detection techniques.

## Features
- Randomized wait times and rotating User-Agent to mimic human browsing:contentReference[oaicite:15]{index=15}:contentReference[oaicite:16]{index=16}.
- Optional headless mode (via `--headless`) for running without opening a visible browser.
- Saves output as JSON or CSV (`--output-format`), and can also store data in SQLite (`--db`) using SQLAlchemy.
- Modular code structure for maintainability.
- Dockerfile included for easy deployment:contentReference[oaicite:17]{index=17}.

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt

2. **Install Playwright browsers**:
    ```bash
    playwright install

3. **Run the scraper**:
    ```bash
    python -m scraper.cli --max-pages 5 --output-format json --headless

This will scrape the first 5 pages in headless mode and save results to output.json

**Output**
 - output.json or output.csv: Scraped data in the chosen format.
 - books.db: (if --db used) SQLite database with a books table.
 - The JSON/CSV columns are: title, price, rating, url.


A sample JSON output would look like:
    ```json

    [
        {
            "title": "A Light in the Attic",
            "price": 51.77,
            "rating": "Three",
            "url": "https://books.toscrape.com/a-light-in-the-attic_1000/index.html"
        },
        {
            "title": "Tipping the Velvet",
            "price": 53.74,
            "rating": "One",
            "url": "https://books.toscrape.com/tipping-the-velvet_999/index.html"
        },
        {
            "title": "Soumission",
            "price": 50.10,
            "rating": "One",
            "url": "https://books.toscrape.com/soumission_998/index.html"
        }
    ]

**Testing**:
Run the unit tests with:
    ```bash
    pytest
These tests cover argument parsing, rating parsing, and output formatting.


**Explanation of Anti-Bot Techniques**

To reduce detection, I mimiced human browsing: inserting pauses between actions makes requests erratic as a person would behave
 - We also rotate User-Agent strings on each browser context to appear as different devices/browsers
 - Using a persistent browser context (or reusing the same context) preserves cookies across page loads, simulating a continuous user session
 - These methods help keep the scraper under the radar of anti-bot systems. Playwright’s async API further enables efficient scraping of multiple pages in sequence
 - Each component (scraping, storage, CLI) is separated to keep the codebase clean and testable, following modular design principles
 - We include unit tests (with pytest) for key functions (e.g. parsing star ratings, writing output) to ensure correctness. The provided Dockerfile allows running the tool in a container that already has Playwright’s browsers installed, which simplifies deployment and ensures consistent behavior across environments. This complete implementation meets all requirements: it scrapes at least 3 pages by default, handles pagination and missing pages gracefully, uses human-like delays and UA rotation to avoid blocks, and stores results in JSON/CSV (plus SQLite)