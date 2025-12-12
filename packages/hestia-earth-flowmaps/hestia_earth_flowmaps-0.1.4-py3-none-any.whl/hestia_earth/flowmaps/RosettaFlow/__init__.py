import os
import datetime
import logging
from datetime import date
from decimal import Decimal
from functools import cache
from pathlib import Path
from typing import Union, List, Optional, Dict, Tuple
from functools import reduce
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from hestia_earth.utils.api import download_hestia
from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    TypeAdapter,
    AliasChoices,
    validate_call,
)

from .file_shemas import (
    MappingChoices,
    FlowmappingFields,
    list_of_flow_mappings,
    template_csv_file_headers,
    FlowQuery,
)
from .file_validation import errors_on_lines

cached_download_hestia = cache(download_hestia)

logger = logging.getLogger(__name__)
logging.basicConfig(level=os.environ.get("LOGLEVEL", logging.INFO))

_FLOW_REVERSE_COLUMNS = {
    "SourceListName": "TargetListName",
    "SourceFlowName": "TargetFlowName",
    "SourceFlowUUID": "TargetFlowUUID",
    "SourceFlowContext": "TargetFlowContext",
    "SourceUnit": "TargetUnit",
    "MemoSource": "MemoTarget",
    "SourceGeography": "TargetGeography",
}


def _get_reverse_column(column: str):
    return next((k for k, v in _FLOW_REVERSE_COLUMNS.items() if v == column), None)


def _filter_df_str_list(
    df: pd.DataFrame,
    filter_col: str,
    filter_value: Union[str, List[str]],
    is_reverse_column: bool = False,
):
    values = (
        filter_value
        if isinstance(filter_value, list)
        else [filter_value] if filter_value else []
    )
    return (
        df.loc[
            df[
                _get_reverse_column(filter_col) if is_reverse_column else filter_col
            ].isin(values)
        ]
        if not df.empty and values
        else df
    )


def _filter_df_mapping_str_list(
    df: pd.DataFrame,
    filters: List[Tuple[str, Union[str, List[str]]]],
    is_reverse_column: bool = False,
):
    return reduce(
        lambda prev, curr: _filter_df_str_list(
            prev, curr[0], curr[1], is_reverse_column
        ),
        filters,
        df,
    )


class RosettaMap:
    def __init__(self, name: str):
        self.data = name
        self.edge = set()

    def __repr__(self):
        return f"Node: '{self.data}' edges: {len(self.edge)}"

    def add_edge(self, edge):
        self.edge.add(edge)

    def traverse(
        self, destinations: List[str] = None, max_depth: int = None
    ) -> List[str]:
        traversed = []
        queue = []
        result = []
        for ed in self.edge:
            queue.append(ed)
        while len(queue) != 0:
            vertex = queue.pop()
            if vertex not in traversed:
                result.append(vertex.data)
                if destinations and vertex.data in destinations:
                    return result
                if max_depth and len(result) > max_depth:
                    return result
                traversed.append(vertex)
                for ed in vertex.edge:
                    queue.append(ed)
        return result


class MapperError(Exception):
    """Base exception for flow mapping Errors"""


class ProductFlowMapperError(MapperError):
    """Base exception for flow mapping Errors related to product flows"""


class ResultNode(BaseModel):
    list_name: str = Field(
        default=None, exclude=True, description="What flowmap list this came from"
    )
    match_condition: Optional[MappingChoices] = Field(default=None, exclude=True)
    verifier: Optional[str] = Field(
        default=None, exclude=True, description="Person verifying the result"
    )
    mapper: Optional[str] = Field(
        default=None, exclude=True, description="Person creating the mapping"
    )

    class Config:
        use_enum_values = True


class MetaData(BaseModel):
    stepping_stones: List[Optional[ResultNode]] = Field(
        default=None,
        exclude=True,
        description="List of nomenclatures traversed to find candidate",
        examples=[
            [
                {
                    "list_name": "Ecoinvent 3.11",
                    "match_condition": "=",
                    "verifier": "Bob",
                    "mapper": "Alice",
                },
                {
                    "list_name": "EF v 2.0",
                    "match_condition": "=",
                    "verifier": "Bob",
                    "mapper": "Alice",
                },
                {
                    "list_name": "HestiaList",
                    "match_condition": "~",
                    "verifier": "Bob",
                    "mapper": "Hestia",
                },
            ]
        ],
        # aka indirection. Candidate found by daisy-chaining 3 flowmaps.
    )


