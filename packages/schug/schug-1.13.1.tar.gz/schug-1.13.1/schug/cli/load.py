import csv
from typing import List, Optional

import typer
from pydantic import parse_obj_as

from schug.database.genes import create_gene_item
from schug.load.ensembl import (
    fetch_ensembl_exons,
    fetch_ensembl_genes,
    fetch_ensembl_transcripts,
)
from schug.models.exon import EnsemblExon
from schug.models.gene import EnsemblGene
from schug.models.transcript import EnsemblTranscript

app = typer.Typer()


@app.command()
def exons(
    exons_file: typer.FileText = typer.Option(None, "--infile", "-i"),
    build: str = typer.Option("37", "-b", "--build"),
):
    """Load exon data"""
    typer.echo("Loading exons")
    if not exons_file:
        exons_file = fetch_ensembl_exons(build=build, chromosomes=["Y"])
    parsed_exons = parse_obj_as(
        List[EnsemblExon],
        [parsed_line for parsed_line in csv.DictReader(exons_file, delimiter="\t")],
    )
    for i, exon in enumerate(parsed_exons):
        if i > 10:
            break
        typer.echo(exon)


@app.command()
def transcripts(
    transcripts_file: typer.FileText = typer.Option(None, "--infile", "-i")
):
    """Load transcript data"""
    typer.echo("Loading transcripts")
    if not transcripts_file:
        transcripts_file = fetch_ensembl_transcripts(build="37", chromosomes=["Y"])
    parsed_transcripts = parse_obj_as(
        List[EnsemblTranscript],
        [
            parsed_line
            for parsed_line in csv.DictReader(transcripts_file, delimiter="\t")
        ],
    )
    for i, tx in enumerate(parsed_transcripts):
        if i == 5:
            break
        typer.echo(tx)


@app.command()
def genes(
    ensembl_file: typer.FileText = typer.Option(None, "--infile", "-i"),
    build: Optional[str] = typer.Option("37", "--build", "-b"),
    chromosome: Optional[List[str]] = typer.Option(["Y"], "--chromosome", "-c"),
):
    """Load gene data into database"""
    typer.echo("Loading genes")
    if not ensembl_file:
        ensembl_file = fetch_ensembl_genes(build=build, chromosomes=chromosome)

    parsed_genes = parse_obj_as(
        List[EnsemblGene],
        [parsed_line for parsed_line in csv.DictReader(ensembl_file, delimiter="\t")],
    )

    for i, gene in enumerate(parsed_genes):
        if i == 5:
            break
        gene.genome_build = build
        create_gene_item(ensembl_gene=gene)
        typer.echo(gene)


@app.command()
def hgnc(ensembl_file: typer.FileText = typer.Option(None, "--infile", "-i")):
    """Load transcript data"""
    typer.echo("Parsing genes")
    from pprint import pprint

    for i, gene in enumerate(csv.DictReader(ensembl_file, delimiter="\t")):
        if i == 5:
            break
        pprint(gene)
