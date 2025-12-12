from typing import Union


class ISBN:
    """
    A class used to represent an ISBN (either ISBN-13 or ISBN-10).
    """
    def __init__(self, isbn):
        """
        Args:
            isbn (str): The ISBN to validate and format.

        Examples:
            >>> ISBN('978-1-86197-876-9')
            ISBN(978-1-86197-876-9)
            >>> ISBN('0-306-40615-2')
            ISBN(0-306-40615-2)
            >>> ISBN('9780306406157')
            ISBN(9-780-306-40615-7)

        Raises:
            ValueError: If the ISBN is invalid (either format is incorrect or check digit is incorrect).
        """
        self.isbn = self._sanitize_and_normalize_isbn(isbn)
        is_valid = self.is_valid()
        if not is_valid:
            raise ValueError("Invalid ISBN, check digit is incorrect")

    def _sanitize_and_normalize_isbn(self, isbn):
        # Sanitize and normalize the provided ISBN
        isbn = isbn.replace("-", "").replace(" ", "").upper()
        normalize = ''.join(char for char in isbn if char.isdigit() or char == 'X')
        if len(normalize) == 10 or len(normalize) == 13:
            return normalize
        else:
            raise ValueError("Invalid ISBN, format is incorrect")

    def _break_down_isbn_13(self) -> list[str]:
        """
        Breaks down an ISBN-13 into its parts.

        Returns:
            list[str]: A list of strings containing the ISBN-13 parts.
        """
        parts = [
            "Prefix: " + self.isbn[:3],
            "Registration group: " + self.isbn[3],
            "Registrant: " + self.isbn[4:9],
            "Publication: " + self.isbn[9:12],
            "Check digit: " + self.isbn[12]
        ]

        return parts

    def _break_down_isbn_10(self) -> list[str]:
        """
        Breaks down an ISBN-10 into its parts.

        Returns:
            list[str]: A list of strings containing the ISBN-10 parts.
        """
        parts = [
            "Group: " + self.isbn[:2],
            "Publisher: " + self.isbn[2:6],
            "Title: " + self.isbn[6:9],
            "Check digit: " + self.isbn[-1]
        ]

        return parts

    def break_down_isbn(self) -> list[str]:
        """
        Breaks down an ISBN into its parts.

        Returns:
            list[str]: A list of strings containing the ISBN parts.

        Example:
            >>> ISBN('9780306406157').break_down_isbn()
            ['Prefix: 978', 'Registration group: 0', 'Registrant: 30640', 'Publication: 615', 'Check digit: 7']
            >>> ISBN('0306406152').break_down_isbn()
            ['Group: 03', 'Publisher: 0640', 'Title: 615', 'Check digit: 2']
        """
        if len(self.isbn) == 13:
            return self._break_down_isbn_13()
        elif len(self.isbn) == 10:
            return self._break_down_isbn_10()
        else:
            raise ValueError("Invalid ISBN")

    def _is_isbn_13_valid(self) -> bool:
        """
        Checks the validity of an ISBN-13, allowing for dashes and lowercase characters.

        Returns:
            bool: True if the ISBN-13 is valid, False otherwise.
        """
        # (a * 1 + b * 3 + c * 1 + d * 3 + e * 1 + f * 3 + g * 1 + h * 3 + i * 1 + j * 3 + k * 1 + l * 3) % 10
        check_sum = sum(int(digit) * (1 if index % 2 == 0 else 3) for index, digit in enumerate(self.isbn[:-1]))
        calculated_check_digit = (10 - (check_sum % 10)) % 10
        return calculated_check_digit == int(self.isbn[-1])

    def _is_isbn_10_valid(self) -> bool:
        """
        Checks the validity of an ISBN-10, allowing for dashes and lowercase characters.

        Returns:
            bool: True if the ISBN-10 is valid, False otherwise.
        """
        # (a * 1 + b * 2 + c * 3 + d * 4 + e * 5 + f * 6 + g * 7 + h * 8 + i * 9 + j * 10 + k * 11) % 11
        check_sum = sum((i + 1) * int(digit) if digit != 'X' else 10 for i, digit in enumerate(self.isbn[:-1]))
        return check_sum % 11 == int(self.isbn[-1]) if self.isbn[-1] != 'X' else check_sum % 11 == 10

    def is_valid(self) -> bool:
        """
        Checks the validity of an ISBN (either ISBN-13 or ISBN-10), allowing for dashes and lowercase characters.

        Returns:
            bool: True if the ISBN is valid, False otherwise.
        """
        if len(self.isbn) == 13:
            return self._is_isbn_13_valid()
        elif len(self.isbn) == 10:
            return self._is_isbn_10_valid()
        else:
            return False

    def format(self) -> str:
        """
        Formats an ISBN by adding dashes for better readability after normalizing the input.
    
        Returns:
            str: The formatted ISBN.
    
        Examples:
            >>> ISBN('9783161484105').format()
            '978-3-16-148410-5'
            >>> ISBN('316148410X').format()
            '3-16-148410-X'
            >>> ISBN('9781861978769').format()
            '978-1-86-197876-9'
        """
        if len(self.isbn) == 10:
            return f"{self.isbn[:1]}-{self.isbn[1:4]}-{self.isbn[4:9]}-{self.isbn[9]}"
        elif len(self.isbn) == 13:
            return f"{self.isbn[:3]}-{self.isbn[3:4]}-{self.isbn[4:6]}-{self.isbn[6:12]}-{self.isbn[12]}"

    def _generate_isbn_13_check_digit(self, prefix: str = "978") -> int:
        """
        Generates the check digit for an ISBN-13.

        Args:
            prefix (str, optional): The EAN-13 prefix to use for ISBN-10. Defaults to "978".

        Returns:
            int: The check digit.

        Examples:
            >>> ISBN('0306406152')._generate_isbn_13_check_digit()
            7
            >>> ISBN('0306406152')._generate_isbn_13_check_digit("979")
            7
            >>> ISBN('9783161484105')._generate_isbn_13_check_digit()
            5

        Raises:
            ValueError: If the prefix is invalid.
        """
        if prefix not in ("978", "979"):
            raise ValueError("Invalid prefix")

        check_sum = sum(int(digit) * (1 if index % 2 == 0 else 3) for index, digit in enumerate(prefix + self.isbn[:-1]))
        return (10 - (check_sum % 10)) % 10

    def _isbn_10_to_isbn_13(self, prefix: str = "978") -> object:
        """
        Converts an ISBN-10 to ISBN-13.

        Args:
            prefix (str, optional): The EAN-13 prefix to use for ISBN-10. Defaults to "978".

        Returns:
            ISBN: The converted ISBN-13.

        Examples:
            >>> ISBN('0306406152')._isbn_10_to_isbn_13()
            ISBN(978-0-30-640615-7)
            >>> ISBN('0306406152')._isbn_10_to_isbn_13("979")
            ISBN(979-0-30-640615-7)
            >>> ISBN('9783161484105')._isbn_10_to_isbn_13()
            ISBN(978-3-16-148410-5)

        Raises:
            ValueError: If the prefix is invalid.
        """
        if prefix not in ("978", "979"):
            raise ValueError("Invalid prefix")

        return ISBN(prefix + self.isbn[:-1] + str(self._generate_isbn_13_check_digit(prefix)))

    def to_isbn_13(self, prefix: str = "978") -> str:
        """
        Converts an ISBN-10 to ISBN-13.

        Args:
            prefix (str, optional): The EAN-13 prefix to use for ISBN-10. Defaults to "978".

        Returns:
            str: The converted ISBN-13.

        Examples:
            >>> ISBN('0306406152').to_isbn_13()
            '9780306406157'
            >>> ISBN('0306406152').to_isbn_13("979")
            '9790306406157'
            >>> ISBN('9783161484105').to_isbn_13()
            '9783161484105'
        """
        if prefix not in ("978", "979"):
            raise ValueError("Invalid prefix")

        if len(self.isbn) == 10:
            return self._isbn_10_to_isbn_13(prefix).format()
        elif len(self.isbn) == 13:
            return self.format()

    def to_ean_13(self, prefix: str = "978") -> str:
        """
        Converts an ISBN to EAN-13.

        Args:
            prefix (str, optional): The EAN-13 prefix to use for ISBN-10. Defaults to "978".

        Returns:
            str: The converted EAN-13.

        Examples
            >>> ISBN('0306406152').to_ean_13()
            '9780306406157'
            >>> ISBN('0306406152').to_ean_13("979")
            '9790306406157'
            >>> ISBN('9783161484105').to_ean_13()
            '9783161484105'
        """
        if prefix not in ("978", "979"):
            raise ValueError("Invalid prefix")

        if len(self.isbn) == 10:
            return self._isbn_10_to_isbn_13(prefix).isbn
        elif len(self.isbn) == 13:
            return self.isbn

    def __str__(self):
        return self.format()

    def __repr__(self):
        return f"ISBN({self.format()})"

    def __eq__(self, other: Union[object, str]) -> bool:
        """
        Compares two ISBNs.

        Args:
            other (ISBN or str): The other ISBN to compare to.

        Returns:
            bool: True if the ISBNs are equal, False otherwise.

        Examples:
            >>> ISBN('978-1-86197-876-9') == ISBN('978-1-86197-876-9')
            True
            >>> ISBN('978-1-86197-876-9') == '978-1-86197-876-9'
            True
        """
        if isinstance(other, ISBN):
            return self.isbn == other.isbn
        elif isinstance(other, str):
            return self.isbn == ISBN(other).isbn
        else:
            return False
