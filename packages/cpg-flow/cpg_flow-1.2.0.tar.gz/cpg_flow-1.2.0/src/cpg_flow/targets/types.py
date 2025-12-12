"""
This module defines the `Sex` enumeration, which represents the sex of an individual as specified in the PED format.

Classes:
    Sex (Enum): An enumeration representing the sex of an individual with values UNKNOWN, MALE, and FEMALE.

Methods:
    Sex.parse(sex: str | int | None) -> Sex:
        Parses a string or integer into a `Sex` object. Accepts 'm', 'male', '1', 1 for MALE, 'f', 'female', '2', 2 for FEMALE, and 'u', 'unknown', '0', 0 for UNKNOWN. Raises a ValueError for unrecognized values.

    Sex.__str__() -> str:
        Returns the name of the `Sex` enumeration member as a string.

"""

from enum import Enum


class Sex(Enum):
    """
    Sex as in PED format
    """

    UNKNOWN = 0
    MALE = 1
    FEMALE = 2

    @staticmethod
    def parse(input_sex: str | int | None) -> 'Sex':
        """
        Parse a string into a Sex object.
        """
        if input_sex:
            sex = input_sex.lower() if isinstance(input_sex, str) else input_sex
            if sex in {'m', 'male', '1', 1}:
                return Sex.MALE
            if sex in {'f', 'female', '2', 2}:
                return Sex.FEMALE
            if sex in {'u', 'unknown', '0', 0}:
                return Sex.UNKNOWN
            raise ValueError(f'Unrecognised sex value {input_sex}')
        return Sex.UNKNOWN

    def __str__(self):
        return self.name