class CandidateFlow(BaseModel):
    MatchCondition: MappingChoices = Field(
        default=MappingChoices.EQUAL_TO,
        description="Single character. =, >,<,~. Meaning 'equal to','a superset of',"
        " 'a subset of', 'a proxy for'. "
        "Assumes = if not present",
    )
    ConversionFactor: Union[Decimal, None] = Field(
        default=1,
        description="Value for multiplying with source flow to"
        " equal target flow. "
        "Assumes 1 if not present",
    )
    ListName: str = Field(
        description="Name and version of the target flowlist, e.g. openLCA1.7 or TRACI2.1",
        validation_alias=AliasChoices("ListName", "TargetListName", "SourceListName"),
    )
    FlowName: str = Field(
        description="Name of the Fed Commons flowable",
        validation_alias=AliasChoices("FlowName", "TargetFlowName", "SourceFlowName"),
    )
    FlowUUID: str = Field(
        description="UUID for Fed Commons flow",
        validation_alias=AliasChoices("FlowUUID", "TargetFlowUUID", "SourceFlowUUID"),
    )

    FlowContext: str = Field(
        description="Fed commons context, in form like emission/air",
        validation_alias=AliasChoices(
            "FlowContext", "TargetFlowContext", "SourceFlowContext"
        ),
    )
    Unit: str = Field(
        description="A unit abbreviation, like kg",
        validation_alias=AliasChoices("Unit", "TargetUnit", "SourceUnit"),
    )
    Mapper: Union[str, None] = Field(
        default=None,
        description="Person creating the mapping",
        validation_alias=AliasChoices("Mapper", "TargetMapper", "SourceMapper"),
    )
    Verifier: Union[str, None] = Field(
        default=None,
        description="Person verifying the mapping",
        validation_alias=AliasChoices("Verifier", "TargetVerifier", "SourceVerifier"),
    )
    LastUpdated: Union[date, None] = Field(
        default=None,
        description="Date mapping last updated",
        validation_alias=AliasChoices(
            "LastUpdated", "TargetLastUpdated", "SourceLastUpdated"
        ),
    )

    MemoMapper: Union[str, None] = Field(
        default=None,
        description="Memo by Mapper",
        validation_alias=AliasChoices(
            "MemoMapper", "TargetMemoMapper", "SourceMemoMapper"
        ),
    )
    MemoVerifier: Union[str, None] = Field(
        default=None,
        description="Memo by Verifier",
        validation_alias=AliasChoices(
            "MemoVerifier", "TargetMemoVerifier", "SourceMemoVerifier"
        ),
    )
    Memo: Union[str, None] = Field(
        default=None,
        description="Memo by Source EF system admin",
        validation_alias=AliasChoices("MemoTarget", "MemoSource"),
    )

    meta_data: Optional[MetaData] = Field(
        default=None,
        exclude=True,
        description="Optional dictionary explaining how this result was found.",
    )
    Geography: Union[str, None] = Field(
        default=None,
        description="Optional field containing location information",
        validation_alias=AliasChoices(
            "Geography", "TargetGeography", "SourceGeography"
        ),
    )

    class Config:
        use_enum_values = True


list_of_candidate_flow_mappings = TypeAdapter(list[CandidateFlow])


