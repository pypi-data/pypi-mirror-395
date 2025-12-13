from __future__ import annotations

from pathlib import Path
from typing import Sequence

import serde.yaml

from sera.models._schema import Schema
from sera.models.parse.parse_class import parse_class_without_prop
from sera.models.parse.parse_enum import parse_enum
from sera.models.parse.parse_property import parse_property


def parse_schema(name: str, files: Sequence[Path | str]) -> Schema:
    schema = Schema(name=name, classes={}, enums={})

    # parse all classes
    raw_defs = {}
    for file in files:
        for k, v in serde.yaml.deser(file).items():
            if k.startswith("enum:"):
                schema.enums[k[5:]] = parse_enum(schema, k[5:], v)
                continue
            cdef = parse_class_without_prop(schema, k, v)
            assert k not in schema.classes
            schema.classes[k] = cdef
            raw_defs[k] = v

    # now parse properties of the classes
    for clsname, v in raw_defs.items():
        cdef = schema.classes[clsname]
        for propname, prop in (v["props"] or {}).items():
            assert propname not in cdef.properties
            parsed_prop = parse_property(schema, propname, prop)
            parsed_prop.owner = cdef
            cdef.properties[propname] = parsed_prop

    return schema
