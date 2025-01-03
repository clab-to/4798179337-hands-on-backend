from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication


class AccessJWTAuthentication(JWTAuthentication):
    def get_header(self, request: Request):
        token = request.COOKIES.get("access")
        header_type = "Bearer"
        access_token = token
        request.META["HTTP_AUTHORIZATION"] = f"{header_type} {access_token}"
        return super().get_header(request)


class RefreshJWTAuthentication(JWTAuthentication):
    def get_header(self, request: Request):
        refresh = request.COOKIES.get("refresh")
        request.META["HTTP_REFRESH_TOKEN"] = refresh
        return super().get_header(request)
