import logging
from typing import Dict, List

from schug.load.fetch_resource import fetch_resource

LOG = logging.getLogger(__name__)


def fetch_mim2genes() -> List[str]:
    url = "https://omim.org/static/omim/data/mim2gene.txt"
    return fetch_resource(url)


def fetch_mimtitles(api_key: str) -> List[str]:
    url = f"https://data.omim.org/downloads/{api_key}/mimTitles.txt"
    return fetch_resource(url)


def fetch_morbidmap(api_key: str) -> List[str]:
    url = f"https://data.omim.org/downloads/{api_key}/morbidmap.txt"
    return fetch_resource(url)


def fetch_genemap2(api_key: str) -> List[str]:
    url = f"https://data.omim.org/downloads/{api_key}/genemap2.txt"
    return fetch_resource(url)


def fetch_mim_files(api_key: str) -> Dict[str, List[str]]:
    """Fetch the necessary mim files using a api key"""

    LOG.info("Fetching OMIM files from https://omim.org/")
    mim_files = {
        "mim2genes": fetch_mim2genes(),
        "mimtitles": fetch_mimtitles(api_key=api_key),
        "morbidmap": fetch_morbidmap(api_key=api_key),
        "genemap2": fetch_genemap2(api_key=api_key),
    }

    return mim_files
