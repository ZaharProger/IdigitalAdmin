import io
import PIL.Image as Image
from sqlalchemy import select
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
            return bytearray(image.read())

    def write_image(self, image_bytes, path):
        image = Image.open(io.BytesIO(image_bytes))
        image.save(path)


class EventService:
    def get_all_events(self, db_context: DbContext):
        with Session(db_context.engine) as session:
            statement = select(Event)
            events = session.scalars(statement).all()

        return events