import pytest
import respx
from httpx import Response

from oc_opsdevnz import GraphQLError, HTTPRequestError, OpenCollectiveClient, PROD_URL, STAGING_URL


def test_prod_guard():
    with pytest.raises(ValueError):
        OpenCollectiveClient(api_url=PROD_URL, token="t")

    client = OpenCollectiveClient.for_prod(token="t")
    assert client.api_url == PROD_URL
    client.close()


@respx.mock
def test_http_error_redacts_token():
    respx.post(STAGING_URL).mock(return_value=Response(401, text="bad secret-token here"))

    client = OpenCollectiveClient(token="secret-token")
    with pytest.raises(HTTPRequestError) as excinfo:
        client.graphql("query { viewer { id } }")

    msg = str(excinfo.value)
    assert "secret-token" not in msg
    assert "HTTP 401" in msg
    # Uncomment to inspect the error message manually while debugging:
    # import pdb; pdb.set_trace()
    client.close()


@respx.mock
def test_graphql_error_surfaces_message():
    respx.post(STAGING_URL).mock(return_value=Response(200, json={"errors": [{"message": "No account found with slug"}]}))

    client = OpenCollectiveClient(token="secret-token-123")
    with pytest.raises(GraphQLError) as excinfo:
        client.graphql("query { account(slug:\"x\") { id } }")

    assert "No account found with slug" in str(excinfo.value)
    client.close()
