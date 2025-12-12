import numpy
import simplejson as json


class JsonEncoder(json.JSONEncoder):
    """
    This encoder can be used to convert incompatible data types to types compatible with json.dumps()
    Use like json.dumps(output, cls=JsonEncoder)
    """

    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
