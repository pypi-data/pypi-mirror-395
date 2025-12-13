from os import getenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.exceptions import RequestValidationError

from ebuffer.errors import Eb_Exception, Eb_HTTP_Error, Eb_HTTP_Validation_Error

from ebservice.application import app_g
from ebservice.config import logger

from ebservice.routers import restAuth, restAdminMicroservice, restClientMicroservice, restRuntime, restPolicy

# https://patorjk.com/software/taag/#p=display&f=Doom&t=Application%20Microservices
icon = r"""
  ___              _ _           _   _              ___  ____                                    _               
 / _ \            | (_)         | | (_)             |  \/  (_)                                  (_)              
/ /_\ \_ __  _ __ | |_  ___ __ _| |_ _  ___  _ __   | .  . |_  ___ _ __ ___  ___  ___ _ ____   ___  ___ ___  ___ 
|  _  | '_ \| '_ \| | |/ __/ _` | __| |/ _ \| '_ \  | |\/| | |/ __| '__/ _ \/ __|/ _ \ '__\ \ / / |/ __/ _ \/ __|
| | | | |_) | |_) | | | (_| (_| | |_| | (_) | | | | | |  | | | (__| | | (_) \__ \  __/ |   \ V /| | (_|  __/\__ \
\_| |_/ .__/| .__/|_|_|\___\__,_|\__|_|\___/|_| |_| \_|  |_/_|\___|_|  \___/|___/\___|_|    \_/ |_|\___\___||___/
      | |   | |                                                                                                  
      |_|   |_|
"""
icon_md = "```text\n%s\n```" % icon

summary = "This API is a proposal for an application (micro) service based on Ephemeral Buffers."

description = """
### Application Microservice API Principles

Application Services principles reuse the generic properties already
described for the Ephemeral Buffers : the Unique Identifier (UID), the
Access Control Metadata, and the Annotation Tags. In complement, they
are characterized by the following key properties :

 * **Application types**: Application types create the link between a micro-service and a runtime able to execute its jobs. It is declared as a mime type name. While declarative only, conventions could be defined to simplify the execution of standardized micro-services codes on normalized runtimes.
 * **Policy properties**: A policy is defined by a scope and a list of rules in the form <subject>:<action>:[<condition>] that is for now implementation dependent.
 * **Runtime properties**: A Runtime is defined by a unique identifier (UUID), a name, an application type, and a policy UUID.
 * **Micro-Service properties**: A Micro-service is defined by a unique identifier (UUID), a signature, a code bootstrap, either an application type or by an explicit runtime UID, and a policy UUID.
 * **Micro-service Signature**: is composed of the list of input and output names passed by values, and the list of input and output names passed by Ephemeral Buffer UUID.
 * **A Job**: is defined  by a unique identifier (UUID), a micro-service UUID, and a set of input/output values or Ephemeral Buffer UUIDs corresponding to the micro-service signature.

All services deployed within a federation is controlled by a Global Identity provider. Operations issued in any of the services require a
prior authentication process providing an appropriate access token. The traceability of all following actions is then guarantied.

In the federation, both Ephemeral Buffers and Application Services form a trust zone, i.e. a zone where the authenticity of all
operations have been verified and recorded. Sensible code and data shall be securely signed whenever possible. The only potentially
resource demanding application is the Ephemeral Buffer Service that has to offer significant storage at a reasonable performance. Both
services shall offer a strong horizontal scalability, and support high availability deployments.

Based on this architecture, an application service developer, is able to *publish* its software elements as micro-services. At this
stage, it only serves as a software publishing mechanism. The scale and granularity of microservices shall be able to vary significantly,
from the simple call of a little context free computation, to the complex coordination of multiple highly compute intensive scientific
applications.

In the federation, Scientist users can already *provision*, simplify, or optimize data transfers between infrastructures only with
the Ephemeral Buffer Services. It is typically useful between the scientific databases distributed worldwide and the HPC center on which
they have computing quotas. But they can also *call* micro-services published in the federation, and create jobs ready to
be scheduled by an HPC center willing to provide resources for this kind of task.

Part of the federation, application maintainers in HPC center are encouraged to provide resources to the community, declare runtimes to
the application services, and pull jobs for their execution. The first and obvious reason for this is that an application developer can also
be an application maintainer. In order to integrate its work in a larger collaboration, improve his algorithms, or promote the usage of
his scientific work (in particular when seeking certification for published papers), he can share the resources allocated for his
project on the HPC center. Another reason could also be to help in the deployment of standardized computations or in the execution of complex
workflow.

"""

tags_metadata = []
tags_metadata.append(restAuth.rest_metadata)
tags_metadata.append(restAdminMicroservice.rest_metadata)
tags_metadata.append(restClientMicroservice.rest_metadata)
tags_metadata.append(restRuntime.rest_metadata)
tags_metadata.append(restPolicy.rest_metadata)

app = FastAPI(
    root_path=app_g.config.base.root_path,
    title="Application Microservice, a streamlined mechanism for cross-facilities service execution.",
    description=icon_md+description,
    summary=summary,
    version="1.0",
    terms_of_service="http://ebservice.aqmo.org/terms/",
    contact={
        "name": "Equipe Logica Université Rennes/IRISA",
        "url": "https://www.irisa.fr/equipes/logica",
        "email": "contact@aqmo.org",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata,
    openapi_url="/docs/openapi.json",
    docs_url="/docs/ui",
    redoc_url="/docs/redoc",
)

@app.exception_handler(Eb_Exception)

async def eb_exception_handler(request: Request, exc: Eb_Exception):
    # logger.debug(r'------- NEW EXCEPTION: %s -------' % (str(exc)))
    return exc.response(request)

@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException):
    return Eb_HTTP_Error(exc, "Page not found.").response(request)

@app.exception_handler(405)
async def custom_405_handler(request: Request, exc: HTTPException):
    return Eb_HTTP_Error(exc, "Method not allowed.").response(request)

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.debug(r'Validation exception, data=%s, exc=%s', request, str(exc))
    return Eb_HTTP_Validation_Error(exc).response(request)

app.exception_handler(RequestValidationError)(validation_exception_handler)
logger.info(icon)

@app.on_event("startup")
def on_startup() -> None:
    app_g.start()

@app.on_event("shutdown")
async def shutdown_event():
    app_g.destroy()

@app.get("/", summary=r'Redirect to default documentation.', response_description="Temporary page redirect.", status_code=302, response_class=Response)
async def home() -> None:
    return RedirectResponse(url="/docs/ui", status_code=302)

app.include_router(restAuth)
app.include_router(restAdminMicroservice)
app.include_router(restClientMicroservice)
app.include_router(restRuntime)
app.include_router(restPolicy)
