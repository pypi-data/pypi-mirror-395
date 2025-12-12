from .msg import Msg
from .protobuf import boostfactors_pb2

class BoostRequestRecord(Msg):

    def __init__(self, *args, **kwargs):
        instance = boostfactors_pb2.BoostRequestRecord()
        super(BoostRequestRecord, self).__init__(instance, args, kwargs)

class BoostRequestRecordList(Msg):

    def __init__(self, *args, **kwargs):
        super(BoostRequestRecordList, self).__init__(boostfactors_pb2.BoostRequestRecordList(), args, kwargs)


class BoostResponseRecord(Msg):

    def __init__(self, *args, **kwargs):
        instance = boostfactors_pb2.BoostResponseRecord()
        super(BoostResponseRecord, self).__init__(instance, args, kwargs)

class BoostResponseRecordList(Msg):

    def __init__(self, *args, **kwargs):
        super(BoostResponseRecordList, self).__init__(boostfactors_pb2.BoostResponseRecordList(), args, kwargs)

