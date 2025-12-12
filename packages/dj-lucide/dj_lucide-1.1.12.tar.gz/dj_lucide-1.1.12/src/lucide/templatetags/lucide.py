from __future__ import annotations

from django import template
from django.utils.safestring import SafeString, mark_safe

import lucide as _lucide

register = template.Library()


@register.simple_tag
def lucide(name: str, *, size: int | None = 24, **kwargs: object) -> str:
    return _render_icon(name, size, **kwargs)


def _render_icon(name: str, size: int | None, **kwargs: object) -> str:
    fixed_kwargs = {
        key: (value + "" if isinstance(value, SafeString) else value)
        for key, value in kwargs.items()
    }
    try:
        return mark_safe(_lucide._render_icon(name, size, **fixed_kwargs))
    except (KeyError, AttributeError, ValueError):
        # Fallback: try a known "alert-triangle" icon if available
        try:
            return mark_safe(_lucide._render_icon("alert-triangle", size, **fixed_kwargs))
        except Exception:
            # As last resort, just render the name as plain text
            return mark_safe(f"<span class='lucide-fallback'>{name}</span>")
