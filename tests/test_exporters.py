import json
from datetime import datetime
from unittest import mock
from unittest.mock import call

from peneira.exporters import write_results_to_file, to_json
import aiofiles
import time_machine
from zoneinfo import ZoneInfo
from peneira.sources import ResultBundle

# taken from https://github.com/Tinche/aiofiles?tab=readme-ov-file#writing-tests-for-aiofiles
aiofiles.threadpool.wrap.register(mock.MagicMock)(
    lambda *args, **kwargs: aiofiles.threadpool.AsyncBufferedIOBase(*args, **kwargs)
)


@time_machine.travel(datetime(1970, 1, 1, 10, 59, 0, tzinfo=ZoneInfo("UTC")))
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
    call_data_1 = {
        "source": "open_alex",
        "url": "https://www.openalex.org",
        "result": results[0],
        "created_at": "1970-01-01 10:59:00",
    }
    call_data_2 = {
        "source": "open_alex",
        "url": "https://www.openalex.org",
        "result": results[1],
        "created_at": "1970-01-01 10:59:00",
    }
    expected_calls = [
        call(f"{json.dumps(call_data_1)}\n"),
        call(f"{json.dumps(call_data_2)}\n"),
    ]
    filename = "results-from-tests.json"
    result_bundle = ResultBundle(
        url="https://www.openalex.org", source="open_alex", results=results
    )
    read_file_chunks = [
        b"",
    ]
    file_chunks_iter = iter(read_file_chunks)

    mock_file_stream = mock.MagicMock(
        read=lambda *args, **kwargs: next(file_chunks_iter)
    )

    with mock.patch("aiofiles.threadpool.sync_open", return_value=mock_file_stream):
        received_results = await write_results_to_file(result_bundle, filename)

        assert received_results == results
        mock_file_stream.write.assert_has_calls(expected_calls)


def test_to_json():
    capsule = {
        "source": "open_alex",
        "url": "https://openalex.org/W4361280476",
        "result": {
            "id": "https://openalex.org/W4361280476",
            "doi": "https://doi.org/10.3390/ani13071196",
            "title": "Peste Des Petits Ruminants in the Middle East: "
            "Epidemiological Situation and Status of Control and Eradication "
            "Activities after the First Phase of the PPR Global Eradication "
            "Program (2017\u20132021)",
            "updated_date": "2024-05-11T02:05:05.673802",
            "created_date": "2023-03-31",
        },
        "created_at": str(datetime.now()),
    }

    assert json.loads(to_json(capsule)) == capsule
