from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from apps.core.product import product_baseline


def home(request: HttpRequest) -> HttpResponse:
    baseline = product_baseline()
    return render(
        request,
        "home.html",
        {
            "owner": baseline["owner"],
            "primary_audiences": baseline["audiences"]["primary"],
            "visitor_goals": baseline["visitor_goals"],
        },
    )
