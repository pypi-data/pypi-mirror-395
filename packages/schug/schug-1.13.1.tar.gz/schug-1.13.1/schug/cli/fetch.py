import logging

import typer

from schug.load.biomart import EnsemblBiomartClient
from schug.load.ensembl import (
    fetch_ensembl_exons,
    fetch_ensembl_genes,
    fetch_ensembl_transcripts,
)
from schug.load.gene_resources import (
    fetch_exac_constraint,
    fetch_genes_to_hpo_to_disease,
    fetch_hgnc,
)
from schug.load.omim import fetch_mim2genes

app = typer.Typer()
LOG = logging.getLogger(__name__)


@app.command()
def ensembl_genes(build: str = typer.Option("37", "-b", "--build")):
    """Fetch genes from ensembl"""
    ensembl_client: EnsemblBiomartClient = fetch_ensembl_genes(
        build=build, chromosomes=["Y"]
    )
    for line in ensembl_client:
        typer.echo(line)


@app.command()
def ensembl_transcripts(build: str = typer.Option("37", "-b", "--build")):
    """Fetch genes from ensembl"""
    ensembl_client: EnsemblBiomartClient = fetch_ensembl_transcripts(
        build=build, chromosomes=["Y"]
    )
    for line in ensembl_client:
        typer.echo(line)


@app.command()
def ensembl_exons(build: str = typer.Option("37", "-b", "--build")):
    """Fetch genes from ensembl"""
    ensembl_client: EnsemblBiomartClient = fetch_ensembl_exons(
        build=build, chromosomes=["Y"]
    )
    for line in ensembl_client:
        typer.echo(line)


@app.command()
def hgnc_genes():
    """Fetch genes from genenames.org"""
    for line in fetch_hgnc():
        typer.echo(line)


@app.command()
def exac_genes():
    """Fetch genes from exac"""
    for line in fetch_exac_constraint():
        typer.echo(line)


@app.command()
def hpo_genes():
    """Fetch genes from exac"""
    for line in fetch_genes_to_hpo_to_disease():
        typer.echo(line)


@app.command()
def mim2genes():
    """Fetch mim2genes file from omim"""

    for line in fetch_mim2genes():
        typer.echo(line)
