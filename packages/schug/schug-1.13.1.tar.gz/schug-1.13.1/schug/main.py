from fastapi import FastAPI, status

from schug import __version__

from .endpoints import exons, genes, transcripts

app = FastAPI()
NOT_FOUND_MESSAGE = "Not found"

### REST API


@app.get("/")
async def root():
    return {"message": f"Welcome to Schug v.{__version__}!"}


app.include_router(
    genes.router,
    prefix="/genes",
    tags=["genes"],
    responses={status.HTTP_404_NOT_FOUND: {"description": NOT_FOUND_MESSAGE}},
)


app.include_router(
    transcripts.router,
    prefix="/transcripts",
    tags=["transcripts"],
    responses={status.HTTP_404_NOT_FOUND: {"description": NOT_FOUND_MESSAGE}},
)

app.include_router(
    exons.router,
    prefix="/exons",
    tags=["exons"],
    responses={status.HTTP_404_NOT_FOUND: {"description": NOT_FOUND_MESSAGE}},
)
