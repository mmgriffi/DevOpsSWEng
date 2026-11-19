from django.conf import settings

def app_version(_request):
    return {
        "APP_VERSION": settings.APP_VERSION,
        "BUILD_DATE": settings.BUILD_DATE,
    }

