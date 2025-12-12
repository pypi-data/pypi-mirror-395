from .msg import Msg
from .protobuf import nonbibrecord_pb2
from .master import master_pb2

class NonBibRecord(Msg):

    def __init__(self, *args, **kwargs):
        instance = nonbibrecord_pb2.NonBibRecord()
        
        data_links_rows = kwargs.pop('data_links_rows', None)  # remove for special handling
        links = kwargs.pop('links', None)
        identifier = kwargs.pop('identifier', None)
        
        super(NonBibRecord, self).__init__(instance, args, kwargs)

        if data_links_rows:
            # populate rows from database field
            for current in data_links_rows:
                row = instance.data_links_rows.add()
                row.link_type = current['link_type']
                row.link_sub_type = current['link_sub_type']
                row.item_count = current['item_count']
                row.url.extend(current['url'])
                row.title.extend(current['title'])

        elif links:
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
                            lt = link_record.DATA[sub_type_key]
                            lt.url.extend(sub_dict.get('url', []))
                            lt.title.extend(sub_dict.get('title', []))
                            lt.count = sub_dict.get('count', 0)
                    elif key == 'ESOURCE':
                        for sub_type_key, sub_dict in value.items():
                            lt = link_record.ESOURCE[sub_type_key]
                            lt.url.extend(sub_dict.get('url', []))
                            lt.title.extend(sub_dict.get('title', []))
                    elif key in ['ASSOCIATED', 'INSPIRE', 'LIBRARYCATALOG', 'PRESENTATION']:
                        lt = getattr(link_record, key)
                        lt.url.extend(value.get('url', []))
                        lt.title.extend(value.get('title', []))
                        if 'count' in value:
                            lt.count = value['count']

        if identifier: 
            instance.identifier.extend(identifier)

class NonBibRecordList(Msg):

    def __init__(self, *args, **kwargs):
        super(NonBibRecordList, self).__init__(nonbibrecord_pb2.NonBibRecordList(), args, kwargs)


class DataLinksRecord(Msg):

    def __init__(self, *args, **kwargs):
        instance = nonbibrecord_pb2.DataLinksRecord()
        data_links_rows = kwargs.pop('data_links_rows', None)  # remove for special handling
        super(DataLinksRecord, self).__init__(instance, args, kwargs)
        if data_links_rows:
            # populate rows from database field
            for current in data_links_rows:
                row = instance.data_links_rows.add()
                row.link_type = current['link_type']
                row.link_sub_type = current['link_sub_type']
                row.item_count = current['item_count']
                row.url.extend(current['url'])
                row.title.extend(current['title'])


class DataLinksRecordList(Msg):
    def __init__(self, *args, **kwargs):
        super(DataLinksRecordList, self).__init__(nonbibrecord_pb2.DataLinksRecordList(), args, kwargs)
