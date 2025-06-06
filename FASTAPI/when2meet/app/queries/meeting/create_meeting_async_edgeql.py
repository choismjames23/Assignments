# AUTOGENERATED FROM 'app/queries/meeting/create_meeting.edgeql' WITH:
#     $ edgedb-py


from __future__ import annotations

import asyncio
import dataclasses
import uuid

import edgedb

from app.utils.base62 import Base62
from app.utils.edge import edgedb_client


@dataclasses.dataclass
class CreateMeetingResult:
    id: uuid.UUID
    url_code: str


async def create_meeting(
    executor: edgedb.AsyncIOExecutor,
    *,
    url_code: str,
) -> CreateMeetingResult:
    from typing import cast

    return cast(
        CreateMeetingResult,
        await executor.query_single(
            """\
        with
            url_code := <str>$url_code
        select (
            insert Meeting {
                url_code := url_code,
            }
        ) {url_code}\
        """,
            url_code=url_code,
        ),
    )


if __name__ == "__main__":

    async def main() -> None:
        await create_meeting(edgedb_client, url_code=Base62.encode(uuid.uuid4().int))

    asyncio.run(main())
