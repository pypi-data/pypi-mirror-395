import shared_gdb_pb2 as _shared_gdb_pb2
import shared_ddx_pb2 as _shared_ddx_pb2
import shared_qa_pb2 as _shared_qa_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetProjectWorkspacesRequest(_message.Message):
    __slots__ = ("environment", "object_classes", "workspaces")
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    OBJECT_CLASSES_FIELD_NUMBER: _ClassVar[int]
    WORKSPACES_FIELD_NUMBER: _ClassVar[int]
    environment: str
    object_classes: _containers.RepeatedCompositeFieldContainer[_shared_gdb_pb2.ObjectClassMsg]
    workspaces: _containers.RepeatedCompositeFieldContainer[_shared_gdb_pb2.WorkspaceMsg]
    def __init__(self, environment: _Optional[str] = ..., object_classes: _Optional[_Iterable[_Union[_shared_gdb_pb2.ObjectClassMsg, _Mapping]]] = ..., workspaces: _Optional[_Iterable[_Union[_shared_gdb_pb2.WorkspaceMsg, _Mapping]]] = ...) -> None: ...

class GetSpecificationRefsRequest(_message.Message):
    __slots__ = ("environment", "dataset_ids", "include_hidden")
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    DATASET_IDS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_HIDDEN_FIELD_NUMBER: _ClassVar[int]
    environment: str
    dataset_ids: _containers.RepeatedScalarFieldContainer[int]
    include_hidden: bool
    def __init__(self, environment: _Optional[str] = ..., dataset_ids: _Optional[_Iterable[int]] = ..., include_hidden: bool = ...) -> None: ...

class GetSpecificationRequest(_message.Message):
    __slots__ = ("environment", "quality_specification_id")
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    QUALITY_SPECIFICATION_ID_FIELD_NUMBER: _ClassVar[int]
    environment: str
    quality_specification_id: int
    def __init__(self, environment: _Optional[str] = ..., quality_specification_id: _Optional[int] = ...) -> None: ...

class GetConditionRequest(_message.Message):
    __slots__ = ("environment", "condition_name")
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    CONDITION_NAME_FIELD_NUMBER: _ClassVar[int]
    environment: str
    condition_name: str
    def __init__(self, environment: _Optional[str] = ..., condition_name: _Optional[str] = ...) -> None: ...

class GetDatasetDetailsRequest(_message.Message):
    __slots__ = ("environment", "dataset_ids")
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    DATASET_IDS_FIELD_NUMBER: _ClassVar[int]
    environment: str
    dataset_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, environment: _Optional[str] = ..., dataset_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class GetProjectWorkspacesResponse(_message.Message):
    __slots__ = ("project_workspaces", "projects", "models", "datasets", "environment_name")
    PROJECT_WORKSPACES_FIELD_NUMBER: _ClassVar[int]
    PROJECTS_FIELD_NUMBER: _ClassVar[int]
    MODELS_FIELD_NUMBER: _ClassVar[int]
    DATASETS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    project_workspaces: _containers.RepeatedCompositeFieldContainer[ProjectWorkspaceMsg]
    projects: _containers.RepeatedCompositeFieldContainer[_shared_ddx_pb2.ProjectMsg]
    models: _containers.RepeatedCompositeFieldContainer[_shared_ddx_pb2.ModelMsg]
    datasets: _containers.RepeatedCompositeFieldContainer[_shared_ddx_pb2.DatasetMsg]
    environment_name: str
    def __init__(self, project_workspaces: _Optional[_Iterable[_Union[ProjectWorkspaceMsg, _Mapping]]] = ..., projects: _Optional[_Iterable[_Union[_shared_ddx_pb2.ProjectMsg, _Mapping]]] = ..., models: _Optional[_Iterable[_Union[_shared_ddx_pb2.ModelMsg, _Mapping]]] = ..., datasets: _Optional[_Iterable[_Union[_shared_ddx_pb2.DatasetMsg, _Mapping]]] = ..., environment_name: _Optional[str] = ...) -> None: ...

class GetSpecificationRefsResponse(_message.Message):
    __slots__ = ("quality_specifications",)
    QUALITY_SPECIFICATIONS_FIELD_NUMBER: _ClassVar[int]
    quality_specifications: _containers.RepeatedCompositeFieldContainer[QualitySpecificationRefMsg]
    def __init__(self, quality_specifications: _Optional[_Iterable[_Union[QualitySpecificationRefMsg, _Mapping]]] = ...) -> None: ...

