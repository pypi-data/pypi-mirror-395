from enum import Enum
from typing import Literal, Optional

from pydantic import field_validator
from sqlmodel import SQLModel


class Build(str, Enum):
    build_37 = "37"
    build_38 = "38"

    @classmethod
    def _missing_(cls, value) -> Optional[Enum]:
        """Force GRCh37 and GRCh38 values into accepted formats."""
        for member in cls:
            if member in value:
                return member
        return None


class CoordBase(SQLModel):
    chromosome: str
    start: int
    end: int
    resource: str
    resource_id: str
    genome_build: str

    @field_validator("genome_build", mode="before")
    def correct_build(cls, v):
        if v != "37" and v != "38":
            raise ValueError(f"genome build: {v} must be either 37 or 38")
        return v
