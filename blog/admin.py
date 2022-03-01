from django.contrib import admin
from .models import Pdf

class Filter(admin.ModelAdmin):
    list_display = ("id","title","student","season","lesson","keywords")
    list_filter = ("student","lesson","title","season")
    search_fields = ["keywords"]

admin.site.register(Pdf,Filter)
