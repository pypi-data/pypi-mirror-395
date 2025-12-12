import http

from fastapi import Response


def health_check() -> Response:
    return Response(status_code=http.HTTPStatus.OK)
