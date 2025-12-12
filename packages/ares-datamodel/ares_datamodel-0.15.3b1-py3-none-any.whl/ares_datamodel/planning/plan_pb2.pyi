import ares_struct_pb2 as _ares_struct_pb2
import ares_data_type_pb2 as _ares_data_type_pb2
import ares_outcome_enum_pb2 as _ares_outcome_enum_pb2
import request_metadata_pb2 as _request_metadata_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PlanningRequest(_message.Message):
    __slots__ = ("planning_parameters", "adapter_settings", "analysis_results", "metadata")
    PLANNING_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    ADAPTER_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_RESULTS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    planning_parameters: _containers.RepeatedCompositeFieldContainer[PlanningParameter]
    adapter_settings: _ares_struct_pb2.AresStruct
    analysis_results: _containers.RepeatedScalarFieldContainer[float]
    metadata: _request_metadata_pb2.RequestMetadata
    def __init__(self, planning_parameters: _Optional[_Iterable[_Union[PlanningParameter, _Mapping]]] = ..., adapter_settings: _Optional[_Union[_ares_struct_pb2.AresStruct, _Mapping]] = ..., analysis_results: _Optional[_Iterable[float]] = ..., metadata: _Optional[_Union[_request_metadata_pb2.RequestMetadata, _Mapping]] = ...) -> None: ...

class PlanningResponse(_message.Message):
    __slots__ = ("planned_parameters", "planning_outcome", "error_string")
    PLANNED_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    PLANNING_OUTCOME_FIELD_NUMBER: _ClassVar[int]
    ERROR_STRING_FIELD_NUMBER: _ClassVar[int]
    planned_parameters: _containers.RepeatedCompositeFieldContainer[PlannedParameter]
    planning_outcome: _ares_outcome_enum_pb2.Outcome
    error_string: str
    def __init__(self, planned_parameters: _Optional[_Iterable[_Union[PlannedParameter, _Mapping]]] = ..., planning_outcome: _Optional[_Union[_ares_outcome_enum_pb2.Outcome, str]] = ..., error_string: _Optional[str] = ...) -> None: ...

class PlanningParameter(_message.Message):
    __slots__ = ("parameter_name", "minimum_value", "maximum_value", "minimum_precision", "parameter_history", "data_type", "metadata", "is_planned", "is_result", "planner_name", "initial_value")
    PARAMETER_NAME_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_VALUE_FIELD_NUMBER: _ClassVar[int]
    MAXIMUM_VALUE_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_PRECISION_FIELD_NUMBER: _ClassVar[int]
    PARAMETER_HISTORY_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    IS_PLANNED_FIELD_NUMBER: _ClassVar[int]
    IS_RESULT_FIELD_NUMBER: _ClassVar[int]
    PLANNER_NAME_FIELD_NUMBER: _ClassVar[int]
    INITIAL_VALUE_FIELD_NUMBER: _ClassVar[int]
    parameter_name: str
    minimum_value: float
    maximum_value: float
    minimum_precision: float
    parameter_history: _containers.RepeatedCompositeFieldContainer[ParameterHistoryInfo]
    data_type: _ares_data_type_pb2.AresDataType
    metadata: PlannerMetadata
    is_planned: bool
    is_result: bool
    planner_name: str
    initial_value: _ares_struct_pb2.AresValue
    def __init__(self, parameter_name: _Optional[str] = ..., minimum_value: _Optional[float] = ..., maximum_value: _Optional[float] = ..., minimum_precision: _Optional[float] = ..., parameter_history: _Optional[_Iterable[_Union[ParameterHistoryInfo, _Mapping]]] = ..., data_type: _Optional[_Union[_ares_data_type_pb2.AresDataType, str]] = ..., metadata: _Optional[_Union[PlannerMetadata, _Mapping]] = ..., is_planned: bool = ..., is_result: bool = ..., planner_name: _Optional[str] = ..., initial_value: _Optional[_Union[_ares_struct_pb2.AresValue, _Mapping]] = ...) -> None: ...

class ParameterHistoryInfo(_message.Message):
    __slots__ = ("planned_value", "achieved_value")
    PLANNED_VALUE_FIELD_NUMBER: _ClassVar[int]
    ACHIEVED_VALUE_FIELD_NUMBER: _ClassVar[int]
    planned_value: _ares_struct_pb2.AresValue
    achieved_value: _ares_struct_pb2.AresValue
    def __init__(self, planned_value: _Optional[_Union[_ares_struct_pb2.AresValue, _Mapping]] = ..., achieved_value: _Optional[_Union[_ares_struct_pb2.AresValue, _Mapping]] = ...) -> None: ...

class PlannedParameter(_message.Message):
    __slots__ = ("parameter_name", "parameter_value", "metadata")
    PARAMETER_NAME_FIELD_NUMBER: _ClassVar[int]
    PARAMETER_VALUE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    parameter_name: str
    parameter_value: _ares_struct_pb2.AresValue
    metadata: PlannerMetadata
    def __init__(self, parameter_name: _Optional[str] = ..., parameter_value: _Optional[_Union[_ares_struct_pb2.AresValue, _Mapping]] = ..., metadata: _Optional[_Union[PlannerMetadata, _Mapping]] = ...) -> None: ...

class PlannerMetadata(_message.Message):
    __slots__ = ("metadata_name",)
    METADATA_NAME_FIELD_NUMBER: _ClassVar[int]
    metadata_name: str
    def __init__(self, metadata_name: _Optional[str] = ...) -> None: ...
