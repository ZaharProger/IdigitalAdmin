import io
import PIL.Image as Image
from sqlalchemy import select, delete, insert, update
from sqlalchemy.orm import Session

from .models.contexts import DbContext
from .models.db_entities import Event


"""
    Сервисы нужны для выполнения некоторой бизнес-логики
    Не отличаются от обычных классов
"""


class ImageService:
    def read_image(self, path):
        with open(path, 'rb') as image:
            image_data = image.read()

        return image_data

    def write_image(self, image_bytes, path):
        image = Image.open(io.BytesIO(image_bytes))
        image.save(path)


class EventService:
    def get_all_events(self, db_context: DbContext):
        with Session(db_context.engine) as session:
            statement = select(Event).order_by(Event.date)
            events = session.scalars(statement).all()

        return events

    def get_event_by_id(self, db_context: DbContext, event_id: int):
        with Session(db_context.engine) as session:
            statement = select(Event).where(Event.id == event_id)
            event = session.scalar(statement)

        return event

    def remove_events_by_ids(self, db_context: DbContext, ids: list[int]):
        with Session(db_context.engine) as session:
            statement = delete(Event).where(Event.id.in_(ids))
            session.execute(statement)
            session.commit()

    def add_event(self, db_context: DbContext, event: Event):
        with Session(db_context.engine) as session:
            statement = insert(Event).values(
                name=event.name,
                image_uri=event.image_uri,
                date=event.date,
                ref=event.ref
            )
            session.execute(statement)
            session.commit()

    def edit_event(self, db_context: DbContext, event: Event):
        with Session(db_context.engine) as session:
            statement = update(Event).where(Event.id == event.id).values(
                name=event.name,
                image_uri=event.image_uri,
                date=event.date,
                ref=event.ref
            )
            session.execute(statement)
            session.commit()
