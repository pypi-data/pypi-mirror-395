from typing import Any, Optional, Sequence, Union

from invenio_records_permissions.generators import ConditionalGenerator, Generator

class IfTransferType(ConditionalGenerator):
    _transfer_type: Any

    def __init__(
        self,
        transfer_type: Any,
        then_: Union[Generator, Sequence[Generator]],
        else_: Optional[Union[Generator, Sequence[Generator]]] = ...,
    ) -> None: ...
    def _condition(self, **kwargs: Any) -> bool: ...
