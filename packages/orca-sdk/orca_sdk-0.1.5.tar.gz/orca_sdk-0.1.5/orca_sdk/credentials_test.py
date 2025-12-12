from uuid import uuid4

import pytest

from .client import OrcaClient
from .credentials import OrcaCredentials


def test_is_authenticated():
    assert OrcaCredentials.is_authenticated()


def test_is_authenticated_false(unauthenticated_client):
    with unauthenticated_client.use():
        assert not OrcaCredentials.is_authenticated()


def test_is_healthy():
    assert OrcaCredentials.is_healthy()


def test_is_healthy_false(api_key):
    with OrcaClient(api_key=api_key, base_url="http://localhost:1582").use():
        assert not OrcaCredentials.is_healthy()


def test_list_api_keys():
    api_keys = OrcaCredentials.list_api_keys()
    assert len(api_keys) >= 1
    assert "orca_sdk_test" in [api_key.name for api_key in api_keys]


def test_list_api_keys_unauthenticated(unauthenticated_client):
    with unauthenticated_client.use():
        with pytest.raises(ValueError, match="Invalid API key"):
            OrcaCredentials.list_api_keys()


def test_manage_api_key():
    api_key_name = f"orca_sdk_test_{uuid4().hex[:8]}"
    api_key = OrcaCredentials.create_api_key(api_key_name)
    assert api_key is not None
    assert len(api_key) > 0
    assert api_key_name in [aki.name for aki in OrcaCredentials.list_api_keys()]
    OrcaCredentials.revoke_api_key(api_key_name)
    assert api_key_name not in [aki.name for aki in OrcaCredentials.list_api_keys()]


def test_create_api_key_unauthenticated(unauthenticated_client):
    with unauthenticated_client.use():
        with pytest.raises(ValueError, match="Invalid API key"):
            OrcaCredentials.create_api_key(f"orca_sdk_test_{uuid4().hex[:8]}")


def test_create_api_key_unauthorized(predict_only_client):
    with predict_only_client.use():
        with pytest.raises(PermissionError):
            OrcaCredentials.create_api_key(f"orca_sdk_test_{uuid4().hex[:8]}")


def test_revoke_api_key_unauthenticated(unauthenticated_client):
    with unauthenticated_client.use():
        with pytest.raises(ValueError, match="Invalid API key"):
            OrcaCredentials.revoke_api_key(f"orca_sdk_test_{uuid4().hex[:8]}")


def test_revoke_api_key_unauthorized(predict_only_client):
    with predict_only_client.use():
        with pytest.raises(PermissionError):
            OrcaCredentials.revoke_api_key(f"orca_sdk_test_{uuid4().hex[:8]}")


def test_create_api_key_already_exists():
    with pytest.raises(ValueError, match="API key with this name already exists"):
        OrcaCredentials.create_api_key("orca_sdk_test")


def test_set_api_key(api_key):
    client = OrcaClient(api_key=str(uuid4()))
    with client.use():
        assert not OrcaCredentials.is_authenticated()
        client.api_key = api_key
        assert client.api_key == api_key
        assert OrcaCredentials.is_authenticated()


def test_set_base_url(api_key):
    client = OrcaClient(base_url="http://localhost:1582")
    assert client.base_url == "http://localhost:1582"
    client.base_url = "http://localhost:1583"
    assert client.base_url == "http://localhost:1583"


# deprecated methods:


def test_deprecated_set_api_key(api_key):
    with OrcaClient(api_key=str(uuid4())).use():
        assert not OrcaCredentials.is_authenticated()
        OrcaCredentials.set_api_key(api_key)
        assert OrcaCredentials.is_authenticated()


def test_deprecated_set_invalid_api_key(api_key):
    with OrcaClient(api_key=api_key).use():
        assert OrcaCredentials.is_authenticated()
        with pytest.raises(ValueError, match="Invalid API key"):
            OrcaCredentials.set_api_key(str(uuid4()))
        assert not OrcaCredentials.is_authenticated()


def test_deprecated_set_api_url(api_key):
    with OrcaClient(api_key=api_key).use():
        OrcaCredentials.set_api_url("http://api.orcadb.ai")
        assert str(OrcaClient._resolve_client().base_url) == "http://api.orcadb.ai"


def test_deprecated_set_invalid_api_url(api_key):
    with OrcaClient(api_key=api_key).use():
        with pytest.raises(ValueError, match="No API found at http://localhost:1582"):
            OrcaCredentials.set_api_url("http://localhost:1582")
