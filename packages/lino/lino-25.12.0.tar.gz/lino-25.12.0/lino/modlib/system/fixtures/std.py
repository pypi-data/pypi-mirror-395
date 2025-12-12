from django.conf import settings

def objects():
    settings.SITE.site_config.update()
    return []
