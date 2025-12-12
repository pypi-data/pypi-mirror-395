from .augmentrecord import AugmentAffiliationRequestRecord, \
                           AugmentAffiliationRequestRecordList, \
                           AugmentAffiliationResponseRecord, \
                           AugmentAffiliationResponseRecordList
from .classifyrecord import ClassifyRequestRecord, \
                            ClassifyRequestRecordList, \
                            ClassifyResponseRecord, \
                            ClassifyResponseRecordList
from .bibrecord import BibRecord
from .denormalized_record import DenormalizedRecord
from .fulltext_requests import FulltextRequests
from .fulltext_update import FulltextUpdate
from .metrics_record import MetricsRecord, \
                            MetricsRecordList
from .nonbibrecord import NonBibRecord, \
                NonBibRecordList, \
                DataLinksRecord, \
                DataLinksRecordList
from .master import DocumentRecord, \
                DocumentRecords
from .orcid_claims import OrcidClaims
from .status import Status
from .citation_changes import CitationChanges, CitationChange
from .citation_changes_content_type import CitationChangeContentType
from .docmatch import DocMatchRecord, \
    DocMatchRecordList
from .boostfactors import BoostRequestRecord, BoostRequestRecordList, \
    BoostResponseRecord, BoostResponseRecordList



