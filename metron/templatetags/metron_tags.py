from django import template
from django.conf import settings

from metron import activity


register = template.Library()


@register.simple_tag(takes_context=True)
def analytics(context):
    content = ""
    for kind, codes in getattr(settings, "METRON_SETTINGS", {}).items():
        code = codes.get(int(settings.SITE_ID))
        if code is not None and "user" in context and "request" in context:
            t = template.loader.get_template("metron/_%s.html" % kind)
            content += t.render(template.Context({
                "code": code,
                "user": context["user"],
                "actions": activity.all(context["request"], kind)
            }))
    return content

@register.simple_tag(takes_context=True)
def adwords_conversion(context, key, conversion_value=0):
    content = ""
    page_ids = getattr(settings, "METRON_ADWORDS_SETTINGS", {}).get(key)
    if page_ids:
        t = template.loader.get_template("metron/_adwords_conversion.html")
        content = t.render(template.Context({
            "conversion_id": page_ids["conversion_id"],
            "conversion_format": page_ids["conversion_format"],
            "conversion_label": page_ids["conversion_label"],
            "conversion_value": conversion_value,
        }))
    return content

@register.simple_tag(takes_context=True)
def adwords_remarketing(context, key):
    content = ""
    page_ids = getattr(settings, "METRON_ADWORDS_REMARKETING_SETTINGS", {}).get(key)
    if page_ids:
        t = template.loader.get_template("metron/_adwords_remarketing.html")
        content = t.render(template.Context({
            "conversion_id": page_ids["conversion_id"],
            "conversion_label": page_ids["conversion_label"],
        }))
    return content

@register.simple_tag(takes_context=True)
def bingads_conversion(context, key, conversion_value=0):
    content = ""
    page_ids = getattr(settings, "METRON_BINGADS_SETTINGS", {}).get(key)
    if page_ids:
        t = template.loader.get_template("metron/_bingads_conversion.html")
        content = t.render(template.Context({
            "account_id": page_ids["account_id"],
            "domain_id": page_ids["domain_id"],
            "action_id": page_ids["action_id"],
            "conversion_value": conversion_value,
            "web_protocol": "https" if context["request"].is_secure else "http"
        }))
    return content
