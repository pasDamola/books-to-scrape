import os
import json
import csv
from scraper.storage import save_to_json, save_to_csv, save_to_sqlite
from sqlalchemy import create_engine, inspect, text

sample_data = [
    {"title": "Book A", "price": 10.99, "rating": "Four", "url": "https://example.com/book-a"},
    {"title": "Book B", "price": 20.00, "rating": "Two", "url": "https://example.com/book-b"},
]

def test_save_to_json(tmp_path):
    file_path = tmp_path / "books.json"
    save_to_json(sample_data, file_path)
    assert file_path.exists()

    with open(file_path, "r") as f:
        data = json.load(f)
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["title"] == "Book A"

def test_save_to_csv(tmp_path):
    file_path = tmp_path / "books.csv"
    save_to_csv(sample_data, file_path)
    assert file_path.exists()

    with open(file_path, newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 2
    assert rows[1]["title"] == "Book B"

def test_save_to_sqlite(tmp_path):
    db_path = tmp_path / "test_books.db"
    save_to_sqlite(sample_data, db_path)

    engine = create_engine(f"sqlite:///{db_path}")
    inspector = inspect(engine)
    assert "books" in inspector.get_table_names()

    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM books"))
        count = result.fetchone()[0]
        assert count == 2
