import random
from urllib.parse import urljoin
from playwright.async_api import async_playwright, Page
from .utils import USER_AGENTS, human_delay, parse_star_rating, setup_logger


logger = setup_logger("scraper")

async def scrape_books(start_url: str, max_pages: int, headless: bool) -> list:
    """
    Use Playwright to navigate the book listings and extract data.
    Returns a list of dicts: {title, price, rating, url}.
    """
    logger.info(f"Launching browser with headless={headless}")
    output = []
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=headless)
        context = await browser.new_context(
            user_agent=random.choice(USER_AGENTS),
            viewport={"width": 1280, "height": 720}
        )
        page: Page = await context.new_page()
        current_url = start_url
        pages_scraped = 0

        while pages_scraped < max_pages:
            logger.info(f"Scraping page {pages_scraped + 1}: {current_url}")
            await page.goto(current_url)
            await page.wait_for_load_state('networkidle')
            # Random delay to avoid detection
            await human_delay(1, 3)

            products = await page.query_selector_all("article.product_pod")
            if not products:
                logger.warning(f"[Warning] No products found on page: {current_url}")
                break

            for prod in products:
                
                title_el = await prod.query_selector("h3 a")
                title_text = await title_el.get_attribute("title")
                price_el = await prod.query_selector(".price_color")
                if price_el:
                    price_text = await price_el.inner_text()
                    price_value = float(price_text.replace("£", "").strip())
                rating_el = await prod.query_selector("p.star-rating")
                if rating_el:
                    rating_class = await rating_el.get_attribute("class")
                    rating_text = parse_star_rating(rating_class)
                rel_url = await title_el.get_attribute("href")
                full_url = urljoin(current_url, rel_url)

                output.append({
                    "title": title_text,
                    "price": price_value,
                    "rating": rating_text,
                    "url": full_url
                })

            logger.info(f"Extracted {len(products)} products from page {pages_scraped + 1}")
            pages_scraped += 1
            # Try to navigate to next page
            next_link = await page.query_selector("li.next > a")
            if next_link:
                href = await next_link.get_attribute("href")
                current_url = urljoin(current_url, href)
                await human_delay(2, 5)
            else:
                break

        await browser.close()

    return output
