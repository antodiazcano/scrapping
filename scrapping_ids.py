from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from utils import wait


class IdsScrapping:
    def __init__(self, base_url: str) -> None:
        self.browser = uc.Chrome()
        self.base_url = base_url

    def _get_new_soup(self, page: int) -> BeautifulSoup:
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
        current_page = 1
        ids = []

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
                return ids

            current_page += 1

            for article in articles:
                id_ = int(article.get("data-element-id"))
                if id_ is not None:
                    ids.append(id_)
                wait()
