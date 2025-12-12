from .msg import Msg
from .protobuf import classifyrecord_pb2

class ClassifyRequestRecord(Msg):

    def __init__(self, *args, **kwargs):
        instance = classifyrecord_pb2.ClassifyRequestRecord()
        super(ClassifyRequestRecord, self).__init__(instance, args, kwargs)

class ClassifyRequestRecordList(Msg):

    def __init__(self, *args, **kwargs):
        super(ClassifyRequestRecordList, self).__init__(classifyrecord_pb2.ClassifyRequestRecordList(), args, kwargs)


class ClassifyResponseRecord(Msg):

    def __init__(self, *args, **kwargs):
        instance = classifyrecord_pb2.ClassifyResponseRecord()
        super(ClassifyResponseRecord, self).__init__(instance, args, kwargs)

class ClassifyResponseRecordList(Msg):

    def __init__(self, *args, **kwargs):
        super(ClassifyResponseRecordList, self).__init__(classifyrecord_pb2.ClassifyResponseRecordList(), args, kwargs)

