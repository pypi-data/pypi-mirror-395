from typing import List, Tuple

from super_scad.boolean.Compound import Compound
from super_scad.boolean.Difference import Difference
from super_scad.scad.ScadWidget import ScadWidget


class YinYang:
    """
    A helper class for adding and subtracting widgets.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object contructor.
        """
        self._negatives: List[ScadWidget] = []
        self._positives: List[ScadWidget] = []

    # ------------------------------------------------------------------------------------------------------------------
    def __add__(self, other: Tuple[ScadWidget | None, ScadWidget | None]):
        """
        Adds an optional negative and an optional positive widget to the lists of negative and positive widgets.

        :param other: A tuple with an optional negative (the first element of the tuple) and an optional positive
                     (the second element of the tuple) widget.
        """
        if other[0] is not None:
            assert isinstance(other[0], ScadWidget)
            self._negatives.append(other[0])
        if other[1] is not None:
            assert isinstance(other[1], ScadWidget)
            self._positives.append(other[1])

        return self

    # ------------------------------------------------------------------------------------------------------------------
    def apply_negatives_positives(self, body: ScadWidget) -> ScadWidget:
        """
        First, subtracts all negatives from the body and then adds all positives.

        :param body: The body widget.
        """
        if self._negatives:
            body = Difference(children=[body, *self._negatives])
        if self._positives:
            body = Compound(children=[body, *self._positives])

        return body

    # ------------------------------------------------------------------------------------------------------------------
    def apply_positives_negatives(self, body: ScadWidget) -> ScadWidget:
        """
        First, adds all positives to the body and then subtracts all negatives.

        :param body: The body widget.
        """
        if self._positives:
            body = Compound(children=[body, *self._positives])
        if self._negatives:
            body = Difference(children=[body, *self._negatives])

        return body

# ----------------------------------------------------------------------------------------------------------------------
