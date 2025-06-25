import argparse
from scraper.cli import parse_args

def test_parse_args_defaults():
    args = parse_args([])
    assert args.max_pages == 3
    assert args.output_format == "json"
    assert args.headless is False
    assert args.db is False

def test_parse_args_custom():
    args = parse_args(["--max-pages", "5", "--output-format", "csv", "--headless", "--db"])
    assert args.max_pages == 5
    assert args.output_format == "csv"
    assert args.headless is True
    assert args.db is True
