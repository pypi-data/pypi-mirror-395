from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WireFieldType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FIELD_TYPE_UNKNOWN: _ClassVar[WireFieldType]
    FIELD_TYPE_INT16: _ClassVar[WireFieldType]
    FIELD_TYPE_INT32: _ClassVar[WireFieldType]
    FIELD_TYPE_INT64: _ClassVar[WireFieldType]
    FIELD_TYPE_FLOAT: _ClassVar[WireFieldType]
    FIELD_TYPE_DOUBLE: _ClassVar[WireFieldType]
    FIELD_TYPE_STRING: _ClassVar[WireFieldType]
    FIELD_TYPE_BYTES: _ClassVar[WireFieldType]
    FIELD_TYPE_UUID: _ClassVar[WireFieldType]
    FIELD_TYPE_DATETICKS: _ClassVar[WireFieldType]
    FIELD_TYPE_GEOMETRY: _ClassVar[WireFieldType]
FIELD_TYPE_UNKNOWN: WireFieldType
FIELD_TYPE_INT16: WireFieldType
FIELD_TYPE_INT32: WireFieldType
FIELD_TYPE_INT64: WireFieldType
FIELD_TYPE_FLOAT: WireFieldType
FIELD_TYPE_DOUBLE: WireFieldType
FIELD_TYPE_STRING: WireFieldType
FIELD_TYPE_BYTES: WireFieldType
FIELD_TYPE_UUID: WireFieldType
FIELD_TYPE_DATETICKS: WireFieldType
FIELD_TYPE_GEOMETRY: WireFieldType

