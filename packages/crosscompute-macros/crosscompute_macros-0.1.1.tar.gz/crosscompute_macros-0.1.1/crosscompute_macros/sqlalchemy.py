from datetime import UTC
from pathlib import Path

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.types import DateTime, LargeBinary, String, TypeDecorator

from .security import hash_text


class MutableMap(Mutable, dict):

    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableMap):
            if isinstance(value, dict):
                return MutableMap(value)
            return Mutable.coerce(key, value)
        return value

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self.changed()


class EncryptedBinary(TypeDecorator):
    impl = LargeBinary
    cache_ok = False
    context = None

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = self.context.encrypt(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = self.context.decrypt(value)
        return value


class EncryptedString(TypeDecorator):
    impl = String
    cache_ok = False
    encoding = 'utf-8'
    context = None

    def process_bind_param(self, value, dialect):
        if value is not None:
            encoded_value = bytes(value, encoding=self.encoding)
            value = self.context.encrypt(encoded_value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            encoded_value = self.context.decrypt(value)
            value = bytes.decode(encoded_value, encoding=self.encoding)
        return value


class HashedString(TypeDecorator):
    impl = String
    cache_ok = False

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = hash_text(value)
        return value


class UTCDateTime(TypeDecorator):
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = value.astimezone(UTC).replace(tzinfo=None)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = value.replace(tzinfo=UTC)
        return value


def get_database_engine(database_uri):
    if database_uri.startswith('sqlite') and not database_uri.endswith('://'):
        database_path = Path(database_uri.split(':///', maxsplit=1)[1])
        database_folder = database_path.parent
        database_folder.mkdir(parents=True, exist_ok=True)
    return create_async_engine(database_uri)


def define_get_database_session(database_engine):
    return async_sessionmaker(
        database_engine,
        autoflush=False,
        expire_on_commit=False)


async def make_tables(database_engine, database_metadata):
    async with database_engine.begin() as database_connection:
        await database_connection.run_sync(database_metadata.create_all)
