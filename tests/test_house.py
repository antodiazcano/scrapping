"""
Script for testing the scrapping of the html of a house.
"""

import pytest
from bs4 import BeautifulSoup

from src.scraping_house import HouseScraping


with open("data/house.html", "r", encoding="utf-8") as f:
    html = f.read()
soup = BeautifulSoup(html, "html.parser")
scraper = HouseScraping(soup)


@pytest.mark.run(order=1)
def test_title() -> None:
    """
    Test for the title of a house.
    """

    result = scraper._get_title()
    expected = "Piso en venta en calle Reino Unido"
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.run(order=2)
def test_type() -> None:
    """
    Test for the type of a house.
    """

    result = scraper._get_type()
    expected = "flat"
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.run(order=3)
def test_location() -> None:
    """
    Test for the location of a house.
    """

    result = scraper._get_location()
    expected = "Buenavista-Valparaíso-La Legua, Toledo"
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.run(order=4)
def test_price() -> None:
    """
    Test for the price of a house.
    """

    result = scraper._get_price()
    expected = 304900
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.run(order=5)
def test_m2() -> None:
    """
    Test for the m2 of a house.
    """

    result = scraper._get_m2()
    expected = 120
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.run(order=6)
def test_status() -> None:
    """
    Test for the status of a house.
    """

    result = scraper._get_status()
    expected = "Segunda mano/buen estado"
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.run(order=7)
def test_floor() -> None:
    """
    Test for the floor of a house.
    """

    result = scraper._get_floor()
    expected = 1
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.run(order=8)
def test_description() -> None:
    """
    Test for the description of a house.
    """

    result = scraper._get_description()
    length = 1155
    assert isinstance(result, str), f"Expcted str, got {type(result)}"
    assert (
        len(result) == length
    ), f"Expected str with length {length}, got str with length {len(result)}"


@pytest.mark.run(order=9)
def test_n_photos() -> None:
    """
    Test for the number of photos of a house.
    """

    result = scraper._get_number_of_photos()
    expected = 41
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.run(order=10)
def test_n_rooms() -> None:
    """
    Test for the number of rooms of a house.
    """

    result = scraper._get_number_of_rooms()
    expected = 3
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.run(order=11)
def test_n_bathrooms() -> None:
    """
    Test for the number of bathrooms of a house.
    """

    result = scraper._get_number_of_bathrooms()
    expected = 2
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.run(order=12)
def test_particular() -> None:
    """
    Test for the seller (particular or company) of a house.
    """

    result = scraper._get_particular()
    expected = False
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.run(order=13)
def test_luxury() -> None:
    """
    Test for the luxury of a house.
    """

    result = scraper._get_luxury()
    expected = False
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.run(order=14)
def test_video() -> None:
    """
    Test for if an advertisement has a video.
    """

    result = scraper._get_video()
    expected = False
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.run(order=15)
def test_virtual_tour() -> None:
    """
    Test for if an advertisement has a virtual tour.
    """

    result = scraper._get_virtual_tour()
    expected = True
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.run(order=16)
def test_3d_tour() -> None:
    """
    Test for if an advertisement has a 3d tour.
    """

    result = scraper._get_3d_tour()
    expected = False
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.run(order=17)
def test_homestaging() -> None:
    """
    Test for if an advertisement has a homestaging.
    """

    result = scraper._get_homestaging()
    expected = True
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.run(order=18)
def test_plane() -> None:
    """
    Test for if an advertisement has a plane.
    """

    result = scraper._get_plane()
    expected = True
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.run(order=19)
def test_air_conditioning() -> None:
    """
    Test for if a house has air conditioning.
    """

    result = scraper._get_air_conditioning()
    expected = True
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.run(order=20)
def test_heating() -> None:
    """
    Test for if a house has heating.
    """

    result = scraper._get_heating()
    expected = "Calefacción individual: Gas natural"
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.run(order=21)
def test_elevator() -> None:
    """
    Test for if the building has elevator.
    """

    result = scraper._get_elevator()
    expected = True
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.run(order=22)
def test_furnished() -> None:
    """
    Test for if the house is furnished.
    """

    result = scraper._get_furnished()
    assert result is None, f"Expected None, got {result}"


@pytest.mark.run(order=23)
def test_terrace() -> None:
    """
    Test for if the house has terrace.
    """

    result = scraper._get_terrace()
    assert result is None, f"Expected None, got {result}"


@pytest.mark.run(order=24)
def test_consume() -> None:
    """
    Test for the consume of the house.
    """

    result = scraper._get_consume()
    expected = "D"
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.run(order=25)
def test_emisions() -> None:
    """
    Test for the emisions of the house.
    """

    result = scraper._get_emisions()
    expected = "D"
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.run(order=26)
def test_get_house_info() -> None:
    """
    Test for the information of the house.
    """

    result = scraper.get_house_information()
    expected = 25
    assert len(result) == expected, f"Expected length {expected}, got {len(result)}"


@pytest.mark.run(order=27)
def test_get_html() -> None:
    """
    Test for the get_html function.
    """

    result = scraper.get_html()
    assert isinstance(
        result, BeautifulSoup
    ), f"Expected type BeautifoulSoup, got {type(result)}"
