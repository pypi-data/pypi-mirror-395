from .msg import Msg
from .protobuf import augmentrecord_pb2

class AugmentAffiliationRequestRecord(Msg):

    def __init__(self, *args, **kwargs):
        instance = augmentrecord_pb2.AugmentAffiliationRequestRecord()
        super(AugmentAffiliationRequestRecord, self).__init__(instance, args, kwargs)

class AugmentAffiliationRequestRecordList(Msg):

    def __init__(self, *args, **kwargs):
        super(AugmentAffiliationRequestRecordList, self).__init__(augmentrecord_pb2.AugmentAffiliationRequestRecordList(), args, kwargs)


class AugmentAffiliationResponseRecord(Msg):

    def __init__(self, *args, **kwargs):
        instance = augmentrecord_pb2.AugmentAffiliationResponseRecord()
        super(AugmentAffiliationResponseRecord, self).__init__(instance, args, kwargs)

class AugmentAffiliationResponseRecordList(Msg):

    def __init__(self, *args, **kwargs):
        super(AugmentAffiliationResponseRecordList, self).__init__(augmentrecord_pb2.AugmentAffiliationResponseRecordList(), args, kwargs)

