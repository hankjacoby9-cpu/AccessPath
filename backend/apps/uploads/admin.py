from django.contrib import admin

from .models import ParsedDocument, ProcessingJob, SourceFile


@admin.register(SourceFile)
class SourceFileAdmin(admin.ModelAdmin):
    list_display = ["original_name", "klass", "lecture", "status", "created_at"]
    list_filter = ["status"]


admin.site.register(ProcessingJob)
admin.site.register(ParsedDocument)