class FlowMap:
    def __init__(
        self, flow_mapping_path: Path, default_filename: str = "new_mappings.csv"
    ):
        if flow_mapping_path.exists():
            self.flow_mapping_path = flow_mapping_path
        else:
            raise Exception("Invalid path {}".format(flow_mapping_path))

        self.all_flow_mappings = None
        self.rosetta_flow_map: dict[str, RosettaMap] = None
        self.have_indirect_mappings = False
        self.load_files()
        self.default_filename = default_filename

    def load_files(self):
        self.all_flow_mappings = self.get_all_flowmapping()
        self.make_rosetta_stone_map()
        self.have_indirect_mappings = self.contains_indirect_maps()

    def _get_valid_entries(self, file_path: str, name: Path):
        try:
            file_mappings = self.read_flow_file(file_path)
            return self.validate_csv_file(file_mappings)
        except ValidationError as e:
            logger.error("{} errors in file {}".format(e.error_count(), name))
            logger.error("Errors are on lines: {}.".format(errors_on_lines(e)))
            logger.error("Skipping file {} due to invalid format".format(name))
        except Exception:
            logger.error("Failed to load file {}".format(name))
        return None

    def get_all_flowmapping(self) -> pd.DataFrame:
        flow_mappings = pd.DataFrame()

        for name in self.flow_mapping_path.iterdir():
            if name.suffix == ".csv":
                logger.info(f"Loading '{name.name}'")
                file_path = (
                    name
                    if name.is_relative_to(self.flow_mapping_path)
                    else self.flow_mapping_path / name
                )
                valid_entries = self._get_valid_entries(file_path, name)
                if valid_entries is None:
                    continue

                try:
                    new_df = pd.DataFrame.from_dict(
                        list_of_flow_mappings.dump_python(valid_entries),
                        orient="columns",
                    )
                except Exception as err:
                    raise err

                flow_mappings = pd.concat([flow_mappings, new_df])
        return flow_mappings

    @staticmethod
    def read_flow_file(file_path) -> pd.DataFrame:
        flow_mapping = pd.read_csv(file_path, header=0)
        flow_mapping = flow_mapping.replace({np.nan: None})
        return flow_mapping

    @staticmethod
    def validate_csv_file(file_mappings: pd.DataFrame) -> list:
        try:
            valid_entries = list_of_flow_mappings.validate_python(
                file_mappings.to_dict(orient="records")
            )
        except ValidationError as e:
            raise e
        return valid_entries

    def add_map_to_file(
        self,
        source_flow: dict,
        hestia_term_id: str = None,
        term_dict: dict = None,
        source_list_name: str = "ecoinvent",
        match_condition: MappingChoices = MappingChoices.EQUAL_TO,
        target_flow_context: str = None,
        conversion_factor: Decimal = 1,
        memo_mapper: str = None,
        memo_source: str = None,
        memo_verifier: str = None,
        memo_target: str = None,
        output_file_path: Optional[Path] = None,
    ):
        if output_file_path:
            target_file_path = output_file_path
        else:
            target_file_path = self.flow_mapping_path / self.default_filename
        if not Path(target_file_path).exists():
            with open(target_file_path, "w") as f:
                f.write(template_csv_file_headers)

        if not hestia_term_id and not term_dict:
            raise Exception("Must specify hestia_term_id or term_dict")

        original_df = pd.read_csv(target_file_path)
        term_dict = term_dict or cached_download_hestia(node_id=hestia_term_id)
        new_row = FlowmappingFields(
            SourceListName=source_list_name,
            SourceFlowName=source_flow["name"],
            SourceFlowUUID=source_flow["@id"],
            SourceFlowContext=source_flow.get("category", "Locations"),
            SourceUnit=_pull_out_unit(source_flow),
            MatchCondition=match_condition,
            ConversionFactor=conversion_factor,
            TargetListName="HestiaList",
            TargetFlowName=term_dict.get("name", hestia_term_id),
            TargetFlowUUID=term_dict.get("@id", hestia_term_id),
            TargetFlowContext=target_flow_context or term_dict.get("termType"),
            TargetUnit=term_dict.get("units", "NONE"),
            Mapper="HESTIA",
            Verifier="REQUIRES VALIDATION",
            LastUpdated=datetime.date.today(),
            MemoMapper=memo_mapper,
            MemoSource=memo_source,
            MemoVerifier=memo_verifier,
            MemoTarget=memo_target,
        )

        try:
            new_row_df = pd.DataFrame.from_dict(
                [new_row.model_dump(mode="json")], orient="columns"
            )
        except Exception as err:
            raise err
        out = pd.concat([original_df, new_row_df])
        out.drop_duplicates(inplace=True)
        out.to_csv(target_file_path, index=False)

    @staticmethod
    def add_row_to_file(new_row: FlowmappingFields, output_file_path: Path):
        if not output_file_path.exists():
            with open(output_file_path, "w") as f:
                f.write(template_csv_file_headers)

        original_df = pd.read_csv(output_file_path)

        try:
            new_row_df = pd.DataFrame.from_dict(
                [new_row.model_dump(mode="json")], orient="columns"
            )
        except Exception as err:
            raise err
        out = pd.concat([original_df, new_row_df])
        out.drop_duplicates(inplace=True)
        out.to_csv(output_file_path, index=False)

    def map_flow_to_destination_id(
        self, source_flow: dict, check_reverse=False
    ) -> Optional[str]:
        if self.all_flow_mappings.empty:
            logger.warning("No mappings loaded.")
        results = (
            self.all_flow_mappings["TargetFlowUUID"]
            .loc[self.all_flow_mappings["SourceFlowUUID"] == source_flow["@id"]]
            .values.tolist()
        )
        if results:
            return results[0]

        if check_reverse:
            results = (
                self.all_flow_mappings["SourceFlowUUID"]
                .loc[self.all_flow_mappings["TargetFlowUUID"] == source_flow["@id"]]
                .values.tolist()
            )
            if results:
                return results[0]
        return None

    def map_flow(
        self,
        source_flow: dict,
        target_nomenclature: Union[str, list] = None,
        target_context: Union[str, list] = None,
        check_reverse=True,
        search_indirect_mappings=False,
        source_nomenclatures: List[str] = None,
        source_units: Union[str, list] = None,
    ) -> List[CandidateFlow]:
        if self.all_flow_mappings.empty:
            logger.warning("No mappings loaded.")
        if isinstance(target_nomenclature, str):
            target_nomenclature = [target_nomenclature]

        search_term = source_flow.get("@id") or source_flow.get("id")

        filters = [
            ("TargetListName", target_nomenclature),
            ("TargetFlowContext", target_context),
            ("SourceUnit", source_units),
        ]

        results = _filter_df_mapping_str_list(
            df=self.all_flow_mappings,
            filters=[
                ("SourceFlowUUID", search_term),
            ]
            + filters,
        )

        if not results.empty:
            return list_of_candidate_flow_mappings.validate_python(
                results.to_dict(orient="records")
            )

        if check_reverse:
            results = self.all_flow_mappings[
                (
                    self.all_flow_mappings["MatchCondition"].isin(
                        [
                            MappingChoices.EQUAL_TO.value,
                            MappingChoices.A_PROXY_FOR.value,
                            MappingChoices.A_SUPERSET_OF.value,
                        ]
                    )
                )
                & (self.all_flow_mappings["TargetFlowUUID"] == search_term)
            ].copy()

            results = _filter_df_mapping_str_list(
                df=results,
                filters=filters,
                is_reverse_column=True,
            )

            if not results.empty:
                results = reverse_flowmaps(results)

                return list_of_candidate_flow_mappings.validate_python(
                    results.to_dict(orient="records")
                )

        if (
            search_indirect_mappings and source_nomenclatures and target_nomenclature
        ):  # todo rewrite structure for better indirect mapping
            return self.map_flow_daisy_chain(
                source_flow,
                source_nomenclatures=source_nomenclatures,
                target_nomenclatures=target_nomenclature,
                target_context=target_context,
            )
        return []

    @validate_call
    def map_flow_query(
        self,
        flow_query: FlowQuery,
        check_reverse=True,
        search_indirect_mappings=False,
    ) -> List[CandidateFlow]:

        filters = [
            ("TargetListName", flow_query.TargetListNames),
            ("TargetFlowContext", flow_query.TargetFlowContexts),
            ("SourceUnit", flow_query.SourceUnit),
        ]

        direct_results = _filter_df_mapping_str_list(
            df=self.all_flow_mappings,
            filters=[
                ("SourceFlowUUID", flow_query.SourceFlowUUID),
            ]
            + filters,
        )

        if check_reverse:
            reverse_result = self.all_flow_mappings[
                (
                    self.all_flow_mappings["MatchCondition"].isin(
                        [
                            MappingChoices.EQUAL_TO.value,
                            MappingChoices.A_PROXY_FOR.value,
                            MappingChoices.A_SUPERSET_OF.value,
                        ]
                    )
                )
                & (
                    self.all_flow_mappings["TargetFlowUUID"]
                    == flow_query.SourceFlowUUID
                )
            ].copy()

            reverse_result = _filter_df_mapping_str_list(
                df=reverse_result,
                filters=filters,
                is_reverse_column=True,
            )

            if not reverse_result.empty:
                reverse_result = reverse_flowmaps(reverse_result)
                results = pd.concat([direct_results, reverse_result], axis=0)
            else:
                results = direct_results
        else:
            results = direct_results

        if not results.empty:
            return list_of_candidate_flow_mappings.validate_python(
                results.to_dict(orient="records")
            )

        if (
            search_indirect_mappings
            and flow_query.SourceListNames
            and flow_query.TargetListNames
        ):
            # todo rewrite structure for better indirect mapping
            return self.map_flow_daisy_chain(
                {"@id": flow_query.SourceFlowUUID},
                source_nomenclatures=flow_query.SourceListNames,
                target_nomenclatures=flow_query.TargetListNames,
                target_context=flow_query.SourceFlowContexts,
            )
        return []

    def map_flow_raw(
        self, source_flow: dict, check_reverse=False
    ) -> List[FlowmappingFields]:
        if self.all_flow_mappings.empty:
            logger.warning("No mappings loaded.")

        search_term = source_flow.get("@id") or source_flow.get("id")

        results = self.all_flow_mappings.loc[
            self.all_flow_mappings["SourceFlowUUID"] == search_term
        ]
        if not results.empty:
            return list_of_flow_mappings.validate_python(
                results.to_dict(orient="records")
            )

        if check_reverse:
            results = self.all_flow_mappings.loc[
                self.all_flow_mappings["TargetFlowUUID"] == search_term
            ]
            if not results.empty:
                return list_of_flow_mappings.validate_python(
                    results.to_dict(orient="records")
                )

        return []

    def map_flow_daisy_chain(
        self,
        source_flow: dict,
        source_nomenclatures: List[str] = None,
        target_nomenclatures: List[str] = None,
        target_context: Optional[List[str]] = None,
        check_reverse=True,
    ) -> List[CandidateFlow]:
        if self.all_flow_mappings.empty:
            logger.warning("No mappings loaded.")
        collected_results = []

        if not target_nomenclatures or not source_nomenclatures:
            raise Exception("Need to specify target and source nomenclature")

        if not self.have_indirect_mappings:
            raise Exception("No indirect mappings loaded.")

        if not self.path_exists_between_nomenclature(
            source_nomenclatures, target_nomenclatures
        ):
            raise Exception(
                "No known paths between {} and {}".format(
                    source_nomenclatures, target_nomenclatures
                )
            )

        compatible_flow_mappings = self.get_all_flowmappings(
            source_nomenclatures=source_nomenclatures
        )

        search_term = source_flow.get("@id") or source_flow.get("id")
        results = compatible_flow_mappings.loc[
            compatible_flow_mappings["SourceFlowUUID"] == search_term
        ]

        if not results.empty and target_nomenclatures:
            direct_map_results = results.loc[
                results["TargetListName"].isin(target_nomenclatures)
            ]

            # if not results.empty and target_context: # todo
            #     results = results.loc[results['TargetFlowContext'] == target_context]

            if not direct_map_results.empty:
                collected_results.extend(
                    list_of_candidate_flow_mappings.validate_python(
                        direct_map_results.to_dict(orient="records")
                    )
                )

            found_intermediary_nomenclatures = set(
                results["TargetListName"].values.tolist()
            )
            logger.debug(
                f"Using nomenclatures: {found_intermediary_nomenclatures} as stepping stones from "
                f"{source_nomenclatures} to {target_nomenclatures}"
            )

            stepping_stone_df = self.get_all_flowmappings(
                source_nomenclatures=list(found_intermediary_nomenclatures),
                target_nomenclatures=target_nomenclatures,
            )

            explored_paths = pd.merge(
                results,
                stepping_stone_df,
                left_on="TargetFlowUUID",
                right_on="SourceFlowUUID",
                how="inner",
                suffixes=("_results", "_stepping_stone"),
            )  # todo only use "=" or subset?

            if not explored_paths.empty:
                distant_results = explored_paths.drop(
                    columns=[
                        # 'SourceListName_results',
                        "SourceFlowName_results",
                        "SourceFlowUUID_results",
                        "SourceFlowContext_results",
                        "SourceUnit_results",
                        # 'MatchCondition_results',
                        # 'ConversionFactor_results',
                        "TargetListName_results",
                        "TargetFlowName_results",
                        "TargetFlowUUID_results",
                        "TargetFlowContext_results",
                        "TargetUnit_results",
                        # 'Mapper_results', 'Verifier_results',
                        "LastUpdated_results",
                        "MemoMapper_results",
                        "MemoVerifier_results",
                        "MemoSource_results",
                        "MemoTarget_results",
                        # 'SourceListName_stepping_stone',
                        "SourceFlowName_stepping_stone",
                        "SourceFlowUUID_stepping_stone",
                        "SourceFlowContext_stepping_stone",
                        "SourceUnit_stepping_stone",
                        # 'MatchCondition_stepping_stone',
                        # 'ConversionFactor_stepping_stone',
                        # 'TargetListName_stepping_stone',
                        # 'TargetFlowName_stepping_stone',
                        # 'TargetFlowUUID_stepping_stone',
                        # 'TargetFlowContext_stepping_stone',
                        # 'TargetUnit_stepping_stone',
                        # 'Mapper_stepping_stone',
                        # 'Verifier_stepping_stone',
                        # 'LastUpdated_stepping_stone',
                        # 'MemoMapper_stepping_stone',
                        # 'MemoVerifier_stepping_stone',
                        "MemoSource_stepping_stone",
                        # 'MemoTarget_stepping_stone'
                    ],
                    inplace=False,
                )

                distant_results.drop_duplicates(inplace=True)

                if not distant_results.empty and target_context:
                    distant_results = distant_results.loc[
                        distant_results["TargetFlowContext_stepping_stone"].isin(
                            target_context
                        )
                    ]

                dict_lst = distant_results.to_dict(orient="records")

                for d_result in dict_lst:
                    if any(
                        [
                            d_result[v] != "="
                            for v in [
                                "MatchCondition_results",
                                "MatchCondition_stepping_stone",
                            ]
                        ]
                    ):
                        match_condition = "~"
                    else:
                        match_condition = "="

                    steps = [
                        ResultNode(
                            list_name=d_result["SourceListName_results"],
                            match_condition=d_result["MatchCondition_results"],
                            mapper=d_result["Mapper_results"],
                            verifier=d_result["Verifier_results"],
                        ),
                        ResultNode(
                            list_name=d_result["SourceListName_stepping_stone"],
                            match_condition=d_result["MatchCondition_stepping_stone"],
                            mapper=d_result["Mapper_stepping_stone"],
                            verifier=d_result["Verifier_stepping_stone"],
                        ),
                        ResultNode(list_name=d_result["TargetListName_stepping_stone"]),
                    ]
                    new_candidate = CandidateFlow(
                        MatchCondition=match_condition,
                        ConversionFactor=d_result["ConversionFactor_results"]
                        * d_result["ConversionFactor_stepping_stone"],
                        ListName=d_result["TargetListName_stepping_stone"],
                        FlowName=d_result["TargetFlowName_stepping_stone"],
                        FlowUUID=d_result["TargetFlowUUID_stepping_stone"],
                        FlowContext=d_result["TargetFlowContext_stepping_stone"],
                        Unit=d_result["TargetUnit_stepping_stone"],
                        Mapper=d_result["Mapper_stepping_stone"],
                        Verifier=d_result["Verifier_stepping_stone"],
                        LastUpdated=d_result["LastUpdated_stepping_stone"],
                        MemoMapper=d_result["MemoMapper_stepping_stone"],
                        MemoVerifier=d_result["MemoVerifier_stepping_stone"],
                        Memo=d_result["MemoTarget_stepping_stone"],
                        meta_data=MetaData(stepping_stones=steps),
                    )
                    collected_results.append(new_candidate)
                # collected_results.extend(list_of_candidate_flow_mappings.validate_python(dict_list))

        return collected_results

    def get_all_flowmappings(
        self, source_nomenclatures: List[str], target_nomenclatures: List[str] = None
    ) -> pd.DataFrame:
        df1 = self.all_flow_mappings[
            self.all_flow_mappings["SourceListName"].isin(source_nomenclatures)
        ]
        # add reverse
        results = self.all_flow_mappings[
            (
                self.all_flow_mappings["MatchCondition"].isin(
                    [MappingChoices.EQUAL_TO.value, MappingChoices.A_PROXY_FOR.value]
                )
            )
            & (self.all_flow_mappings["TargetListName"].isin(source_nomenclatures))
        ].copy()

        if not results.empty:
            results = reverse_flowmaps(results)
            df1 = pd.concat([df1, results], axis=0)

        if target_nomenclatures:
            df1 = df1[df1["TargetListName"].isin(target_nomenclatures)]
        return df1

    def make_rosetta_stone_map(self):
        known_links = self.all_flow_mappings[["SourceListName", "TargetListName"]]
        unique_known_links = known_links.drop_duplicates()
        list_of_pair = unique_known_links.to_dict(orient="records")

        self.rosetta_flow_map = {}
        for list_name in (
            self.all_flow_mappings["SourceListName"].drop_duplicates().values.tolist()
        ):
            self.rosetta_flow_map[list_name] = RosettaMap(list_name)
        for list_name in (
            self.all_flow_mappings["TargetListName"].drop_duplicates().values.tolist()
        ):
            self.rosetta_flow_map[list_name] = RosettaMap(list_name)

        for d1 in list_of_pair:
            self.rosetta_flow_map[d1["SourceListName"]].add_edge(
                self.rosetta_flow_map[d1["TargetListName"]]
            )
            self.rosetta_flow_map[d1["TargetListName"]].add_edge(
                self.rosetta_flow_map[d1["SourceListName"]]
            )

    def path_exists_between_nomenclature(
        self, source_nomenclatures: List[str], target_nomenclatures: List[str]
    ) -> bool:
        for source_nomenclature in source_nomenclatures:
            if source_nomenclature not in self.rosetta_flow_map:
                logger.warning(
                    f"Was asked for unknown source nomenclature: {source_nomenclature}"
                )
                continue
            possible_paths = self.rosetta_flow_map[source_nomenclature].traverse(
                destinations=target_nomenclatures
            )
            if any(
                [
                    target_nomenclature in possible_paths
                    for target_nomenclature in target_nomenclatures
                ]
            ):
                return True
        return False

    def contains_indirect_maps(self) -> bool:
        has_indirect_mappings = False
        for nomenclature_name, rosetta_node in self.rosetta_flow_map.items():
            result = rosetta_node.traverse(max_depth=2)
            if len(result) > 1:
                logger.debug(f"Have indirect mappings: {nomenclature_name} > {result}")
                has_indirect_mappings = True
        return has_indirect_mappings


