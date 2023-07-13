import io
import os

import PIL.Image as Image
from sqlalchemy import select, delete, insert, update
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import max

from .models.contexts import DbContext
from .models.db_entities import Event, Organizer

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

    def remove_unused_images(self, paths, directory):
        for file_name in os.listdir(directory):
            usages = len(list(filter(lambda path: file_name in path, paths)))
            if usages == 0:
                os.remove('{0}/{1}'.format(directory, file_name))


class EventService:
    def get_all_events(self, db_context: DbContext):
        with Session(db_context.engine) as session:
            statement = select(Event)
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


class OrganizerService:
    def get_all_organizers(self, db_context: DbContext):
        with Session(db_context.engine) as session:
            statement = select(Organizer)
            organizers = session.scalars(statement).all()

        return organizers

    def get_organizer_by_id(self, db_context: DbContext, organizer_id: int):
        with Session(db_context.engine) as session:
            statement = select(Organizer).where(Organizer.id == organizer_id)
            organizer = session.scalar(statement)

        return organizer

    def remove_organizers_by_ids(self, db_context: DbContext, ids: list[int]):
        with Session(db_context.engine) as session:
            statement = delete(Organizer).where(Organizer.id.in_(ids))
            session.execute(statement)
            session.commit()

    def add_organizer(self, db_context: DbContext, organizer: Organizer):
        with Session(db_context.engine) as session:
            statement = insert(Organizer).values(
                name=organizer.name,
                image_uri=organizer.image_uri,
                role=organizer.role,
                additional_role=organizer.additional_role,
                order=organizer.order
            )
            session.execute(statement)
            session.commit()

    def edit_organizer(self, db_context: DbContext, organizer: Organizer):
        with Session(db_context.engine) as session:
            statement = update(Organizer).where(Organizer.id == organizer.id).values(
                name=organizer.name,
                image_uri=organizer.image_uri,
                role=organizer.role,
                additional_role=organizer.additional_role,
                order=organizer.order
            )
            session.execute(statement)
            session.commit()

    def calculate_order(self, db_context: DbContext):
        with Session(db_context.engine) as session:
            last_order = session.query(max(Organizer.order)).scalar()

        return last_order + 1 if last_order is not None else 0

    def edit_organizers_order(self, db_context: DbContext, order_dict: dict[int, int]):
        with Session(db_context.engine) as session:
            for organizer_id, organizer_order in order_dict.items():
                statement = update(Organizer).where(Organizer.id == organizer_id).values(
                    order=organizer_order
                )

                session.execute(statement)
                session.commit()
