# peneira

[![Tests](https://github.com/anapaulagomes/peneira/actions/workflows/tests.yml/badge.svg)](https://github.com/anapaulagomes/peneira/actions/workflows/tests.yml)

It's time to sift through some articles 🤭

## Sources available

- [ ] [OpenAlex](https://openalex.org/)
- [ ] [PubMed](https://pubmed.ncbi.nlm.nih.gov/)
- [ ] [Semantic Scholar](https://www.semanticscholar.org/)

## Usage

```python
import asyncio
from pn.sources.open_alex import fetch_papers

asyncio.run(fetch_papers("artificial intelligence AND public health"))
```
