from typing import Optional

from sqlmodel import Field, SQLModel


class ExonTranscriptLink(SQLModel, table=True):
    exon_id: Optional[int] = Field(
        default=None, foreign_key="exon.id", primary_key=True
    )
    transcript_id: Optional[int] = Field(
        default=None, foreign_key="transcript.id", primary_key=True
    )
