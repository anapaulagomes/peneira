# peneira

![PyPI - Version](https://img.shields.io/pypi/v/peneira) [![Tests](https://github.com/anapaulagomes/peneira/actions/workflows/tests.yml/badge.svg)](https://github.com/anapaulagomes/peneira/actions/workflows/tests.yml)

It's time to sift through some articles 🤭

With this CLI you can search for papers for your research
in different sources and export the results.

> DISCLAIMER: This is a work in progress. The code is under active development
> and it's not ready for production use.

## Available sources

- [x] [OpenAlex](https://openalex.org/)

...and [many more to come](https://github.com/anapaulagomes/peneira/issues?q=is%3Aissue+is%3Aopen+label%3Asources)!
Feel free to contribute. There is [a world of papers](https://en.wikipedia.org/wiki/List_of_academic_databases_and_search_engines)
out there!

### OpenAlex

Here are some details about this source:

* [OpenAlex data sources](https://help.openalex.org/how-it-works#our-data-sources)
* [OpenAlex search syntax](https://docs.openalex.org/how-to-use-the-api/get-lists-of-entities/search-entities#boolean-searches)
* [Open Alex filters](https://docs.openalex.org/api-entities/works/search-works)
* [Open Alex rate limits and authentication](https://docs.openalex.org/how-to-use-the-api/rate-limits-and-authentication)

This library obeys the rate limits of the OpenAlex API (10 requests per second).

## Usage

### CLI

You can interact with the CLI using `peneira`. For example, to search for papers on
_"artificial intelligence" and "syndromic surveillance"_ and save the results to a file, you can run:

```bash
peneira '"artificial intelligence" and "syndromic surveillance"' --filename my-papers.json
```

It will search for papers in OpenAlex and store it in a file named `my-papers.json`.
You have also the option of export it to a bibtex file:

```bash
peneira '"artificial intelligence" and "public health"' --format bibtex --filename my-papers.bib
```

### Python module

In case you want to call the OpenAlex source directly, you can use the following code:

```python
import asyncio
from peneira.sources.open_alex import fetch_papers

asyncio.run(fetch_papers("artificial intelligence AND public health"))
```
