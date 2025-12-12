from typing import List


def get_unique_measured_depths(*items) -> List:
    """
    Find the edge measure depths of the given items
    :param items: an object of class Drilling or Hole
    :return:
    """
    mds = {depth for item in items for sec in item for depth in (sec.top_depth, sec.bottom_depth)}
    mds = sorted(list(mds))  # sorting them
    return mds
