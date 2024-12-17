"""
Script to obtain the information of all the houses of a particular zone.
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

from src.scraping_ids import IdsScraping
from src.scraping_house import HouseScraping
from src.utils import wait, MAX_TIME_REQUEST


IDS_OUTPUT_PATH = "data/house_ids.csv"
MAIN_OUTPUT_PATH = "data/houses_df.csv"


def _save_df(house_dfs: list[pd.DataFrame]) -> None:
    """
    Saves the list of dfs to a unified df.

    Parameters
    ----------
    house_dfs : List with the df of each house.
    """

    df = pd.DataFrame(house_dfs)
    cols = ["id"] + [col for col in df.columns if col != "id"]
    df = df[cols]
    df.to_csv(MAIN_OUTPUT_PATH, index=False)


def _get_soup(url: str) -> BeautifulSoup:
    """
    Gets the soup of a given house.

    Parameters
    ----------
    url     : Url of the house.

    Returns
    -------
    Soup with the information.
    """

    wait()
    html = requests.get(url, timeout=MAX_TIME_REQUEST)
    wait()
    soup = BeautifulSoup(html.text, "html.parser")

    return soup


def main(base_url: str, save_every: int = 5) -> None:
    """
    Scraping of all houses of a given zone.

    Parameters
    ----------
    base_url   : Url of the zone.
    save_every : To save the progress of the scraping of the house ids.
    """

    # Obtain house ids
    obtainer = IdsScraping(base_url)
    house_ids = obtainer.obtain_ids()
    house_ids_df = pd.DataFrame({"house_id": house_ids})
    house_ids_df.to_csv(IDS_OUTPUT_PATH, index=False)

    # Obtain info for each house
    house_dfs: list[pd.DataFrame] = []
    for i, house_id in enumerate(house_ids):
        # Save progress
        if i % save_every == 0 and i > 0:
            print(f"Scraped id's: {i}/{len(house_dfs)}")
            _save_df(house_dfs)

        # Get house url
        url = f"https://www.idealista.com/inmueble/{house_id}/"

        # Get house soup
        soup = _get_soup(url)

        # Get house info
        scraper = HouseScraping(soup)
        house_info = scraper.get_house_information()
        house_info["id"] = house_id
        house_dfs.append(house_info)

    _save_df(house_dfs)


if __name__ == "__main__":
    BASE_URL = "https://www.idealista.com/venta-viviendas/toledo/buenavista-valparaiso-la-legua/"
    main(BASE_URL)
