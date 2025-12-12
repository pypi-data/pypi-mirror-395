from worker.data.operations import get_data_by_path, nanround


class Element:
    """
    This is a base object for any element in the wellbore:
    - Pipe, and Bit
    - Hole section
    - Annulus section
    """

    def __init__(self, **kwargs):
        """
        Set the element properties through kwargs. The keys are:
        - 'top_depth'
        - 'length'
        - 'bottom_depth'
        """
        self.top_depth = None
        self.bottom_depth = None
        self.length = None

        if {"top_depth", "length"} <= kwargs.keys():
            self.top_depth = get_data_by_path(kwargs, "top_depth", func=float)
            self.length = get_data_by_path(kwargs, "length", func=float)
            self.set_bottom_depth()
        elif {"top_depth", "bottom_depth"} <= kwargs.keys():
            self.top_depth = get_data_by_path(kwargs, "top_depth", func=float)
            self.bottom_depth = get_data_by_path(kwargs, "bottom_depth", func=float)
            self.set_length()
        elif "length" in kwargs:
            self.length = get_data_by_path(kwargs, "length", func=float)
        else:
            raise KeyError("Missing keys: 'top_depth', 'bottom_depth', and 'length'")

    def set_length(self, length: float = None):
        if length is None:
            length = self.bottom_depth - self.top_depth
        self.length = length

    def set_bottom_depth(self, bottom_depth: float = None):
        if bottom_depth is None:
            bottom_depth = self.top_depth + self.length
        self.bottom_depth = bottom_depth

    def set_top_depth(self, top_depth: float = None):
        if top_depth is None:
            top_depth = self.bottom_depth - self.length
        self.top_depth = top_depth

    @property
    def area(self):
        return self.compute_get_area()

    def compute_get_area(self):
        """
        Compute the area of the element
        :return: area of the element in INCH^2
        :return:
        """
        raise NotImplementedError()

    @property
    def volume(self):
        return self.compute_get_volume()

    def compute_get_volume(self):
        """
        Compute the volume of the element
        :return: volume in FOOT^3
        """
        raise NotImplementedError()

    def cmp(self, measured_depth: float) -> int:
        """
        To check the position of the given measured depth vs the current section
        if measured depth is closer to surface compared to the annulus it returns -1,
        and if deeper it returns +1 and otherwise it is 0
        :param measured_depth:
        :return: -1: above, 0: at, +1: below
        """
        if measured_depth <= self.top_depth:
            return -1

        if self.bottom_depth < measured_depth:
            return +1

        return 0

    def __contains__(self, measured_depth: float):
        """
        To check if this element covers the given measured depth.
        :param measured_depth:
        :return:
        """
        return self.top_depth < measured_depth <= self.bottom_depth

    def __repr__(self):
        return (
            f"{nanround(self.length, 2):>8} ft --> {nanround(self.top_depth, 2):>8} ft "
            f"- {nanround(self.bottom_depth, 2):>8} ft"
        )
