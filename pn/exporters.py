import aiofiles

import json


def to_json(capsule):
    return json.dumps(capsule)


async def write_results_to_file(result_bundle, filename, format="json"):
    async with aiofiles.open(filename, "a") as file:
        for result in result_bundle.results:
            capsule = {
                "source": result_bundle.source,
                "url": result_bundle.url,
                "result": result,
                "created_at": str(result_bundle.created_at),
            }
            to_write = None
            if format == "json":
                to_write = to_json(capsule)
            await file.write(f"{to_write}\n")
    return result_bundle.results
