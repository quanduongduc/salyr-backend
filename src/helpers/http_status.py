class StatusCode:
    HTTP_200_OK = 200
    HTTP_201_CREATED = 201
    HTTP_202_ACCEPTED = 202
    HTTP_400_BAD_REQUEST = 400
    HTTP_401_UNAUTHORIZED = 401
    HTTP_403_FORBIDDEN = 403
    HTTP_404_NOT_FOUND = 404
    HTTP_422_UNPROCESSABLE_ENTITY = 422
    HTTP_500_INTERNAL_SERVER_ERROR = 500
    HTTP_503_SERVICE_UNAVAILABLE = 503

http_status_messages = {
    StatusCode.HTTP_200_OK: "OK",
    StatusCode.HTTP_201_CREATED: "Created",
    StatusCode.HTTP_202_ACCEPTED: "Accepted",
    StatusCode.HTTP_400_BAD_REQUEST: "Bad Request",
    StatusCode.HTTP_401_UNAUTHORIZED: "Unauthorized",
    StatusCode.HTTP_403_FORBIDDEN: "Forbidden",
    StatusCode.HTTP_404_NOT_FOUND: "Not Found",
    StatusCode.HTTP_422_UNPROCESSABLE_ENTITY: "Unprocessable Entity",
    StatusCode.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
    StatusCode.HTTP_503_SERVICE_UNAVAILABLE: "Service Unavailable",
}