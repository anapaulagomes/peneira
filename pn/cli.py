import asyncio

import asyncclick as click

from pn.sources.open_alex import establish_number_of_pages, fetch_papers


@click.group()
async def cli():
    pass


@cli.command()
@click.argument("query")
async def cli(query):
    """Fetch articles from different sources using given QUERY."""
    number_of_pages = await establish_number_of_pages(query)
    tasks = [fetch_papers(query, page) for page in range(1, number_of_pages + 1)]
    gathered = await asyncio.gather(*tasks)

    all_results = []
    for results in gathered:
        all_results.extend(results)
    click.echo(f"Done. Pages: {number_of_pages} All results length: {len(all_results)}")


def main():
    asyncio.run(cli())


if __name__ == "__main__":
    main()
