from rest_framework.generics import get_object_or_404

from movie_recommendation.models import Customer, Movie


class DoubleFieldLookupMixin(object):
    """
    title, director 2개의 lookup_fields
    """

    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]:  # Ignore empty fields.
                filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


class TripleFieldLookupMixin(object):
    """
    title, director, nickname 3개의 lookup_fields
    """

    def get_object(self):
        queryset = self.get_queryset().filter(customer__nickname=self.kwargs['nickname'])
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if field == 'nickname':
                filter["customer__" + field] = self.kwargs[field]
            elif self.kwargs[field]:  # Ignore empty fields.
                filter["movie__" + field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj
