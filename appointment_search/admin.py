from django.conf.urls import url
from django.contrib import admin

from appointment_search.views import ImportSpreadsheetView
from . import models


class DetailsInline(admin.TabularInline):
    model = models.AsylumOfficeDetails


@admin.register(models.AsylumOffice)
class AsylumOfficeAdmin(admin.ModelAdmin):
    fields = ('name',)
    inlines = [
        DetailsInline
    ]

    def get_urls(self):
        urls = super(AsylumOfficeAdmin, self).get_urls()
        my_urls = [
            url(r'^import_spreadsheet/$', ImportSpreadsheetView.as_view(), name='import_spreadsheet'),
        ]
        return my_urls + urls

admin.site.register(
    models.AppointmentSchedule,
    list_display=[
        'registration_number',
        'date',
        'office',
    ],
    search_fields=[
        'registration_number',
    ],
    list_filter=[
        'date',
        'office',
    ],
    list_select_related=['office']
)
admin.site.index_template = "admin/custom_index.html"
