#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the relevant http response codes that need to be sent by
the server and various scenarios corresponding to them.
These have been compiled based on JSON:API v1.0 specifications.
For further details refer - https://jsonapi.org/format/
HTTP Response codes spec -
https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
"""

# SUCCESS responses
"""
200 OK
Generic success status
"""
OK = 200


"""
201 CREATED
new resource created successfully but not returned in response
"""
CREATED = 201


"""
202 ACCEPTED
If an update request has been accepted for processing, but the processing has
not been completed by the time the server responds.
This can be used for async requests.
"""
ACCEPTED = 202


"""
204 NO CONTENT
* resouce created successfully with client-generated-id and
created resouce not sent in response;
* update is successful and the server doesn’t update any attributes besides
those provided and no response document;
"""
NO_CONTENT = 204


# ERROR responses
"""
400 BAD REQUEST
* server encounters a query parameter that does not follow JSON API naming
conventions, and the server does not know how to process it as a query
parameter from this specification
* request contains 'include' parameter but endpoint does not support it.
* server does not support sorting as specified in the query parameter 'sort'
* server is unable to identify a relationship path or does not support
inclusion of resources from a path
* multiple 4xx errors
"""
BAD_REQUEST = 400


"""
401 UNAUTHORIZED
Missing/invlaid JWT token
"""
UNAUTHORIZED = 401


"""
404 NOT FOUND
* processing a request to fetch a single resource that does not exist.
* processing a request to fetch a relationship link URL that does not exist.
* processing a request to modify a resource that does not exist.
* processing a request that references a related resource that does not exist.
* deletion request fails due to the resource not existing.
"""
NOT_FOUND = 404


"""
403 FORBIDDEN
* unsupported request to create a resource
* unsupported request to create a resource with a client-generated ID
* server MAY reject an attempt to do a full replacement of a
to-many relationship. In such a case, the server MUST reject the entire update,
and return a 403 Forbidden response
* unsupported request to update a resource or relationship.
* if complete replacement is not allowed by the server in PATCH request.
* If the client makes a DELETE request to a URL from a relationship link
the server MUST delete the specified members from the relationship
or return a 403 Forbidden response
"""
FORBIDDEN = 403


"""
409 CONFLICT
* processing a POST request to create a resource with a client-generated ID
that already exists.
* processing a POST request in which the resource object’s type is not among
the type(s) that constitute the collection represented by the endpoint.
* processing a PATCH request to update a resource that would
violate other server-enforced constraints
(such as a uniqueness constraint on a property other than id).
* processing a PATCH request in which the resource object’s type and id
do not match the server’s endpoint.
"""
CONFLICT = 409


"""
413 PAYLOAD TOO LARGE
the request entity is larger than limits defined by server
"""
PAYLOAD_TOO_LARGE = 413


"""
415 UNSUPPORTED MEDIA TYPE
If a request specifies the header Content-Type: application/vnd.api+json with
any media type parameters
"""
UNSUPPORTED_MEDIA_TYPE = 415


"""
405 METHOD NOT ALLOWED
method is known by the origin server but not allowed for the
requested resource
"""
METHOD_NOT_ALLOWED = 405


"""
406 NOT ACCEPTABLE
If a request’s Accept header contains the JSON:API media type and all
instances of that media type are modified with media type parameters.
"""
NOT_ACCEPTABLE = 406

"""
422 UNPROCESSABLE ENTITY
Server understands the content type of the request entity, and the
syntax of the request entity is correct, but it was unable to process
the contained instructions
"""
UNPROCESSABLE_ENTITY = 422

"""
429 TOO MANY REQUESTS
Client has sent too many requests in a given amount of time ("rate limiting").
"""
TOO_MANY_REQUESTS = 429

"""
500 INTERNAL SERVER ERROR
Generic server error
"""
INTERNAL_SERVER_ERROR = 500

"""
501 NOT IMPLEMENTED
Server does not support the functionality required to fulfill the request.
This is the appropriate response when the server does not recognize
the request method and is not capable of supporting it for any resource.
The only request methods that servers are required to support
(and therefore that must not return this code) are GET and HEAD
"""
NOT_IMPLEMENTED = 501


"""
502 Bad Gateway
Server, while acting as a gateway or proxy, received an invalid response
from the upstream server.
Note: A Gateway might refer to different things in networking and a 502 error
is usually not something you can fix, but requires a fix by the web server or
the proxies you are trying to get access through.
"""
BAD_GATEWAY = 502


"""
504 Gateway Timeout
The server, while acting as a gateway or proxy, did not receive a timely
response from an upstream server it needed to access in order to complete
the request.
"""
GATEWAY_TIMEOUT = 504
