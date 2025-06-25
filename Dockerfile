FROM mcr.microsoft.com/playwright/python:latest

# Install dependencies
RUN pip install --no-cache-dir \
    sqlalchemy \
    playwright

# Install browsers and dependencies
RUN playwright install --with-deps

# Set working directory
WORKDIR /app

# Copy project files into container
COPY . /app

# Run the CLI scraper as default command
CMD ["python", "-m", "scraper.cli", "--max-pages", "3", "--output-format", "json"]
