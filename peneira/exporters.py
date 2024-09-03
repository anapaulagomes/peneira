import aiofiles

import json

from peneira.sources.open_alex import map_to_bibtex_type


def to_json(capsule):
    return json.dumps(capsule)


def to_bibtex(capsule):
    bibtex_dict = map_to_bibtex_type(capsule)

    bibtex_str = f"@{bibtex_dict['type']}{{{bibtex_dict['id']},\n"
    for key, value in bibtex_dict.items():
        if key != "id" and key != "type":
            bibtex_str += f"  {key} = {{{value}}},\n"
    bibtex_str += "}\n\n"

    return bibtex_str


async def write_results_to_file(result_bundle, filename, output_format_func=to_json):
    async with aiofiles.open(filename, "a", encoding="utf-8") as file:
        for result in result_bundle.results:
            capsule = {
                "source": result_bundle.source,
                "url": result_bundle.url,
                "result": result,
                "created_at": str(result_bundle.created_at),
            }

            await file.write(f"{output_format_func(capsule)}\n")
    return result_bundle.results
