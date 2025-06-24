FROM mcr.microsoft.com/playwright/python:latest
# Use root user (disable sandbox) or create non-root per Playwright guidance
RUN pip install --no-cache-dir sqlalchemy
WORKDIR /app
COPY . /app
# Install Playwright browsers
RUN playwright install --with-deps
CMD ["python", "-m", "scraper.cli", "--max-pages", "3", "--output-format", "json"]
