import collections
import enum


ApiResponse = collections.namedtuple("ApiResponse", ["payload", "status_code"])


class HttpMethods(enum.Enum):
    DELETE = "DELETE"
    GET = "GET"
    POST = "POST"


class RoleEnum(enum.Enum):
    USER_ROLE_UNKNOWN = "USER_ROLE_UNKNOWN"
    USER_ROLE_ADMIN = "USER_ROLE_ADMIN"
    USER_ROLE_DEVELOPER = "USER_ROLE_DEVELOPER"
    USER_ROLE_MAINTAINER = "USER_ROLE_MAINTAINER"
    USER_ROLE_READONLY = "USER_ROLE_READONLY"
