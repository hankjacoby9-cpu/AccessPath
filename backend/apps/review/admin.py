from django.contrib import admin

from .models import Comment, Node, NodeVersion, ReviewAction


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ["id", "lecture", "order", "kind", "state", "confidence"]
    list_filter = ["state", "kind"]


admin.site.register(NodeVersion)
admin.site.register(Comment)
admin.site.register(ReviewAction)
