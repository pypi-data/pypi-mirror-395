from typing import Union

COUNTRY_CODES = {
    "000-019": "United States and Canada",
    "020-029": "Restricted distribution (MO defined)",
    "030-039": "United States drugs (MO defined)",
    "040-049": "Restricted distribution (MO defined)",
    "050-059": "Coupons",
    "060-099": "United States and Canada",
    "100-139": "United States",
    "200-299": "Restricted distribution (MO defined)",
    "300-379": "France and Monaco",
    "380": "Bulgaria",
    "383": "Slovenia",
    "385": "Croatia",
    "387": "Bosnia and Herzegovina",
    "389": "Montenegro",
    "400-440": "Germany",
    "450-459": "Japan",
    "460-469": "Russia",
    "470": "Kyrgyzstan",
    "471": "Taiwan",
    "474": "Estonia",
    "475": "Latvia",
    "476": "Azerbaijan",
    "477": "Lithuania",
    "478": "Uzbekistan",
    "479": "Sri Lanka",
    "480": "Philippines",
    "481": "Belarus",
    "482": "Ukraine",
    "484": "Moldova",
    "485": "Armenia",
    "486": "Georgia",
    "487": "Kazakhstan",
    "489": "Hong Kong",
    "490-499": "Japan",
    "500-509": "United Kingdom",
    "520-521": "Greece",
    "528": "Lebanon",
    "529": "Cyprus",
    "530": "Albania",
    "531": "Macedonia",
    "535": "Malta",
    "539": "Ireland",
    "540-549": "Belgium and Luxembourg",
    "560": "Portugal",
    "569": "Iceland",
    "570-579": "Denmark, Faroe Islands and Greenland",
    "590": "Poland",
    "594": "Romania",
    "599": "Hungary",
    "600-601": "South Africa",
    "603": "Ghana",
    "604": "Senegal",
    "608": "Bahrain",
    "609": "Mauritius",
    "611": "Morocco",
    "613": "Algeria",
    "616": "Kenya",
    "618": "Ivory Coast",
    "619": "Tunisia",
    "621": "Syria",
    "622": "Egypt",
    "624": "Libya",
    "625": "Jordan",
    "626": "Iran",
    "627": "Kuwait",
    "628": "Saudi Arabia",
    "629": "United Arab Emirates",
    "640-649": "Finland",
    "690-695": "China",
    "700-709": "Norway",
    "729": "Israel",
    "730-739": "Sweden",
    "740": "Guatemala",
    "741": "El Salvador",
    "742": "Honduras",
    "743": "Nicaragua",
    "744": "Costa Rica",
    "745": "Panama",
    "746": "Dominican Republic",
    "750": "Mexico",
    "754-755": "Canada",
    "759": "Venezuela",
    "760-769": "Switzerland and Liechtenstein",
    "770": "Colombia",
    "773": "Uruguay",
    "775": "Peru",
    "777": "Bolivia",
    "779": "Argentina",
    "780": "Chile",
    "784": "Paraguay",
    "785": "Peru",
    "786": "Ecuador",
    "789-790": "Brazil",
    "800-839": "Italy, San Marino and Vatican City",
    "840-849": "Spain and Andorra",
    "850": "Cuba",
    "858": "Slovakia",
    "859": "Czech Republic",
    "860": "Serbia",
    "865": "Mongolia",
    "867": "North Korea",
    "868-869": "Turkey",
    "870-879": "Netherlands",
    "880": "South Korea",
    "884": "Cambodia",
    "885": "Thailand",
    "888": "Singapore",
    "890": "India",
    "893": "Vietnam",
    "896": "Pakistan",
    "899": "Indonesia",
    "900-919": "Austria",
    "930-939": "Australia",
    "940-949": "New Zealand",
    "950": "GS1 Global Office: Special applications",
    "951": "EPCglobal: Special applications",
    "955": "Malaysia",
    "958": "Macau",
    "960-969": "GS1 UK: GTIN-8 allocations",
    "977": "Serial publications (ISSN)",
    "978-979": "Bookland (ISBN)",
    "980": "Refund receipts",
    "981-982": "Common Currency Coupons",
    "990-999": "Coupons",
}


