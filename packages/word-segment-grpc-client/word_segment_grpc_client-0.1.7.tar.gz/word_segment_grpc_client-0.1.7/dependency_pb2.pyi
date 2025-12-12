from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Dependency(_message.Message):
    __slots__ = ("word", "gov_idx", "rel")
    WORD_FIELD_NUMBER: _ClassVar[int]
    GOV_IDX_FIELD_NUMBER: _ClassVar[int]
    REL_FIELD_NUMBER: _ClassVar[int]
    word: str
    gov_idx: int
    rel: str
    def __init__(self, word: _Optional[str] = ..., gov_idx: _Optional[int] = ..., rel: _Optional[str] = ...) -> None: ...

class DependencyList(_message.Message):
    __slots__ = ("dependencies",)
    DEPENDENCIES_FIELD_NUMBER: _ClassVar[int]
    dependencies: _containers.RepeatedCompositeFieldContainer[Dependency]
    def __init__(self, dependencies: _Optional[_Iterable[_Union[Dependency, _Mapping]]] = ...) -> None: ...

class ParseDependenciesRequest(_message.Message):
    __slots__ = ("lang", "text")
    LANG_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    lang: str
    text: str
    def __init__(self, lang: _Optional[str] = ..., text: _Optional[str] = ...) -> None: ...

class ParseDependenciesResponse(_message.Message):
    __slots__ = ("dependency_list",)
    DEPENDENCY_LIST_FIELD_NUMBER: _ClassVar[int]
    dependency_list: _containers.RepeatedCompositeFieldContainer[DependencyList]
    def __init__(self, dependency_list: _Optional[_Iterable[_Union[DependencyList, _Mapping]]] = ...) -> None: ...
