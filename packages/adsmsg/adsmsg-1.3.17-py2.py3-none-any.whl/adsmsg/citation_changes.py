from .msg import Msg
from .protobuf import citation_changes_pb2

class CitationChange(Msg):

    def __init__(self, *args, **kwargs):
        super(CitationChange, self).__init__(citation_changes_pb2.CitationChange(), args, kwargs)

class CitationChanges(Msg):

    def __init__(self, *args, **kwargs):
        if 'changes_array' in kwargs:
            kwargs['changes'] = [citation_changes_pb2.CitationChange(**x) for x in kwargs.pop('changes_array')]
        super(CitationChanges, self).__init__(citation_changes_pb2.CitationChanges(), args, kwargs)

