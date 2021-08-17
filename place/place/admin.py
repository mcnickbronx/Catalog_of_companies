from django.contrib import admin

from .models import Place, Open, Review, Highlights, Question

from import_export.admin import ImportExportModelAdmin
from .resources import PlaceResource, OpenResource, ReviewResource, HighlightsResource, QuestionResource


class ReviewInline(admin.TabularInline):
    model = Review


class PlaceAdmin(ImportExportModelAdmin):
    resource_class = PlaceResource
    search_fields = ('id', 'company_name', 'region')
    list_filter = ('city', 'price',)
    inlines = [
        ReviewInline,
    ]


admin.site.register(Place, PlaceAdmin)


class OpenAdmin(ImportExportModelAdmin):
    resource_class = OpenResource
    search_fields = ('place__id', 'day', 'open_interval',)
    # list_filter = ('day','open_interval')


admin.site.register(Open, OpenAdmin)


class ReviewAdmin(ImportExportModelAdmin):
    search_fields = ('place__id', 'reviewer_name', 'review_text',)
    resource_class = ReviewResource


admin.site.register(Review, ReviewAdmin)


class HighlightsAdmin(ImportExportModelAdmin):
    search_fields = ('place__id', 'food_name',)
    resource_class = HighlightsResource


admin.site.register(Highlights, HighlightsAdmin)


class QuestionAdmin(ImportExportModelAdmin):
    search_fields = ('place__id',)
    resource_class = QuestionResource


admin.site.register(Question, QuestionAdmin)
