from typing import Any

class ServiceResult:
    pass

class ServiceItemResult(ServiceResult):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

class ServiceListResult(ServiceResult):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

class ServiceBulkItemResult(ServiceResult):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

class ServiceBulkListResult(ServiceResult):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
