from sqlalchemy import create_engine, Engine

from .db_entities import Base


class DbContext:
    def __init__(self, db_user, db_password, db_host, db_name, driver):
        self.engine: Engine
        self.__connect(db_user, db_password, db_host, db_name, driver)

        if self.engine:
            Base.metadata.create_all(self.engine)

    def __connect(self, db_user, db_password, db_host, db_name, driver):
        self.engine = create_engine(f'{driver}://{db_user}:{db_password}@{db_host}/{db_name}')


class PyMySqlContext(DbContext):
    def __init__(self, db_user, db_password, db_host, db_name):
        super().__init__(db_user, db_password, db_host, db_name, 'mysql+pymysql')