def _pull_out_unit(source_flow):
    if source_flow.get("refUnit"):
        return source_flow.get("refUnit")

    if source_flow.get("flowProperties"):
        return source_flow["flowProperties"][0].get("flowProperty", {}).get("refUnit")
    return "None"


@validate_call
def pick_best_match(
    candidate_mapped_flow: List[CandidateFlow],
    match_conditions: Optional[List[MappingChoices]] = None,
    trusted_verifiers: Optional[List[str]] = None,
    trusted_mappers: Optional[List[str]] = None,
    prefer_inputs_production: Optional[bool] = True,
    prefer_unit: Optional[str] = None,
    context: Optional[dict] = None,
    requirement: Optional[dict] = None,  # todo
    preferred_list_names: Optional[List[str]] = None,
) -> Optional[CandidateFlow]:
    if not candidate_mapped_flow:
        return None

    sorted_candidates = rank_candidates(
        candidate_mapped_flow,
        match_conditions,
        trusted_verifiers,
        trusted_mappers,
        prefer_inputs_production,
        prefer_unit,
        context,
        preferred_list_names,
    )
    if sorted_candidates:
        if requirement:
            filtered_candidates = filter_candidates(sorted_candidates, requirement)
            return filtered_candidates[0] if filtered_candidates else None
        else:
            return sorted_candidates[0]
    else:
        return None


