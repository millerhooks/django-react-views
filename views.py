import os.path
from typing import Type, List, Tuple, Union, Any, Dict

from django.db.models import QuerySet, Model
from django.views.generic import *
from django.views.generic.base import ContextMixin


class ModelSerializer(object):
    """
    The expected interface of a ModelSerializer.
    Recommended to use django rest framework's ModelSerializer as the implementation.
    """

    def __init__(self, instance:Union[Model, QuerySet]=None, context=None, many=None):
        raise NotImplementedError

    @property
    def data(self) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        :return: If instance is a single Model instance return a dictionary of that objects fields, otherwise return an
        """
        raise NotImplementedError


def get_app_name(obj):
    return obj.__module__.split('.')[0]


class ReactMixin(object):
    initial_react_state = {}
    react_component = None
    template_component_name = 'component'
    react_dist_directory = 'dist'
    template_state_name = 'props'
    key_field = 'url'

    def get_initial_react_state(self):
        if isinstance(self, ReactMultiModelMixin) and self.use_objects_as_state:
            return self.object_based_react_state()
        else:
            return self.initial_react_state

    def get_react_component(self):
        return os.path.join(self.react_dist_directory, get_app_name(self), self.react_component)


class ReactMultiModelMixin(object):
    use_objects_as_state = True
    queryset_serializer_pairs = None  # type: List[Tuple[Union[QuerySet, Model], Type[ModelSerializer]]]

    def get_queryset_serializer_pairs(self) -> List[Tuple[Union[QuerySet, Model], Type[ModelSerializer]]]:
        return self.queryset_serializer_pairs

    def object_based_react_state(self):
        return {"objects": self.get_serialized_objects()}

    def get_serialized_objects(self):
        model_object_pairs = []
        for queryset_or_object, serializer in self.get_queryset_serializer_pairs():
            if isinstance(queryset_or_object, QuerySet):
                model_name = queryset_or_object.model._meta.label_lower
                many = True
            else:
                model_name = queryset_or_object._meta.label_lower
                many = False
            serialized_objects = serializer(queryset_or_object,
                                            context={'request': self.request, 'view': self, 'format': None},
                                            many=many).data
            model_object_pairs.append((model_name, serialized_objects))
        return redux_objects(self.key_field, *model_object_pairs)


class ReactSingleModelMixin(ReactMultiModelMixin):
    model_serializer = None  # type: Type[ModelSerializer]

    def get_queryset_serializer_pairs(self):
        return [(self.get_queryset(), self.model_serializer)]


def redux_objects(key_field, *model_object_pairs):
    object_state = {}
    for pair in model_object_pairs:
        model_name, serialized_objects = pair
        existing = object_state.get(model_name, {})
        object_state[model_name] = {
            **existing,
            **key_to_object_dict(key_field, serialized_objects)
        }
    return object_state


def key_to_object_dict(key_field, serialized_objects: Union[list, dict]):
    if isinstance(serialized_objects, list):
        return {obj[key_field]: obj for obj in serialized_objects}
    else:
        return {serialized_objects[key_field]: serialized_objects}


def get_react_context(react_view: ReactMixin):
    context = {
        react_view.template_state_name: react_view.get_initial_react_state(),
        react_view.template_component_name: react_view.get_react_component(),
        "key_field": react_view.key_field
    }
    return context


def get_full_context(react_view: ReactMixin, parent_view: ContextMixin, *args, **kwargs):
    return {
        **parent_view.get_context_data(*args, **kwargs),
        **get_react_context(react_view)
    }


class ReactView(View, ReactMixin):
    pass


class ReactRedirectView(RedirectView, ReactMixin):
    pass


class ReactTemplateView(TemplateView, ReactMixin):
    def get_context_data(self, *args, **kwargs):
        return get_full_context(self, super(), *args, **kwargs)


class ReactArchiveIndexView(ArchiveIndexView, ReactMixin, ReactSingleModelMixin):
    def get_context_data(self, *args, **kwargs):
        return get_full_context(self, super(), *args, **kwargs)


class ReactYearArchiveView(YearArchiveView, ReactMixin, ReactSingleModelMixin):
    def get_context_data(self, *args, **kwargs):
        return get_full_context(self, super(), *args, **kwargs)


class ReactMonthArchiveView(MonthArchiveView, ReactMixin, ReactSingleModelMixin):
    def get_context_data(self, *args, **kwargs):
        return get_full_context(self, super(), *args, **kwargs)


class ReactWeekArchiveView(WeekArchiveView, ReactMixin, ReactSingleModelMixin):
    def get_context_data(self, *args, **kwargs):
        return get_full_context(self, super(), *args, **kwargs)


class ReactDayArchiveView(DayArchiveView, ReactMixin, ReactSingleModelMixin):
    def get_context_data(self, *args, **kwargs):
        return get_full_context(self, super(), *args, **kwargs)


class ReactTodayArchiveView(TodayArchiveView, ReactMixin, ReactSingleModelMixin):
    def get_context_data(self, *args, **kwargs):
        return get_full_context(self, super(), *args, **kwargs)


class ReactDateDetailView(DateDetailView, ReactMixin, ReactSingleModelMixin):
    def get_context_data(self, *args, **kwargs):
        return get_full_context(self, super(), *args, **kwargs)


class ReactDetailView(DetailView, ReactMixin, ReactSingleModelMixin):
    def get_context_data(self, *args, **kwargs):
        return get_full_context(self, super(), *args, **kwargs)


class ReactFormView(FormView, ReactMixin):
    def get_context_data(self, *args, **kwargs):
        return get_full_context(self, super(), *args, **kwargs)


class ReactCreateView(CreateView, ReactMixin, ReactSingleModelMixin):
    def get_context_data(self, *args, **kwargs):
        return get_full_context(self, super(), *args, **kwargs)


class ReactUpdateView(UpdateView, ReactMixin, ReactSingleModelMixin):
    def get_context_data(self, *args, **kwargs):
        return get_full_context(self, super(), *args, **kwargs)


class ReactDeleteView(DeleteView, ReactMixin, ReactSingleModelMixin):
    def get_context_data(self, *args, **kwargs):
        return get_full_context(self, super(), *args, **kwargs)


class ReactListView(ListView, ReactMixin, ReactSingleModelMixin):
    def get_context_data(self, *args, **kwargs):
        return get_full_context(self, super(), *args, **kwargs)


class ReactMultiModelView(TemplateView, ReactMixin, ReactMultiModelMixin):
    def get_context_data(self, *args, **kwargs):
        return get_full_context(self, super(), *args, **kwargs)
