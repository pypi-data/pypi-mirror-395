import types

from django.urls import path, re_path
from django.db.models.fields import NOT_PROVIDED
from django.http import HttpResponse

from .calc_resource import Metrics

data_types = {
    'AutoField': 'integer AUTO_INCREMENT',
    'BigAutoField': 'bigint AUTO_INCREMENT',
    'BinaryField': 'longblob',
    'BooleanField': 'bool',
    'CharField': 'varchar(%(max_length)s)',
    'DateField': 'date',
    'DateTimeField': 'datetime(6)',
    'DecimalField': 'numeric(%(max_digits)s, %(decimal_places)s)',
    'DurationField': 'bigint',
    'FileField': 'varchar(%(max_length)s)',
    'FilePathField': 'varchar(%(max_length)s)',
    'FloatField': 'double precision',
    'IntegerField': 'integer',
    'BigIntegerField': 'bigint',
    'IPAddressField': 'char(15)',
    'GenericIPAddressField': 'char(39)',
    'NullBooleanField': 'bool',
    'OneToOneField': 'integer',
    'PositiveIntegerField': 'integer UNSIGNED',
    'PositiveSmallIntegerField': 'smallint UNSIGNED',
    'SlugField': 'varchar(%(max_length)s)',
    'SmallIntegerField': 'smallint',
    'TextField': 'longtext',
    'TimeField': 'time(6)',
    'UUIDField': 'char(32)',
}


def get_route(route, view):
    if hasattr(view, 'as_view'):
        view = view.as_view()
        return re_path(rf'{route}', view)

    return path(route, view)


def get_routes(endpoints, **kwargs):
    enable_docs = kwargs.get('enable_docs')

    def docs(request, *args, **kwargs):
        response = '<pre>'
        for route, view in endpoints.items():

            response += '<br/>'
            # print('View', view)
            print('---------------------------------')
            print('Model', view.model)
            print('Rota', route)
            print('---------------------------------')

            response += f'Route: /{route}<br/>'

            # if view.model:
            #     print(view.model._meta.get_field('id'))
            #     field = view.model._meta.get_field('id')
            #     field_type = field.get_internal_type()
            #     response += f'   {field.name}: {field_type}<br/>'
            #     print(response)

            #     continue
            all_fields = {}
            if view.model:
                # print(dir(view.model._meta))
                # print(view.model._meta.verbose_name)
                for field in view.model._meta.fields:
                    # print(dir(field))
                    field_type = field.get_internal_type()
                    # response += f'   {field.name}: {field_type}<br/>'

                    choices = field.choices
                    default = field.default
                    if choices:
                        options = {}
                        for choice in choices:
                            options[choice[0]] = choice[1]

                        if default and default is not NOT_PROVIDED:
                            default = options[default]

                        # response += f'    default: {default}'

                    # print()
                    # print(field.name, field_type, field.choices, field.default)  # , field.description)
                    # all = {}
                    all_fields[field.name] = field_type
                    # all_fields.append(all)
                    # print(field.db_column)
                    # print('choices', field.choices)
                    # print('Name', field.name)
                    # print('Null', field.null)
                    # print('Description', field.description)

            methods = view.allowed_methods
            response += f'Allowed: {", ".join(view.allowed_methods)}<br/>'

            edit_fields = view.edit_fields
            if 'get' in methods:
                response += '  GET<br/>'
                if edit_fields:
                    for field in edit_fields:
                        field = view.model._meta.get_field(field)
                        field_type = field.get_internal_type()
                        response += f'   {field.name}: {field_type}<br/>'
                else:
                    for key, value in all_fields.items():
                        response += f'   {key}: {value}<br/>'

            list_fields = view.edit_fields

            update_fields = view.update_fields
            if 'patch' in methods:
                response += '  PATCH<br/>'
                if update_fields:
                    for field in update_fields:
                        try:
                            field = view.model._meta.get_field(field)
                            field_type = field.get_internal_type()
                            response += f'   {field.name}: {field_type}<br/>'
                        except Exception:
                            pass
                else:
                    for key, value in all_fields.items():
                        response += f'   {key}: {value}<br/>'

            create_fields = view.create_fields
            if 'post' in methods:
                response += '  POST<br/>'
                if create_fields:
                    for field in create_fields:
                        try:
                            field = view.model._meta.get_field(field)
                            field_type = field.get_internal_type()
                            response += f'   {field.name}: {field_type}<br/>'
                        except Exception:
                            pass

                else:
                    response += '   None<br/>'


            list_related_fields = view.list_related_fields
            edit_related_fields = view.edit_related_fields
            print('Rotas:')
            for route in view.__dict__.get('routes', []):
                print(route)

            continue

            # if view.model:
            #     for field in view._meta.get_fields():
            #         print(field)


            # print('Path', view.path)
            # print('DICT', view.__dict__)
            for key, value in view.__dict__.items():
                # print(key, value)
                # print(type(value)  'function')
                if isinstance(value, types.FunctionType):
                    print('Função', value)
                # print(callable(value))

            # print( )
            print('Autenticated:', view.__dict__.get('authenticated', True))
            print('Rotas:')
            for route in view.__dict__.get('routes', []):
                print(route)

            # methods = view.allowed_methods
            # edit_fields = view.edit_fields
            # list_fields = view.edit_fields
            # update_fields = view.update_fields
            # print('Metodos', methods)
            # print(methods, edit_fields, list_fields, update_fields)

            # model = view.model
            # if model:
            #     print(model.__dict__)
            #     print(view.fields)

            print()
        # return HttpResponse("<pre>Primeira linha\nSegunda linha</pre>")
        response += '</pre>'
        return HttpResponse(response)
        return HttpResponse('Docs')

    routes = [
        get_route(key, value) for key, value in endpoints.items()
    ] + [path('metrics', Metrics.as_view())]

    if enable_docs:
        routes += [
            path('docs', docs),
        ]
    return routes
