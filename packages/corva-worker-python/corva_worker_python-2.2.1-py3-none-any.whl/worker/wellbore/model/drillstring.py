from copy import deepcopy
from typing import List, Union

from worker.data.operations import get_data_by_path
from worker.data.serialization import serialization
from worker.wellbore.model.drillstring_components import MWD, PDM, RSS, Agitator, Bit, Pipe, UnderReamer
from worker.wellbore.model.enums import PipeType
from worker.wellbore.model.hole import Hole
from worker.wellbore.sections_mixin import SectionsMixin


@serialization
class Drillstring(SectionsMixin):
    SERIALIZED_VARIABLES = {"sections": list, "mongo_id": str}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mongo_id = kwargs.get("mongo_id")
        self.sections: List[Union[Pipe, Bit]] = kwargs.get("sections") or []
        if args:
            self.set_drillstring(args[0])

    def add_section(self, section: Union[Pipe, Bit]):
        """
        Add a new pipe element to the end of the drillstring.
        :param section:
        :return:
        """
        section.top_depth = 0 if not self else self[-1].bottom_depth
        # length is the source of truth, so we are updating the bottom depth
        section.set_bottom_depth()

        self.sections.append(section)

    def insert_section(self, section: Union[Pipe, Bit], index: int):
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

    def update(self, bit_depth: Union[dict, float]):
        """
        This method gets the bit depth and chops the current drill string to fit the criteria in the wellbore.
        If the drill string length is more than the bit measured depth it chops the extra length from
        surface. And if it is short in length then it extends the top section to the surface.
        In addition, the indices of the special tools are updated accordingly, when the drillstring is chopped.
        :param bit_depth: a wits dict or actual bit depth
        :return:
        """

        if isinstance(bit_depth, dict):
            bit_depth = get_data_by_path(bit_depth, "data.bit_depth", float)

        self[-1].set_bottom_depth(bit_depth)
        self[-1].set_top_depth()

        for i in range(len(self) - 2, -1, -1):
            self[i].set_bottom_depth(self[i + 1].top_depth)
            self[i].set_top_depth()

            if self[i].bottom_depth < 0:
                del self.sections[i]

        self[0].top_depth = 0
        self[0].set_length()

    @property
    def bit_depth(self):
        if not self:
            return None
        return self[-1].bottom_depth

    def set_drillstring(self, drillstring: dict):
        """
        This gets the whole drillstring json and sets it
        :return:
        """
        if not drillstring:
            return

        self.mongo_id = drillstring.get("_id")

        self.sections = []

        # family to class mapping
        mapping = {"bit": Bit, "agitator": Agitator, "pdm": PDM, "mwd": MWD, "rss": RSS, "ur": UnderReamer}

        drillstring_components = drillstring.get("data", {}).get("components", [])
        for component in drillstring_components:
            family = component.get("family", None)
            if family in mapping:
                component = mapping[family](**component)
            else:
                component = Pipe(**component)

            self.add_section(component)

    def perform_qc(self, hole: Hole):
        """
        Removes the items that the pipe OD is equal to or greater than the bit/hole size or OD is equal to 0.
        If the pipe id is zero then set it equal to 0.5 of the OD
        :return:
        """
        bit_diameter = self.get_bit().size

        self.sections = [sec for sec in self.sections if 0 < sec.outer_diameter < bit_diameter]

        for component in self.sections:
            if component.inner_diameter == 0:
                component.inner_diameter = component.outer_diameter / 2

    def compute_get_inside_volume(self):
        """
        Compute and get the inside volume of the pipes of the drill string only,
        not the body and outside of it.
        :return: volume in FOOT^3
        """
        return sum(sec.compute_get_volume() for sec in self)

    def compute_get_outside_volume(self):
        """
        Compute and get the outside volume of the pipes of the drill string only,
        using outer diameter
        :return: volume in FOOT^3
        """
        ds = self.get_a_copy_without_bit()
        return sum(sec.compute_outer_volume_tj_adjusted() for sec in ds)

    def compute_get_body_volume(self):
        """
        Compute and get the body volume of the pipes of the drill string only,
        not inside and outside of it.
        :return: volume in FOOT^3
        """
        ds = self.get_a_copy_without_bit()
        return sum(sec.compute_body_volume_tj_adjusted() for sec in ds)

    def get_a_copy_without_bit(self):
        """
        To get a deep copy of the current drillstring without the bit
        :return:
        """
        ds = deepcopy(self)
        bit = ds.get_bit()
        if bit:
            ds.sections.remove(bit)
        return ds

    def get_bit(self):
        """
        Get the bit element from the drillstring
        :return:
        """
        if not self:
            return None

        bit = self[-1]
        if isinstance(bit, Bit):
            return bit

        return None

    def get_under_reamer(self):
        """
        Get the under-reamer element from the drillstring
        :return:
        """
        if not self:
            return None

        return next((pipe for pipe in self if pipe.pipe_type == PipeType.UNDERREAMER), None)

    def get_bha_length(self) -> float:
        """
        To get the length of the BHA
        :return:
        """
        dp_indices = [index for index, pipe in enumerate(self) if pipe.pipe_type == PipeType.DP]
        last_dp_index = -1
        if dp_indices:
            last_dp_index = max(dp_indices)
        length = sum(el.length for el in self[last_dp_index + 1 :])
        return length
