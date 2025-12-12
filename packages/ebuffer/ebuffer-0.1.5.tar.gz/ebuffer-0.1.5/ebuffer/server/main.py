from types import MethodType
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.exceptions import RequestValidationError

from ebuffer.application import app_g
from ebuffer.errors import Eb_Exception, Eb_HTTP_Error
from ebuffer.errors import Eb_HTTP_Validation_Error

from ebuffer.config import logger
from ebuffer.routers import restBuffer, restAuth

icon = r"""
 _____      _                                   _  ______ _   _____________ ___________     
|  ___|    | |                                 | | | ___ \ | | |  ___|  ___|  ___| ___ \    
| |__ _ __ | |__   ___ _ __ ___   ___ _ __ __ _| | | |_/ / | | | |_  | |_  | |__ | |_/ /___ 
|  __| '_ \| '_ \ / _ \ '_ ` _ \ / _ \ '__/ _` | | | ___ \ | | |  _| |  _| |  __||    // __|
| |__| |_) | | | |  __/ | | | | |  __/ | | (_| | | | |_/ / |_| | |   | |   | |___| |\ \\__ \
\____/ .__/|_| |_|\___|_| |_| |_|\___|_|  \__,_|_| \____/ \___/\_|   \_|   \____/\_| \_|___/
     | |                                                                                    
     |_|                                                                                    
"""
icon_md = "```text\n%s\n```" % icon

summary = """
This API is a proposal for an efficient implementation of Ephemeral Buffers. Its purpose is to support large scale Data Logistics using a streamlined mechanism for data transfer.
"""

description = """
# Toward a Minimalist Approach to Data Logistics

We proposed an approach to operate Data Logistics around the concept of **Ephemeral Buffers**.

Ephemeral buffers offer a streamlined mechanism for data transfer. This approach enables a task to write data into a buffer of predefined maximum size on a remote system. Tasks on the receiving system are then responsible for transferring the data from the buffer into their local workspace.

The rationale behind this approach is to simplify authentication processes and avoid complex cybersecurity challenges. By limiting direct access to remote storage and decoupling authentication from individual workflows, ephemeral buffers provide a secure yet flexible data logistics solution.

In the remainder of this document, we delve into the functionalities and implementation of ephemeral buffers.

### Ephemeral Buffers (EB) high level concepts

Ephemeral Buffers (EB) are defined by the following key properties:

1. **System-Dependent Maximum Size:** Each buffer has a predefined maximum size determined by the system configuration, which users cannot modify. If the data to be transferred exceeds this size, additional buffers are automatically allocated to accommodate the transfer.
2. **Time-Limited Availability:** Ephemeral Buffers (EB) have a system-defined lifespan. Once this predefined lifetime expires, the buffer is automatically destroyed without prior notification, ensuring efficient resource management and minimizing the risk of stale or unused data persisting in the system.
3. **Finite Availability:** The number of buffers is limited and system-dependent. This ensures efficient resource management and prevents over-allocation.
4. **A Unique Identifiers (UID):** Every buffer is assigned a unique identifier, enabling precise tracking and management across the system.
5. **A set of mandatory Metadata:**
   * an access control set of metadata. This ensures secure and regulated access to the buffers. Possible implementations are:
     - a signed request based on genuine public key database,
     - a token recognized by an Authentication and Authorization Infrastructure (AAI),
     - a POSIX ACL.
   * a size limited list of *Tags* stored as arbitrary key-value couples and writable only at creation time
   * a set of metadata providing information about the persistence and storage rules applied to the buffer and decided by the infrastructure

The next section describes the EB Microservice.

### Ephemeral Buffers Application context

The approach may require two other components:

1. **A VPN Connection Between Infrastructures:** The Virtual Private Network (VPN) provides guarantees regarding the origin of data transfer requests. While critical for ensuring secure inter-infrastructure communication, this aspect is not elaborated upon in this document, as it pertains to national-level deployment policies and strategies.
2. **A Global Buffer Namespace:** This global namespace for basic storage provides the ability to identify and manage workflow data at any scale, and ensures that secured inter-infrastructure communications are feasible not only via VPNs but also by other means like authentication tokens.

### Ephemeral Buffer (EB) Microservice API Principles

Each system supporting Ephemeral Buffers (EB) implements a microservice accessible either locally or externally, typically via a VPN connection. This microservice provides the following functionalities, contingent upon the presentation of a valid token:

1. **Availability:** This method checks the availability of buffers and provides additional information, such as the maximum buffer size and the system-defined buffer lifetime duration.
2. **Write Buffer:** This method allows a user to write data to a buffer. Upon successful creation, the method returns the buffer's Unique Identifier (UID).
3. **Get Buffer Metadata:** For a specified user, this method retrieves metadata for all active buffers, including the UIDs, sizes, and time limits for each buffer.
4. **Destroy Buffer:** This method enables a user to delete a buffer manually before its lifetime expires.
5. **Get Buffer Content:** This method retrieves the content of a buffer identified by its UID.
6. **Notifications:** Notifications can be sent to registered processes on the host system.
7. **Logging and Monitoring:** This method provides access to logs and monitoring tools, allowing users and administrators to track usage, detect anomalies, and ensure system health.

# The Exa-ATow Ephemeral Buffer API

The current implementation proposes a reference implementation of the concept of Ephemeral Buffers.

The API and its implementation rely on the following technical principles:

  * The API is a REST API operating on the data models in Json (schemas provided below).
  * When successful, i.e. the return code is 200 or equivalent, all returned objects are either:
     - one of the data models in Json,
     - or a raw data-stream corresponding to the element requested.
  * When unsuccessful, all results are/must be an object based on the Json 'Message' with a proper error code and description.
  * Buffer data are pure binary (bytes in many programming languages), transferred as 'application/octet-stream', there are nothing like file related metadata. For any metadata, use *tags*.
  * Buffers *tags* **cannot be removed**, but a tag can be added.
  * Buffers content **cannot be modified**:
     - A buffer can be written multiple times, what is written is concatenated to the existing buffer.
     - The behavior of multiple and concurrent write requests is backend dependent (atomicity cannot be guaranteed by default).
     - Unless mentioned explicitly (with the *seek* or *limit*), a buffer read is by default done on the full content of the buffer at the date of fetch.
     - A read can be made using a session name, a size limited UTF-8 string of any content. For that session, subsequent requests return the next content of the buffer, including any '*write*' that could have been done since the last read.
     - A read session has as limited and deployment defined life-time.


The ephemeral buffers have a life cycle visible with a integer state. A strictly negative value always represents a buffer that is invalid at some point, and a positive value a valid buffer going through its natural life.
  * In order, the integer states are the following:
    - error = -2, the error state. The buffer is not usable, something bad happened, a read can be issued without guarantees.
    - deleted = -1, the buffer is deleted but still exists, this state lasts a deployment dependent limited time.
    - disabled = 0, the buffer is unavailable, typically before a proper destruction.
    - initialized = 1, the buffer is created, but not ready.
    - created = 2, the buffer is ready.
    - full = 3, the buffer is fine but full.
  * In detail, the buffer life cycle is the following:
     1. At creation its state is set to '*initialized*'. During this period, of a fixed limited time, a storage allocation is performed. If it fails, the buffer will be set in error state and then destroyed before the requested life span period.
     2. When the storage backend has successfully allocated the reserved data, the state is set to '*created*'. The life time is then the one requested.
     3. The state remains '*created*' up to the point where it might become eventually '*full*' after some writes.
     4. The state becomes '*disabled*' as soon as a delete operation is issued, either by an explicit delete, or because the life time limit is reached. The destruction process is then started in the background, and neither read or write operations are possible.
     5. If anything bad happen, the buffer is set in the '*error*' state, and write operations are not possible anymore, but the buffer might be able to read the data (error and backend dependent).
     6. When the storage backend has successfully destroyed the buffer, and after a deployment dependent grace time, the buffer is removed from the database.

The API is common to all deployments, but error codes and messages may differ depending on the selected backends. Two class of backend exist in the API:
  * Authorization backend.
    - They can be based on either a *Basic Authorization* scheme (regular HTTP login/password) or on a *Bearer Authorization* scheme, or both.
    - If the Basic Authorization scheme is available, it can be used without the login procedure for all the API.
    - The 'login' request shall always return a Bearer token (do not login and use the token as the Basic Authorization scheme)
  * Storage backend.
    - Default and limit values showed in the documentation shall be provided by the backends based on the deployment configuration.
    - Some backends may or may not support concurrent transfers and sessions.

"""

