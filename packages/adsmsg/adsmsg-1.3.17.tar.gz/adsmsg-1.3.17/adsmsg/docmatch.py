from .msg import Msg
from .protobuf import docmatch_pb2


# for oracle db
class DocMatchRecord(Msg):

    def __init__(self, *args, **kwargs):
        super(DocMatchRecord, self).__init__(docmatch_pb2.DocMatchRecord(), args, kwargs)

class DocMatchRecordList(Msg):

    def __init__(self, *args, **kwargs):
        if 'docmatch_records' in kwargs:
            kwargs['docmatch_records'] = [docmatch_pb2.DocMatchRecord(**x) for x in kwargs.pop('docmatch_records')]
        super(DocMatchRecordList, self).__init__(docmatch_pb2.DocMatchRecordList(), args, kwargs)

