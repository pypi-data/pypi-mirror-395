from dataclasses import dataclass, field

@dataclass
class TemplateColumn:
    name: str
    comment: str
    is_primary_key: bool
    is_foreign_key: bool
    type2: str
    type: str
    clazz: str
    model_type: int
    params: list[str] = field(default_factory=list)

@dataclass
class TemplateClazz:
    schema_name: str
    table_name: str
    view_name: str
    comment: str
    file_name: str
    class_name: str
    table_args: str
    primary_key: str
    from_imports: list[str] = field(default_factory=list)
    database_columns: list[TemplateColumn] = field(default_factory=list)
    create_columns: list[TemplateColumn] = field(default_factory=list)
    update_columns: list[TemplateColumn] = field(default_factory=list)
    response_columns: list[TemplateColumn] = field(default_factory=list)
    relation_columns: list[TemplateColumn] = field(default_factory=list)