tags_metadata = []
tags_metadata.append(restAuth.rest_metadata)
tags_metadata.append(restBuffer.rest_metadata)

app = FastAPI(
    root_path=app_g.config.base.root_path,
    title="Ephemeral buffers, a streamlined mechanism for cross-facilities data transfer.",
    description=icon_md+description,
    summary=summary,
    version="1.0",
    terms_of_service="https://ebuffer.aqmo.org/terms/",
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
    #logger.debug(r'------- NEW EXCEPTION: %s -------' % (str(exc)))
    return exc.response(request)

@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException):
    # logger.debug(r'------- NEW EXCEPTION: %s -------' % (str(exc)))
    return Eb_HTTP_Error(exc, "Page not found.").response(request)

@app.exception_handler(405)
async def custom_405_handler(request: Request, exc: HTTPException):
    return Eb_HTTP_Error(exc, "Method not allowed.").response(request)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.debug(r'Validation exception, data=%s, body=%s exc=%s', request, exc.body, str(exc))
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
app.include_router(restBuffer)

def fixed_openapi(self):
    if self.openapi_schema: return self.openapi_schema
    self.openapi_schema = self.openapi_base()
    self.openapi_schema[r'paths']["/eph_buffer/{uid}/data"]["put"]["requestBody"] = {
        "required": True,
        "content": {
            "application/octet-stream": {
                "schema": {
                    "type": "string",
                    "format": "binary",
                    "title": "A raw byte stream to append to the ephemeral buffer."
                }
            }
        }
    }
    return self.openapi_schema

app.openapi_base = app.openapi
app.openapi = MethodType(fixed_openapi, app)
