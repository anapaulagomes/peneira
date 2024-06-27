import asyncio

import asyncclick as click

from peneira.exporters import write_results_to_file, to_json, to_bibtex
from peneira.sources.open_alex import establish_number_of_pages, fetch_papers
from peneira.sources.semantic_scholar import SemanticScholar


async def create_open_alex_tasks(query):
    number_of_pages, total = await establish_number_of_pages(query)
    click.echo(
        f"Fetching articles for OPEN_ALEX... {total} papers "
        f"distributed in {number_of_pages} pages."
    )
    tasks = [fetch_papers(query, page) for page in range(1, number_of_pages + 1)]
    return tasks


async def create_semantic_scholar_tasks(query):
    click.echo("Fetching articles for SEMANTIC_SCHOLAR...")
    semantic_scholar = SemanticScholar(query=query)
    return [semantic_scholar.search()]


sources_func = {
    "open_alex": create_open_alex_tasks,
    "semantic_scholar": create_semantic_scholar_tasks,
}


@click.group()
async def cli():
    pass


@cli.command()
@click.option(
    "--filename",
    "-f",
    default="results.json",
    help="Filename with extension. Example: -f results.bib",
)
@click.option(
    "--sources",
    "-s",
    multiple=True,
    default=["open_alex"],
    help="Articles sources. Options: open_alex, semantic_scholar.",
    show_default=True,
)
@click.option(
    "--output", "-o", default="json", help="Output format. Options: json, bibtex."
)
async def cli(filename, sources, output):
    """Fetch articles from different sources using given QUERY."""
    if output.lower() == "bibtex":
        output_format_func = to_bibtex
    elif output.lower() == "json":
        output_format_func = to_json
    else:
        raise ValueError(f"Unsupported format {output}")

    all_tasks = []
    for source in sources:
        search_string = click.prompt(f"Please enter the search string for {source}")
        try:
            all_tasks.extend(await sources_func[source](search_string))
        except ValueError:
            raise ValueError(f"Unsupported source {source}")

    click.echo("Executing the search...")
    results = await asyncio.gather(*all_tasks)

    for result_bundle in results:
        await write_results_to_file(result_bundle, filename, output_format_func)
    click.echo("Done.")


def main():
    asyncio.run(cli())


if __name__ == "__main__":
    main()
