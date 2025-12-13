import shared_gdb_pb2 as _shared_gdb_pb2
import shared_qa_pb2 as _shared_qa_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VerificationRequest(_message.Message):
    __slots__ = ("work_context", "specification", "parameters", "features", "user_name", "max_parallel_processing", "environment")
    WORK_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    SPECIFICATION_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    MAX_PARALLEL_PROCESSING_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    work_context: _shared_qa_pb2.WorkContextMsg
    specification: _shared_qa_pb2.QualitySpecificationMsg
    parameters: _shared_qa_pb2.VerificationParametersMsg
    features: _containers.RepeatedCompositeFieldContainer[_shared_gdb_pb2.GdbObjectMsg]
    user_name: str
    max_parallel_processing: int
    environment: str
    def __init__(self, work_context: _Optional[_Union[_shared_qa_pb2.WorkContextMsg, _Mapping]] = ..., specification: _Optional[_Union[_shared_qa_pb2.QualitySpecificationMsg, _Mapping]] = ..., parameters: _Optional[_Union[_shared_qa_pb2.VerificationParametersMsg, _Mapping]] = ..., features: _Optional[_Iterable[_Union[_shared_gdb_pb2.GdbObjectMsg, _Mapping]]] = ..., user_name: _Optional[str] = ..., max_parallel_processing: _Optional[int] = ..., environment: _Optional[str] = ...) -> None: ...

class DataVerificationRequest(_message.Message):
    __slots__ = ("request", "data", "schema", "error_message")
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    request: VerificationRequest
    data: _shared_qa_pb2.GdbData
    schema: _shared_qa_pb2.SchemaMsg
    error_message: str
    def __init__(self, request: _Optional[_Union[VerificationRequest, _Mapping]] = ..., data: _Optional[_Union[_shared_qa_pb2.GdbData, _Mapping]] = ..., schema: _Optional[_Union[_shared_qa_pb2.SchemaMsg, _Mapping]] = ..., error_message: _Optional[str] = ...) -> None: ...

class QueryDataRequest(_message.Message):
    __slots__ = ("data_sources", "schema", "transformer", "data_request", "user_name", "max_row_count", "input_data")
    DATA_SOURCES_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMER_FIELD_NUMBER: _ClassVar[int]
    DATA_REQUEST_FIELD_NUMBER: _ClassVar[int]
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    MAX_ROW_COUNT_FIELD_NUMBER: _ClassVar[int]
    INPUT_DATA_FIELD_NUMBER: _ClassVar[int]
    data_sources: _containers.RepeatedCompositeFieldContainer[_shared_qa_pb2.DataSourceMsg]
    schema: _shared_qa_pb2.SchemaMsg
    transformer: _shared_qa_pb2.InstanceConfigurationMsg
    data_request: _shared_qa_pb2.DataRequest
    user_name: str
    max_row_count: int
    input_data: _shared_qa_pb2.GdbData
    def __init__(self, data_sources: _Optional[_Iterable[_Union[_shared_qa_pb2.DataSourceMsg, _Mapping]]] = ..., schema: _Optional[_Union[_shared_qa_pb2.SchemaMsg, _Mapping]] = ..., transformer: _Optional[_Union[_shared_qa_pb2.InstanceConfigurationMsg, _Mapping]] = ..., data_request: _Optional[_Union[_shared_qa_pb2.DataRequest, _Mapping]] = ..., user_name: _Optional[str] = ..., max_row_count: _Optional[int] = ..., input_data: _Optional[_Union[_shared_qa_pb2.GdbData, _Mapping]] = ...) -> None: ...

class StandaloneVerificationRequest(_message.Message):
    __slots__ = ("xml_specification", "condition_list_specification", "parameters", "output_directory", "user_name")
    XML_SPECIFICATION_FIELD_NUMBER: _ClassVar[int]
    CONDITION_LIST_SPECIFICATION_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    xml_specification: _shared_qa_pb2.XmlQualitySpecificationMsg
    condition_list_specification: _shared_qa_pb2.ConditionListSpecificationMsg
    parameters: _shared_qa_pb2.VerificationParametersMsg
    output_directory: str
    user_name: str
    def __init__(self, xml_specification: _Optional[_Union[_shared_qa_pb2.XmlQualitySpecificationMsg, _Mapping]] = ..., condition_list_specification: _Optional[_Union[_shared_qa_pb2.ConditionListSpecificationMsg, _Mapping]] = ..., parameters: _Optional[_Union[_shared_qa_pb2.VerificationParametersMsg, _Mapping]] = ..., output_directory: _Optional[str] = ..., user_name: _Optional[str] = ...) -> None: ...

