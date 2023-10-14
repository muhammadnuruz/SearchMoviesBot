import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.future import select
from db import Base, db

db.init()


# ----------------------------- ABSTRACTS ----------------------------------
class AbstractClass:
    @staticmethod
    async def commit():
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

    @classmethod
    async def create(cls, **kwargs):
        object_ = cls(**kwargs)
        db.add(object_)
        await cls.commit()
        return object_

    @classmethod
    async def update(cls, id_, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id_)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def get(cls, id_):
        query = select(cls).where(cls.chat_id == id_)
        objects = await db.execute(query)
        object_ = objects.first()
        return object_

    @classmethod
    async def id_get(cls, id_):
        query = select(cls).where(cls.id == id_)
        objects = await db.execute(query)
        object_ = objects.first()
        return object_

    @classmethod
    async def delete(cls, id_):
        query = sqlalchemy_delete(cls).where(cls.id == id_)
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def get_all(cls):
        query = select(cls)
        objects = await db.execute(query)
        return objects.all()

    @classmethod
    async def filter_by_name(cls, name):
        query = select(cls).where(cls.name == name)
        objects = await db.execute(query)
        return objects.first()

    @classmethod
    async def filter_by_created_at(cls, num):
        query = select(cls).order_by(cls.created_at.desc()).limit(10).offset(num)
        objects = await db.execute(query)
        return objects.all()

    @classmethod
    async def filter_by_seen(cls, num):
        query = select(cls).order_by(cls.seen.desc()).limit(10).offset(num)
        objects = await db.execute(query)
        return objects.all()


class CreatedModel(Base, AbstractClass):
    __abstract__ = True
    created_at = Column(DateTime(), default=datetime.datetime.utcnow)

# ------------------------------ ENUMS --------------------------------------
