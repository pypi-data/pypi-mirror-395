from django.template import Library

register = Library()


@register.simple_tag(takes_context=True)
def get_changeform_actions_dropdown(context, model_admin) -> str:
    """Return optional <select> HTML if ModelAdmin has been configured accordingly."""
    request = context["request"]
    try:
        return model_admin.get_changeform_actions_dropdown(request, context)
    except AttributeError:
        return ""
