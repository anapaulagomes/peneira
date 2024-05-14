import asyncio

import asyncclick as click


@click.group()
async def cli():
    pass


@cli.command()
@click.argument("query")
async def cli(query):
    """Fetch articles from different sources using given QUERY."""
    click.echo(f"Hello, {query}!")


def main():
    asyncio.run(cli())


if __name__ == "__main__":
    main()
