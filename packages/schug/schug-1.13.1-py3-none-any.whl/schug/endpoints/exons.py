import urllib.request
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select

from schug.database.session import get_session
from schug.load.ensembl import CHROMOSOMES, fetch_ensembl_exons
from schug.load.fetch_resource import stream_resource
from schug.models import Exon, ExonRead
from schug.models.common import Build

router = APIRouter()

"""
@router.get("/", response_model=List[ExonRead])
def read_exons(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    exons = session.exec(select(Exon).offset(offset).limit(limit)).all()
    return exons
"""


@router.get("/ensembl_exons/", response_class=StreamingResponse)
async def ensembl_exons(build: Build):
    """A proxy to the Ensembl Biomart that retrieves exons in a specific genome build."""

    async def chromosome_stream():
        for chrom in CHROMOSOMES:
            print(f"Retrieving exons from chromosome: {chrom}")
            ensembl_client: EnsemblBiomartClient = fetch_ensembl_exons(
                build=build, chromosomes=[chrom]
            )
            url: str = ensembl_client.build_url(xml=ensembl_client.xml)
            encoded_url = urllib.parse.quote(url, safe=":/?=&")
            with urllib.request.urlopen(encoded_url) as response:
                for line in response:
                    yield line

    # Return the StreamingResponse with the asynchronous generator
    return StreamingResponse(chromosome_stream(), media_type="text/tsv")