class EAN:
    """
    A class used to represent an EAN-13 (either EAN-13 or EAN-8).
    """
    def __init__(self, ean):
        """
        Args:
            ean (str): The EAN-13 to validate and format.

        Examples:
            >>> EAN('9783161484100')
            EAN(9783161484100)
            >>> EAN('978-3-16-148410-0')
            EAN(9783161484100)

        Raises:
            ValueError: If the EAN-13 is invalid (either format is incorrect or check digit is incorrect).
        """
        self.ean = self._sanitize_and_normalize_ean(ean)
        is_valid = self.is_valid()
        if not is_valid:
            raise ValueError("Invalid EAN, check digit is incorrect")

    def _sanitize_and_normalize_ean(self, ean):
        # Sanitize and normalize the provided EAN-13
        ean = ean.replace("-", "").replace(" ", "").lower()
        normalize = ''.join(char for char in ean if char.isdigit())
        # if len(normalize) == 13 or len(normalize) == 8:
        if len(normalize) == 13:
            return normalize
        else:
            raise ValueError("Invalid EAN, format is incorrect")

    def _break_down_ean_13(self) -> list[str]:
        """
        Breaks down an EAN-13 into its parts.

        Returns:
            list[str]: A list of strings containing the EAN-13 parts.
        """
        parts = [
            "Country: " + self.ean[:3],
            "Manufacturer/Product: " + self.ean[3:12],
            "Check digit: " + self.ean[12]
        ]

        return parts

    def _break_down_ean_8(self) -> list[str]:
        """
        Breaks down an EAN-8 into its parts.

        Returns:
            list[str]: A list of strings containing the EAN-8 parts.
        """
        parts = [
            "Country: " + self.ean[:3],
            "Manufacturer/Product: " + self.ean[3:7],
            "Check digit: " + self.ean[7]
        ]

        return parts

    def break_down_ean(self) -> list[str]:
        """
        Breaks down an EAN-13 or EAN-8 into its parts.

        Returns:
            list[str]: A list of strings containing the EAN-13 or EAN-8 parts.
        """
        if len(self.ean) == 13:
            return self._break_down_ean_13()
        elif len(self.ean) == 8:
            return self._break_down_ean_8()
        else:
            raise ValueError("Invalid EAN")

    def is_valid(self) -> bool:
        """
        Validates an EAN-13 by checking if the check digit is correct.

        Returns:
            bool: True if the EAN-13 is valid, False otherwise.

        Examples:
            >>> EAN('9783161484100').is_valid()
            True
            >>> EAN('9783161484105').is_valid()
            False
        """
        check_digit = sum(int(self.ean[i]) * (1 if i % 2 == 0 else 3) for i in range(12))
        check_digit = (10 - (check_digit % 10)) % 10
        return check_digit == int(self.ean[-1])

    def format(self) -> str:
        """
        Formats an EAN-13 by adding dashes.

        Returns:
            str: The formatted EAN-13.
        """
        return self.ean

    def get_country_name(self) -> str:
        """
        Gets the country name of the EAN-13.

        Returns:
            str: The country name of the EAN-13.
        """
        country_code = self.ean[:3]
        for key in COUNTRY_CODES:
            codes = key.split("-")
            if len(codes) == 1 and codes[0] == country_code:
                return COUNTRY_CODES[key]
            elif len(codes) != 1 and int(codes[0]) <= int(country_code) <= int(codes[1]):
                return COUNTRY_CODES[key]
        return "Unknown"

    def __str__(self):
        return self.format()

    def __repr__(self):
        return f"EAN({self.format()})"

    def __eq__(self, other: Union[object, str]) -> bool:
        """
        Compares two EAN-13s.

        Args:
            other (EAN or str): The EAN-13 to compare to.

        Returns:
            bool: True if the EAN-13s are equal, False otherwise.

        Examples:
            >>> EAN('9783161484100') == EAN('9783161484100')
            True
            >>> EAN('9783161484100') == '9783161484100'
            True
        """
        if isinstance(other, EAN):
            return self.ean == other.ean
        elif isinstance(other, str):
            return self.ean == other
        else:
            return False
