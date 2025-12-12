import itertools
from collections import OrderedDict
from typing import List, Union

from worker.data import operations
from worker.data.activity import Activity
from worker.data.math import split_zip_edges
from worker.data.serialization import serialization
from worker.data.wits import WITS


@serialization
class ActivityGroup:
    SERIALIZED_VARIABLES = {"activity": Activity, "start": int, "end": int}

    def __init__(self, activity: Activity, start: int, end: int, **kwargs):
        self.activity = activity
        if end >= start:
            self.start = start
            self.end = end

    @property
    def duration(self) -> int:
        """
        :return: duration in seconds
        """
        return self.end - self.start + 1

    @classmethod
    def merge(
        cls,
        grp1: "ActivityGroup",
        grp2: "ActivityGroup",
        max_duration_gap: int = None,
        resultant_activity: Activity = None,
    ) -> Union["ActivityGroup", None]:
        """
        Merging two groups of activities into one.
        :param grp1:
        :param grp2:
        :param max_duration_gap: allowed gap between groups
        :param resultant_activity: if provided it will be used as the output activity, otherwise the activity
        of both groups are checked and if they are only the same it will continue the merging
        :return:
        """
        min_start = min(grp1.start, grp2.start)
        max_end = max(grp1.end, grp2.end)

        if max_duration_gap is not None:
            max_start = max(grp1.start, grp2.start)
            min_end = min(grp1.end, grp2.end)

            # if the gap between two activities are greater than the threshold, return None
            if max_start - min_end > max_duration_gap:
                return None

        if not resultant_activity:
            if grp1.activity != grp2.activity:
                return None
            resultant_activity = grp1.activity

        return ActivityGroup(resultant_activity, min_start, max_end)

    @staticmethod
    def has_overlap(group1: "ActivityGroup", group2: "ActivityGroup") -> bool:
        """
        Checking if two activity groups has overlap regardless of their precedence
        :param group1:
        :param group2:
        :return:
        """
        if not all([group1, group2]):
            return False

        max_start = max(group1.start, group2.start)
        min_end = min(group1.end, group2.end)

        return max_start <= min_end

    def __eq__(self, other):
        if not isinstance(other, ActivityGroup):
            return False

        return operations.equal(self, other, list(self.SERIALIZED_VARIABLES.keys()))

    def __repr__(self):
        return f"{self.activity.value:<25}: {self.start}-{self.end} -> duration={self.duration:>4}"


"""
In 1-second data frequency sometimes some activities will be added that can be
part of the bounding activities. For instance, you might be Reaming Down and
for a second the bit depth is the same as the previous timestamp and the activity
is Rotary Off Bottom. This will then be grouped into Reaming Down group.
"""
NEUTRAL_ACTIVITIES = OrderedDict(
    [
        (Activity.RUN_IN_HOLE, [Activity.STATIC_OFF_BOTTOM]),
        (Activity.PULL_OUT_OF_HOLE, [Activity.STATIC_OFF_BOTTOM]),
        (Activity.WASHING_DOWN, [Activity.CIRCULATING]),
        (Activity.WASHING_UP, [Activity.CIRCULATING]),
        (Activity.DRY_REAMING_DOWN, [Activity.DRY_ROTARY_OFF_BOTTOM]),
        (Activity.DRY_REAMING_UP, [Activity.DRY_ROTARY_OFF_BOTTOM]),
        (Activity.REAMING_DOWN, [Activity.ROTARY_OFF_BOTTOM]),
        (Activity.REAMING_UP, [Activity.ROTARY_OFF_BOTTOM]),
        (Activity.STATIC_OFF_BOTTOM, [Activity.RUN_IN_HOLE, Activity.PULL_OUT_OF_HOLE]),
        (Activity.CIRCULATING, [Activity.WASHING_DOWN, Activity.WASHING_UP]),
        (Activity.DRY_ROTARY_OFF_BOTTOM, [Activity.DRY_REAMING_DOWN, Activity.DRY_REAMING_UP]),
        (Activity.ROTARY_OFF_BOTTOM, [Activity.REAMING_DOWN, Activity.REAMING_UP]),
    ]
)


