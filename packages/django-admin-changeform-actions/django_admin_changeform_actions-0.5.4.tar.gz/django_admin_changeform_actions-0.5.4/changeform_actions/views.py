from django.apps import apps
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods


@staff_member_required
@require_http_methods(("POST",))
def run_action_for_model_instance(request):
    """Run specified custom admin action on a model instance.

    This acts as a custom handler for our custom admin actions
    dropdown on a ModelAdmin's changeform page. The idea is to have the
    same outcome as selecting the model instance on the changelist page
    and executing the action there, just more conveniently from its
    changeform aka detail page.

    After running the action we redirect back to where we came from.

    For the corresponding ModelAdmin code, see:

        admin.ChangeFormActionsMixin

    POST Args:

        app_label: str = The app label of the model.

        model_name: str = The model name.

        pk: int = The primary key of the model instance.

        action: str = The action name to run.

    Returns:

        HttpResponseRedirect = Redirect back to the changeform page.

    """
    referer_url: str = request.META["HTTP_REFERER"]

    app_label: str = request.POST["app_label"]
    model_name: str = request.POST["model_name"]
    pk: int = int(request.POST["pk"])
    action_name: str = request.POST.get("action", "")

    if not action_name:
        # Probably submitted the default empty option, ignore.
        return HttpResponseRedirect(referer_url)

    model_cls: type = apps.get_model(app_label, model_name)
    queryset: QuerySet = model_cls.objects.filter(pk=pk)

    model_admin: object = admin.site._registry[model_cls]
    for action, name, label in model_admin._get_base_actions():
        if name == action_name:
            action(model_admin, request, queryset)
            model_admin.message_user(request, _("Action:") + f" {label}")

    return HttpResponseRedirect(referer_url)
