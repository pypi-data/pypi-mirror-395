from .msg import Msg
from .protobuf import master_pb2


# for resolver db 2.0
class DocumentRecord(Msg):
    def __init__(self, *args, **kwargs):
        instance = master_pb2.DocumentRecord()
        links = kwargs.pop('links', None)
        super(DocumentRecord, self).__init__(instance, args, kwargs)
        if links:
            link_record = instance.links
            for key, value in links.items():
                if isinstance(value, bool):
                    setattr(link_record, key, value)
                elif isinstance(value, list):
                    if key == 'ARXIV':
                        link_record.ARXIV.extend(value)
                    elif key == 'DOI':
                        link_record.DOI.extend(value)
                elif isinstance(value, dict):
                    if key == 'DATA':
                        for sub_type_key, sub_dict in value.items():
                            link_type = link_record.DATA[sub_type_key]
                            link_type.url.extend(sub_dict.get('url', []))
                            link_type.title.extend(sub_dict.get('title', []))
                            link_type.count = sub_dict.get('count', 0)
                    elif key == 'ESOURCE':
                        for sub_type_key, sub_dict in value.items():
                            link_type = link_record.ESOURCE[sub_type_key]
                            link_type.url.extend(sub_dict.get('url', []))
                            link_type.title.extend(sub_dict.get('title', []))
                            link_type.count = sub_dict.get('count', 0)
                    elif key in ['ASSOCIATED', 'INSPIRE', 'LIBRARYCATALOG', 'PRESENTATION']:
                        link_type = getattr(link_record, key)
                        link_type.url.extend(value.get('url', []))
                        link_type.title.extend(value.get('title', []))
                        if 'count' in value:
                            link_type.count = value['count']

class DocumentRecords(Msg):
    def __init__(self, *args, **kwargs):
        """converts list of dicts to list of protobuf instances of message DocumentRecord"""
        if 'document_records' in kwargs:
            kwargs['document_records'] = [DocumentRecord(**x)._data for x in kwargs['document_records']]
        super(DocumentRecords, self).__init__(master_pb2.DocumentRecords(), args, kwargs)
