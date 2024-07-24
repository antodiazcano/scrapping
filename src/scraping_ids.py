from bs4 import BeautifulSoup
import undetected_chromedriver as uc  # pip install --upgrade undetected-chromedriver
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
        base_url : Url of the advertisements of the zone
        """

        self.base_url = base_url
        self.browser = uc.Chrome()

    def _get_new_soup(self, page: int) -> BeautifulSoup:
        """
        Gets the html of the current page of the zone.

        Parameters
        ----------
        page : Number of the page

        Returns
        -------
        html of the current page
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

    def obtain_ids(self) -> list[int]:
        """
        Obtains all the house ids of a zone.

        Returns
        -------
        ids : List with all ids of the zone
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
                articles = soup.find("main", {"class": "listing-items"}).find_all(
                    "article"
                )
            else:  # we reach the end
                self.browser.quit()
                return ids

            for article in articles:
                id_ = article.get("data-element-id")
                if id_ is not None:
                    ids.append(int(id_))

            current_page += 1
            wait()
