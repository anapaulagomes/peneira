import aiofiles

import json


async def write_results_to_file(results, filename):
    async with aiofiles.open(filename, "w") as file:
        for result in results:
            await file.write(f"{json.dumps(result)}\n")
    return results
