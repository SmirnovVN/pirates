import pytest


@pytest.mark.anyio
class TestMain:
    """Test class for main endpoints."""

    async def test_root(self, client):
        response = await client.get("/")
        assert response.status_code == 200
        assert response.json() == {'message': 'Hello World'}
