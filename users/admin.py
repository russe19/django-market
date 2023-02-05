from django.contrib import admin

from catalog.admin_mixins import ExportAsCSVMixin
from users.models import Bonus, Profile, ProfileImage, Status


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    list_display = ('__str__', )
    actions = [
        "export_csv",
    ]
    fieldsets = [
        ("main", {
            "fields": ("user", "balance"),
        }),
        ("addition", {
            "fields": ("number", "telegram"),
        })
    ]


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = "name",


@admin.register(ProfileImage)
class ProfileImageAdmin(admin.ModelAdmin):
    list_display = ('profile', )


@admin.register(Bonus)
class BonusAdmin(admin.ModelAdmin):
    list_display = ('profile', )
