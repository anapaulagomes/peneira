import json
from unittest import mock
from unittest.mock import call

from pn.exporters import write_results_to_file
import aiofiles


# taken from https://github.com/Tinche/aiofiles?tab=readme-ov-file#writing-tests-for-aiofiles
aiofiles.threadpool.wrap.register(mock.MagicMock)(
    lambda *args, **kwargs: aiofiles.threadpool.AsyncBufferedIOBase(*args, **kwargs)
)


async def test_write_results_to_file():
    results = [
        {
            "id": "https://openalex.org/W4361280476",
            "doi": "https://doi.org/10.3390/ani13071196",
            "title": "Peste Des Petits Ruminants in the Middle East: "
            "Epidemiological Situation and Status of Control and Eradication "
            "Activities after the First Phase of the PPR Global Eradication "
            "Program (2017\u20132021)",
            "updated_date": "2024-05-11T02:05:05.673802",
            "created_date": "2023-03-31",
        },
        {
            "id": "https://openalex.org/W4379385710",
            "doi": "https://doi.org/10.14569/ijacsa.2023.0140549",
            "title": "An Investigation of Asthma Experiences in Arabic Communities "
            "Through Twitter Discourse",
            "updated_date": "2024-05-13T06:53:31.534953",
            "created_date": "2023-06-06",
        },
    ]
    filename = "results-from-tests.json"
    expected_calls = [call(f"{json.dumps(result)}\n") for result in results]
    read_file_chunks = [
        b"",
    ]
    file_chunks_iter = iter(read_file_chunks)

    mock_file_stream = mock.MagicMock(
        read=lambda *args, **kwargs: next(file_chunks_iter)
    )

    with mock.patch("aiofiles.threadpool.sync_open", return_value=mock_file_stream):
        received_results = await write_results_to_file(results, filename)

        assert received_results == results
        mock_file_stream.write.assert_has_calls(expected_calls)
