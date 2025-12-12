from typing import Annotated
from fastapi import APIRouter, Request, Depends, Path, Query, Body
from fastapi.responses import Response
from sqlmodel import Session

from ebuffer.errors import a_exc2msg, Eb_HTTP_Validation_Error, Eb_TagSyntaxError
from ebuffer.auth import AuthExceptionList

from ebservice.application import app_g
from ebservice.models_job import JobRequest, Job, JobRunStatusEnum, JobRunStatus
from ebservice.models_mservice import MicroserviceRequest, Microservice
from ebservice.database import MicroserviceEntry, MicroserviceExceptionList, JobEntry
from ebservice.apimservice import Eb_MicroserviceInvalid
from ebservice.routers.routes_auth import check_token

#
# -- Microservices DB Management
#
routerclient = APIRouter(prefix="/app_service", tags=["Microservices Client"])
routerclient.rest_metadata = {
    "name": "Microservices Client",
    "description": "Application *Microservice* for end-users.",
    "externalDocs": {
        "description": "Items external docs",
        "url": "https://ebservice.aqmo.org/",
    }
}

routeradmin = APIRouter(prefix="/app_service", tags=["Microservices Admin"])
routeradmin.rest_metadata = {
    "name": "Microservices Admin",
    "description": "Application *Microservice* administration.",
    "externalDocs": {
        "description": "Items external docs",
        "url": "https://ebservice.aqmo.org/",
    }
}

