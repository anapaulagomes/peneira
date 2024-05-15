import aiofiles

import json


async def write_results_to_file(result_bundle, filename):
    async with aiofiles.open(filename, "a") as file:
        for result in result_bundle.results:
            capsule = {
                "source": result_bundle.source,
                "url": result_bundle.url,
                "result": result,
                "created_at": str(result_bundle.created_at),
            }
            await file.write(f"{json.dumps(capsule)}\n")
    return result_bundle.results
