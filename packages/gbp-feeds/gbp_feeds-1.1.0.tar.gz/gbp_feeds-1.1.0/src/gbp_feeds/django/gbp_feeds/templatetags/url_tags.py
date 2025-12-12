"""Custom template tags for gbp-feeds"""

from typing import Any

from django import template
from django.http import HttpRequest
from django.template.context import Context
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def full_url(context: Context, name: str, **kwargs: Any) -> str:
    """Return the full url of the given named url given the context"""
    request: HttpRequest = context["request"]

    return request.build_absolute_uri(reverse(name, kwargs=kwargs))


@register.filter
def machine_feed_link(machine: str) -> str:
    """Render the machine-specific (atom) feed link tag"""
    url = reverse("gbp-feeds-rss-machine", kwargs={"machine": machine})

    return mark_safe(f'<a href="{url}"><span><i class="bi bi-rss"></i></span></a>')
