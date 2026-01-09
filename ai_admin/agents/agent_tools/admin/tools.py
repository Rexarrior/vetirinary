from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
import json

def get_all_model_names():
    """
    Returns a list of all available models in the format 'app_label.model_name'.
    """
    models_list = []
    for model in apps.get_models():
        models_list.append(f"{model._meta.app_label}.{model._meta.model_name}")
    return models_list

def get_model_schema(app_label, model_name):
    """
    Returns the schema (fields and types) of a specific model.
    """
    try:
        model = apps.get_model(app_label, model_name)
    except LookupError:
        return f"Error: Model '{app_label}.{model_name}' not found."

    schema = {
        "model": f"{app_label}.{model_name}",
        "fields": []
    }
    
    for field in model._meta.get_fields():
        if field.auto_created:
            continue
            
        field_info = {
            "name": field.name,
            "type": field.get_internal_type(),
            "help_text": getattr(field, 'help_text', ''),
        }
        
        if field.is_relation:
            if field.related_model:
                field_info["related_model"] = f"{field.related_model._meta.app_label}.{field.related_model._meta.model_name}"
            else:
                field_info["related_model"] = "Self"
            
        schema["fields"].append(field_info)
        
    return schema

def list_objects(app_label, model_name, filters=None):
    """
    Lists objects of a model, optionally filtered.
    filters should be a dictionary of field lookups.
    """
    try:
        model = apps.get_model(app_label, model_name)
    except LookupError:
        return f"Error: Model '{app_label}.{model_name}' not found."

    try:
        qs = model.objects.all()
        if filters:
            qs = qs.filter(**filters)
        
        # Limit to 10 objects to avoid token overflow
        qs = qs[:10]
        
        results = []
        for obj in qs:
            # Simple serialization
            data = {}
            for field in model._meta.fields:
                val = getattr(obj, field.name)
                data[field.name] = str(val)
            results.append(data)
            
        return results
    except Exception as e:
        return f"Error listing objects: {str(e)}"

def get_object(app_label, model_name, object_id):
    """
    Gets a specific object by ID.
    """
    try:
        model = apps.get_model(app_label, model_name)
        obj = model.objects.get(pk=object_id)
        
        data = {}
        for field in model._meta.fields:
            val = getattr(obj, field.name)
            data[field.name] = str(val)
            
        return data
    except LookupError:
        return f"Error: Model '{app_label}.{model_name}' not found."
    except ObjectDoesNotExist:
        return f"Error: Object with ID {object_id} not found."

def create_object(app_label, model_name, data):
    """
    Creates a new object.
    """
    try:
        model = apps.get_model(app_label, model_name)
        # Handle foreign keys: if data contains FK ID, ensure it's an integer
        # This is a basic implementation.
        obj = model.objects.create(**data)
        return f"Success: Created object with ID {obj.pk}"
    except LookupError:
        return f"Error: Model '{app_label}.{model_name}' not found."
    except Exception as e:
        return f"Error creating object: {str(e)}"

def update_object(app_label, model_name, object_id, data):
    """
    Updates an existing object.
    """
    try:
        model = apps.get_model(app_label, model_name)
        model.objects.filter(pk=object_id).update(**data)
        return f"Success: Updated object with ID {object_id}"
    except LookupError:
        return f"Error: Model '{app_label}.{model_name}' not found."
    except Exception as e:
        return f"Error updating object: {str(e)}"

def delete_object(app_label, model_name, object_id):
    """
    Deletes an object.
    """
    try:
        model = apps.get_model(app_label, model_name)
        model.objects.filter(pk=object_id).delete()
        return f"Success: Deleted object with ID {object_id}"
    except LookupError:
        return f"Error: Model '{app_label}.{model_name}' not found."
    except Exception as e:
        return f"Error deleting object: {str(e)}"