class GetSpecificationResponse(_message.Message):
    __slots__ = ("specification", "referenced_instance_descriptors", "referenced_datasets", "referenced_models")
    SPECIFICATION_FIELD_NUMBER: _ClassVar[int]
    REFERENCED_INSTANCE_DESCRIPTORS_FIELD_NUMBER: _ClassVar[int]
    REFERENCED_DATASETS_FIELD_NUMBER: _ClassVar[int]
    REFERENCED_MODELS_FIELD_NUMBER: _ClassVar[int]
    specification: _shared_qa_pb2.ConditionListSpecificationMsg
    referenced_instance_descriptors: _containers.RepeatedCompositeFieldContainer[_shared_qa_pb2.InstanceDescriptorMsg]
    referenced_datasets: _containers.RepeatedCompositeFieldContainer[_shared_ddx_pb2.DatasetMsg]
    referenced_models: _containers.RepeatedCompositeFieldContainer[_shared_ddx_pb2.ModelMsg]
    def __init__(self, specification: _Optional[_Union[_shared_qa_pb2.ConditionListSpecificationMsg, _Mapping]] = ..., referenced_instance_descriptors: _Optional[_Iterable[_Union[_shared_qa_pb2.InstanceDescriptorMsg, _Mapping]]] = ..., referenced_datasets: _Optional[_Iterable[_Union[_shared_ddx_pb2.DatasetMsg, _Mapping]]] = ..., referenced_models: _Optional[_Iterable[_Union[_shared_ddx_pb2.ModelMsg, _Mapping]]] = ...) -> None: ...

class GetConditionResponse(_message.Message):
    __slots__ = ("condition", "category_name", "referenced_instance_descriptors", "referenced_datasets", "referenced_models")
    CONDITION_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_NAME_FIELD_NUMBER: _ClassVar[int]
    REFERENCED_INSTANCE_DESCRIPTORS_FIELD_NUMBER: _ClassVar[int]
    REFERENCED_DATASETS_FIELD_NUMBER: _ClassVar[int]
    REFERENCED_MODELS_FIELD_NUMBER: _ClassVar[int]
    condition: _shared_qa_pb2.QualityConditionMsg
    category_name: str
    referenced_instance_descriptors: _containers.RepeatedCompositeFieldContainer[_shared_qa_pb2.InstanceDescriptorMsg]
    referenced_datasets: _containers.RepeatedCompositeFieldContainer[_shared_ddx_pb2.DatasetMsg]
    referenced_models: _containers.RepeatedCompositeFieldContainer[_shared_ddx_pb2.ModelMsg]
    def __init__(self, condition: _Optional[_Union[_shared_qa_pb2.QualityConditionMsg, _Mapping]] = ..., category_name: _Optional[str] = ..., referenced_instance_descriptors: _Optional[_Iterable[_Union[_shared_qa_pb2.InstanceDescriptorMsg, _Mapping]]] = ..., referenced_datasets: _Optional[_Iterable[_Union[_shared_ddx_pb2.DatasetMsg, _Mapping]]] = ..., referenced_models: _Optional[_Iterable[_Union[_shared_ddx_pb2.ModelMsg, _Mapping]]] = ...) -> None: ...

class GetDatasetDetailsResponse(_message.Message):
    __slots__ = ("datasets", "associations")
    DATASETS_FIELD_NUMBER: _ClassVar[int]
    ASSOCIATIONS_FIELD_NUMBER: _ClassVar[int]
    datasets: _containers.RepeatedCompositeFieldContainer[_shared_ddx_pb2.DatasetMsg]
    associations: _containers.RepeatedCompositeFieldContainer[_shared_ddx_pb2.AssociationMsg]
    def __init__(self, datasets: _Optional[_Iterable[_Union[_shared_ddx_pb2.DatasetMsg, _Mapping]]] = ..., associations: _Optional[_Iterable[_Union[_shared_ddx_pb2.AssociationMsg, _Mapping]]] = ...) -> None: ...

class ProjectWorkspaceMsg(_message.Message):
    __slots__ = ("project_id", "workspace_handle", "dataset_ids", "is_master_database_workspace")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_HANDLE_FIELD_NUMBER: _ClassVar[int]
    DATASET_IDS_FIELD_NUMBER: _ClassVar[int]
    IS_MASTER_DATABASE_WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    project_id: int
    workspace_handle: int
    dataset_ids: _containers.RepeatedScalarFieldContainer[int]
    is_master_database_workspace: bool
    def __init__(self, project_id: _Optional[int] = ..., workspace_handle: _Optional[int] = ..., dataset_ids: _Optional[_Iterable[int]] = ..., is_master_database_workspace: bool = ...) -> None: ...

class QualitySpecificationRefMsg(_message.Message):
    __slots__ = ("quality_specification_id", "name")
    QUALITY_SPECIFICATION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    quality_specification_id: int
    name: str
    def __init__(self, quality_specification_id: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...
