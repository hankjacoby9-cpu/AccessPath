"""Picks which model handles which kind of work. Models come from settings, so swapping is a config change."""

from django.conf import settings

CHEAP_KINDS = {"image", "graph"}


def model_for(kind: str) -> str:
    return settings.LLM_CHEAP_MODEL if kind in CHEAP_KINDS else settings.LLM_STRONG_MODEL