class VerificationResponse(_message.Message):
    __slots__ = ("service_call_status", "progress", "issues", "quality_verification", "verified_perimeter", "obsolete_exceptions")
    SERVICE_CALL_STATUS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    ISSUES_FIELD_NUMBER: _ClassVar[int]
    QUALITY_VERIFICATION_FIELD_NUMBER: _ClassVar[int]
    VERIFIED_PERIMETER_FIELD_NUMBER: _ClassVar[int]
    OBSOLETE_EXCEPTIONS_FIELD_NUMBER: _ClassVar[int]
    service_call_status: int
    progress: _shared_qa_pb2.VerificationProgressMsg
    issues: _containers.RepeatedCompositeFieldContainer[_shared_qa_pb2.IssueMsg]
    quality_verification: _shared_qa_pb2.QualityVerificationMsg
    verified_perimeter: _shared_gdb_pb2.ShapeMsg
    obsolete_exceptions: _containers.RepeatedCompositeFieldContainer[_shared_gdb_pb2.GdbObjRefMsg]
    def __init__(self, service_call_status: _Optional[int] = ..., progress: _Optional[_Union[_shared_qa_pb2.VerificationProgressMsg, _Mapping]] = ..., issues: _Optional[_Iterable[_Union[_shared_qa_pb2.IssueMsg, _Mapping]]] = ..., quality_verification: _Optional[_Union[_shared_qa_pb2.QualityVerificationMsg, _Mapping]] = ..., verified_perimeter: _Optional[_Union[_shared_gdb_pb2.ShapeMsg, _Mapping]] = ..., obsolete_exceptions: _Optional[_Iterable[_Union[_shared_gdb_pb2.GdbObjRefMsg, _Mapping]]] = ...) -> None: ...

class DataVerificationResponse(_message.Message):
    __slots__ = ("response", "data_request", "schema_request")
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    DATA_REQUEST_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_REQUEST_FIELD_NUMBER: _ClassVar[int]
    response: VerificationResponse
    data_request: _shared_qa_pb2.DataRequest
    schema_request: _shared_qa_pb2.SchemaRequest
    def __init__(self, response: _Optional[_Union[VerificationResponse, _Mapping]] = ..., data_request: _Optional[_Union[_shared_qa_pb2.DataRequest, _Mapping]] = ..., schema_request: _Optional[_Union[_shared_qa_pb2.SchemaRequest, _Mapping]] = ...) -> None: ...

class StandaloneVerificationResponse(_message.Message):
    __slots__ = ("service_call_status", "message", "issues")
    SERVICE_CALL_STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ISSUES_FIELD_NUMBER: _ClassVar[int]
    service_call_status: int
    message: _shared_qa_pb2.LogMsg
    issues: _containers.RepeatedCompositeFieldContainer[_shared_qa_pb2.IssueMsg]
    def __init__(self, service_call_status: _Optional[int] = ..., message: _Optional[_Union[_shared_qa_pb2.LogMsg, _Mapping]] = ..., issues: _Optional[_Iterable[_Union[_shared_qa_pb2.IssueMsg, _Mapping]]] = ...) -> None: ...

class QueryDataResponse(_message.Message):
    __slots__ = ("service_call_status", "data", "message", "data_request")
    SERVICE_CALL_STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DATA_REQUEST_FIELD_NUMBER: _ClassVar[int]
    service_call_status: int
    data: _shared_qa_pb2.GdbData
    message: _shared_qa_pb2.LogMsg
    data_request: _shared_qa_pb2.DataRequest
    def __init__(self, service_call_status: _Optional[int] = ..., data: _Optional[_Union[_shared_qa_pb2.GdbData, _Mapping]] = ..., message: _Optional[_Union[_shared_qa_pb2.LogMsg, _Mapping]] = ..., data_request: _Optional[_Union[_shared_qa_pb2.DataRequest, _Mapping]] = ...) -> None: ...
