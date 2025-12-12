from typing import Annotated
from fastapi import APIRouter, Request, Depends, Path, Query, Body
from fastapi.responses import Response
from sqlmodel import Session

from ebuffer.errors import a_exc2msg

from ebservice.application import app_g
from ebservice.models_policy import PolicyRequest, Policy
from ebservice.database import PolicyEntry
from ebservice.routers.routes_auth import check_token

#
# -- Policy Management
#

router = APIRouter(prefix="/policy", tags=["Policies"])
router.rest_metadata = { "name": "Policies" }

@router.post("")
@a_exc2msg
async def createPolicy(
    request: Request,
    policy: Annotated[ PolicyRequest, Body() ],
    blocking: Annotated[bool | None, Query()] = False,
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Policy:
    policy = PolicyEntry(policy)
    return await app_g.policyAPI.create(policy, blocking, user, session)

@router.get("")
@a_exc2msg
async def searchPolicy(
    request: Request,
    limit: Annotated[int | None, Query(title="Maximum number of element returned", ge=1, le=app_g.config.base.search_max_limit)] = app_g.config.base.search_limit,
    skip: Annotated[int | None, Query(title="Number of element skipped", ge=0)] = 0,
    owner: Annotated[str | None, Query(title="The owner", min_length=4, max_length=120, pattern=app_g.regexp_email)] = None,
    tags: Annotated[list[str] | None, Query(title="A tag to match. The option can be added multiple times.")] = [],
    all: Annotated[bool | None, Query(title="Whether it matches all tags or just one tag.")] = False,
    count: Annotated[bool | None, Query(title="Returns the number of elements, and not the list itself. The parameters '*skip*' and '*limit*' are ignored.")] = False,
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> list[Policy] | int:
    result = await app_g.policyAPI.search(session, user, limit, skip, owner, tags, all, count)
    return Response(content=str(result), media_type=r'text/plain') if isinstance(result, int) else result

@router.get("/{uid}")
@a_exc2msg
async def getPolicy(
    request: Request,
    uid: Annotated[str, Path(title="The UID", min_length=36, max_length=36)],
    owner: Annotated[str | None, Query(title="The owner", min_length=4, max_length=120, pattern=app_g.regexp_email)] = None,
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Policy:
    return await app_g.policyAPI.get(uid, owner, user, session)

@router.delete("/{uid}")
@a_exc2msg
async def delPolicy(
    request: Request,
    uid: Annotated[str, Path(title="The UID", min_length=36, max_length=36)],
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Policy:
    return await app_g.policyAPI.delete(uid, user, session)

@router.get("/{uid}/tags")
@a_exc2msg
async def getTagsFromPolicy(
    request: Request,
    uid: Annotated[str, Path(title="The UID", min_length=36, max_length=36)],
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> list[str]:
    return await app_g.policyAPI.getTags(uid, user, session)

@router.post("/{uid}/tags/{tag}")
@a_exc2msg
async def addTagsToPolicy(
    request: Request,
    uid: Annotated[str, Path(title="The UID", min_length=36, max_length=36)],
    tag: Annotated[
        str,
        Path(
            title="A tag, an UTF-8 string with a size between %d and %d." % (app_g.config.base.tag_min_size, app_g.config.base.tag_max_size),
            min_length=app_g.config.base.tag_min_size,
            max_length=app_g.config.base.tag_max_size,
        ),
    ],
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Policy:
    return await app_g.policyAPI.addTag(uid, tag, user, session)
