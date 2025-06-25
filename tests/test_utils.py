from scraper.utils import parse_star_rating

def test_parse_star_rating():
    assert parse_star_rating("star-rating Three") == "Three"
    assert parse_star_rating("star-rating Five") == "Five"
    assert parse_star_rating("star-rating") == ""
    assert parse_star_rating("") == ""
