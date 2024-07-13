import pandas as pd
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException

from src.scraping_ids import IdsScraping
from src.scraping_house import HouseScraping
from src.utils import wait


def _save_df(house_dfs: list[pd.DataFrame]) -> None:
    """
    Saves the list of dfs to a unified df.

    Parameters
    ----------
    house_dfs : List with the df of each house
    """

    df = pd.DataFrame(house_dfs)
    cols = ["id"] + [col for col in df.columns if col != "id"]
    df = df[cols]
    df.to_csv("data/houses_df.csv", index=False)


def _get_soup(browser: uc.Chrome, url: str) -> BeautifulSoup:
    """
    Gets the soup of a given house.

    Parameters
    ----------
    browser : Browser
    url     : Url of the house

    Returns
    -------
    soup : Soup with the information
    """

    wait()
    browser.get(url)
    wait()
    try:  # disagree with cookies
        browser.find_element(
            "xpath", "//*[@id='didomi-notice-disagree-button']"
        ).click()
    except NoSuchElementException:
        pass
    html = browser.page_source
    soup = BeautifulSoup(html, "lxml")

    return soup


def main(base_url: str, save_every: int = 5) -> None:
    """
    Scraping of all houses of a given zone.

    Parameters
    ----------
    base_url    : Url of the zone
    print_every : To save the progress of the scraping of the house ids
    """

    # obtain house ids
    obtainer = IdsScraping(base_url)
    house_ids = obtainer.obtain_ids()
    house_ids_df = pd.DataFrame({"house_id": house_ids})
    house_ids_df.to_csv("data/house_ids.csv", index=False)

    browser = uc.Chrome()

    # obtain info for each house
    house_dfs: list[pd.DataFrame] = []
    for i, house_id in enumerate(house_ids):
        # Save progress
        if i % save_every == 0:
            print(f"Number of scraped id's: {i}")
            _save_df(house_dfs)

        # get house url
        url = f"https://www.idealista.com/inmueble/{house_id}/"

        # get house soup
        soup = _get_soup(browser, url)

        # get house info
        scraper = HouseScraping(soup)
        house_info = scraper.get_house_information()
        house_info["id"] = house_id
        house_dfs.append(house_info)

    browser.quit()
    _save_df(house_dfs)