def filter_candidates(
    sorted_candidates: list[CandidateFlow], requirement: Dict[str, Optional[str]]
):
    filtered_candidates = list(
        filter(
            lambda c: all(
                [
                    (
                        hasattr(c, required_field)
                        and (
                            getattr(c, required_field) is required_value
                            or (  # todo specify is substring or superstring
                                isinstance(required_value, str)
                                and isinstance(getattr(c, required_field), str)
                                and required_value in getattr(c, required_field)
                            )
                            or (
                                isinstance(required_value, str)
                                and hasattr(c, required_field)
                                and isinstance(getattr(c, required_field), str)
                                and getattr(c, required_field) in required_value
                            )
                        )
                    )
                    for required_field, required_value in requirement.items()
                ]
            ),
            sorted_candidates,
        )
    )

    return filtered_candidates


default_context_rank = {
    "emission": 0,
    "heavyMetalsToWaterInputsProduction": 1,
    "pesticideToAirInputsProduction": 99,
    "pesticideToAirIndoorInputsProduction": 99,
    "pesticideToAirUrbanCloseToGroundInputsProduction": 99,
    "pesticideToAirOtherHigherAltitudesInputsProduction": 99,
    "pesticideToWaterInputsProduction": 99,
    "pesticideToSaltWaterInputsProduction": 99,
    "pesticideToFreshWaterInputsProduction": 99,
    "pesticideToSoilInputsProduction": 99,
    "pesticideToSoilAgriculturalInputsProduction": 99,
    "pesticideToSoilNonAgriculturalInputsProduction": 99,
    "pesticideToHarvestedCropInputsProduction": 99,
}


