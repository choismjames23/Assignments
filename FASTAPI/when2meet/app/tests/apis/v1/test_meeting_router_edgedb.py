import httpx
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

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


async def test_api_get_meeting() -> None:
    # Given
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        create_meeting_response = await client.post(
            url="/v1/edgedb/meetings",
        )
        url_code = create_meeting_response.json()["url_code"]

        # When
        response = await client.get(
            url=f"/v1/edgedb/meetings/{url_code}",
        )

    # Then
    assert response.status_code == HTTP_200_OK
    response_body = response.json()
    assert response_body["url_code"] == url_code


async def test_api_get_meeting_404() -> None:
    # Given
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # When
        response = await client.get(
            url="/v1/edgedb/meetings/invalid_url",
        )

    # Then
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "meeting with url_code: invalid_url not found"
