# peneira

![PyPI - Version](https://img.shields.io/pypi/v/peneira) [![Tests](https://github.com/anapaulagomes/peneira/actions/workflows/tests.yml/badge.svg)](https://github.com/anapaulagomes/peneira/actions/workflows/tests.yml)

It's time to sift through some articles 🤭

With this CLI you can search for papers for your research
in different sources and export the results.

> DISCLAIMER: This is a work in progress. The code is under active development
> and it's not ready for production use.

## Available sources

- [x] [OpenAlex](https://openalex.org/)
- [x] [Semantic Scholar](https://api.semanticscholar.org/)

...and [many more to come](https://github.com/anapaulagomes/peneira/issues?q=is%3Aissue+is%3Aopen+label%3Asources)!
Feel free to contribute. There is [a world of papers](https://en.wikipedia.org/wiki/List_of_academic_databases_and_search_engines)
out there!

### OpenAlex

Here are some details about this source:

* [Data sources](https://help.openalex.org/how-it-works#our-data-sources)
* [Search syntax](https://docs.openalex.org/how-to-use-the-api/get-lists-of-entities/search-entities#boolean-searches)
* [Filters](https://docs.openalex.org/api-entities/works/search-works)
* [Rate limits and authentication](https://docs.openalex.org/how-to-use-the-api/rate-limits-and-authentication)

This library obeys the rate limits of the OpenAlex API (10 requests per second).

### Semantic Scholar

Here are some details about this source:

* [Data sources](https://www.semanticscholar.org/about/publishers)
* [Search syntax](https://api.semanticscholar.org/api-docs/#tag/Paper-Data/operation/get_graph_paper_bulk_search)
* [Rate limits and authentication](https://www.semanticscholar.org/product/api)

This library obeys the rate limits of the Semantic Scholar API (1 request per second).

## Usage

### CLI

You can interact with the CLI using `peneira`. For example, to search for papers on
_"artificial intelligence" and "syndromic surveillance"_ and save the results to a file, you can run:

```bash
peneira -s open_alex -s semantic_scholar --filename my-papers.json
```

You will be prompted to enter the search query for each source. The lib will search for papers in
OpenAlex and Semantic Scholar and store it in a file named `my-papers.json`.
If no filename is provided, the results will be stored to `results.json`.

You have also the option of export it to a bibtex file:

```bash
peneira -s open_alex -s semantic_scholar --format bibtex --filename my-papers.bib
```
