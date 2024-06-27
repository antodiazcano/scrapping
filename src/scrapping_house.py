import re
import numpy as np
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException

from src.utils import wait

# pip install lxml


class HouseScrapping:
    def __init__(self, url: str) -> None:
        """ """

        self.url = url
        browser = uc.Chrome()
        browser.get(url)
        wait()
        try:
            browser.find_element(
                "xpath", "//*[@id='didomi-notice-disagree-button']"
            ).click()
        except NoSuchElementException:
            pass
        html = browser.page_source
        self.soup = BeautifulSoup(html, "lxml")
        browser.quit()

    def _get_title(self) -> str:
        """ """

        return re.sub(
            r"\s+",
            " ",
            self.soup.find("span", {"class": "main-info__title-main"}).text.replace(
                "\n", ""
            ),
        )

    def _get_type(self) -> str:
        """ """
        if "piso" in re.sub(
            r"\s+",
            " ",
            self.soup.find("span", {"class": "main-info__title-main"})
            .text.replace("\n", "")
            .lower(),
        ):
            return "flat"

        return "house"

    def _get_location(self) -> str:
        """ """

        return re.sub(
            r"\s+",
            " ",
            self.soup.find("span", {"class": "main-info__title-minor"}).text.split(",")[
                0
            ],
        )

    def _get_price(self) -> int:
        """ """

        return int(self.soup.find("span", {"class": "txt-bold"}).text.replace(".", ""))

    def _get_m2(self) -> int | None:
        """ """

        for characteristic in self.soup.find(
            "div", {"class": "details-property-feature-one"}
        ).find_all("li"):
            if "construidos" in characteristic.text.lower():
                words = characteristic.text.split(" ")
                if "útiles" in characteristic.text:
                    return int(words[-3].replace(".", ""))
                else:
                    return int(words[0].replace(".", ""))

        return None

    def _get_status(self) -> str | None:
        """ """

        for characteristic in self.soup.find(
            "div", {"class": "details-property-feature-one"}
        ).find_all("li"):
            if "segunda mano" in characteristic.text.lower():
                return characteristic.text

        return None

    def _get_floor(self) -> str | None:
        """ """

        for characteristic in self.soup.find(
            "div", {"class": "details-property-feature-one"}
        ).find_all("li"):
            if "planta" in characteristic.text.lower():
                return characteristic.text

        return None

    def _get_description(self) -> str:
        """ """

        try:
            return re.sub(
                r"\s+",
                " ",
                self.soup.find(
                    "div", {"class": "adCommentsLanguage expandable is-expandable"}
                )
                .find("p")
                .text.replace("\n", ""),
            )
        except AttributeError:
            return re.sub(
                r"\s+",
                " ",
                self.soup.find(
                    "div",
                    {
                        "class": "adCommentsLanguage expandable is-expandable with-expander-button"
                    },
                )
                .find("p")
                .text.replace("\n", ""),
            )

    def _get_number_of_photos(self) -> int:
        """ """

        photos_horizontal = self.soup.find_all(
            "div",
            {
                "class": "placeholder-multimedia image overlay-box horizontal printable mb-small"
            },
        )
        photos_vertical = self.soup.find_all(
            "div",
            {
                "class": "placeholder-multimedia image overlay-box vertical printable mb-small"
            },
        )
        hidden_photos_horizontal = self.soup.find_all(
            "div",
            {"class": "placeholder-multimedia image overlay-box horizontal mb-small"},
        )
        hidden_photos_vertical = self.soup.find_all(
            "div",
            {"class": "placeholder-multimedia image overlay-box vertical mb-small"},
        )

        photos = (
            photos_horizontal
            + photos_vertical
            + hidden_photos_horizontal
            + hidden_photos_vertical
        )
        photos = [str(photo) for photo in photos if "plano" not in str(photo).lower()]

        return len(photos)

    def _get_number_of_rooms(self) -> int | None:
        """ """

        for characteristic in self.soup.find(
            "div", {"class": "details-property-feature-one"}
        ).find_all("li"):
            if (
                "habitaciones" in characteristic.text.lower()
                or "habitación" in characteristic.text.lower()
            ):
                return int(characteristic.text[0])
        return None

    def _get_number_of_bathrooms(self) -> int | None:
        """ """

        for characteristic in self.soup.find(
            "div", {"class": "details-property-feature-one"}
        ).find_all("li"):
            if (
                "baños" in characteristic.text.lower()
                or "baño" in characteristic.text.lower()
            ):
                return int(characteristic.text[0])
        return None

    def _get_particular(self) -> bool:
        """ """

        return "particular" in self.soup.find("div", {"class": "name"}).text.lower()

    def _get_luxury(self) -> bool:
        """ """

        try:
            return (
                True
                if self.soup.find("div", {"class": "detail-info-tags"})
                .find("span", {"class": "tag"})
                .text
                else False
            )
        except AttributeError:
            return False

    def _get_video(self) -> bool:
        """ """

        try:
            return (
                True
                if self.soup.find(
                    "button", {"class": "multimedia-shortcuts-button btn video"}
                ).text
                else False
            )
        except AttributeError:
            return False

    def _get_virtual_tour(self) -> bool:
        """ """

        try:
            return (
                True
                if self.soup.find(
                    "button", {"class": "multimedia-shortcuts-button btn virtual-tour"}
                ).text
                else False
            )
        except AttributeError:
            return False

    def _get_3d_tour(self) -> bool:
        """ """

        try:
            return (
                True
                if self.soup.find(
                    "button", {"class": "multimedia-shortcuts-button btn three-d-tour"}
                ).text
                else False
            )
        except AttributeError:
            return False

    def _get_plane(self) -> bool:
        """ """

        try:
            return (
                True
                if self.soup.find(
                    "button", {"class": "multimedia-shortcuts-button btn plan"}
                ).text
                else False
            )
        except AttributeError:
            return False

    def _get_air_conditioning(self) -> bool:
        """ """

        characteristics = [
            str(characteristic.text).lower()
            for characteristic in self.soup.find(
                "div", {"class": "details-property-feature-two"}
            )
            .find_all("div", {"class": "details-property_features"})[0]
            .find_all("li")
        ]
        return np.min(
            [
                1,
                len(
                    [
                        substring
                        for substring in characteristics
                        if "aire acondicionado" in substring
                    ]
                ),
            ]
        ).astype(bool)

    def _get_heating(self) -> str | None:
        """ """

        for characteristic in self.soup.find(
            "div", {"class": "details-property-feature-one"}
        ).find_all("li"):
            if "calefacción" in characteristic.text.lower():
                return characteristic.text

        return None

    def _get_elevator(self) -> bool | None:
        """ """

        for characteristic in self.soup.find(
            "div", {"class": "details-property-feature-one"}
        ).find_all("li"):
            if "con ascensor" in characteristic.text.lower():
                return True
            elif "sin ascensor" in characteristic.text.lower():
                return False

        return None

    def _get_furnished(self) -> bool | None:
        """ """

        for characteristic in self.soup.find(
            "div", {"class": "details-property-feature-one"}
        ).find_all("li"):
            if "amueblado" in characteristic.text.lower():
                return True
            elif "sin amueblar" in characteristic.text.lower():
                return False

        return None

    def _get_terrace(self) -> str | None:
        """ """

        for characteristic in self.soup.find(
            "div", {"class": "details-property-feature-one"}
        ).find_all("li"):
            if (
                "terraza" in characteristic.text.lower()
                or "balcón" in characteristic.text.lower()
            ):
                return characteristic.text

        return None

    def _get_consume(self) -> str | None:
        """ """

        try:
            consume_string = str(
                self.soup.find("div", {"class": "details-property-feature-two"})
                .find_all("div", {"class": "details-property_features"})[1]
                .find_all("li")[0]
                .find_all("span")[-1]
            )
            return consume_string[consume_string.find("title=") + 7].upper()
        except IndexError:
            return None

    def _get_emisions(self) -> str | None:
        """ """

        try:
            emisions_string = str(
                self.soup.find("div", {"class": "details-property-feature-two"})
                .find_all("div", {"class": "details-property_features"})[1]
                .find_all("li")[1]
                .find_all("span")[-1]
            )
            return emisions_string[emisions_string.find("title=") + 7].upper()
        except IndexError:
            return None

    def get_house_information(self) -> dict:
        """ """

        return {
            "title": self._get_title(),
            "location": self._get_location(),
            "price": self._get_price(),
            "m2": self._get_m2(),
            "type": self._get_type(),
            "status": self._get_status(),
            "floor": self._get_floor(),
            "description": self._get_description(),
            "n_photos": self._get_number_of_photos(),
            "n_rooms": self._get_number_of_rooms(),
            "n_bathrooms": self._get_number_of_bathrooms(),
            "particular": self._get_particular(),
            "luxury": self._get_luxury(),
            "video": self._get_video(),
            "virtual_tour": self._get_virtual_tour(),
            "3d_tour": self._get_3d_tour(),
            "plane": self._get_plane(),
            "air_conditioning": self._get_air_conditioning(),
            "heating": self._get_heating(),
            "elevator": self._get_elevator(),
            "furnished": self._get_furnished(),
            "terrace": self._get_terrace(),
            "consume": self._get_consume(),
            "emisions": self._get_emisions(),
        }
