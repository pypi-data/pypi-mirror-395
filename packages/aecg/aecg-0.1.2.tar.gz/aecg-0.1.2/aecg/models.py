import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Literal, Optional, Tuple
from uuid import UUID

import numpy as np
import pandas as pd
from pydantic import ConfigDict, computed_field, field_validator
from pydantic_xml import BaseXmlModel, attr, element, wrapped

from aecg import utils

NSMAP = {"xsi": "http://www.w3.org/2001/XMLSchema-instance"}


class ValueUnitTime(BaseXmlModel, search_mode="unordered"):
    value: float = attr(name="value")
    unit: Literal["us", "ms", "s"] = attr(name="unit")


class ValueUnitVoltage(BaseXmlModel, search_mode="unordered"):
    value: float = attr(name="value")
    unit: Literal["nV", "uV", "mV", "V"] = attr(name="unit")


class Time(BaseXmlModel, search_mode="unordered"):
    center: Optional[datetime] = wrapped("center", attr(name="value", default=None))
    low: Optional[datetime] = wrapped("low", attr(name="value", default=None))
    high: Optional[datetime] = wrapped("high", attr(name="value", default=None))

    @field_validator("center", "low", "high", mode="before")
    @classmethod
    def parse_datetime(cls, v: str) -> datetime:
        return utils.parse_hl7_timestamps(v)

    def get_date(self) -> datetime:
        return self.low or self.center or self.high


class Code(BaseXmlModel, search_mode="unordered"):
    code: str = attr()
    code_system: str = attr(name="codeSystem")
    code_system_name: Optional[str] = attr(name="codeSystemName", default=None)
    display_name: Optional[str] = attr(name="displayName", default=None)


class SequenceTimeInfo(BaseXmlModel, search_mode="unordered", nsmap=NSMAP):
    code: Code = wrapped("sequence", element(tag="code"))
    xsi_type: str = wrapped("sequence/value", attr(name="type", ns="xsi"))
    head: str = wrapped("sequence/value/head", attr(name="value"))
    increment: ValueUnitTime = wrapped("sequence/value")


class Sequence(BaseXmlModel, search_mode="unordered", nsmap=NSMAP):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    code: Code = wrapped("sequence", element(tag="code"))
    xsi_type: str = wrapped("sequence/value", attr(name="type", ns="xsi"))
    origin: ValueUnitVoltage = wrapped("sequence/value")
    scale: ValueUnitVoltage = wrapped("sequence/value")
    digits: np.ndarray = wrapped("sequence/value", element("digits"))

    @field_validator("digits", mode="before")
    @classmethod
    def parse_digits(cls, v: str) -> np.ndarray:
        return np.array(list(map(float, re.split(r"\s+", v.strip()))))

    @computed_field
    @property
    def physical_digits(self) -> np.ndarray:
        """Transforms digits to physical values in mV"""
        origin = self.origin.value
        scale = self.scale.value

        match self.origin.unit:
            case "nV":
                origin *= 1e-6
            case "uV":
                origin *= 1e-3
            case "mV":
                origin *= 1
            case "V":
                origin *= 1e3

        match self.scale.unit:
            case "nV":
                scale *= 1e-6
            case "uV":
                scale *= 1e-3
            case "mV":
                scale *= 1
            case "V":
                scale *= 1e3

        return self.digits * scale + origin


class SequenceSet(BaseXmlModel, search_mode="unordered"):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    time_info: SequenceTimeInfo = element("component")
    sequences: List[Sequence] = element("component")

    def get_sequences_df(self) -> pd.DataFrame:
        increment = self.time_info.increment.value

        match self.time_info.increment.unit:
            case "us":
                increment *= 1e-3
            case "ms":
                increment *= 1
            case "s":
                increment *= 1e3

        length = len(self.sequences[0].physical_digits)

        relative_ts = np.arange(0, length) * increment

        if self.time_info.code.code == "TIME_ABSOLUTE":
            head_ts = utils.parse_hl7_timestamps(self.time_info.head)
            absolute_ts = np.array(
                list(map(lambda x: head_ts + timedelta(milliseconds=x), relative_ts))
            )
        else:
            absolute_ts = None

        seq_dict = {"RELATIVE_TS": relative_ts, "ABSOLUTE_TS": absolute_ts}

        for seq in self.sequences:
            seq_dict.update({seq.code.code: seq.physical_digits})

        return pd.DataFrame(seq_dict)


class Series(BaseXmlModel, search_mode="unordered"):
    id: UUID = wrapped("id", attr(name="root"))
    code: Code = element(tag="code")
    effective_time: Time = element(tag="effectiveTime")
    sequence_sets: List[SequenceSet] = wrapped("component", element("sequenceSet"))
    derived_sequence_sets: List[SequenceSet] = wrapped(
        "derivation/derivedSeries/component", element("sequenceSet")
    )


class AnnotatedECG(BaseXmlModel, search_mode="unordered"):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: UUID = wrapped("id", attr(name="root"))
    code: Code = element(tag="code")
    text: Optional[str] = element(default=None)
    effective_time: Time = element(tag="effectiveTime")
    confidentiality_code: Optional[Code] = element(
        tag="confidentialityCode", default=None
    )
    reason_code: Optional[Code] = element(tag="reasonCode", default=None)
    series: List[Series] = wrapped("component", element("series"))

    _raw: Any = None
    _root: Any = None

    def summary(self) -> Dict:
        return {
            "id": self.id,
            "date": self.effective_time.get_date(),
            "series_count": len(self.series),
            "annotations_count": len(self.get_annotations()),
        }

    def get_annotations(self) -> List[Tuple]:
        return self._raw.search(
            "annotation", in_keys=True, in_values=False, exact=True, case_sensitive=True
        )
