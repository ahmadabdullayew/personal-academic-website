from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from apps.core.product import product_identity
from apps.core.serializers import PublicIdentitySerializer


@extend_schema(responses=PublicIdentitySerializer)
@api_view(["GET"])
@permission_classes([AllowAny])
def public_identity(_request: Request) -> Response:
    owner_name, _language = product_identity()
    return Response({"owner": owner_name, "api_version": "v1"})
