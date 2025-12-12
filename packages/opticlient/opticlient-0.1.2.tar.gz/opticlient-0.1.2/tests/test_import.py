from opticlient import OptiClient


def test_import_client():
    client = OptiClient(api_token="dummy", base_url="https://api.test")
    assert client.api_token == "dummy"
    assert client.base_url == "https://api.test"


def test_client_env_defaults(monkeypatch):
    monkeypatch.setenv("OPTICLIENT_API_TOKEN", "envtoken")
    monkeypatch.setenv("OPTICLIENT_BASE_URL", "https://api.from.env")

    client = OptiClient()
    assert client.api_token == "envtoken"
    assert client.base_url == "https://api.from.env"

def test_http_headers(monkeypatch):
    from opticlient.client import OptiClient

    client = OptiClient(api_token="abc123", base_url="https://api.test")
    http = client._http

    # Private method but we test because correct header is critical
    headers = http._auth_headers()
    assert headers == {"X-Api-Key": "abc123", "Accept": "application/json",}
