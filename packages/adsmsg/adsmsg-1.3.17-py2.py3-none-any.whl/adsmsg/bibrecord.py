from .msg import Msg
from .protobuf import bibrecord_pb2

class BibRecord(Msg):

    def __init__(self, *args, **kwargs):
        super(BibRecord, self).__init__(bibrecord_pb2.BibRecord(), args, kwargs)

