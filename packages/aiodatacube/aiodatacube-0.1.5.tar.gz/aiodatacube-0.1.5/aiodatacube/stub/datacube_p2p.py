# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 6.33.1 
# Pydantic Version: 2.12.5 
from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel
from pydantic import Field
import typing


class PingRequest(BaseModel):
    pass

class PingResponse(BaseModel):
    message: str = Field(default="")
    version: str = Field(default="")

class CreateCollectionRequest(BaseModel):
    cf: str = Field(default="")

class CreateCollectionResponse(BaseModel):
    ack: bool = Field(default=False)

class DeleteCollectionRequest(BaseModel):
    cf: str = Field(default="")

class DeleteCollectionResponse(BaseModel):
    ack: bool = Field(default=False)

class MeasureByKey(BaseModel):
    key: str = Field(default="")
    ts: int = Field(default=0)
    value: float = Field(default=0.0)

class SaveRequest(BaseModel):
    cf: str = Field(default="")
    records: typing.List[MeasureByKey] = Field(default_factory=list)
# uint32 count = 3;
    overwrite: bool = Field(default=False)

class SaveResponse(BaseModel):
    ack: bool = Field(default=False)

class MeasureStats(BaseModel):
    count: int = Field(default=0)
    sum: float = Field(default=0.0)
    squared_sum: float = Field(default=0.0)
    min: float = Field(default=0.0)
    max: float = Field(default=0.0)
    count_nulls: int = Field(default=0)
    ts: int = Field(default=0)
    key: str = Field(default="")
    min_ts: int = Field(default=0)
    max_ts: int = Field(default=0)

class QueryRequest(BaseModel):
    keys: typing.List[str] = Field(default_factory=list)
    start_ts: int = Field(default=0)
    end_ts: int = Field(default=0)
    cf: str = Field(default="")
    as_freq: str = Field(default="")

class QueryResponse(BaseModel):
    stats: typing.List[MeasureStats] = Field(default_factory=list)

class DeleteKeyRequest(BaseModel):
    cf: str = Field(default="")
    keys: typing.List[str] = Field(default_factory=list)
    start_ts: int = Field(default=0)
    end_ts: int = Field(default=0)

class DeleteKeyResponse(BaseModel):
    ack: bool = Field(default=False)

class ListCollectionsRequest(BaseModel):
    pass

class ListCollectionsResponse(BaseModel):
    cfs: typing.List[str] = Field(default_factory=list)

class QueryKeysRequest(BaseModel):
    cf: str = Field(default="")
    prefix: str = Field(default="")
    start: str = Field(default="")
    end: str = Field(default="")
    limit: int = Field(default=0)
    reverse: bool = Field(default=False)

class QueryKeysResponse(BaseModel):
    keys: typing.List[str] = Field(default_factory=list)

class NetworkRequest(BaseModel):
    cf: str = Field(default="")
    prefix: str = Field(default="")
    src_ids: typing.List[str] = Field(default_factory=list)
    start_ts: int = Field(default=0)
    end_ts: int = Field(default=0)
    max_depth: int = Field(default=0)
    separator: str = Field(default="")

class NetworkResponseItem(BaseModel):
    src: str = Field(default="")
    dst: str = Field(default="")
    stats: MeasureStats = Field(default_factory=MeasureStats)

class NetworkResponse(BaseModel):
    items: typing.List[NetworkResponseItem] = Field(default_factory=list)
    scan_count: int = Field(default=0)
    scan_rate: int = Field(default=0)

class FindPathsRequest(BaseModel):
    cf: str = Field(default="")
    prefix: str = Field(default="")
    start_ts: int = Field(default=0)
    end_ts: int = Field(default=0)
    separator: str = Field(default="")
    src: str = Field(default="")
    dst: str = Field(default="")
    max_depth: int = Field(default=0)

class Path(BaseModel):
    ids: typing.List[str] = Field(default_factory=list)

class FindPathsResponse(BaseModel):
    paths: typing.List[Path] = Field(default_factory=list)
    scan_count: int = Field(default=0)
    scan_rate: int = Field(default=0)

class BuildAdjacencyListRequest(BaseModel):
    cf: str = Field(default="")
    prefix: str = Field(default="")
    separator: str = Field(default="")

class BuildAdjacencyListResponse(BaseModel):
    ack: bool = Field(default=False)
    scan_count: int = Field(default=0)
    scan_rate: int = Field(default=0)

class FindTrianglesRequest(BaseModel):
    cf: str = Field(default="")
    prefix: str = Field(default="")
    max_depth: int = Field(default=0)
    separator: str = Field(default="")
    src: str = Field(default="")
    start_ts: int = Field(default=0)
    end_ts: int = Field(default=0)

class FindTrianglesResponse(BaseModel):
    triangles: typing.List[Path] = Field(default_factory=list)

class ScanRequest(BaseModel):
    cf: str = Field(default="")
    prefix: str = Field(default="")
    start: str = Field(default="")
    size: int = Field(default=0)

class ScanResponse(BaseModel):
    batch: typing.List[MeasureStats] = Field(default_factory=list)
