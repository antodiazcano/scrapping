import re
import numpy as np
from bs4 import BeautifulSoup

# pip install lxml


class HouseScraping:
    def __init__(self, soup: BeautifulSoup) -> None:
        """
        Constructor of the class.

        Parameters
        ----------
        soup : Soup
        """

        self.soup = soup

    def _get_title(self) -> str:
        """
        Gets the title of the advertisement.
        """

        return re.sub(
            r"\s+",
            " ",
            self.soup.find("span", {"class": "main-info__title-main"}).text.replace(
                "\n", ""
            ),
        )

    def _get_type(self) -> str:
        """
        Gets the type of the house.
        """

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
        """
        Gets the location of the house.
        """

        return re.sub(
            r"\s+",
            " ",
            self.soup.find("span", {"class": "main-info__title-minor"}).text.split(",")[
                0
            ],
        )

    def _get_price(self) -> int:
        """
        Gets the price of the house.
        """

        return int(self.soup.find("span", {"class": "txt-bold"}).text.replace(".", ""))

    def _get_m2(self) -> int | None:
        """
        Gets the m2 of the house.
        """

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
        """
        Gets the status of the house (new, used...).
        """

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

    def _get_description(self) -> str | None:
        """
        Gets the description of the advertisement.
        """

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
            try:
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
            except AttributeError:
                return None

    def _get_number_of_photos(self) -> int | None:
        """
        Gets the number of photos of the advertisement.
        """

        try:
            try:
                return int(
                    self.soup.find(
                        "span", {"class": "multimedia-shortcuts-button-text"}
                    ).text.split()[0]
                )
            except AttributeError:
                return None
        except ValueError:
            return None

    def _get_number_of_rooms(self) -> int | None:
        """
        Gets the number of rooms of the house.
        """

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
        """
        Gets the number of bathrooms of the house.
        """

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
        """
        Gets if the advertisement is of a particular or a company.
        """

        return "particular" in self.soup.find("div", {"class": "name"}).text.lower()

    def _get_luxury(self) -> bool:
        """
        Gets if the house is of luxury.
        """

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
        """
        Gets it the advertisement has a video.
        """

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
        """
        Gets if the advertisement has a virtual tour.
        """

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
        """
        Gets if the advertisement has a 3d tour.
        """

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
        """
        Gets if the advertisement has a plane of the house.
        """

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
        """
        Gets if the house has air conditioning.
        """

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
        """
        Gets if the house has heating.
        """

        for characteristic in self.soup.find(
            "div", {"class": "details-property-feature-one"}
        ).find_all("li"):
            if "calefacción" in characteristic.text.lower():
                return characteristic.text

        return None

    def _get_elevator(self) -> bool | None:
        """
        Gets if the house has an elevator.
        """

        for characteristic in self.soup.find(
            "div", {"class": "details-property-feature-one"}
        ).find_all("li"):
            if "con ascensor" in characteristic.text.lower():
                return True
            elif "sin ascensor" in characteristic.text.lower():
                return False

        return None

    def _get_furnished(self) -> bool | None:
        """
        Gets if the house is furnished.
        """

        for characteristic in self.soup.find(
            "div", {"class": "details-property-feature-one"}
        ).find_all("li"):
            if "amueblado" in characteristic.text.lower():
                return True
            elif "sin amueblar" in characteristic.text.lower():
                return False

        return None

    def _get_terrace(self) -> str | None:
        """
        Gets if the house has terrace.
        """

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
        """
        Gets the energetic consume of the house.
        """

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
        """
        Gets the emissions of the house.
        """

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

    def get_house_information(self) -> dict[str, int | str | bool | None]:
        """
        Summarises all the information of the house.

        Returns
        -------
        Dict with all fields of the above functions.
        """

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
