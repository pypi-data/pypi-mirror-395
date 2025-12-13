import csv
from typing import Dict


class BOM:
    """
    Class for BOM (Bill of Materials).
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self) -> None:
        """
        Constructor.
        """
        self.__bom: Dict[tuple[str, str], int] = {}

    # ------------------------------------------------------------------------------------------------------------------
    def add(self, *, material_type: str, description: str):
        """
        Adds a material to the BOM.

        :param material_type: The type of the material.
        :param description: The description of the material.
        """
        material = (material_type, description)
        if material not in self.__bom:
            self.__bom[material] = 1
        else:
            self.__bom[material] += 1

        return self

    # ------------------------------------------------------------------------------------------------------------------
    def save(self, filename: str) -> None:
        """
        Saves the BOM to a file.

        :param filename: The filename to save the BOM to.
        """
        with open(filename, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['#', 'Material', 'Description'])
            for entry in sorted(self.__bom):
                writer.writerow([self.__bom[entry], entry[0], entry[1]])

# ----------------------------------------------------------------------------------------------------------------------
