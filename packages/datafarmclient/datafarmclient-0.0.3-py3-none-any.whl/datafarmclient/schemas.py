import datetime
from typing import Literal, Optional, Union

import pandera.pandas as pa
from pydantic import BaseModel

DateTime = Union[str, datetime.datetime]
EntityType = Literal[
    "enTimeSeries",
    "enTimeSeriesQuality",
    "enTimeSeriesDatasourceDescription",
    "enTimeSeriesType",
    "enTimeSeriesStatus",
    "enLocation",
    "enTimeSeriesUnit",
    "enTimeSeriesMedia",
    "enTimeSeriesParameter",
    "enGlobalVariable",
    "enGlobalVariableCategory",
    "enGlobalVariableType",
]
Fields = Literal[
    "vtDateTime",
    "vtData",
    "vtQualityTxt",
    "vtQualityLevel",
    "vtQualityId",
    "vtDuration",
    "vtConfidence",
    "vtVirtualString",
    "vtObjectSize",
    "vtObjectValue",
    "vtVersionItem",
    "vtXCoordinate",
    "vtYCoordinate",
    "vtZCoordinate",
]
VariableType = Literal["int", "float", "str", "bool", "datetime"]

TPeriodDirection = Literal["pdStraight", "pdInverted", "pdInstantaneous"]


TAggregationMethod = Literal[
    "amAverage",
    "amMinimum",
    "amMaximum",
    "amStdDeviation",
    "amMedian",
    "amSum",
    "amDifference",
    "amNIntegration",
    "amCount",
    "amPercentile",
    "amResample",
]
TAggregationPeriod = Literal[
    "apNone", "apHour", "apDay", "apWeek", "apMonth", "apYear", "apUserDefinedSeconds"
]


class TGapFill(BaseModel):
    Enabled: bool
    Method: Literal["fmInterpolation", "fmRepetition"]
    RepetitionType: Literal["rtStairs", "rtInvertedStairs"]


class TAggregation(BaseModel):
    Direction: TPeriodDirection = "pdStraight"
    Enabled: bool = True
    Method: TAggregationMethod
    MethodConstant: float = 0
    Period: TAggregationPeriod
    PeriodOffset: float = 0
    Resampling: Optional[TGapFill]
    UserDefPeriod: int = 0
    UserDefTimeRef: datetime.datetime = datetime.datetime.now()


class TimeSeriesInsertSchema(pa.DataFrameModel):
    TimeStamp: str = pa.Field()
    QualityLevel: int = pa.Field()
    Confidence: Optional[int] = pa.Field(nullable=True)
    Data: Optional[float] = pa.Field(nullable=True)
    Duration: Optional[int] = pa.Field(nullable=True)
    FilePath: Optional[str] = pa.Field()
