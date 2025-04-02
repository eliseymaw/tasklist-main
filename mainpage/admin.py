from django.contrib import admin
from . import models
@admin.register(models.Geoposition)
class GeopositionAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in models.Geoposition._meta.get_fields() if field.name !='id'] 
    list_display = ['lat','lon']


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.Task._meta.get_fields()]
