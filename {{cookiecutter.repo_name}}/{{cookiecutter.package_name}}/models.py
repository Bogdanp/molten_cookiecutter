from sqlalchemy.ext.declarative import declarative_base

from molten.contrib.sqlalchemy import Session

Model = declarative_base()


class Manager:
    __slots__ = ["session"]

    def __init__(self, session):
        self.session = session


class ManagerComponent:
    def __init__(self, manager_type):
        self.manager_type = manager_type

    def can_handle_parameter(self, parameter):
        return parameter.annotation is self.manager_type

    def resolve(self, session: Session):
        return self.manager_type(session)
