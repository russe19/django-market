from django.contrib import admin

from catalog.models import (Cover, Genre, Music, MusicText, Offer,
                            ProductProperty, Property, Style)

from .admin_mixins import ExportAsCSVMixin


class PropertyInline(admin.TabularInline):
    model = Offer.property.through


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        "export_csv",
    ]
    inlines = [
        PropertyInline,
    ]
    list_display = ('id', 'name', 'description_short', 'price', 'type')
    list_display_links = ('id', 'name')
    ordering = ('type', '-pk')
    search_fields = "name", "description"
    fieldsets = [
        ("main", {
            "fields": ("name", "description", "price"),
        }),
        ("addition", {
            "fields": ("seller", "type", "user", "date"),
            "classes": ("collapse", ),
        })
    ]

    def description_short(self, obj: Offer) -> str:
        if len(obj.description) < 40:
            return obj.description
        return obj.description[:40] + '...'


# class GenreInline(admin.StackedInline):
#     model = Music.genre.through

@admin.register(Cover)
class CoverAdmin(admin.ModelAdmin):
    list_display = ('id', 'offer', )
    search_fields = "offer",

    def get_queryset(self, request):
        return Cover.objects.select_related("offer")


@admin.register(MusicText)
class MusicTextAdmin(admin.ModelAdmin):
    list_display = ('id', 'offer', )
    search_fields = "offer",

    def get_queryset(self, request):
        return MusicText.objects.select_related("offer")


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ('id', 'offer', )
    search_fields = "offer",

    def get_queryset(self, request):
        return Music.objects.select_related("offer")


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    search_fields = "name",


@admin.register(ProductProperty)
class ProductPropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', )
    search_fields = "property",


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    search_fields = "name",


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    search_fields = "name",
