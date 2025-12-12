from .msg import Msg
from .protobuf import orcid_claims_pb2

class OrcidClaims(Msg):

    def __init__(self, *args, **kwargs):
        super(OrcidClaims, self).__init__(orcid_claims_pb2.OrcidClaims(), args, kwargs)

