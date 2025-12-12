from typing import Optional

from invenio_db.uow import UnitOfWork
from invenio_records_resources.services.base.service import Service

class BaseServiceComponent:
    service: Service
    _uow: Optional[UnitOfWork]
    def __init__(self, service: Service): ...
    @property
    def uow(self) -> UnitOfWork: ...
    @uow.setter
    def uow(self, value: Optional[UnitOfWork]) -> None: ...
