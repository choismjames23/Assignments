from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from app.dtos.create_meeting_response import CreateMeetingResponse
from app.dtos.get_meeting_response import GetMeetingResponse
from app.services.meeting_service_edgedb import (
    service_create_meeting_edgedb,
    service_get_meeting_edgedb,
)
from app.services.meeting_services_mysql import service_create_meeting_mysql

edgedb_router = APIRouter(prefix="/v1/edgedb/meetings", tags=["Meeting"], redirect_slashes=False)
mysql_router = APIRouter(prefix="/v1/mysql/meetings", tags=["Meeting"], redirect_slashes=False)
# 원래는 어떤 DB를 쓰는지 URL에 적지 않는다.
# 강의에서는 2가지 경우를 모두 다 보여주고, 구분하기 위해 URL에 DB 종류를 포함했다.


@edgedb_router.post("", description="meeting 을 생성합니다.")
async def api_create_meeting_edgedb() -> CreateMeetingResponse:
    return CreateMeetingResponse(url_code=(await service_create_meeting_edgedb()).url_code)


@mysql_router.post("", description="meeting 을 생성합니다.")
async def api_create_meeting_mysql() -> CreateMeetingResponse:
    return CreateMeetingResponse(url_code=(await service_create_meeting_mysql()).url_code)


@edgedb_router.get(
    "/{meeting_url_code}",
    description="meeting을 조회합니다.",
)
async def api_get_meeting_edgedb(meeting_url_code: str) -> GetMeetingResponse:
    meeting = await service_get_meeting_edgedb(meeting_url_code)
    if meeting is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=f"meeting with url_code: {meeting_url_code} not found"
        )
    return GetMeetingResponse(url_code=meeting_url_code)


@mysql_router.get(
    "/{meeting_url_code}",
    description="meeting을 조회합니다.",
)
async def api_get_meeting_mysql(meeting_url_code: str) -> GetMeetingResponse:
    return GetMeetingResponse(url_code="abc")