class UUID(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: bytes
    def __init__(self, value: _Optional[bytes] = ...) -> None: ...

class EnvelopeMsg(_message.Message):
    __slots__ = ("x_min", "y_min", "x_max", "y_max")
    X_MIN_FIELD_NUMBER: _ClassVar[int]
    Y_MIN_FIELD_NUMBER: _ClassVar[int]
    X_MAX_FIELD_NUMBER: _ClassVar[int]
    Y_MAX_FIELD_NUMBER: _ClassVar[int]
    x_min: float
    y_min: float
    x_max: float
    y_max: float
    def __init__(self, x_min: _Optional[float] = ..., y_min: _Optional[float] = ..., x_max: _Optional[float] = ..., y_max: _Optional[float] = ...) -> None: ...

class ShapeMsg(_message.Message):
    __slots__ = ("esri_shape", "wkb", "envelope", "spatial_reference")
    ESRI_SHAPE_FIELD_NUMBER: _ClassVar[int]
    WKB_FIELD_NUMBER: _ClassVar[int]
    ENVELOPE_FIELD_NUMBER: _ClassVar[int]
    SPATIAL_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    esri_shape: bytes
    wkb: bytes
    envelope: EnvelopeMsg
    spatial_reference: SpatialReferenceMsg
    def __init__(self, esri_shape: _Optional[bytes] = ..., wkb: _Optional[bytes] = ..., envelope: _Optional[_Union[EnvelopeMsg, _Mapping]] = ..., spatial_reference: _Optional[_Union[SpatialReferenceMsg, _Mapping]] = ...) -> None: ...

class AttributeValue(_message.Message):
    __slots__ = ("db_null", "short_int_value", "int_value", "big_int_value", "float_value", "double_value", "string_value", "date_time_ticks_value", "uuid_value", "blob_value")
    DB_NULL_FIELD_NUMBER: _ClassVar[int]
    SHORT_INT_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT_VALUE_FIELD_NUMBER: _ClassVar[int]
    BIG_INT_VALUE_FIELD_NUMBER: _ClassVar[int]
    FLOAT_VALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    DATE_TIME_TICKS_VALUE_FIELD_NUMBER: _ClassVar[int]
    UUID_VALUE_FIELD_NUMBER: _ClassVar[int]
    BLOB_VALUE_FIELD_NUMBER: _ClassVar[int]
    db_null: bool
    short_int_value: int
    int_value: int
    big_int_value: int
    float_value: float
    double_value: float
    string_value: str
    date_time_ticks_value: int
    uuid_value: UUID
    blob_value: bytes
    def __init__(self, db_null: bool = ..., short_int_value: _Optional[int] = ..., int_value: _Optional[int] = ..., big_int_value: _Optional[int] = ..., float_value: _Optional[float] = ..., double_value: _Optional[float] = ..., string_value: _Optional[str] = ..., date_time_ticks_value: _Optional[int] = ..., uuid_value: _Optional[_Union[UUID, _Mapping]] = ..., blob_value: _Optional[bytes] = ...) -> None: ...

class GdbObjectMsg(_message.Message):
    __slots__ = ("object_id", "class_handle", "values", "shape")
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    CLASS_HANDLE_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    object_id: int
    class_handle: int
    values: _containers.RepeatedCompositeFieldContainer[AttributeValue]
    shape: ShapeMsg
    def __init__(self, object_id: _Optional[int] = ..., class_handle: _Optional[int] = ..., values: _Optional[_Iterable[_Union[AttributeValue, _Mapping]]] = ..., shape: _Optional[_Union[ShapeMsg, _Mapping]] = ...) -> None: ...

class ColumnarGdbObjects(_message.Message):
    __slots__ = ("row_count", "columns")
    ROW_COUNT_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    row_count: int
    columns: _containers.RepeatedCompositeFieldContainer[Column]
    def __init__(self, row_count: _Optional[int] = ..., columns: _Optional[_Iterable[_Union[Column, _Mapping]]] = ...) -> None: ...

class Int16Column(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, values: _Optional[_Iterable[int]] = ...) -> None: ...

class Int32Column(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, values: _Optional[_Iterable[int]] = ...) -> None: ...

class Int64Column(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, values: _Optional[_Iterable[int]] = ...) -> None: ...

class FloatColumn(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, values: _Optional[_Iterable[float]] = ...) -> None: ...

class DoubleColumn(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, values: _Optional[_Iterable[float]] = ...) -> None: ...

class StringColumn(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...

class BytesColumn(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, values: _Optional[_Iterable[bytes]] = ...) -> None: ...

class UuidColumn(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[UUID]
    def __init__(self, values: _Optional[_Iterable[_Union[UUID, _Mapping]]] = ...) -> None: ...

class DateTicksColumn(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, values: _Optional[_Iterable[int]] = ...) -> None: ...

class GeometryColumn(_message.Message):
    __slots__ = ("shapes",)
    SHAPES_FIELD_NUMBER: _ClassVar[int]
    shapes: _containers.RepeatedCompositeFieldContainer[ShapeMsg]
    def __init__(self, shapes: _Optional[_Iterable[_Union[ShapeMsg, _Mapping]]] = ...) -> None: ...

class Column(_message.Message):
    __slots__ = ("name", "type", "nulls", "short_int_values", "int_values", "big_int_values", "float_values", "double_values", "string_values", "byte_values", "uuid_values", "date_time_ticks_values", "geometries")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NULLS_FIELD_NUMBER: _ClassVar[int]
    SHORT_INT_VALUES_FIELD_NUMBER: _ClassVar[int]
    INT_VALUES_FIELD_NUMBER: _ClassVar[int]
    BIG_INT_VALUES_FIELD_NUMBER: _ClassVar[int]
    FLOAT_VALUES_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_VALUES_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUES_FIELD_NUMBER: _ClassVar[int]
    BYTE_VALUES_FIELD_NUMBER: _ClassVar[int]
    UUID_VALUES_FIELD_NUMBER: _ClassVar[int]
    DATE_TIME_TICKS_VALUES_FIELD_NUMBER: _ClassVar[int]
    GEOMETRIES_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: WireFieldType
    nulls: bytes
    short_int_values: Int16Column
    int_values: Int32Column
    big_int_values: Int64Column
    float_values: FloatColumn
    double_values: DoubleColumn
    string_values: StringColumn
    byte_values: BytesColumn
    uuid_values: UuidColumn
    date_time_ticks_values: DateTicksColumn
    geometries: GeometryColumn
    def __init__(self, name: _Optional[str] = ..., type: _Optional[_Union[WireFieldType, str]] = ..., nulls: _Optional[bytes] = ..., short_int_values: _Optional[_Union[Int16Column, _Mapping]] = ..., int_values: _Optional[_Union[Int32Column, _Mapping]] = ..., big_int_values: _Optional[_Union[Int64Column, _Mapping]] = ..., float_values: _Optional[_Union[FloatColumn, _Mapping]] = ..., double_values: _Optional[_Union[DoubleColumn, _Mapping]] = ..., string_values: _Optional[_Union[StringColumn, _Mapping]] = ..., byte_values: _Optional[_Union[BytesColumn, _Mapping]] = ..., uuid_values: _Optional[_Union[UuidColumn, _Mapping]] = ..., date_time_ticks_values: _Optional[_Union[DateTicksColumn, _Mapping]] = ..., geometries: _Optional[_Union[GeometryColumn, _Mapping]] = ...) -> None: ...

class GdbObjRefMsg(_message.Message):
    __slots__ = ("class_handle", "object_id")
    CLASS_HANDLE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    class_handle: int
    object_id: int
    def __init__(self, class_handle: _Optional[int] = ..., object_id: _Optional[int] = ...) -> None: ...

class ObjectClassMsg(_message.Message):
    __slots__ = ("class_handle", "workspace_handle", "name", "alias", "geometry_type", "spatial_reference", "fields", "ddx_model_id")
    CLASS_HANDLE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_HANDLE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ALIAS_FIELD_NUMBER: _ClassVar[int]
    GEOMETRY_TYPE_FIELD_NUMBER: _ClassVar[int]
    SPATIAL_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    DDX_MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    class_handle: int
    workspace_handle: int
    name: str
    alias: str
    geometry_type: int
    spatial_reference: SpatialReferenceMsg
    fields: _containers.RepeatedCompositeFieldContainer[FieldMsg]
    ddx_model_id: int
    def __init__(self, class_handle: _Optional[int] = ..., workspace_handle: _Optional[int] = ..., name: _Optional[str] = ..., alias: _Optional[str] = ..., geometry_type: _Optional[int] = ..., spatial_reference: _Optional[_Union[SpatialReferenceMsg, _Mapping]] = ..., fields: _Optional[_Iterable[_Union[FieldMsg, _Mapping]]] = ..., ddx_model_id: _Optional[int] = ...) -> None: ...

class WorkspaceMsg(_message.Message):
    __slots__ = ("workspace_handle", "workspace_db_type", "path", "version_name", "default_version_name", "default_version_description", "default_version_creation_ticks", "connection_properties", "default_version_modification_ticks")
    WORKSPACE_HANDLE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_DB_TYPE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    VERSION_NAME_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_VERSION_NAME_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_VERSION_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_VERSION_CREATION_TICKS_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_VERSION_MODIFICATION_TICKS_FIELD_NUMBER: _ClassVar[int]
    workspace_handle: int
    workspace_db_type: int
    path: str
    version_name: str
    default_version_name: str
    default_version_description: str
    default_version_creation_ticks: int
    connection_properties: _containers.RepeatedCompositeFieldContainer[KeyValuePairMsg]
    default_version_modification_ticks: int
    def __init__(self, workspace_handle: _Optional[int] = ..., workspace_db_type: _Optional[int] = ..., path: _Optional[str] = ..., version_name: _Optional[str] = ..., default_version_name: _Optional[str] = ..., default_version_description: _Optional[str] = ..., default_version_creation_ticks: _Optional[int] = ..., connection_properties: _Optional[_Iterable[_Union[KeyValuePairMsg, _Mapping]]] = ..., default_version_modification_ticks: _Optional[int] = ...) -> None: ...

class KeyValuePairMsg(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class FieldMsg(_message.Message):
    __slots__ = ("name", "alias_name", "type", "length", "domain_name", "scale", "precision", "is_nullable", "is_editable")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ALIAS_NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_NAME_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    PRECISION_FIELD_NUMBER: _ClassVar[int]
    IS_NULLABLE_FIELD_NUMBER: _ClassVar[int]
    IS_EDITABLE_FIELD_NUMBER: _ClassVar[int]
    name: str
    alias_name: str
    type: int
    length: int
    domain_name: str
    scale: int
    precision: int
    is_nullable: bool
    is_editable: bool
    def __init__(self, name: _Optional[str] = ..., alias_name: _Optional[str] = ..., type: _Optional[int] = ..., length: _Optional[int] = ..., domain_name: _Optional[str] = ..., scale: _Optional[int] = ..., precision: _Optional[int] = ..., is_nullable: bool = ..., is_editable: bool = ...) -> None: ...

class SpatialReferenceMsg(_message.Message):
    __slots__ = ("spatial_reference_esri_xml", "spatial_reference_wkt", "spatial_reference_wkid")
    SPATIAL_REFERENCE_ESRI_XML_FIELD_NUMBER: _ClassVar[int]
    SPATIAL_REFERENCE_WKT_FIELD_NUMBER: _ClassVar[int]
    SPATIAL_REFERENCE_WKID_FIELD_NUMBER: _ClassVar[int]
    spatial_reference_esri_xml: str
    spatial_reference_wkt: str
    spatial_reference_wkid: int
    def __init__(self, spatial_reference_esri_xml: _Optional[str] = ..., spatial_reference_wkt: _Optional[str] = ..., spatial_reference_wkid: _Optional[int] = ...) -> None: ...

class ResultObjectMsg(_message.Message):
    __slots__ = ("update", "insert", "delete", "notifications", "has_warning")
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    INSERT_FIELD_NUMBER: _ClassVar[int]
    DELETE_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATIONS_FIELD_NUMBER: _ClassVar[int]
    HAS_WARNING_FIELD_NUMBER: _ClassVar[int]
    update: GdbObjectMsg
    insert: InsertedObjectMsg
    delete: GdbObjRefMsg
    notifications: _containers.RepeatedScalarFieldContainer[str]
    has_warning: bool
    def __init__(self, update: _Optional[_Union[GdbObjectMsg, _Mapping]] = ..., insert: _Optional[_Union[InsertedObjectMsg, _Mapping]] = ..., delete: _Optional[_Union[GdbObjRefMsg, _Mapping]] = ..., notifications: _Optional[_Iterable[str]] = ..., has_warning: bool = ...) -> None: ...

class InsertedObjectMsg(_message.Message):
    __slots__ = ("inserted_object", "original_reference")
    INSERTED_OBJECT_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    inserted_object: GdbObjectMsg
    original_reference: GdbObjRefMsg
    def __init__(self, inserted_object: _Optional[_Union[GdbObjectMsg, _Mapping]] = ..., original_reference: _Optional[_Union[GdbObjRefMsg, _Mapping]] = ...) -> None: ...

class DatasetZSource(_message.Message):
    __slots__ = ("dataset_name", "z_source")
    DATASET_NAME_FIELD_NUMBER: _ClassVar[int]
    Z_SOURCE_FIELD_NUMBER: _ClassVar[int]
    dataset_name: str
    z_source: int
    def __init__(self, dataset_name: _Optional[str] = ..., z_source: _Optional[int] = ...) -> None: ...
