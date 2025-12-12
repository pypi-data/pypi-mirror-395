import datetime
from enum import Enum
from typing import Union, Any, List, Optional

from pydantic import BaseModel, Field, TypeAdapter, field_validator, field_serializer
from pydantic_core.core_schema import FieldValidationInfo

template_csv_file_headers = """SourceListName,SourceFlowName,SourceFlowUUID,SourceFlowContext,SourceUnit,MatchCondition,ConversionFactor,TargetListName,TargetFlowName,TargetFlowUUID,TargetFlowContext,TargetUnit,Mapper,Verifier,LastUpdated,MemoMapper,MemoVerifier,MemoSource,MemoTarget"""  # noqa: E501


class FlowListFields(BaseModel):
    """
    Flow List format schema taken from https://github.com/USEPA/fedelemflowlist/blob/master/format%20specs/FlowList.md

    Based on

    See for live example https://github.com/USEPA/fedelemflowlist/blob/master/Jupyter/run_mappings.ipynb
    """

    Flowable: str = Field(description="The flow name")
    CASNo: Union[str, None] = Field(
        default=None, description="CAS number", serialization_alias="CAS No"
    )
    Formula: Union[str, None] = Field(default=None, description="Chemical formula")
    Synonyms: Union[str, None] = Field(default=None, description="Flow synonyms")
    Unit: str = Field(
        description="The reference unit. uses [olca-schema](https://github.com/GreenDelta/olca-schema)"
        " units"
    )
    Class: str = Field(description="The flow class, e.g. `Energy` or `Chemical`")
    ExternalReference: Union[str, None] = Field(
        default=None,
        description="E.g. a web link",
        serialization_alias="External Reference",
    )
    Preferred: Union[int, None] = Field(
        default=None, description="`1` for preferred*, `0` for non-preferred"
    )
    Context: str = Field(
        description="A path-like set of context compartments in the form of directionality/"
        "environmental media/environmental compartment... e.g. emission/air/tropophere"
    )
    FlowUUID: str = Field(
        description="Unique hexadecimal ID for the flow",
        serialization_alias="Flow UUID",
    )
    AltUnit: Union[str, None] = Field(
        default=None, description="Alternate unit for the flow"
    )
    AltUnitConversionFactor: Union[float, None] = Field(
        default=None,
        description="Conversion factor in the form of "
        "alternate units/reference unit",
    )


class MappingChoices(Enum):
    """
    MatchCondition:
    Single character. =, >,<,~. Meaning 'equal to','a superset of', 'a subset of', 'a proxy for'.
    Assumes = if not present
    """

    EQUAL_TO = "="
    A_SUPERSET_OF = ">"
    A_SUBSET_OF = "<"
    A_PROXY_FOR = "~"


class FlowmappingFields(BaseModel):
    """
    Mapping schema taken from GLAD:
        https://github.com/UNEP-Economy-Division/GLAD-ElementaryFlowResources/tree/master/Formats
    Similar to https://github.com/USEPA/fedelemflowlist/blob/master/format%20specs/FlowMapping.md
    See for USEPA code example https://github.com/USEPA/fedelemflowlist/blob/master/Jupyter/run_mappings.ipynb

    """

    SourceListName: str = Field(
        description="Name and version of the source flowlist, e.g. `openLCA1.7` or `TRACI2.1`"
    )
    SourceFlowName: str = Field(description="Name of the source flow")
    SourceFlowUUID: Union[str, None] = Field(
        default=None,
        description="If no UUID present, UUID generated based on olca algorithm",
    )
    SourceFlowContext: str = Field(
        description="Compartments separated by /, like emission/air"
    )
    SourceUnit: str = Field(description="A unit abbreviation, like kg")

    SourceGeography: Union[str, None] = Field(
        None, description="Optional field containing source location information"
    )

    MatchCondition: MappingChoices = Field(
        default=MappingChoices.EQUAL_TO.value,
        description="Single character. =, >,<,~. Meaning 'equal to','a superset of',"
        " 'a subset of', 'a proxy for'. "
        "Assumes = if not present",
    )
    ConversionFactor: Union[float, None] = Field(
        default=1,
        description="Value for multiplying with source flow to"
        " equal target flow."
        " Assumes 1 if not present",
    )
    TargetListName: str = Field(
        description="Name and version of the target flowlist, e.g. openLCA1.7 or TRACI2.1"
    )
    TargetFlowName: str = Field(description="Name of the Fed Commons flowable")
    TargetFlowUUID: str = Field(description="UUID for Fed Commons flow")
    TargetFlowContext: str = Field(
        description="Fed commons context, in form like emission/air"
    )
    TargetUnit: str = Field(description="A unit abbreviation, like kg")
    Mapper: Union[str, None] = Field(
        default=None, description="Person creating the mapping"
    )
    Verifier: Union[str, None] = Field(
        default=None, description="Person verifying the mapping"
    )
    LastUpdated: Union[datetime.date, datetime.datetime, None] = Field(
        default=None, description="Date mapping last updated"
    )

    MemoMapper: Union[str, None] = Field(default=None, description="Memo by Mapper")
    MemoVerifier: Union[str, None] = Field(default=None, description="Memo by Verifier")
    MemoSource: Union[str, None] = Field(
        default=None, description="Memo by Source EF system admin"
    )
    MemoTarget: Union[str, None] = Field(
        default=None, description="Memo by Target EF system admin"
    )

    TargetGeography: Union[str, None] = Field(
        None, description="Optional field containing target location information"
    )

    class Config:
        use_enum_values = True

    @field_validator("LastUpdated", mode="after")
    def cast_to_date(cls, v):
        """allows assigning a datetime object to a date field"""
        if isinstance(v, datetime.datetime):
            return v.date()
        return v

    @field_validator("ConversionFactor", mode="before")
    def assume_absent_factor_is_one(cls, value: Any, info: FieldValidationInfo):
        if value is None:
            return float(1.0)
        else:
            return value

    @field_validator("TargetFlowUUID", "SourceFlowUUID", mode="before")
    def load_omni_uuids_as_none(cls, value: Any, info: FieldValidationInfo):
        if (
            isinstance(value, str)
            and value.upper() == "FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF"
        ):
            return ""
        else:
            return value

    @field_serializer("TargetFlowUUID", "SourceFlowUUID", when_used="json")
    def empty_flow_uuid_as_string(self, flow_uuid_str: str, info) -> str:
        if flow_uuid_str == "":
            return "FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF"
        else:
            return flow_uuid_str


