from .msg import Msg
from .protobuf import denormalized_record_pb2

class DenormalizedRecord(Msg):

    def __init__(self, *args, **kwargs):
        super(DenormalizedRecord, self).__init__(denormalized_record_pb2.DenormalizedRecord(), args, kwargs)

