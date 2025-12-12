from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel
from pydantic import Field as PydanticField
from sqlmodel import Field, Relationship, SQLModel

from schug.models.link_tables import ExonTranscriptLink

if TYPE_CHECKING:
    from .transcript import Transcript


class ExonBase(SQLModel):
    chromosome: str
    start: int
    end: int
    exon_name: Optional[str]


class Exon(ExonBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    transcripts: List["Transcript"] = Relationship(
        back_populates="exons", link_model=ExonTranscriptLink
    )


class ExonRead(ExonBase):
    id: int


class EnsemblExon(BaseModel):
    """Class to hold exon information from a ensemble exon file"""

    chromosome: str = PydanticField(..., alias="Chromosome/scaffold name")
    gene_id: str = PydanticField(..., alias="Gene stable ID")
    transcript_id: str = PydanticField(..., alias="Transcript stable ID")
    exon_name: str = PydanticField(..., alias="Exon stable ID")
    start: int = PydanticField(..., alias="Exon region start (bp)")
    end: int = PydanticField(..., alias="Exon region end (bp)")
    strand: int = PydanticField(..., alias="Strand")
    rank: int = PydanticField(..., alias="Exon rank in transcript")
