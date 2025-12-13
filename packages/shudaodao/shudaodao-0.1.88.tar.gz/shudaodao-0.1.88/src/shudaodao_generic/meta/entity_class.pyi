from _typeshed import Incomplete
from shudaodao_core.type.var import (
    SQLModelCreate as SQLModelCreate,
    SQLModelDB as SQLModelDB,
    SQLModelResponse as SQLModelResponse,
    SQLModelUpdate as SQLModelUpdate,
)

class EntityClass:
    schema_name: Incomplete
    class_name: Incomplete
    engine_name: Incomplete
    model_class: None
    create_class: None
    update_class: None
    response_class: None
    module_name: Incomplete
    def __init__(
        self,
        *,
        schema_name: str = None,
        entity_name: str,
        engine_name: str = None,
        module_name: str = None,
    ) -> None: ...
