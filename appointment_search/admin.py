from django.contrib import admin

from . import models

class DetailsInline(admin.TabularInline):
    model = models.AsylumOfficeDetails

@admin.register(models.AsylumOffice)
class AsylumOfficeAdmin(admin.ModelAdmin):
    fields = ('name',)
    inlines = [
        DetailsInline
    ]

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


#admin.site.register(models.AppointmentSchedule, admin.ModelAdmin)
