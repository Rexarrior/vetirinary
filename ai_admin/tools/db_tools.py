from django.apps import apps
from django.db import models

class DBTools:
    """
    Tools for interacting with the Django database.
    """
    
    @staticmethod
    def get_all_models():
        """
        Returns a list of all installed models and their fields.
        """
        model_list = []
        for model in apps.get_models():
            fields = [f.name for f in model._meta.get_fields()]
            model_list.append({
                'app_label': model._meta.app_label,
                'model_name': model._meta.model_name,
                'fields': fields
            })
        return model_list

    @staticmethod
    def query_model(app_label, model_name, query_params):
        """
        Queries a model with the given parameters.
        """
        try:
            model = apps.get_model(app_label, model_name)
            return list(model.objects.filter(**query_params).values())
        except LookupError:
            return f"Model {app_label}.{model_name} not found."
        except Exception as e:
            return str(e)
