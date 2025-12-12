from dataclasses import is_dataclass, asdict
from typing import Any, Union
import json
from zpy.utils.objects import ZObjectModel
from zpy.utils.values import is_built_type


def serialize_object_value(value: Any) -> Union[Union[dict, str], Any]:
    if issubclass(value.__class__, ZObjectModel):
        return value.sdump()

    if is_dataclass(value):
        return asdict(value)

    if is_built_type(value) is False:
        try:
            return value.__dict__
        except:
            return value
    else:
        try:
            if isinstance(value, dict):
                return value
            if isinstance(value, tuple):
                return value
            if isinstance(value, list):
                f = []
                for i in value:
                    s = serialize_object_value(i)
                    f.append(s)
                #a = json.dumps(f)
                return f
            return json.dumps(value)
        except Exception as e:
            return value
