from django.contrib import admin
from .models import *

# Register your models here.

class ProductionLogAdmin(admin.ModelAdmin):
    readonly_fields = ["available_operating_time","unplanned_downtime","total_product","duration"]
    list_display = ["material_name","machine","total_product"]
    list_filter = ["material_name","machine","total_product"]
    search_fields = ["material_name","machine","total_product"]

admin.site.register(Machine)
admin.site.register(ProductionLog,ProductionLogAdmin)