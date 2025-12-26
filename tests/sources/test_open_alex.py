import json
from datetime import datetime

import httpx
import pytest

from peneira.exporters import to_bibtex
from peneira.sources.open_alex import fetch_papers, establish_number_of_pages


@pytest.mark.respx(base_url="https://api.openalex.org")
async def test_no_results_due_to_end_of_pagination(respx_mock):
    payload = {
        "meta": {
            "count": 340,
            "db_response_time_ms": 303,
            "page": 15,
            "per_page": 25,
            "groups_count": None,
        },
        "results": [],
        "group_by": [],
    }
    respx_mock.get("/works").mock(return_value=httpx.Response(200, json=payload))
    query = "artificial intelligence AND public health"

    results_bundle = await fetch_papers(query)

    assert results_bundle.results == []


@pytest.mark.respx(base_url="https://api.openalex.org")
async def test_return_all_results_from_first_page(respx_mock):
    expected_url = (
        "https://api.openalex.org/works?"
        "search=machine%20learning%20AND%20public%20health&page=1&per-page=200"
    )

    payload = json.loads(open("tests/sources/fixtures/open_alex.json").read())
    respx_mock.get("/works").mock(return_value=httpx.Response(200, json=payload))
    query = "machine learning AND public health"

    results_bundle = await fetch_papers(query)

    assert results_bundle.source == "open_alex"
    assert results_bundle.url == expected_url
    assert len(results_bundle.results) == 49
    assert isinstance(results_bundle.created_at, datetime)


@pytest.mark.respx(base_url="https://api.openalex.org")
async def test_add_support_to_pagination(respx_mock):
    payload = json.loads(open("tests/sources/fixtures/open_alex.json").read())
    respx_mock.get("/works").mock(return_value=httpx.Response(200, json=payload))
    query = "machine learning AND public health"

    results_bundle = await fetch_papers(query, page=10)

    assert len(results_bundle.results) == 49


@pytest.mark.parametrize(
    "expected_total,expected_pages",
    [
        (340, 2),
        (49, 1),
        (100, 1),
        (200, 1),
        (400, 2),
        (2500, 13),
    ],
)
@pytest.mark.respx(base_url="https://api.openalex.org")
async def test_establish_number_of_pages(respx_mock, expected_total, expected_pages):
    payload = json.loads(open("tests/sources/fixtures/open_alex.json").read())
    payload["meta"]["count"] = expected_total
    respx_mock.get("/works").mock(return_value=httpx.Response(200, json=payload))
    query = "machine learning AND public health"

    number_of_pages, total = await establish_number_of_pages(query)

    assert number_of_pages == expected_pages
    assert total == expected_total