def _order_prefer_emission_over_pesticide(item: CandidateFlow):
    return default_context_rank.get(item.FlowContext, 99)


ecoinvent_mapper_tags_rank = {
    "name": 6,
    "CAS": 5,
    "stripped": 4,
    "synonym": 3,
    "syn_strip": 2,
    "overwrite": 1,
}


def _order_inputs_production(item: CandidateFlow):
    return 0 if "InputsProduction" in item.FlowUUID else 99


def _order_least_indirection(item: CandidateFlow) -> int:
    """
    Favors flowmaps from direct mappings or with the least amount of indirection
    """
    return (
        len(item.meta_data.stepping_stones)
        if (
            hasattr(item, "meta_data")
            and item.meta_data is not None
            and item.meta_data.stepping_stones
        )
        else 96
    )


def _prefer_verified(item: CandidateFlow) -> int:
    if not item.MemoVerifier:
        return 98
    if (
        item.Memo
        and item.Memo.startswith("mapped")
        and item.Mapper
        and item.Mapper.lower() == "ecoinvent"
    ):
        ecoinvent_rank = 0
        memo_tags = (
            item.Memo.removeprefix("mapped")
            .removeprefix(": ")
            .removeprefix(", ")
            .split(",")
        )
        for memo_tag in set(memo_tags):
            ecoinvent_rank = ecoinvent_rank - ecoinvent_mapper_tags_rank.get(
                memo_tag, 0
            )

    return {
        "validated": 0,
        "verified": 0,
    }.get(item.MemoVerifier.lower().strip(), 98)


