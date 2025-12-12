# Schug

Schug :stew: is a service that gather data about genes, transcripts and exons from multiple sources and merge the
information. There is a [REST API][rest-api] with relevant endpoints.

## Test the app using Docker

You can test Schug on your local computer using Docker. Make sure you have [Docker][docker] installed and type the following commands in a terminal window:

```
git clone https://github.com/Clinical-Genomics/schug
cd schug
docker-compose up
```

Then the app endpoints should be listed available at the following address http://localhost:8000/docs

The command to stop the demo is `docker-compose down`.


## Installation (development)

Make sure [poetry][poetry] is installed

```
git clone https://github.com/Clinical-Genomics/schug
cd schug
poetry install
schug serve --reload
```
Go to http://localhost:8000/docs and check out the API.

## Ready-to-use endpoints

Once having set up an instance of Schug, you can use the following endpoints:

 - **/genes/ensembl_genes/**

   Downloads genes from Ensembl in text format. Specify a genome build by using the parameters `37` or `38`.

   Usage: `curl -X 'GET' 'http://0.0.0.0:8000/genes/ensembl_genes/?build=38' > genes_GRCh38.txt`

 - **/transcripts/ensembl_transcripts/**

   Downloads gene transcripts from Ensembl in text format. Specify a genome build by using the parameters `37` or `38`.

   Usage: `curl -X 'GET' 'http://0.0.0.0:8000/transcripts/ensembl_transcripts/?build=38' > transcripts_GRCh38.txt`

 - **/exons/ensembl_exons/**

   Downloads gene exons from Ensembl in text format. Specify a genome build by using the parameters `37` or `38`.

   Usage: `curl -X 'GET' 'http://0.0.0.0:8000/exons/ensembl_exons/?build=38' > exons_GRCh38.txt`

## Issues While Downloading Genes, Transcripts, or Exons

You might encounter errors while downloading genes, transcripts, or exons, such as the following error:

```
httpx.RemoteProtocolError: peer closed connection without sending complete message body (incomplete chunked read)
```

This error often occurs when the external service prematurely closes the connection during data streaming. To address this issue, you can try increasing the `max_tries` parameter in your request, which otherwise defaults to 5. Increasing the number of retries can help handle intermittent network issues or temporary interruptions from the service.

Here’s an example of how to modify the request:

```
curl -X 'GET' 'http://0.0.0.0:8000/exons/ensembl_exons/?build=37&max_retries=10' > exons_GRCh37.txt`
```

## What is left to do?

The basic structure is outlined and implemented, however there are many details left to implement before
this can be used.
Some of the basic endpoints are in place but these need to be extended according to the needs of the
users. Also the gene information needs to be completed, this will be done in a similar fashion as in
[Scout][scout-genes].

[docker]: https://www.docker.com/
[poetry]: https://python-poetry.org/docs/basic-usage/
[rest-api]: https://realpython.com/api-integration-in-python/
[scout-genes]: https://github.com/Clinical-Genomics/scout/blob/121e9577aaf837eadd6b0e231e0fc5f3e187b920/scout/load/setup.py#L41
