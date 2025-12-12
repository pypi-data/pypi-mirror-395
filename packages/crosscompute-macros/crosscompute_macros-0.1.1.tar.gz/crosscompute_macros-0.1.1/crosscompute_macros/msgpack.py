import msgpack

from .sqlalchemy import EncryptedBinary


class EncryptedMap(EncryptedBinary):
    cache_ok = False

    def process_bind_param(self, value, dialect):
        if value is not None:
            payload = msgpack.packb(value)
            value = super().process_bind_param(payload, dialect)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            payload = super().process_result_value(value, dialect)
            value = msgpack.unpackb(payload)
        return value
