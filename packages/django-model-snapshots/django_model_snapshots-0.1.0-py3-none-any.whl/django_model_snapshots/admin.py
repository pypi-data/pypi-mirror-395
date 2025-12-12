from typing import Any, List, Optional

from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import path
from django.utils.translation import gettext_lazy as _


class VersionAdminMixin:
    """
    Mixin for ModelAdmin to show history.
    """

    def history_view(
        self,
        request: HttpRequest,
        object_id: str,
        extra_context: Optional[dict[str, Any]] = None,
    ) -> HttpResponse:
        model = self.model
        obj = get_object_or_404(model, pk=object_id)

        history_model = getattr(model, "_history_model", None)

        if not history_model:
            return super().history_view(request, object_id, extra_context)

        history_model = obj._history_model
        pk_name = obj._meta.pk.name
        history = history_model.objects.filter(**{pk_name: obj.pk}).order_by(
            "-history_date"
        )

        context = {
            "title": _("History for %s") % obj,
            "module_name": str(model._meta.verbose_name_plural),
            "object": obj,
            "history": history,
            "opts": model._meta,
        }
        if extra_context:
            context.update(extra_context)

        return render(request, "admin/django_model_snapshots/history.html", context)

    def get_urls(self) -> List[Any]:
        urls = super().get_urls()
        my_urls = [
            path(
                "<path:object_id>/history/",
                self.admin_site.admin_view(self.history_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_history",
            ),
        ]
        return my_urls + urls


class VersionAdmin(VersionAdminMixin, admin.ModelAdmin):
    """
    Admin class that includes version history.
    """

    pass
