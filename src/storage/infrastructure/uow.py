from .repositories import SQLStorageRepository
from ..application.unit_of_work import UnitOfWork


class PostgreSQLUnitOfWork(UnitOfWork):

    def __init__(self, session):
        self.storage_operations = SQLStorageRepository(session())
        self.session = session()

    def __enter__(self):
        self.repository = SQLStorageRepository(self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