class ActivityGrouping:
    def __init__(
        self,
        min_group_duration: int = 3,
        apply_neutral_grouping: bool = True,
        apply_gap_filling: bool = True,
        merging_dict: dict = None,
        time_step=None,
    ):
        """
        :param min_group_duration: minimum duration of each group
        :param apply_neutral_grouping:
        :param apply_gap_filling:
        :param merging_dict: A dictionary representing the activities to be merged. For instance in the following
        example the Pull Out of Hole, Washing Up and Reaming Up are merged into one group and the activity of the
        whole group is PULL_OUT_OF_HOLE.
        {
            Activity.PULL_OUT_OF_HOLE : [Activity.PULL_OUT_OF_HOLE, Activity.WASHING_UP, Activity.REAMING_UP],
            ...
        }
        """
        self.min_group_duration = min_group_duration
        self.apply_neutral_grouping = apply_neutral_grouping
        self.apply_gap_filling = apply_gap_filling
        self.merging_dict = merging_dict
        self.time_step = time_step

    def group(self, wits_records: List[WITS]) -> List[ActivityGroup]:
        """
        to categorize a stream of wits data into groups of similar activities
        :param wits_records: wits records
        :return:
        """
        timestamps = [wits.timestamp for wits in wits_records]
        activities = [wits.state for wits in wits_records]

        if self.apply_neutral_grouping:
            activities = perform_neutral_grouping(activities)

        if not self.time_step:
            self.time_step = operations.compute_time_step(timestamps, percent=95)

        unique_activities = unique_everseen(activities)
        groups = []
        for activity in unique_activities:
            # Finding timestamps of matching activities
            valid_timestamps = [timestamps[i] for i in range(len(timestamps)) if activities[i] == activity]
            # Grouping and finding the edges of the activities
            edges = split_zip_edges(
                valid_timestamps, separation_length=self.time_step, min_segment_length=self.min_group_duration
            )
            this_groups = [ActivityGroup(activity=activity, start=start, end=end) for (start, end) in edges]
            groups.extend(this_groups)

        groups.sort(key=lambda x: x.start)

        if self.merging_dict:
            # 1. mapping the activities to their merging activities
            for grp in groups:
                grp.activity = self.merge_activity_map(grp.activity)

            # 2. merging adjacent activities with similar merging activities
            index = 1
            while index < len(groups):
                grp1, grp2 = groups[index - 1 : index + 1]
                merged_group = ActivityGroup.merge(grp1, grp2, max_duration_gap=max(self.time_step, 2))
                if not merged_group:
                    index += 1
                    continue
                # update one and remove the next
                groups[index - 1] = merged_group
                groups.pop(index)

        if self.apply_gap_filling:
            groups = perform_gap_filling(groups)

        return groups

    def merge_activity_map(self, activity):
        """
        Map the constituent activity to the group activity
        :param activity:
        :return:
        """
        if not self.merging_dict:
            return activity

        for merging_group, constituent_activities in self.merging_dict.items():
            if activity in constituent_activities:
                return merging_group

        return activity


def perform_neutral_grouping(activities: List[Activity]):
    for bound_activity, neutral_activities in NEUTRAL_ACTIVITIES.items():
        for i in range(1, len(activities) - 1):
            if bound_activity == activities[i - 1] == activities[i + 1] and activities[i] in neutral_activities:
                activities[i] = bound_activity
    return activities


def perform_gap_filling(groups: List[ActivityGroup]):
    # TODO something to consider
    return groups


def unique_everseen(iterable, key=None):
    """
    from: https://docs.python.org/3.3/library/itertools.html
    List unique elements, preserving order. Remember all elements ever seen.
    :param iterable:
    :param key:
    :return:
    Example:
    unique_everseen('AAAABBBCCDAABBB') --> A B C D
    unique_everseen('ABBCcAD', str.lower) --> A B C D
    """
    seen = set()
    if key is None:
        for element in itertools.filterfalse(seen.__contains__, iterable):
            seen.add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen.add(k)
                yield element
