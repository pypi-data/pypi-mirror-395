from typing import List

from worker.data.serialization import serialization
from worker.wellbore.measured_depth_finder import get_unique_measured_depths
from worker.wellbore.model.ann import Ann
from worker.wellbore.model.drillstring import Drillstring
from worker.wellbore.model.enums import PipeType
from worker.wellbore.model.hole import Hole
from worker.wellbore.sections_mixin import SectionsMixin


@serialization
class Annulus(SectionsMixin):
    SERIALIZED_VARIABLES = {"sections": list}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sections: List[Ann] = kwargs.get("sections") or []

        drillstring: Drillstring = kwargs.get("drillstring")
        hole: Hole = kwargs.get("hole")
        if drillstring and hole:
            self.create_annulus(drillstring, hole)

    def add_section(self, section: Ann):
        """
        Add a new ann section to the end of the sections.
        :param section:
        :return:
        """
        if self:
            section.top_depth = self[-1].bottom_depth

        section.set_bottom_depth()

        self.sections.append(section)

    def insert_section(self, section: Ann, index: int):
        """
        Insert a new pipe element in the given index.
        :param section:
        :param index:
        :return:
        """
        if index is not None:
            if self:
                section.top_depth = self[index - 1].bottom_depth
            section.set_bottom_depth()

            self.sections.insert(index, section)

            for i in range(index + 1, len(self)):
                self[i].top_depth = self[i - 1].bottom_depth
                self[i].set_bottom_depth()

    def check_for_concatenation(self):
        """
        Concatenate the adjacent section with the same ID and OD and hole type
        """
        for i in range(len(self) - 2, -1, -1):
            if self[i].eq_without_length(self[i + 1]):
                self[i].set_bottom_depth(self[i + 1].bottom_depth)
                self[i].set_length()
                del self[i + 1]

    def create_annulus(self, drillstring: Drillstring, hole: Hole):
        """
        Create annulus for a given drillstring and hole configuration
        :return:
        """
        self.sections = []

        md_list = get_unique_measured_depths(drillstring, hole)
        md_list = [md for md in md_list if md <= drillstring[-1].bottom_depth]
        epsilon = 0.0001
        for i in range(len(md_list) - 1):
            hole_section = hole.find_section_at_measured_depth(md_list[i] + epsilon, True)
            if not hole_section:
                continue

            drillstring_section = drillstring.find_section_at_measured_depth(md_list[i] + epsilon, False)
            annulus_section = Ann(**{"top_depth": md_list[i], "bottom_depth": md_list[i + 1]})

            # If there is no drillstring_section when the bit is at surface (0ft) or once we reach the bit in the loop
            # stop looping
            if not drillstring_section or drillstring_section.pipe_type == PipeType.BIT:
                break

            annulus_section.set_properties_from_pipe_section(drillstring_section)
            annulus_section.set_properties_from_hole(hole_section)

            self.add_section(annulus_section)

        if not self:
            return

        # extend the last segment to be equal to the bit depth since the bit has been removed
        bit_depth = drillstring.bit_depth
        self[-1].set_bottom_depth(bit_depth)
        self[-1].set_length()

        self.check_for_concatenation()

    @property
    def volume(self):
        return sum(sec.volume for sec in self)

    @property
    def bottom_depth(self):
        if not self:
            return 0
        return self[-1].bottom_depth
