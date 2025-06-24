import random
import asyncio
import logging

# List of User-Agent strings for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
]

def setup_logger(name="scraper", level=logging.INFO):
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        logger.addHandler(handler)
    return logger

async def human_delay(min_sec: float = 1.0, max_sec: float = 3.0):
    """Sleep for a random interval to mimic human reading/think-time."""
    delay = random.uniform(min_sec, max_sec)
    await asyncio.sleep(delay)

def parse_star_rating(class_attr: str) -> str:
    """
    Extract the star rating word from a class attribute.
    For example, "star-rating Three" -> "Three".
    """
    parts = class_attr.split()
    if len(parts) > 1:
        return parts[-1]
    return ""
