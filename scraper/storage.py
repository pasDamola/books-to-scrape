import json
import csv
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from scraper.utils import setup_logger

logger = setup_logger("storage")

Base = declarative_base()
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    rating = Column(String)
    url = Column(String)

def save_to_json(data: list, file_path: str):
    """Save scraped data to a JSON file."""
    logger.info(f"Saving data to JSON: {file_path}")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_to_csv(data: list, file_path: str):
    """Save scraped data to a CSV file."""
    if not data:
        return
    with open(file_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price", "rating", "url"])
        writer.writeheader()
        for item in data:
            writer.writerow(item)

def save_to_sqlite(data: list, db_path: str = "books.db"):
    """Insert scraped data into a SQLite database using SQLAlchemy ORM."""
    logger.info(f"Inserting {len(data)} records into SQLite DB: {db_path}")
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    for item in data:
        book = Book(title=item["title"], price=item["price"],
                    rating=item["rating"], url=item["url"])
        session.add(book)
    session.commit()
    session.close()