def _prefer_verifier(item: CandidateFlow, ranking: dict) -> int:
    return 98 if not item.Verifier else ranking.get(item.Verifier.lower().strip(), 98)


def _prefer_mapper(item: CandidateFlow, ranking: dict) -> int:
    return 97 if not item.Mapper else ranking.get(item.Mapper.lower().strip(), 97)


def _prefer_list_name(item: CandidateFlow, ranking: dict) -> int:
    return 96 if not item.ListName else ranking.get(item.ListName.lower().strip(), 96)


def _order_preferred_unit(item: CandidateFlow, target_unit: str):
    return (
        0
        if target_unit and target_unit in item.Unit or target_unit == item.Unit
        else 99
    )


def _favor_latest(item: CandidateFlow) -> int:
    return (
        999999999999
        if not item.LastUpdated
        else relativedelta(datetime.datetime.now(), item.LastUpdated).days
    )


def _order_prefer_given_flow_context(item: CandidateFlow, context_rank: dict) -> int:
    return context_rank.get(item.FlowContext, 99)


def _best_matching_conditions(item: CandidateFlow, ranking: dict):
    return ranking.get(item.MatchCondition, 99)


@validate_call
def rank_candidates(
    candidate_mapped_flow: List[CandidateFlow],
    match_conditions: Optional[List[MappingChoices]] = None,
    trusted_verifiers: Optional[List[str]] = None,
    trusted_mappers: Optional[List[str]] = None,
    prefer_inputs_production: Optional[bool] = True,
    prefer_unit: Optional[str] = None,
    context: Optional[dict] = None,
    preferred_list_names: Optional[List[str]] = None,
) -> list[CandidateFlow]:
    if not candidate_mapped_flow:
        return []
    elif len(candidate_mapped_flow) == 1:
        return candidate_mapped_flow

    match_condition_ranking = (
        {
            match_conditions.value: order
            for order, match_conditions in enumerate(match_conditions)
        }
        if match_conditions is not None
        else {
            MappingChoices.EQUAL_TO.value: 0,
            MappingChoices.A_PROXY_FOR.value: 1,
            MappingChoices.A_SUPERSET_OF.value: 2,
            MappingChoices.A_SUBSET_OF.value: 3,
        }
    )

    trusted_verifiers_ranking = (
        {
            verified_name.lower().strip(): order
            for order, verified_name in enumerate(trusted_verifiers)
        }
        if trusted_verifiers is not None
        else {"hestia": 0}
    )

    prefer_list_name_ranking = (
        {
            list_name.lower().strip(): order
            for order, list_name in enumerate(preferred_list_names)
        }
        if preferred_list_names is not None
        else {}
    )

    context_rank = {}
    if context is not None and isinstance(context, dict):
        for ii, k in enumerate(context.get("prefer", [])):
            context_rank[k] = ii

    trusted_mapper_ranking = (
        {mapper_name: order for order, mapper_name in enumerate(trusted_mappers)}
        if trusted_mappers is not None
        else {"hestia": 0}
    )

    sorted_list = sorted(
        candidate_mapped_flow,
        key=lambda x: (
            (
                _order_prefer_given_flow_context(x, context_rank)
                if context_rank
                else _order_prefer_emission_over_pesticide(x)
            ),
            _best_matching_conditions(x, match_condition_ranking),
            _prefer_verified(x),
            _prefer_verifier(x, trusted_verifiers_ranking),
            _prefer_mapper(x, trusted_mapper_ranking),
            (
                _prefer_list_name(x, prefer_list_name_ranking)
                if preferred_list_names
                else 0
            ),
            _favor_latest(x),
            _order_least_indirection(x),
            _order_inputs_production(x) if prefer_inputs_production else 0,
            _order_preferred_unit(x, prefer_unit) if prefer_unit else 0,
        ),
    )

    return sorted_list


