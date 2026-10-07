from django.contrib import admin

from .models import Class, ClassMembership, Invite, Lecture


class MembershipInline(admin.TabularInline):
    model = ClassMembership
    fk_name = "klass"
    extra = 0


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ["course_code", "name", "term", "created_by"]
    inlines = [MembershipInline]


admin.site.register(Lecture)
admin.site.register(Invite)
