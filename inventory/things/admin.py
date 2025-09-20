from typing import Any, Dict, Optional
from urllib.parse import urlparse, parse_qs, urlencode

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render

from things.models import Thing, Location


# Register your models here.
@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    list_display = ("name", "quantity", "units", "location")
    list_filter = ("location",)
    actions = ["move_to_location"]
    search_fields = ("name", "description")

    def response_add(
        self, request: HttpRequest, obj: Thing, post_url_continue: Optional[str] = None
    ) -> HttpRequest:
        response = super().response_add(request, obj, post_url_continue)
        if "_addanother" in request.POST:
            parsed_url = urlparse(response["Location"])
            base_url = f"{parsed_url.netloc}{parsed_url.path}"
            query_params = parse_qs(parsed_url.query)
            query_params["location"] = obj.location_id

            response["Location"] = base_url + "?" + urlencode(query_params)
        return response

    def response_change(self, request: HttpRequest, obj: Any) -> HttpResponse:
        response = super().response_change(request, obj)
        if "_addanother" in request.POST:
            parsed_url = urlparse(response["Location"])
            base_url = f"{parsed_url.netloc}{parsed_url.path}"
            query_params = parse_qs(parsed_url.query)
            query_params["location"] = obj.location_id

            response["Location"] = base_url + "?" + urlencode(query_params)
        return response

    def move_to_location(self, request: HttpRequest, queryset: QuerySet[Thing]):
        if "do_action" in request.POST:
            location_id = request.POST["location_id"]
            try:
                location = Location.objects.get(id=location_id)
            except Location.DoesNotExist:
                self.message_user(request, "Invalid location selected", level="error")
                return

            queryset.update(location=location)
            self.message_user(request, "Things moved successfully")
            return None

        locations = Location.objects.all()
        context = admin.site.each_context(request)
        context["locations"] = locations
        context["queryset"] = queryset
        return render(request, "things/admin/move_to_location.html", context)

    move_to_location.short_description = "Move to location"


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    search_fields = ("name", "description")
