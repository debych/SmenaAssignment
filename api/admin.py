from django.contrib import admin
from .models import Printer, Check


# Register your models here.

class PrinterAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General', {
            'fields': (
                'name', 'api_key', 'check_type', 'point_id'
            )
        }),
    )
    search_fields = ('name',)
    list_display = ('name', 'api_key', 'check_type', 'point_id')


class CheckAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General', {
            'fields': (
                'printer', 'type', 'order', 'status', 'pdf_file'
            )
        }),
    )
    search_fields = ('id',)
    list_display = ('id', 'printer', 'type', 'status')


admin.site.register(Printer, PrinterAdmin)
admin.site.register(Check, CheckAdmin)
