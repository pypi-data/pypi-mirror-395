from datetime import datetime
import re
from typing import List, Optional


def to_snake(text: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()


_places_holders = [
    {
        "place": "@project_name",
        "builder": lambda x: x[0]["value"]
    },
    {
        "place": "@project_description",
        "builder": lambda x: x[1]["value"]
    },
    {
        "place": "@repository_name",
        "builder": lambda x: f"{x[6]['value'].title()}Repository"
    },
    {
        "place": "@repository_impl",
        "builder": lambda x: f"Awesome{x[6]['value'].title()}Repository"
    },
    {
        "place": "@repository_action",
        "builder": lambda x: f"{to_snake(x[5]['value']).lower()}"
    },
    {
        "place": "@repository_file",
        "builder": lambda x: f"{x[6]['value'].lower()}_repository"
    },
    {
        "place": "@usecase_file",
        "ex": "GetUser",
        "builder": lambda x: f"{to_snake(x[5]['value'])}"
    },
    {
        "place": "@usecase_file_test",
        "ex": "GetUser",
        "builder": lambda x: f"{to_snake(x[5]['value'])}_test"
    },
    {
        "place": "@usecase_class",
        "ex": "GetUser",
        "builder": lambda x: f"{x[5]['value']}"
    },
    {
        "place": "@usecase_var",
        "ex": "GetUser",
        "builder": lambda x: f"{to_snake(x[5]['value'])}_uc"
    },
    {
        "place": "@developer",
        "builder": lambda x: f"{x[2]['value']}"
    },
    {
        "place": "@dev_url",
        "builder": lambda x: f"{x[3]['value']}"
    },
    {
        "place": "@context_name",
        "builder": lambda x: f"{x[4]['value']}"
    },
    {
        "place": "@date",
        "builder": lambda x: datetime.today().strftime('%Y-%m-%d')
    },
    {
        "place": "@base_path",
        "builder": lambda x: str(x[9]).replace("\\", "\\\\")
    },
]


def place_holders(raw: str, data: Optional[List]) -> str:
    if data is None:
        return raw
    for p in _places_holders:
        try:
            raw = raw.replace(p["place"], p["builder"](data))
        except:
            ...
    return raw
