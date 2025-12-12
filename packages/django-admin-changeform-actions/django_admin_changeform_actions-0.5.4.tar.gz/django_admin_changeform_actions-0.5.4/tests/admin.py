from django.contrib import admin

from changeform_actions import ChangeFormActionsMixin
from tests.models import MyModel


class MyModelAdmin(ChangeFormActionsMixin, admin.ModelAdmin):
    actions = ["add_copy_suffix"]

    def add_copy_suffix(self, request, queryset):
        for instance in queryset:
            instance.name += " - copy"
            instance.save()


admin.site.register(MyModel, MyModelAdmin)