def test_export_to_bibtex():
    capsule = {
        "source": "open_alex",
        "url": "https://www.semanticscholar.org/paper/be6acf8",
        "result": {
            "id": "https://openalex.org/W3195810945",
            "doi": "https://doi.org/10.15620/cdc:108998",
            "title": "A Revised ICD\u201310\u2013CM Surveillance Case Definition for "
            "Injury-related Emergency Department Visits",
            "display_name": "A Revised ICD\u201310\u2013CM Surveillance Case "
            "Definition for Injury-related Emergency Department Visits",
            "relevance_score": 2.3787243,
            "publication_year": 2021,
            "publication_date": "2021-09-29",
            "ids": {
                "openalex": "https://openalex.org/W3195810945",
                "doi": "https://doi.org/10.15620/cdc:108998",
                "mag": "3195810945",
                "pmid": "https://pubmed.ncbi.nlm.nih.gov/34590997",
            },
            "language": "en",
            # keys omitted for brevity
            "open_access": {
                "is_oa": True,
                "oa_status": "hybrid",
                "oa_url": "https://stacks.cdc.gov/view/cdc/108998/cdc_108998_DS1.pdf",
                "any_repository_has_fulltext": True,
            },
            "authorships": [
                {
                    "author_position": "first",
                    "author": {
                        "id": "https://openalex.org/A5087832024",
                        "display_name": "Holly Hedegaard",
                        "orcid": None,
                    },
                    "institutions": [],
                    "countries": ["USA"],
                    "is_corresponding": False,
                    "raw_author_name": "Holly Hedegaard",
                    "raw_affiliation_strings": [],
                },
                {
                    "author_position": "middle",
                    "author": {
                        "id": "https://openalex.org/A5076539989",
                        "display_name": "Matthew Garnett",
                        "orcid": None,
                    },
                    "institutions": [],
                    "countries": ["CA"],
                    "is_corresponding": False,
                    "raw_author_name": "Matthew Garnett",
                    "raw_affiliation_strings": [],
                },
                {
                    "author_position": "last",
                    "author": {
                        "id": "https://openalex.org/A5088809747",
                        "display_name": "Karen Thomas",
                        "orcid": None,
                    },
                    "institutions": [
                        {
                            "id": "https://openalex.org/I889458895",
                            "display_name": "University of Hong Kong",
                            "ror": "https://ror.org/02zhqgq86",
                            "country_code": "HK",
                            "type": "education",
                            "lineage": ["https://openalex.org/I889458895"],
                        }
                    ],
                    "countries": ["HK"],
                    "is_corresponding": False,
                    "raw_author_name": "Karen Thomas",
                    "raw_affiliation_strings": [],
                },
            ],
            "primary_topic": {
                "id": "https://openalex.org/T14400",
                "display_name": "Accuracy of Clinical Coding in Healthcare Data",
                "score": 0.9739,
                "subfield": {
                    "id": "https://openalex.org/subfields/3605",
                    "display_name": "Health Information Management",
                },
                "field": {
                    "id": "https://openalex.org/fields/36",
                    "display_name": "Health Professions",
                },
                "domain": {
                    "id": "https://openalex.org/domains/4",
                    "display_name": "Health Sciences",
                },
            },
            "topics": [
                {
                    "id": "https://openalex.org/T14400",
                    "display_name": "Accuracy of Clinical Coding in Healthcare Data",
                    "score": 0.9739,
                    "subfield": {
                        "id": "https://openalex.org/subfields/3605",
                        "display_name": "Health Information Management",
                    },
                    "field": {
                        "id": "https://openalex.org/fields/36",
                        "display_name": "Health Professions",
                    },
                    "domain": {
                        "id": "https://openalex.org/domains/4",
                        "display_name": "Health Sciences",
                    },
                }
            ],
            "keywords": [
                {
                    "id": "https://openalex.org/keywords/icd-10",
                    "display_name": "ICD-10",
                    "score": 0.516659,
                },
                {
                    "id": "https://openalex.org/keywords/icd-11",
                    "display_name": "ICD-11",
                    "score": 0.505864,
                },
            ],
            "concepts": [
                {
                    "id": "https://openalex.org/C71924100",
                    "wikidata": "https://www.wikidata.org/wiki/Q11190",
                    "display_name": "Medicine",
                    "level": 0,
                    "score": 0.91230285,
                },
                {
                    "id": "https://openalex.org/C2780724011",
                    "wikidata": "https://www.wikidata.org/wiki/Q1295316",
                    "display_name": "Emergency department",
                    "level": 2,
                    "score": 0.8760699,
                },
                {
                    "id": "https://openalex.org/C194828623",
                    "wikidata": "https://www.wikidata.org/wiki/Q2861470",
                    "display_name": "Emergency medicine",
                    "level": 1,
                    "score": 0.634928,
                },
                {
                    "id": "https://openalex.org/C545542383",
                    "wikidata": "https://www.wikidata.org/wiki/Q2751242",
                    "display_name": "Medical emergency",
                    "level": 1,
                    "score": 0.6346897,
                },
                {
                    "id": "https://openalex.org/C2781116378",
                    "wikidata": "https://www.wikidata.org/wiki/Q45127",
                    "display_name": "ICD-10",
                    "level": 2,
                    "score": 0.5659593,
                },
                {
                    "id": "https://openalex.org/C118552586",
                    "wikidata": "https://www.wikidata.org/wiki/Q7867",
                    "display_name": "Psychiatry",
                    "level": 1,
                    "score": 0.06440458,
                },
            ],
            "mesh": [],
            "locations_count": 1,
            "locations": [
                {
                    "is_oa": True,
                    "landing_page_url": "https://doi.org/10.15620/cdc:108998",
                    "pdf_url": "https://stacks.cdc.gov/view/cdc/108998/cdc_108998_DS1.pdf",
                    "source": None,
                    "license": "public-domain",
                    "license_id": "https://openalex.org/licenses/public-domain",
                    "version": "publishedVersion",
                    "is_accepted": True,
                    "is_published": True,
                }
            ],
            "best_oa_location": {
                "is_oa": True,
                "landing_page_url": "https://doi.org/10.15620/cdc:108998",
                "pdf_url": "https://stacks.cdc.gov/view/cdc/108998/cdc_108998_DS1.pdf",
                "source": None,
                "license": "public-domain",
                "license_id": "https://openalex.org/licenses/public-domain",
                "version": "publishedVersion",
                "is_accepted": True,
                "is_published": True,
            },
            "sustainable_development_goals": [],
            "related_works": [
                "https://openalex.org/W4384345078",
                "https://openalex.org/W4226090801",
                "https://openalex.org/W322167246",
                "https://openalex.org/W2946391707",
                "https://openalex.org/W2625702017",
                "https://openalex.org/W2255678829",
                "https://openalex.org/W2244194037",
                "https://openalex.org/W2141668586",
                "https://openalex.org/W2050305294",
                "https://openalex.org/W1989198041",
            ],
            "ngrams_url": "https://api.openalex.org/works/W3195810945/ngrams",
            "abstract_inverted_index": {},
            "cited_by_api_url": "https://api.openalex.org/works?filter=cites:W3195810945",
            "counts_by_year": [{"year": 2023, "cited_by_count": 1}],
            "updated_date": "2024-05-14T12:09:42.901278",
            "created_date": "2021-08-30",
        },
        "created_at": "2024-05-17 12:12:21.049837",
    }
    expected_bibtex = (
        "@{https://openalex.org/W3195810945,\n"
        "  doi = {https://doi.org/10.15620/cdc:108998},\n"
        "  title = {A Revised ICD–10–CM Surveillance Case Definition for "
        "Injury-related Emergency Department Visits},\n"
        "  year = {2021},\n  date = {2021-09-29},\n"
        "  authors = {Holly Hedegaard and Matthew Garnett and Karen Thomas},\n"
        "  institutions = {University of Hong Kong},\n"
        "  country = {CA, HK, USA},\n"
        "  language = {en},\n"
        "  open_access = {hybrid},\n  abstract = {},\n"
        "  keywords = {Emergency department, Emergency medicine, ICD-10, ICD-11, "
        "Medical emergency, Medicine, Psychiatry},\n"
        "  url = {https://www.semanticscholar.org/paper/be6acf8},\n"
        "  source = {open_alex},\n  created_at = {2024-05-17 12:12:21.049837},\n"
        "}"
        "\n\n"
    )

    assert to_bibtex(capsule) == expected_bibtex
