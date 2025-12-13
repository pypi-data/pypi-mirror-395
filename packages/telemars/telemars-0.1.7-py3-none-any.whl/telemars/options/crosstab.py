from pydantic import Field
from typing_extensions import Annotated

from telemars.options import gops
from telemars.params.options import crosstab as cval


class Option(gops.Option):
    issue_type: Annotated[cval.IssueType, Field(serialization_alias='issueType')]
