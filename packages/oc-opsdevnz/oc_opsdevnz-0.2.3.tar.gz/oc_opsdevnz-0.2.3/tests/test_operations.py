import json

import pytest
import respx
from httpx import Response

from oc_opsdevnz import OpenCollectiveClient, upsert_collective, upsert_host, upsert_project


@respx.mock
def test_upsert_host_creates_and_updates():
    long_desc = "Long copy"

    def _edit_account(request):
        payload = json.loads(request.content)
        account = payload["variables"]["account"]
        assert account["longDescription"] == long_desc
        return Response(
            200,
            json={
                "data": {
                    "editAccount": {
                        "id": "org1",
                        "slug": "startmeupnz",
                        "name": "StartMeUp.NZ",
                        "description": "Platform team",
                        "currency": "NZD",
                        "longDescription": long_desc,
                        "tags": ["ops"],
                        "website": "https://startmeup.nz/",
                        "socialLinks": [{"type": "WEBSITE", "url": "https://startmeup.nz/"}],
                    }
                }
            },
        )

    responses = [
        Response(200, json={"data": {"account": None}}),  # lookup
        Response(200, json={"data": {"createOrganization": {"id": "org1", "slug": "startmeupnz", "name": "StartMeUp.NZ", "type": "ORGANIZATION"}}}),
        _edit_account,
    ]
    respx.post().mock(side_effect=responses)

    client = OpenCollectiveClient(token="t")
    result = upsert_host(
        client,
        {
            "name": "StartMeUp.NZ",
            "slug": "startmeupnz",
            "description": "Platform team",
            "long_description": long_desc,
            "website": "https://startmeup.nz",
            "tags": ["ops"],
            "currency": "NZD",
        },
    )

    assert result.created is True
    assert result.updated is True
    assert result.warnings == []
    assert result.account["slug"] == "startmeupnz"
    client.close()


@respx.mock
def test_upsert_host_no_update_when_same():
    respx.post().mock(
        side_effect=[
            Response(
                200,
                json={
                    "data": {
                        "account": {
                            "__typename": "Organization",
                            "id": "org1",
                            "slug": "startmeupnz",
                            "name": "StartMeUp.NZ",
                            "type": "ORGANIZATION",
                            "isHost": True,
                            "description": "Platform team",
                            "longDescription": "Long copy",
                            "currency": "NZD",
                            "tags": ["ops"],
                            "website": "https://startmeup.nz/",
                            "socialLinks": [{"type": "WEBSITE", "url": "https://startmeup.nz/"}],
                            "stats": {"balance": {"currency": "NZD"}},
                        }
                    }
                },
            )
        ]
    )

    client = OpenCollectiveClient(token="t")
    result = upsert_host(
        client,
        {
            "name": "StartMeUp.NZ",
            "slug": "startmeupnz",
            "description": "Platform team",
            "long_description": "Long copy",
            "website": "https://startmeup.nz",
            "tags": ["ops"],
            "currency": "NZD",
        },
    )

    assert result.created is False
    assert result.updated is False
    assert result.warnings == []
    assert result.account["slug"] == "startmeupnz"
    client.close()


@respx.mock
def test_collective_create_and_apply_to_host():
    responses = [
        Response(200, json={"data": {"account": {"id": "host1", "slug": "opsdevnz-host", "name": "OpsDev Host", "type": "ORGANIZATION", "isHost": True}}}),  # host check
        Response(200, json={"data": {"account": None}}),  # collective lookup
        Response(200, json={"data": {"createCollective": {"id": "col1", "slug": "opsdevnz", "name": "OpsDev", "type": "COLLECTIVE"}}}),
        Response(200, json={"data": {"editAccount": {"id": "col1", "slug": "opsdevnz", "name": "OpsDev", "description": "OpsDev collective", "tags": ["ops"], "host": None}}}),
        Response(200, json={"data": {"applyToHost": {"id": "col1", "slug": "opsdevnz", "host": {"slug": "opsdevnz-host", "name": "OpsDev Host"}}}}),
    ]
    respx.post().mock(side_effect=responses)

    client = OpenCollectiveClient(token="t")
    result = upsert_collective(
        client,
        {
            "name": "OpsDev",
            "slug": "opsdevnz",
            "description": "OpsDev collective",
            "tags": ["ops"],
            "host_slug": "opsdevnz-host",
            "apply_to_host": True,
            "host_apply_message": "Please host us for staging.",
        },
    )

    assert result.created is True
    assert result.updated is True
    assert result.applied_to_host is True
    assert result.account.get("host", {}).get("slug") == "opsdevnz-host"
    client.close()


@respx.mock
def test_project_create_and_update():
    responses = [
        Response(200, json={"data": {"account": {"id": "col-parent", "slug": "opsdevnz", "name": "OpsDev", "type": "COLLECTIVE"}}}),  # parent lookup
        Response(200, json={"data": {"account": None}}),  # project lookup
        Response(200, json={"data": {"createProject": {"id": "proj1", "slug": "getjjobs-nz", "name": "GetJJobs", "type": "PROJECT", "parent": {"slug": "opsdevnz"}}}}),
        Response(200, json={"data": {"editAccount": {"id": "proj1", "slug": "getjjobs-nz", "name": "GetJJobs", "description": "Jobs project", "tags": ["jobs"]}}}),
    ]
    respx.post().mock(side_effect=responses)

    client = OpenCollectiveClient(token="t")
    result = upsert_project(
        client,
        {
            "name": "GetJJobs",
            "slug": "getjjobs-nz",
            "parent_slug": "opsdevnz",
            "description": "Jobs project",
            "tags": ["jobs"],
        },
    )

    assert result.created is True
    assert result.updated is True
    assert result.account["slug"] == "getjjobs-nz"
    client.close()


def test_load_items_requires_list(tmp_path: Path):
    from oc_opsdevnz.operations import load_items

    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"slug": "not-a-list"}))

    with pytest.raises(ValueError):
        load_items(bad)
