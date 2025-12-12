from .msg import Msg
from .protobuf import fulltext_update_pb2

class FulltextUpdate(Msg):

    def __init__(self, *args, **kwargs):
        super(FulltextUpdate, self).__init__(fulltext_update_pb2.FulltextUpdate(), args, kwargs)

