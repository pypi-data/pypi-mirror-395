from typing import Self

from sqlalchemy_mixins import SerializeMixin, ReprMixin

from cidc_api.config.db import db


class BaseORM(db.Model, ReprMixin, SerializeMixin):
    __abstract__ = True
    __repr__ = ReprMixin.__repr__

    def merge(self, d: dict) -> Self:
        """Merge keys and values from dict d into this model, overwriting as necessary."""
        for key, value in d.items():
            setattr(self, key, value)
        return self

    def clone(self) -> "BaseORM":
        """Clones a SQLAlchemy ORM object, excluding primary keys."""
        mapper = self.__mapper__
        new_instance = self.__class__()
        for column in mapper.columns:
            if not column.primary_key:
                setattr(new_instance, column.key, getattr(self, column.key))
        return new_instance
