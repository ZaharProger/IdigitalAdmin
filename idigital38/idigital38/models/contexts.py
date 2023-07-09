from sqlalchemy import create_engine, Engine

from .db_entities import Base


"""
    Контекст базы данных нужен для обеспечения доступа (напрямую или через ORM) к данными из таблиц БД
    Контекст отвечает за формирование объекта Engine, отвечающего за доступ к данным БД
    
    В зависимости от СУБД и используемого драйвера можно создать наследников контекста БД, которые
    будут определять конкретное подключение к БД, что и сделано
    В свою очередь каждый наследник имеет доступ к Engine, в связи с чем можно передавать различные контексты
    в контроллеры и при этом контроллер будет одинаково работать со всеми контекстами
"""


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
