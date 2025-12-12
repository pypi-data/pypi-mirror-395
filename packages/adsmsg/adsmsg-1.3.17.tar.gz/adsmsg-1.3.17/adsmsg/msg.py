from builtins import str
from past.builtins import basestring
from builtins import object
from datetime import datetime
from google.protobuf import json_format
from google.protobuf import timestamp_pb2
from .protobuf import status_pb2 as Status
import json
import base64

class Msg(object):

    def __init__(self, instance, args, kwargs):
        self.__dict__['_data'] = instance # Equivalent to: self._data = instance
        if kwargs:

            # every ADS msg object can have status; here we simply allow to specify status as a
            # string that correspons to the key from Status Enum type
            if 'status' in kwargs:
                if isinstance(kwargs['status'], basestring) and hasattr(Status, kwargs['status']):
                    kwargs['status'] = getattr(Status, kwargs['status'])

            for k, v in list(kwargs.items()):
                if isinstance(v, list) or isinstance(v, tuple):
                    getattr(instance, k).extend(v) #TODO(rca): use some smarter reflection
                elif isinstance(v, dict):
                    x = getattr(instance, k)
                    for dk in list(v.keys()):
                         x[dk] = v[dk]
                elif isinstance(v, datetime):
                    getattr(instance, k).FromDatetime(v)
                else:
                    setattr(instance, k, v)


    def __str__(self):
        return str(self._data)


    def __getattr__(self, key):
        if self.__dict__.get('_data') is None:
            # [PATCH] with Python 3 compatible celery packages, a strange
            # case happens where the attribute '__setstate__' gets call onto
            # Msg derived objects but self._data does not exist (although it
            # should since it is setup in the constructor!)
            raise AttributeError("%r object has no attribute %r" % (self.__class__.__name__, key))
        if key == '_data':
            return self._data
        return getattr(self._data, key) # Raises AttributeError if key does not exist

    def __setattr__(self, key, value):
        o = getattr(self._data, key)
        if hasattr(o, 'CopyFrom'):
            return o.CopyFrom(value) # it's an embedded object
        else:
            return setattr(self.__dict__['_data'], key, value)


    @classmethod
    def deserializer(cls, data):
        """
        Receives a serialized protocol buffer message and returns an object.
        """
        record = cls()
        record._data.ParseFromString(data)
        return record


    def serialize(self):
        """
        Returns a serialized protocol buffer message
        """
        return self._data.SerializeToString()


    def dump(self):
        """
        Returns (class, serialized-data)
        """
        return ('%s.%s' % (self.__class__.__module__, self.__class__.__name__), self.serialize())


    @staticmethod
    def loads(cls, serialized_data):
        """
        Creates a new instance from the product of self.dump()
        """
        if isinstance(cls, basestring):
            parts = cls.split('.')
            m = __import__('.'.join(parts[0:-1]))
            cls = getattr(m, parts[-1])
        record = cls()
        record._data.ParseFromString(serialized_data)
        return record


    def is_valid(self):
        return self._data.IsInitialized()


    @property
    def data(self):
        return self._data


    def toJSON(self, return_string=False, including_default_value_fields=False):
        if return_string:
            return json_format.MessageToJson(self.__dict__['_data'],
                                             including_default_value_fields=including_default_value_fields)
        return json_format.MessageToDict(self.__dict__['_data'],
                    preserving_proto_field_name=True,
                                         including_default_value_fields=including_default_value_fields)


    def __json__(self):
        """Serializer used by the Kombu/Celery."""
        cls, data = self.dump()
        return {'__adsmsg__':  (cls, base64.b64encode(data))}
