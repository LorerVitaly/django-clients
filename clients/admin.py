from django.apps import apps
from django.contrib import admin


apps_models = apps.get_models()
apps_models = [model for model in apps_models if model._meta.app_label.startswith('clients')]
for model in apps_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
