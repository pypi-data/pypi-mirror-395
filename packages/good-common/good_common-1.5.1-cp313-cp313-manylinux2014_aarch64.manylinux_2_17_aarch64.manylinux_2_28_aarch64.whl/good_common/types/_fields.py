import datetime
from typing import Annotated

from good_common.utilities import now_utc
from pydantic import Field, AfterValidator, StringConstraints
import re

from ._base import StringDict
from ._uuid import UUID

UUIDField = Annotated[UUID, Field(default_factory=UUID.create_v7)]

StringDictField = Annotated[StringDict, Field(default_factory=dict)]

DateTimeField = Annotated[datetime.datetime, Field(default_factory=now_utc)]


def _validate_zip_code(zip_code: str) -> str:
    zip_code = re.sub(r"[^0-9]", "", zip_code)
    if len(zip_code) == 5:
        return zip_code
    elif len(zip_code) == 9:
        return zip_code[:5] + "-" + zip_code[5:]
    else:
        return zip_code


VALID_ZIP_CODE = Annotated[str, AfterValidator(_validate_zip_code)]

UPPER_CASE_STRING = Annotated[str, StringConstraints(to_upper=True)]
