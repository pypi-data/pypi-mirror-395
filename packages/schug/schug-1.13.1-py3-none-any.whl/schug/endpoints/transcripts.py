import urllib.request
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select

from schug.database.session import get_session
from schug.load.biomart import EnsemblBiomartClient
from schug.load.ensembl import CHROMOSOMES, fetch_ensembl_transcripts
from schug.load.fetch_resource import stream_resource
from schug.models import Transcript, TranscriptRead
from schug.models.common import Build
from schug.models.transcript import TranscriptReadWithExons

router = APIRouter()
"""

@router.get("/", response_model=List[TranscriptRead])
def read_transcripts(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    transcripts = session.exec(select(Transcript).offset(offset).limit(limit)).all()
    return transcripts


@router.get("/{db_id}", response_model=TranscriptReadWithExons)
def read_transcript_db_id(
    *,
    db_id: int,
    session: Session = Depends(get_session),
):
    transcript = session.get(Transcript, db_id)
    if not transcript:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transcript not found"
        )
    return transcript
"""


@router.get("/ensembl_transcripts/", response_class=StreamingResponse)
async def ensembl_transcripts(build: Build, max_retries: int = 5):
    """A proxy to the Ensembl Biomart that retrieves transcripts in a specific genome build."""

    async def chromosome_stream():
        for chrom in CHROMOSOMES:
            print(f"Retrieving transcripts from chromosome: {chrom}")
            ensembl_client: EnsemblBiomartClient = fetch_ensembl_transcripts(
                build=build, chromosomes=[chrom]
            )
            url: str = ensembl_client.build_url(xml=ensembl_client.xml)
            encoded_url = urllib.parse.quote(url, safe=":/?=&")
            with urllib.request.urlopen(encoded_url) as response:
                for line in response:
                    yield line

    # Return the StreamingResponse with the asynchronous generator
    return StreamingResponse(chromosome_stream(), media_type="text/tsv")
