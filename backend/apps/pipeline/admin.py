from django.contrib import admin

from .models import LLMCall


@admin.register(LLMCall)
class LLMCallAdmin(admin.ModelAdmin):
    list_display = ["purpose", "model", "prompt_version", "input_tokens", "output_tokens", "cost_usd", "created_at"]
    list_filter = ["purpose", "model"]
