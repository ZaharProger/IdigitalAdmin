from sqlalchemy import create_engine


class DbContext:
    def __init__(self, db_user, db_password, db_host, db_name, driver):
        self.__connect(db_user, db_password, db_host, db_name, driver)

    def __connect(self, db_user, db_password, db_host, db_name, driver):
        self.__engine = create_engine(f'{driver}://{db_user}:{db_password}@{db_host}/{db_name}')


class PyMySqlContext(DbContext):
    def __init__(self, db_user, db_password, db_host, db_name):
        super().__init__(db_user, db_password, db_host, db_name, 'mysql+pymysql')
