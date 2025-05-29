import httpx
from starlette.status import HTTP_200_OK

from app import app
from app.utils.edge import edgedb_client


async def test_api_meeting_edgedb() -> None:
    # Given ( 테스트에 필요한 데이터를 준비하는 과정
    # meeting 생성에는 특별한 인자가 필요 없기 때문에 생략)

    # When
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            url="/v1/edgedb/meetings",
        )

    # Then
    assert response.status_code == HTTP_200_OK
    url_code = response.json()["url_code"]
    assert await edgedb_client.query_single(f"select exists (select Meeting filter .url_code = '{url_code}');") is True
