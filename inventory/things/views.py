from typing import Any

from django.contrib import messages
from django.views.generic import FormView
from django.urls import reverse

from things.forms import QueryForm
from smarts.commands import process_command, COMMAND_MAP

# Create your views here.


class QueryView(FormView):
    template_name = "things/query.html"
    form_class = QueryForm
    success_url = "/"

    def form_valid(self, form):
        query = form.cleaned_data["query_string"].split("dora")

        if len(query) > 1:
            messages.info(self.request, f"Your last query was: {query}")
            command, target = process_command(query[1])
            messages.info(self.request, f"{command} on {target}")
        else:
            messages.warning(self.request, "Call me by my name bitch!")

        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("query")

    def get_context_data(self, **kwargs: Any) -> Any:
        return super().get_context_data(**kwargs)
