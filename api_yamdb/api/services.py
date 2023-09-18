from django.db.models import (
    Model,
    Avg
)
from django.db.models.query import QuerySet
from django.utils import timezone
from django.shortcuts import get_object_or_404


def create_object(model: Model, **parameters) -> Model:
    return model.objects.create(**parameters)


def get_all_objects(model: Model) -> QuerySet:
    return model.objects.all()


def query_with_filter(model: Model,
                      filter_dict: dict,
                      single=False) -> QuerySet:
    if single:
        return get_object_or_404(
            model,
            **filter_dict
        )
    else:
        return model.objects.filter(
            **filter_dict
        )


def query_average_by_field(model: Model, field: str) -> float:
    return model.objects.aggregate(average_field=Avg(field))['average_field']


def get_current_year() -> int:
    return timezone.now().year
