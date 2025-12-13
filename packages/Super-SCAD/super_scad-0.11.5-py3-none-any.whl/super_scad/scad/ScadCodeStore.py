class ScadCodeStore:
    """
    Class for storing and formatting OpensSCAD code.
    """
    C_INDENTATION: int = 3

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        self.__lines: list[str] = list()
        """
        The stored code.
        """

        self.__indent_level: int = 0
        """
        The current indentation level.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def add_line(self, line: str):
        """
        Adds a line to the code.

        :param line: The line.
        """
        if line == '{':
            self.__lines.append(' ' * (ScadCodeStore.C_INDENTATION * self.__indent_level) + line)
            self.__indent_level += 1
        elif line == '}':
            self.__indent_level = max(0, self.__indent_level - 1)
            self.__lines.append(' ' * (ScadCodeStore.C_INDENTATION * self.__indent_level) + line)
        else:
            self.__lines.append(' ' * (ScadCodeStore.C_INDENTATION * self.__indent_level) + line)

        return self

    # ------------------------------------------------------------------------------------------------------------------
    def append_to_last_line(self, part: str) -> None:
        """
        Appends a part of code to the last line.

        :param part: The part of code.
        """
        self.__lines[-1] += part

    # ------------------------------------------------------------------------------------------------------------------
    def clear(self) -> None:
        """
        Clears the code.
        """
        self.__lines = []
        self.__indent_level = 0

    # ------------------------------------------------------------------------------------------------------------------
    def get_code(self) -> str:
        """
        Returns the code as a string.
        """
        return '\n'.join(self.__lines)

    # ------------------------------------------------------------------------------------------------------------------
    def line_count(self) -> int:
        """
        Returns the number of lines in the code.
        """
        return len(self.__lines)

# ----------------------------------------------------------------------------------------------------------------------
