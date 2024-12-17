"""
Script for testing the scrapping of the ids html.
"""

import pytest
from bs4 import BeautifulSoup

from src.scraping_ids import IdsScraping


scraper = IdsScraping("")


@pytest.mark.run(order=1)
def test_add_ids() -> None:
    """
    Test for obtaining the ids of the houses of a page.
    """

    with open("data/tests/ids.html", "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    result = scraper._add_ids([], soup)
    expected_length = 30

    assert (
        len(result) == expected_length
    ), f"Got list of length {result}, expected length {expected_length}."
    for id_ in result:
        assert isinstance(id_, int), f"Expected id with type int, got {type(id_)}."


@pytest.mark.run(order=2)
def test_get_url() -> None:
    """
    Test for obtaining the url of the class.
    """

    result = scraper.get_url()
    assert isinstance(result, str), f"Expected str, got {type(result)}."
    assert result == "", f"Expected '', got {result}."
