import asyncio

import asyncclick as click

from pn.exporters import write_results_to_file
from pn.sources.open_alex import establish_number_of_pages, fetch_papers


@click.group()
async def cli():
    pass


@cli.command()
@click.argument("query")
@click.option(
    "--filename",
    "-f",
    default="results.json",
    help="Filename with extension. Example: -f results.json",
)
async def cli(query, filename):
    """Fetch articles from different sources using given QUERY."""
    number_of_pages, total = await establish_number_of_pages(query)
    click.echo(
        f"Fetching articles for OPEN_ALEX... {total} papers "
        f"distributed in {number_of_pages} pages."
    )
    tasks = [fetch_papers(query, page) for page in range(1, number_of_pages + 1)]
    results = await asyncio.gather(*tasks)

    for result_bundle in results:
        await write_results_to_file(result_bundle, filename)
    click.echo("Done.")


def main():
    asyncio.run(cli())


if __name__ == "__main__":
    main()
