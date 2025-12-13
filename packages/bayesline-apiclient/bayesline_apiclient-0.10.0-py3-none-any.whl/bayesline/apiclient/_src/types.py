# see https://github.com/pola-rs/polars/issues/13152

import json

import polars as pl


def polars_json_to_dtype(json_dtype_str: str) -> pl.DataType:
    from polars.datatypes import DataTypeClass
    from polars.datatypes.classes import (  # noqa F401
        Array,
        Binary,
        Boolean,
        Categorical,
        Date,
        Datetime,
        Decimal,
        Duration,
        Enum,
        Float32,
        Float64,
        Int8,
        Int16,
        Int32,
        Int64,
        List,
        Null,
        Object,
        String,
        Struct,
        Time,
        UInt8,
        UInt16,
        UInt32,
        UInt64,
        Unknown,
        Utf8,
    )

    dtype = eval(json.loads(json_dtype_str))  # noqa: S307
    if isinstance(dtype, DataTypeClass):
        dtype = dtype()
    return dtype
