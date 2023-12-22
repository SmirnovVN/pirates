import pytest
from fastapi import status


@pytest.mark.anyio
class TestShipPositive:
    """Test class for ship endpoints."""

    async def test_create_ship_ok(self, client):
        res = await client.post("/ships/new?name=SHEEP&x=333.666&y=8")

        assert res.status_code == status.HTTP_201_CREATED
        assert res.json() == {'id': 1, 'name': 'SHEEP', 'x': 333.666, 'y': 8.0}

    async def test_create_and_get_ship_ok(self, client):
        await client.post("/ships/new?name=SHEEP&x=333.666&y=8")
        res = await client.get("/ships/SHEEP")

        assert res.status_code == status.HTTP_200_OK
        assert res.json() == {'id': 1, 'name': 'SHEEP', 'x': 333.666, 'y': 8.0}


@pytest.mark.anyio
class TestShipNegative:
    """Test class for ship endpoints for negative test cases."""

    async def test_read_parent_by_name_not_found(self, client):
        res = await client.get("/ships/target")

        assert res.status_code == status.HTTP_404_NOT_FOUND
        assert res.json() == {'detail': f'Ship not found'}
