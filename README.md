# peneira

[![Tests](https://github.com/anapaulagomes/peneira/actions/workflows/tests.yml/badge.svg)](https://github.com/anapaulagomes/peneira/actions/workflows/tests.yml)

It's time to sift through some articles 🤭

With this CLI you can search for papers for your research
in different sources and export the results.

> DISCLAIMER: This is a work in progress. The code is under active development
> and it's not ready for production use.

## Sources available

- [x] [OpenAlex](https://openalex.org/)
- [ ] [PubMed](https://pubmed.ncbi.nlm.nih.gov/)
- [ ] [Semantic Scholar](https://www.semanticscholar.org/)

## Usage

You can interact with the CLI using `pn`. For example, to search for papers on
_"artificial intelligence" and "syndromic surveillance"_ and save the results to a file, you can run:

```bash
pn '"artificial intelligence" and "syndromic surveillance"' --filename my-papers.json
```

It will search for papers in OpenAlex and store it in a file named `my-papers.json`.

In case you want to call the OpenAlex source directly, you can use the following code:

```python
import asyncio
from pn.sources.open_alex import fetch_papers

asyncio.run(fetch_papers("artificial intelligence AND public health"))
```
