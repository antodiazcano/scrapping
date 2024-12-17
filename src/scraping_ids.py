"""
Script for scraping houses of a particular zone.
"""

from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException

from src.utils import wait


class IdsScraping:
    """
    Class to get all house ids of a particular zone. Each zone has many pages and many
    advertisements per page.
    """

    def __init__(self, base_url: str) -> None:
        """
        Constructor of the class.

        Parameters
        ----------
        base_url : Url of the advertisements of the zone.
        """

        self.base_url = base_url
        self.browser = uc.Chrome()

    def _get_new_soup(self, page: int) -> BeautifulSoup:
        """
        Gets the html of the current page of the zone.

        Parameters
        ----------
        page : Number of the page.

        Returns
        -------
        Html of the current page.
        """

        url = f"{self.base_url}/pagina-{page}.htm"
        self.browser.get(url)
        wait()

        try:
            self.browser.find_element(
                "xpath", "//*[@id='didomi-notice-disagree-button']"
            ).click()
        except NoSuchElementException:
            pass

        html = self.browser.page_source

        return BeautifulSoup(html, "lxml")

    def _add_ids(self, ids: list[int], soup: BeautifulSoup) -> list[int]:
        """
        Updates the list of ids with the ones in the current page.

        Parameters
        ----------
        ids  : Current ids.
        soup : Soup of the new page.

        Returns
        -------
        Updated ids.
        """

        articles = soup.find("main", {"class": "listing-items"}).find_all("article")

        for article in articles:
            id_ = article.get("data-element-id")
            if id_ is not None:
                ids.append(int(id_))

        return ids

    def obtain_ids(self) -> list[int]:
        """
        Obtains all the house ids of a zone.

        Returns
        -------
        List with all ids of the zone.
        """

        current_page = 1
        ids: list[int] = []

        while True:
            soup = self._get_new_soup(current_page)
            new_current_page = int(
                soup.find("main", {"class": "listing-items"})
                .find("div", {"class": "pagination"})
                .find("li", {"class": "selected"})
                .text
            )

            if new_current_page == current_page:
                ids = self._add_ids(ids, soup)
            else:  # we reach the end
                self.browser.quit()
                return ids

            current_page += 1
            wait()

    def get_url(self) -> str:
        """
        Returns the url.

        Returns
        -------
        Base url used.
        """

        return self.base_url
