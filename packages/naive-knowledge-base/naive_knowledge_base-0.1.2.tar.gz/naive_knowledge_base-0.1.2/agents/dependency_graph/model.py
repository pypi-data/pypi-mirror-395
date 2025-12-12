import pydantic
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from pydantic.networks import AnyUrl

class DependencyGraph(BaseModel):
    """
    A class representing a dependency graph for a software project.
    """

    absolutePath: str = Field(
        ...,
        description="The absolute path to the project directory.",
    )
    fanIn: int = Field(
        ...,
        description="The number of incoming dependencies for the project.",
    )
    fanOut: int = Field(
        ...,
        description="The number of outgoing dependencies for the project.",
    )
    numberOfMethods: int = Field(
        ...,
        description="The number of methods in the project.",
    )
    sourceLinesOfCode: int = Field(
        ...,
        description="The number of source lines of code in the project.",
    )
    louvainModularity: float = Field(
        ...,
        description="The Louvain modularity score of the project.",
    )
    dependencies: List[str] = Field(
        ...,
        description="A list of dependencies for the project.",
    )