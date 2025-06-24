import argparse
import asyncio
from .scraper import scrape_books
from .storage import save_to_json, save_to_csv, save_to_sqlite
from .utils import setup_logger


logger = setup_logger("cli")

def parse_args():
    parser = argparse.ArgumentParser(description="Scrape books from books.toscrape.com")
    parser.add_argument("--max-pages", type=int, default=3,
                        help="Maximum number of pages to scrape")
    parser.add_argument("--output-format", choices=["json", "csv"], default="json",
                        help="Output format (json or csv)")
    parser.add_argument("--headless", action="store_true",
                        help="Run browser in headless mode")
    parser.add_argument("--db", action="store_true",
                        help="Also save results to SQLite database")
    return parser.parse_args()

async def run_scraper(args):
    start_url = "https://books.toscrape.com/"
    data = await scrape_books(start_url, args.max_pages, args.headless)
    logger.info(f"Scraped {len(data)} items.")
    # Save to file
    if args.output_format == "json":
        save_to_json(data, "output.json")
        print("Results saved to output.json")
    else:
        save_to_csv(data, "output.csv")
        print("Results saved to output.csv")
    # Save to SQLite if requested
    if args.db:
        save_to_sqlite(data)
        print("Results also saved to books.db (SQLite)")

def main():
    args = parse_args()
    logger.info("Starting CLI tool with arguments: "
                f"max_pages={args.max_pages}, "
                f"output_format={args.output_format}, "
                f"headless={args.headless}, db={args.db}")
    asyncio.run(run_scraper(args))

if __name__ == "__main__":
    main()
