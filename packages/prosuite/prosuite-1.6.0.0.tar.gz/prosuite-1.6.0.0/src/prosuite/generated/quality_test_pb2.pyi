import shared_gdb_pb2 as _shared_gdb_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExecuteTestRequest(_message.Message):
    __slots__ = ("workspaces", "involved_tables", "perimeter", "test_name", "parameters")
    WORKSPACES_FIELD_NUMBER: _ClassVar[int]
    INVOLVED_TABLES_FIELD_NUMBER: _ClassVar[int]
    PERIMETER_FIELD_NUMBER: _ClassVar[int]
    TEST_NAME_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    workspaces: _containers.RepeatedCompositeFieldContainer[_shared_gdb_pb2.WorkspaceMsg]
    involved_tables: _containers.RepeatedCompositeFieldContainer[TestDatasetMsg]
    perimeter: _shared_gdb_pb2.ShapeMsg
    test_name: str
    parameters: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, workspaces: _Optional[_Iterable[_Union[_shared_gdb_pb2.WorkspaceMsg, _Mapping]]] = ..., involved_tables: _Optional[_Iterable[_Union[TestDatasetMsg, _Mapping]]] = ..., perimeter: _Optional[_Union[_shared_gdb_pb2.ShapeMsg, _Mapping]] = ..., test_name: _Optional[str] = ..., parameters: _Optional[_Iterable[str]] = ...) -> None: ...

class ExecuteTestResponse(_message.Message):
    __slots__ = ("service_call_status", "progress", "issues")
    SERVICE_CALL_STATUS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    ISSUES_FIELD_NUMBER: _ClassVar[int]
    service_call_status: int
    progress: TestProgressMsg
    issues: _containers.RepeatedCompositeFieldContainer[DetectedIssueMsg]
    def __init__(self, service_call_status: _Optional[int] = ..., progress: _Optional[_Union[TestProgressMsg, _Mapping]] = ..., issues: _Optional[_Iterable[_Union[DetectedIssueMsg, _Mapping]]] = ...) -> None: ...

class TestDatasetMsg(_message.Message):
    __slots__ = ("class_definition", "filter_expression")
    CLASS_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    FILTER_EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    class_definition: _shared_gdb_pb2.ObjectClassMsg
    filter_expression: str
    def __init__(self, class_definition: _Optional[_Union[_shared_gdb_pb2.ObjectClassMsg, _Mapping]] = ..., filter_expression: _Optional[str] = ...) -> None: ...

class TestProgressMsg(_message.Message):
    __slots__ = ("progress_total_steps", "progress_current_step", "message")
    PROGRESS_TOTAL_STEPS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_CURRENT_STEP_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    progress_total_steps: int
    progress_current_step: int
    message: str
    def __init__(self, progress_total_steps: _Optional[int] = ..., progress_current_step: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class DetectedIssueMsg(_message.Message):
    __slots__ = ("description", "issue_geometry", "issue_code_id", "issue_code_description", "involved_objects", "stop_condition", "affected_component", "creation_date_time_ticks")
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ISSUE_GEOMETRY_FIELD_NUMBER: _ClassVar[int]
    ISSUE_CODE_ID_FIELD_NUMBER: _ClassVar[int]
    ISSUE_CODE_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    INVOLVED_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    STOP_CONDITION_FIELD_NUMBER: _ClassVar[int]
    AFFECTED_COMPONENT_FIELD_NUMBER: _ClassVar[int]
    CREATION_DATE_TIME_TICKS_FIELD_NUMBER: _ClassVar[int]
    description: str
    issue_geometry: _shared_gdb_pb2.ShapeMsg
    issue_code_id: str
    issue_code_description: str
    involved_objects: _containers.RepeatedCompositeFieldContainer[InvolvedObjectsMsg]
    stop_condition: bool
    affected_component: str
    creation_date_time_ticks: int
    def __init__(self, description: _Optional[str] = ..., issue_geometry: _Optional[_Union[_shared_gdb_pb2.ShapeMsg, _Mapping]] = ..., issue_code_id: _Optional[str] = ..., issue_code_description: _Optional[str] = ..., involved_objects: _Optional[_Iterable[_Union[InvolvedObjectsMsg, _Mapping]]] = ..., stop_condition: bool = ..., affected_component: _Optional[str] = ..., creation_date_time_ticks: _Optional[int] = ...) -> None: ...

class InvolvedObjectsMsg(_message.Message):
    __slots__ = ("dataset", "object_ids")
    DATASET_FIELD_NUMBER: _ClassVar[int]
    OBJECT_IDS_FIELD_NUMBER: _ClassVar[int]
    dataset: _shared_gdb_pb2.ObjectClassMsg
    object_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, dataset: _Optional[_Union[_shared_gdb_pb2.ObjectClassMsg, _Mapping]] = ..., object_ids: _Optional[_Iterable[int]] = ...) -> None: ...
