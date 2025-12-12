from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel
from pydantic import Field as PydanticField
from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel

from schug.models.exon import ExonRead

from .link_tables import ExonTranscriptLink

if TYPE_CHECKING:
    from .exon import Exon
    from .gene import Gene


class TranscriptBase(SQLModel):
    chromosome: str
    start: int
    end: int
    transcript_name: str
    is_primary: bool = False
    is_canonical: bool = False
    refseq_id: Optional[str]

    gene_id: Optional[int] = Field(default=None, foreign_key="gene.id")


class Transcript(TranscriptBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    gene: Optional["Gene"] = Relationship(back_populates="transcripts")
    exons: List["Exon"] = Relationship(
        back_populates="transcripts", link_model=ExonTranscriptLink
    )


class TranscriptRead(TranscriptBase):
    id: int


class TranscriptReadWithExons(TranscriptRead):
    id: int

    exons: List[ExonRead] = []


class EnsemblTranscript(BaseModel):
    chromosome: str = PydanticField(..., alias="Chromosome/scaffold name")
    ensembl_gene_id: str = PydanticField(..., alias="Gene stable ID")
    ensembl_transcript_id: str = PydanticField(..., alias="Transcript stable ID")
    start: int = PydanticField(..., alias="Transcript start (bp)")
    end: int = PydanticField(..., alias="Transcript end (bp)")
    refseq_mrna: str = PydanticField(None, alias="RefSeq mRNA ID")
    refseq_mrna_predicted: str = PydanticField(None, alias="RefSeq mRNA predicted ID")
    refseq_ncrna_predicted: str = PydanticField(None, alias="RefSeq ncRNA ID")
    refseq_id: Optional[str] = PydanticField(None, validate_default=True)

    @field_validator("refseq_id")
    def set_refseq_id(cls, _, values: dict) -> Optional[str]:
        order: List[str] = [
            "refseq_mrna",
            "refseq_mrna_predicted",
            "refseq_ncrna_predicted",
        ]
        for keyword in order:
            if values[keyword]:
                return values[keyword]
        return None