@routeradmin.post(
    "",
    responses=Eb_HTTP_Validation_Error().model() | AuthExceptionList | MicroserviceExceptionList | Eb_TagSyntaxError().model(),
    summary=r'Create a new Microservice.',
    description=r'Create a new Microservice.',
    response_description=r'The newly created microservice descriptor, including its UUID.',
)
@a_exc2msg
async def createMicroservice(
    request: Request,
    mservice: Annotated[
        MicroserviceRequest,
        Body(
            title="A descriptor of the Microservice.", examples=[MicroserviceRequest(code=r'{}', tags=["APP::CWL"])]
        ),
    ],
    blocking: Annotated[bool | None, Query(title="Set the microservice creation as blocking, ensuring a complete validation of the code.")] = False,
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Microservice:
    return await app_g.mserviceAPI.createAndRegister(mservice, blocking, user, session)

@routerclient.get(
    "",
    responses=Eb_HTTP_Validation_Error().model() | AuthExceptionList | MicroserviceExceptionList | Eb_TagSyntaxError().model() | {200: {"content": {"text/plain": { "example": "42" }}}},
    summary=r'Count or fetch the list of microservice types.',
    description=r'Look for all the microservice matching the filtering criteria. Be aware that unless the count is requested, the number of results is limited and has a default maximum value defined during the deployment. The full list can be retrieved with a loop and using the query parameters "*limit*" and "*skip*". Additional filters can be applied on the owner and the tags (all or them, or any of them).',
    response_description="Returns either the list of microservice' status or the number of elements.",
)
@a_exc2msg
async def searchMicroservice(
    request: Request,
    limit: Annotated[int | None, Query(title="Maximum number of element returned", ge=1, le=app_g.config.base.search_max_limit)] = app_g.config.base.search_limit,
    skip: Annotated[int | None, Query(title="Number of element skipped", ge=0)] = 0,
    owner: Annotated[str | None, Query(title="The owner", min_length=4, max_length=120, pattern=app_g.regexp_email)] = None,
    tags: Annotated[list[str] | None, Query(title="A tag to match. The option can be added multiple times.")] = [],
    all: Annotated[bool | None, Query(title="Whether the microservice matches all tags or just one tag.")] = False,
    count: Annotated[bool | None, Query(title="Returns the number of elements, and not the list itself. The parameters '*skip*' and '*limit*' are ignored.")] = False,
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> list[Microservice] | int:
    result = await app_g.mserviceAPI.search(session, user, limit, skip, owner, tags, all, count)
    return Response(content=str(result), media_type=r'text/plain') if isinstance(result, int) else result

@routerclient.get(
    "/{uid}",
    responses=Eb_HTTP_Validation_Error().model() | AuthExceptionList | MicroserviceExceptionList,
    summary=r'Get an application microservice.',
    description=r'Get the descriptor of an application microservice.',
    response_description="The status of an application microservice.",
)
@a_exc2msg
async def getMicroservice(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the Microservice", min_length=36, max_length=36)],
    owner: Annotated[str | None, Query(title="The owner", min_length=4, max_length=120, pattern=app_g.regexp_email)] = None,
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Microservice:
    return await app_g.mserviceAPI.get(uid, owner, user, session)

@routeradmin.delete(
    "/{uid}",
    responses=Eb_HTTP_Validation_Error().model() | AuthExceptionList | MicroserviceExceptionList | Eb_MicroserviceInvalid().model(),
    summary=r'Delete an application microservice.',
    description=r'Launch the destruction of an application microservice.',
    response_description="The status of the application microservice before destruction.",
)
@a_exc2msg
async def delMicroservice(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the microservice", min_length=36, max_length=36)],
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Microservice:
    return await app_g.mserviceAPI.delete(uid, user, session)

#
# -- Microservice TAGS Management
#

@routerclient.get(
    "/{uid}/tags",
    responses=Eb_HTTP_Validation_Error().model() | AuthExceptionList | MicroserviceExceptionList | {200: {"content": {"application/json": { "example": '["ISOK","DONE"]' }}}},
    summary=r'Get application microservice tags.',
    description=r'Return the list of tags associated to an application microservice.',
    response_description="The list of tokens as a Json list ot UTF-8 strings.",
)
@a_exc2msg
async def getTagsFromAppMS(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the microservice", min_length=36, max_length=36)],
    owner: Annotated[str | None, Query(title="The owner", min_length=4, max_length=120, pattern=app_g.regexp_email)] = None,
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> list[str]:
    return await app_g.mserviceAPI.getTags(uid, owner, user, session)

@routeradmin.post(
    "/{uid}/tags/{tag}",
    responses=Eb_HTTP_Validation_Error().model() | AuthExceptionList | MicroserviceExceptionList | Eb_TagSyntaxError().model(),
    summary=r'Add a tag to an application microservice.',
    description=r'Append a new tag to the list of tags of an application microservice. The tag order is kept and can be duplicated.',
    response_description="The status of the modified application microservice, including the new tag.",
)
@a_exc2msg
async def addTagsToAppMS(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the microservice", min_length=36, max_length=36)],
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
) -> Microservice:
    return await app_g.mserviceAPI.addTag(uid, tag, user, session)

#
# -- Microservice Jobs' Management
#

@routerclient.post("/{uid}/job")
@a_exc2msg
async def createJobToAppMS(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the microservice", min_length=36, max_length=36)],
    job: Annotated[JobRequest, Body()],
    blocking: Annotated[bool | None, Query()] = False,
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Job:
    return await app_g.mserviceAPI.createJob(uid, job, blocking, user, session)

@routerclient.get("/{uid}/job")
@a_exc2msg
async def searchJobsFromAppMS(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the microservice", min_length=36, max_length=36)],
    limit: Annotated[int | None, Query(title="Maximum number of element returned", ge=1, le=app_g.config.base.search_max_limit)] = app_g.config.base.search_limit,
    skip: Annotated[int | None, Query(title="Number of element skipped", ge=0)] = 0,
    owner: Annotated[str | None, Query(title="The owner", min_length=4, max_length=120, pattern=app_g.regexp_email)] = None,
    tags: Annotated[list[str] | None, Query(title="A tag to match. The option can be added multiple times.")] = [],
    all: Annotated[bool | None, Query(title="Whether the microservice matches all tags or just one tag.")] = False,
    count: Annotated[bool | None, Query(title="Returns the number of elements, and not the list itself. The parameters '*skip*' and '*limit*' are ignored.")] = False,
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> list[Job] | int:
    result = await app_g.mserviceAPI.searchJobs(uid, limit, skip, owner, tags, all, count, user, session)
    #print(r'°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°', result)
    return Response(content=str(result), media_type=r'text/plain') if isinstance(result, int) else result

@routerclient.get("/{uid}/job/{jid}")
@a_exc2msg
async def getJobFromAppMS(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the Microservice", min_length=36, max_length=36)],
    jid: Annotated[str, Path(title="The UID of the Job", min_length=36, max_length=36)],
    owner: Annotated[str | None, Query(title="The owner", min_length=4, max_length=120, pattern=app_g.regexp_email)] = None,
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Job:
    return await app_g.mserviceAPI.getJob(uid, jid, owner, user, session)

@routerclient.delete("/{uid}/job/{jid}")
@a_exc2msg
async def delJobFromAppMS(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the microservice", min_length=36, max_length=36)],
    jid: Annotated[str, Path(title="The UID of the Job", min_length=36, max_length=36)],
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Job:
    return await app_g.mserviceAPI.deleteJob(uid, jid, user, session)

#
# -- Microservice Jobs' Tags Management
#

@routerclient.get(
    "/{uid}/job/{jid}/tags",
    responses=Eb_HTTP_Validation_Error().model() | AuthExceptionList | MicroserviceExceptionList | {200: {"content": {"application/json": { "example": '["ISOK","DONE"]' }}}},
    summary=r'Get application microservice tags.',
    description=r'Return the list of tags associated to an application microservice.',
    response_description="The list of tokens as a Json list ot UTF-8 strings.",
)
@a_exc2msg
async def getTagsFromJobInAppMS(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the microservice", min_length=36, max_length=36)],
    jid: Annotated[str, Path(title="The UID of the Job", min_length=36, max_length=36)],
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> list[str]:
    return await app_g.mserviceAPI.getJobTags(uid, jid, user, session)

@routerclient.post(
    "/{uid}/job/{jid}/tags/{tag}",
    responses=Eb_HTTP_Validation_Error().model() | AuthExceptionList | MicroserviceExceptionList | Eb_TagSyntaxError().model(),
    summary=r'Add a tag to an job.',
    description=r'Append a new tag to the list of tags. The tag order is kept and can be duplicated.',
    response_description="The status of the modified job, including the new tag.",
)
@a_exc2msg
async def addTagsToJobInAppMS(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the microservice", min_length=36, max_length=36)],
    jid: Annotated[str, Path(title="The UID of the Job", min_length=36, max_length=36)],
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
) -> Job:
    return await app_g.mserviceAPI.addJobTag(uid, jid, tag, user, session)

#
# -- Runtime Jobs' Execution Management
#

@routerclient.get("/{uid}/job/{jid}/status")
@a_exc2msg
async def getJobStatusToRuntime(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the Microservice", min_length=36, max_length=36)],
    jid: Annotated[str, Path(title="The UID of the Job", min_length=36, max_length=36)],
    owner: Annotated[str | None, Query(title="The owner", min_length=4, max_length=120, pattern=app_g.regexp_email)] = None,
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> JobRunStatus:
    return await app_g.mserviceAPI.getJobStatus(uid, jid, owner, user, session)
