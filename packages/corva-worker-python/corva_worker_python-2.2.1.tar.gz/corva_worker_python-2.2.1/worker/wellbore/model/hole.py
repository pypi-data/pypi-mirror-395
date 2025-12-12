from copy import deepcopy
from typing import List, Union

from worker.data.operations import get_data_by_path
from worker.data.serialization import serialization
from worker.wellbore.model.enums import HoleType
from worker.wellbore.model.hole_section import HoleSection
from worker.wellbore.sections_mixin import SectionsMixin


@serialization
class Hole(SectionsMixin):
    DEPTH_THRESHOLD = 50  # ft
    LENGTH_THRESHOLD = 1  # ft

    SERIALIZED_VARIABLES = {"sections": list}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sections = kwargs.get("sections") or []

    def add_section(self, section: HoleSection):
        """
        Add a new hole section to the end of the hole.
        :param section:
        :return:
        """
        if not self:
            top_depth = section.top_depth

            if top_depth < Hole.DEPTH_THRESHOLD:
                section.top_depth = 0

        if self:
            section.top_depth = self[-1].bottom_depth

        # bottom depth is the source of truth, so we are updating the length
        section.set_length()

        self.sections.append(section)

    def insert_section(self, section: HoleSection, index: int):
        """
        Insert a new hole section in the given index.
        :param section:
        :param index:
        :return:
        """
        if index is not None:
            if self:
                section.top_depth = self[index - 1].bottom_depth
            section.set_bottom_depth()

            self.sections.insert(index, section)
            self.update_depths(start_index=index + 1)

    def insert_section_after(self, section: HoleSection, section_before: HoleSection):
        index_section_before = self.sections.index(section_before)
        self.insert_section(section, index_section_before + 1)

    def get_bottom_depth(self) -> float:
        if not self:
            return 0
        return self[-1].bottom_depth

    def update_depths(self, start_index: int = 0):
        """
        To update the top and bottom depth of the components
        :param start_index:
        :return:
        """
        if start_index < 1:
            self[0].top_depth = 0
            self[0].set_bottom_depth()
            start_index = 1

        for i in range(start_index, len(self)):
            self[i].top_depth = self[i - 1].bottom_depth
            self[i].set_bottom_depth()

    def get_cased_hole(self):
        """
        Get the cased sections of the hole.
        :return:
        """
        cased_hole = Hole()

        for sec in self:
            if sec.hole_type == HoleType.CASED_HOLE:
                cased_hole.add_section(sec)

        return cased_hole

    def get_open_hole(self):
        """
        Get the open sections of the hole.
        :return:
        """
        open_hole = Hole()

        for sec in self:
            if sec.hole_type == HoleType.OPEN_HOLE:
                open_hole.add_section(sec)

        return open_hole

    def get_casing_bottom_depth(self):
        return self.get_cased_hole().get_bottom_depth()

    def is_casing_exist(self) -> bool:
        """
        Get the cased sections of the hole.
        :return:
        """
        return any(sec.hole_type == HoleType.CASED_HOLE for sec in self)

    def update(self, hole_depth: Union[dict, float]) -> bool:
        """
        Update the last open hole segment of the hole.
        :param hole_depth: a wits dict or actual hole depth
        :return: if any update occurred or not
        """

        # If there are no sections in the hole or the last hole is Open Hole, do not update hole and return
        if not self or self[-1].hole_type != HoleType.OPEN_HOLE:
            return False

        if isinstance(hole_depth, dict):
            hole_depth = get_data_by_path(hole_depth, "data.hole_depth", float)

        # if the hole depth < casing bottom depth, then ignore
        cased_hole_bottom_depth = self.get_cased_hole().get_bottom_depth()
        if hole_depth < cased_hole_bottom_depth:
            return False

        self[-1].set_bottom_depth(hole_depth)
        self[-1].set_length()

        return True

    def set_casings(self, casings: List[dict]):
        """
        Set the casing by providing the list of the jsons
        :param casings: list of casings from API in json dict format
        :return: None
        """
        # TODO we need to consider using 'data.components' if available to set the casings
        self.sections = []

        if not casings:
            return

        # sorting the casings in the ascending order (the smaller the inner_diameter the earlier it is added)
        casings = sorted(casings, key=lambda csg: csg.get("data", {}).get("inner_diameter"))

        # removing the outer casings at the surface
        surface_index = next(
            (
                idx
                for idx, csg in enumerate(casings)
                if csg.get("data", {}).get("top_depth", 1000) < Hole.DEPTH_THRESHOLD
            ),
            0,
        )
        casings = casings[0 : surface_index + 1]

        # finding if a liner is overlapping outer liners
        # this is common in offshore drilling where they set the casings at the sea floor
        index = 1
        while index < len(casings):
            top_depth_inner = casings[index - 1].get("data", {}).get("top_depth", 1000)
            top_depth_outer = casings[index].get("data", {}).get("top_depth", 1000)
            if top_depth_outer + Hole.DEPTH_THRESHOLD > top_depth_inner:
                casings.pop(index)
            else:
                index += 1

        # reversing the order (the larger the inner_diameter the earlier it is)
        casings = reversed(casings)

        for csg in casings:
            hole_section = HoleSection(**csg.get("data", {}), hole_type=HoleType.CASED_HOLE)
            self.add_section(hole_section)

    def update_casings(self, casings: "Hole"):
        """
        To remove the casings of the current hole and
        replace them with the given one
        :param casings:
        :return:
        """
        casings = casings.get_cased_hole()
        # TODO: check if deepcopy is required
        open_holes = deepcopy([sec for sec in self if sec.hole_type == HoleType.OPEN_HOLE])

        self.sections = []
        self.sections.extend(casings)
        self.sections.extend(open_holes)

        self.update_depths()

    def get_min_inner_diameter(self) -> Union[float, None]:
        if not self:
            return None
        return self[-1].inner_diameter

    def get_last_hole_section(self):
        if self:
            return self[-1]
        return None

    def compute_get_total_volume(self, top_depth: float = None, bottom_depth: float = None) -> float:
        """
        Compute the volume of the hole section
        :return: volume of the hole section in FOOT^3
        """
        if top_depth is None and bottom_depth is None:
            return sum(sec.compute_get_volume() for sec in self)

        top_depth = top_depth or 0
        bottom_depth = bottom_depth or self.get_bottom_depth()

        total_volume = 0

        for index, section in enumerate(self):
            if section.bottom_depth <= top_depth:
                continue
            if section.top_depth >= bottom_depth:
                break

            area = section.compute_get_area()  # in INCH^2
            length = min(bottom_depth, section.bottom_depth) - max(top_depth, section.top_depth)  # in FOOT
            volume = area / 144 * length
            total_volume += volume

        return total_volume

    def trim_to_bottom_depth(self, depth):
        if not self.sections:
            return

        self.sections = [section for section in self.sections if section.top_depth <= depth]
        if self.sections:
            self.sections[-1].set_bottom_depth(depth)
            self.sections[-1].set_length()

            if self.sections[-1].length < Hole.LENGTH_THRESHOLD:
                self.sections.pop(-1)

    def trim_to_top_depth(self, depth):
        if not self.sections:
            return

        self.sections = [section for section in self.sections if section.bottom_depth > depth]
        if self.sections:
            self.sections[0].set_top_depth(depth)
            self.sections[0].set_length()

            if self.sections[0].length < Hole.LENGTH_THRESHOLD:
                self.sections.pop(0)

    @staticmethod
    def merge_holes(casing_holes: List):
        """
        This method can be used to merge Holes. The overlapping sections are trimmed and updated.
        The mergedHole is the ultimate hole being generated starting from the bottom and keep adding
        elements (sections) to the top of it.

        :param casing_holes: casingHoles List of holes to be merged from surface to bottom;
        the wider casing is closer to surface (index 0), except for the riser that is always the first section.
        :return: a merged hole
        """
        if not casing_holes:
            return None

        merged_hole = deepcopy(casing_holes[-1])

        if len(casing_holes) == 1:
            return merged_hole

        for i in range(len(casing_holes) - 2, -1, -1):
            casing_hole = casing_holes[i]
            current_section = casing_hole.sections[-1]
            bottom_section = merged_hole.sections[0]

            # comparing the inner diameter of the current section vs the one below
            if current_section.inner_diameter > bottom_section.inner_diameter > 0:
                # normal situation where the casings are telescopic from surface
                casing_hole.trim_to_bottom_depth(bottom_section.top_depth)
            else:
                # in case there is a riser smaller than the casing below.
                merged_hole.trim_to_top_depth(current_section.bottom_depth)

            for j in range(len(casing_hole.sections) - 1, -1, -1):
                merged_hole.sections.insert(0, casing_hole.sections[j])

        return merged_hole
