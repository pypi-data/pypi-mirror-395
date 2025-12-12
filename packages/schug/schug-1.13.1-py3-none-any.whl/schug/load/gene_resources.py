import logging
from typing import List
from urllib.error import HTTPError

from schug.load.fetch_resource import fetch_resource

LOG = logging.getLogger(__name__)
HPO_URL = (
    "https://ci.monarchinitiative.org/view/hpo/job/hpo.annotations/lastSuccessfulBuild"
    "/artifact/rare-diseases/util/annotation/{}"
)


def fetch_genes_to_hpo_to_disease() -> List[str]:
    """Fetch the latest version of the map from genes to phenotypes
        Returns:
        res(list(str)): A list with the lines formatted this way:
        #Format: entrez-gene-id<tab>entrez-gene-symbol<tab>HPO-Term-Name<tab>\
        HPO-Term-ID<tab>Frequency-Raw<tab>Frequency-HPO<tab>
        Additional Info from G-D source<tab>G-D source<tab>disease-ID for link
        72	ACTG2	HP:0002027	Abdominal pain			-	mim2gene	OMIM:155310
        72	ACTG2	HP:0000368	Low-set, posteriorly rotated ears		HP:0040283		orphadata
        ORPHA:2604
    """
    return fetch_resource(HPO_URL.format("genes_to_phenotype.txt"))


def fetch_hgnc() -> List[str]:
    """Fetch the hgnc genes file from
        sftp://sftp.ebi.ac.uk/pub/databases/genenames/new/tsv/hgnc_complete_set.txt
    Returns:
        hgnc_gene_lines(list(str))
    """
    url = "sftp://sftp.ebi.ac.uk/pub/databases/genenames/new/tsv/hgnc_complete_set.txt"
    LOG.info("Fetching HGNC genes from %s", url)

    return fetch_resource(url)


def fetch_exac_constraint() -> List[str]:
    """Fetch the file with exac constraint scores"""
    file_name = "fordist_cleaned_exac_r03_march16_z_pli_rec_null_data.txt"
    url = (
        "sftp://sftp.broadinstitute.org/pub/ExAC_release/release0.3/functional_gene_constraint/{0}"
    ).format(file_name)

    LOG.info("Fetching ExAC genes")

    try:
        exac_lines = fetch_resource(url)
    except HTTPError:
        LOG.info("Failed to fetch exac constraint scores file from ftp server")
        LOG.info("Try to fetch from google bucket...")
        url = (
            "https://storage.googleapis.com/gnomad-public/legacy/exacv1_downloads/release0.3.1"
            "/manuscript_data/forweb_cleaned_exac_r03_march16_z_data_pLI.txt.gz"
        )
        exac_lines = fetch_resource(url)

    return exac_lines
