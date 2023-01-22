from django.contrib import admin
from utm_tags_tracking.models import UTMVisit


class UTMVisitAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'medium', 'campaign', 'timestamp')
    search_fields = ('source', 'medium', 'term', 'content')
    list_filter = ('source', 'medium', 'timestamp')
    readonly_fields = ('timestamp',)


admin.site.register(UTMVisit, UTMVisitAdmin)

