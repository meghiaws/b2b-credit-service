from typing import Sequence, Type

from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from app.credits.permissions import IsOrganizerUser


class ApiAuthMixin:
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)


class OrganizerAuthMixin:
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated, IsOrganizerUser,)