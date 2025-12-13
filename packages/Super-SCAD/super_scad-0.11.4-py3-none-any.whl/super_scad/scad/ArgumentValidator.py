from typing import List, Set


class ArgumentValidator:
    """
    Class for the validation of arguments of a SupeSCAD widget constructor.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, args):
        """
        Object constructor.

        """
        self.__arguments_set: Set[str] = set(name for name, value in args.items() if value is not None)
        """
        A set with all the none empty arguments passed to the constructor of a ScadWidget.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _to_string(sets: List[Set[str] | str]) -> str:
        """

        """
        if len(sets) == 0:
            return ''

        if len(sets) == 1:
            return str(sets[0])

        if len(sets) == 2:
            return str(sets[0]) + ' and ' + str(sets[1])

        ret = ''
        for i in range(len(sets) - 1):
            ret += str(sets[i]) + ', '
        ret += 'and ' + str(sets[-1])

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def validate_exclusive(self, *args: Set[str] | str) -> None:
        """
        Validates that only arguments belonging to one of the given sets are passed to the constructor of the SuperScad
        widget.
        """
        supplied_sets = []
        for index, arg in enumerate(args):
            if isinstance(arg, str):
                supplied = arg in self.__arguments_set
            elif isinstance(arg, set):
                supplied = set.intersection(self.__arguments_set, arg)
            else:
                raise TypeError(f'Argument {index + 1} must be a set or str, got a {type(arg)} instead.')
            if supplied:
                supplied_sets.append(supplied)

        if len(supplied_sets) > 1:
            sets = self._to_string(supplied_sets)
            raise ValueError(f'The following set of arguments are not exclusive: {sets}.')

    # ------------------------------------------------------------------------------------------------------------------
    def validate_required(self, *args: Set[str] | str) -> None:
        """
        Validates that at least one argument belonging to each of the given sets are passed to the constructor of the
        SuperSCAD widget.
        """
        for index, arg in enumerate(args):
            if isinstance(arg, str):
                supplied = arg in self.__arguments_set
                if not supplied:
                    raise ValueError(f'Argument {arg} is mandatory.')
            elif isinstance(arg, set):
                supplied = set.intersection(self.__arguments_set, arg)
                if not supplied:
                    raise ValueError(f'At least one of these arguments {str(arg)} must be supplied.')
            else:
                raise TypeError(f'Argument {index + 1} must be a set or str, got a {type(arg)} instead.')

    # ------------------------------------------------------------------------------------------------------------------
    def validate_count(self, count: int, *args: Set[str] | str) -> None:
        """
        Validates that exactly the given number of arguments are passed to the constructor of the SuperSCAD widget.
        """
        actual = 0
        for index, arg in enumerate(args):
            if isinstance(arg, str):
                if arg in self.__arguments_set:
                    actual += 1
            elif isinstance(arg, set):
                if set.intersection(self.__arguments_set, arg):
                    actual += 1
            else:
                raise TypeError(f'Argument {index + 1} must be a set or str, got a {type(arg)} instead.')

        if actual != count:
            arguments = self._to_string(list(args))
            raise ValueError(f'Of arguments {arguments} exactly {count} must be supplied, got {actual} instead.')

# ----------------------------------------------------------------------------------------------------------------------
