import logging
import time
import urllib
import zlib
from typing import AsyncGenerator, List
from urllib.request import urlopen
from urllib.response import addinfourl

import httpx
import requests

LOG = logging.getLogger(__name__)
TIMEOUT = 20


def get_request(url: str) -> requests.Response:
    """Return a requests response from url"""
    try:
        LOG.info("Requesting %s", url)
        response: requests.Response = requests.get(url, timeout=TIMEOUT)
        if response.status_code != 200:
            response.raise_for_status()
        LOG.info("Encoded to %s", response.encoding)
    except requests.exceptions.HTTPError as err:
        LOG.warning("Something went wrong, perhaps the api key is not valid?")
        raise err
    except requests.exceptions.MissingSchema as err:
        LOG.warning("Something went wrong, perhaps url is invalid?")
        raise err
    except requests.exceptions.Timeout as err:
        LOG.error("socket timed out - URL %s", url)
        raise err

    return response


def fetch_from_ftp(url: str) -> List[str]:
    """Fetch information from a ftp resource"""
    LOG.info("Fetching data from ftp resource %s", url)
    response: addinfourl = urlopen(url, timeout=TIMEOUT)
    if isinstance(response, Exception):
        raise response
    data: str = response.read().decode("utf-8")
    return data.split("\n")


def fetch_resource(url: str) -> List[str]:
    """Fetch a resource and return the resulting lines in a list or a json object"""
    if url.startswith("ftp"):
        return fetch_from_ftp(url)

    response: requests.Response = get_request(url)

    content: str = response.text
    if response.url.endswith(".gz"):
        LOG.info("gzipped!")
        encoded_content = b"".join(
            chunk for chunk in response.iter_content(chunk_size=128)
        )
        content = zlib.decompress(encoded_content, 16 + zlib.MAX_WBITS).decode("utf-8")

    data = content.split("\n")

    return data


async def stream_resource(url: str, max_retries: int) -> AsyncGenerator:
    """Stream a file from an external service with retries for failed chunks."""
    retries = 0
    while retries < max_retries:
        try:
            async with httpx.AsyncClient(timeout=None) as client:
                async with client.stream("GET", url) as r:
                    r.raise_for_status()  # Ensure successful response
                    async for chunk in r.aiter_bytes():
                        yield chunk
            # If successful, break out of the loop
            break
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            print(f"Error occurred: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

        # Increment retry count and delay before retrying
        retries += 1
        if retries < max_retries:
            print(f"Retrying... ({retries}/{max_retries})")
            time.sleep(1)  # Sleep for 1 second before retrying (you can adjust this)
        else:
            print("Max retries reached, failing.")
            raise httpx.HTTPStatusError(
                "Failed after multiple attempts", request=None, response=None
            )
