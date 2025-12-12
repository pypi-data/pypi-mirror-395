import clr
import os
from aacommpy.category import categories
from aacommpy.settings import AACOMM_DLL_PATH

if os.path.isfile(AACOMM_DLL_PATH):
    clr.AddReference(AACOMM_DLL_PATH)
    for category in categories:
        if category["enable"]:
            exec(f"from {category['from']} import {category['name']}")
    __all__ = [category["name"] for category in categories if category["enable"]]