class SourceFlowmappingFields(BaseModel):
    SourceListName: str = Field(
        description="Name and version of the source flowlist, e.g. `openLCA1.7` or `TRACI2.1`"
    )
    SourceFlowName: str = Field(description="Name of the source flow")
    SourceFlowUUID: Union[str, None] = Field(
        default=None,
        description="If no UUID present, UUID generated based on olca algorithm",
    )
    SourceFlowContext: str = Field(
        description="Compartments separated by /, like emission/air"
    )
    SourceUnit: str = Field(description="A unit abbreviation, like kg")
    MatchCondition: MappingChoices = Field(
        default=MappingChoices.EQUAL_TO.value,
        description="Single character. =, >,<,~. Meaning 'equal to','a superset of',"
        " 'a subset of', 'a proxy for'. "
        "Assumes = if not present",
    )
    ConversionFactor: Union[float, None] = Field(
        default=1,
        description="Value for multiplying with source flow to"
        " equal target flow. "
        "Assumes 1 if not present",
    )

    class Config:
        use_enum_values = True


class TargetFlowmappingFields(BaseModel):
    MatchCondition: MappingChoices = Field(
        default=MappingChoices.EQUAL_TO.value,
        description="Single character. =, >,<,~. Meaning 'equal to','a superset of',"
        " 'a subset of', 'a proxy for'. "
        "Assumes = if not present",
    )
    ConversionFactor: Union[float, None] = Field(
        default=1,
        description="Value for multiplying with source flow to"
        " equal target flow. "
        "Assumes 1 if not present",
    )
    TargetListName: str = Field(
        description="Name and version of the target flowlist, "
        "e.g. openLCA1.7 or TRACI2.1"
    )
    TargetFlowName: str = Field(description="Name of the Fed Commons flowable")
    TargetFlowUUID: str = Field(description="UUID for Fed Commons flow")
    TargetFlowContext: str = Field(
        description="Fed commons context, in form like emission/air"
    )
    TargetUnit: str = Field(description="A unit abbreviation, like kg")
    Mapper: Union[str, None] = Field(
        default=None, description="Person creating the mapping"
    )
    Verifier: Union[str, None] = Field(
        default=None, description="Person verifying the mapping"
    )
    LastUpdated: Union[datetime.date, None] = Field(
        default=None, description="Date mapping last updated"
    )

    MemoMapper: Union[str, None] = Field(default=None, description="Memo by Mapper")
    MemoVerifier: Union[str, None] = Field(default=None, description="Memo by Verifier")
    MemoSource: Union[str, None] = Field(
        default=None, description="Memo by Source EF system admin"
    )
    MemoTarget: Union[str, None] = Field(
        default=None, description="Memo by Target EF system admin"
    )

    class Config:
        use_enum_values = True


class FlowQuery(BaseModel):
    SourceListNames: List[str] = Field(
        description="Name and version of the source flowlist / nomenclature, "
        "e.g. `openLCA1.7` or `TRACI2.1`"
    )

    SourceFlowName: Optional[str] = Field(
        default=None, description="Name of the source flow"
    )
    SourceFlowUUID: str = Field(
        description="Can be a string or uuid in some nomenclatures"
    )
    SourceFlowContexts: Optional[List[str]] = Field(
        default_factory=list,
        description="List of compartments separated by '/', like 'emission/air'",
    )
    SourceUnit: Optional[str] = Field(
        default=None, description="A unit abbreviation, like kg"
    )

    SourceGeography: Optional[str] = Field(
        None, description="Optional field for matching source location information"
    )
    TargetGeography: Optional[str] = Field(
        None, description="Optional field for matching target location information"
    )

    TargetListNames: Optional[List[str]] = Field(
        default_factory=list,
        description="Name and version of the target flowlist / nomenclature, e.g. `openLCA1.7` or `TRACI2.1`",
    )
    TargetFlowContexts: Optional[List[str]] = Field(
        default_factory=list,
        description="List of compartments separated by '/', like 'emission/air'",
    )

    class Config:
        use_enum_values = True


list_of_flow_mappings = TypeAdapter(list[FlowmappingFields])
list_of_target_flow_mappings = TypeAdapter(list[TargetFlowmappingFields])
list_of_source_flow_mappings = TypeAdapter(list[SourceFlowmappingFields])