def swap_columns(
    results: pd.DataFrame, first_column: str, second_column: str
) -> pd.DataFrame:
    if first_column not in results.columns:
        raise Exception(f"{repr(first_column)} is not in dataframe")
    if second_column not in results.columns:
        raise Exception(f"{repr(first_column)} is not in dataframe")

    results.rename(
        columns={
            first_column: first_column + "_rev",
            second_column: first_column,
        },
        inplace=True,
    )
    results.rename(
        columns={
            first_column + "_rev": second_column,
        },
        inplace=True,
    )
    return results


def reverse_flowmaps(flowmap_df: pd.DataFrame) -> pd.DataFrame:
    for first_column, second_column in _FLOW_REVERSE_COLUMNS.items():
        flowmap_df = swap_columns(flowmap_df, first_column, second_column)

    flowmap_df["ConversionFactor"] = flowmap_df["ConversionFactor"].apply(
        lambda x: 1 / x
    )  # flip ratio

    flowmap_df["MatchCondition"] = flowmap_df["MatchCondition"].apply(
        _flip_is_super_set_is_subset
    )
    # flip subset/superset
    return flowmap_df


def _flip_is_super_set_is_subset(match_condition: MappingChoices) -> str:
    if match_condition in [
        MappingChoices.EQUAL_TO.value,
        MappingChoices.A_PROXY_FOR.value,
    ]:
        return match_condition
    elif match_condition == MappingChoices.A_SUPERSET_OF.value:
        return MappingChoices.A_SUBSET_OF.value
    elif match_condition == MappingChoices.A_SUBSET_OF.value:
        return MappingChoices.A_SUPERSET_OF.value
    else:
        raise Exception("unknown match_condition")
