from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Entity(_message.Message):
    __slots__ = ("type", "start", "end", "prob", "span")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    PROB_FIELD_NUMBER: _ClassVar[int]
    SPAN_FIELD_NUMBER: _ClassVar[int]
    type: str
    start: int
    end: int
    prob: float
    span: str
    def __init__(self, type: _Optional[str] = ..., start: _Optional[int] = ..., end: _Optional[int] = ..., prob: _Optional[float] = ..., span: _Optional[str] = ...) -> None: ...

class EntityList(_message.Message):
    __slots__ = ("entities",)
    ENTITIES_FIELD_NUMBER: _ClassVar[int]
    entities: _containers.RepeatedCompositeFieldContainer[Entity]
    def __init__(self, entities: _Optional[_Iterable[_Union[Entity, _Mapping]]] = ...) -> None: ...

class NerRequest(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...

class NerResponse(_message.Message):
    __slots__ = ("entity_list",)
    ENTITY_LIST_FIELD_NUMBER: _ClassVar[int]
    entity_list: EntityList
    def __init__(self, entity_list: _Optional[_Union[EntityList, _Mapping]] = ...) -> None: ...
