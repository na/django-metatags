﻿from django.contrib import admin
from metatags.models import Metatag, MetatagType

class MetatagAdmin(admin.ModelAdmin):
    list_display = ('type', '_content_object', 'content_type', 'object_id')
    list_filter = ('type','content_type')
    ordering = ('content_type','object_id')

admin.site.register(MetatagType)
admin.site.register(Metatag, MetatagAdmin)
