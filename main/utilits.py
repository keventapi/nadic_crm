from django.shortcuts import get_object_or_404
from .models import ProductType

def get_formated_form_response(response, keys, values):
    db_update = []
    for i in range(len(keys)):
        if keys[i] == "type":
            type_id = response.POST.get(f"product_{keys[i]}")
            value = get_object_or_404(ProductType, id=int(type_id))      
        elif keys[i] == "image":
            value = response.FILES.get(f"product_{keys[i]}")
        else:
            value = response.POST.get(f"product_{keys[i]}")

        if value is None:
            if keys[i] == "type":
                value = get_object_or_404(ProductType, id=int(values[i]))
            else:
                value = values[i]

        db_update.append(value)
        
    return format_to_dictionary(keys, db_update)

def format_to_dictionary(keys, db_update):
    db_dict = {}
    for index in range(len(keys)):
        db_dict[f'product_{keys[index]}'] = db_update[index]
    return db_dict    