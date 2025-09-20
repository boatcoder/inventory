from django.urls import path, include

from things.views import QueryView

urlpatterns = [
    path("query/", QueryView.as_view(), name="query"),
]
