from typing import Union

from worker.wellbore.model.ann import Ann
from worker.wellbore.model.drillstring_components import Pipe
from worker.wellbore.model.hole_section import HoleSection


class SectionsMixin(object):
    def __init__(self, *args, **kwargs):
        self.sections = []

    def __len__(self):
        return len(self.sections)

    def __getitem__(self, index):
        return self.sections[index]

    def __delitem__(self, index):
        del self.sections[index]

    def __bool__(self):
        return len(self) != 0

    def __repr__(self):
        return "\n".join(str(sec) for sec in self.sections)

    def compute_volume(self, top_depth: float, bottom_depth: float) -> float:
        """
        Compute the volume between two depths
        :param top_depth: in ft
        :param bottom_depth: in ft
        :return: volume in cuft
        """
        volume = 0
        for element in self:
            if element.top_depth <= bottom_depth <= element.bottom_depth:
                volume += (bottom_depth - top_depth) * element.area / 144
                break

            elif element.top_depth <= top_depth <= element.bottom_depth:
                volume += (element.bottom_depth - top_depth) * element.area / 144
                top_depth = element.bottom_depth

        return volume

    def find_section_at_measured_depth(
        self, measured_depth: float, at_exact_measured_depth: bool = False
    ) -> Union[HoleSection, Ann, Pipe, None]:
        """
        :param measured_depth:
        :param at_exact_measured_depth:
        :return:
        """
        if measured_depth > self[-1].bottom_depth:
            return None

        for sec in self:
            if sec.top_depth < measured_depth <= sec.bottom_depth:
                return sec

        if at_exact_measured_depth:
            return None

        return self[0]
