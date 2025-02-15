from django.db.models import Q

def build_q(fields_dict, params_dict, request=None):
    
    and_query = Q()

    for fieldname in fields_dict:
        search_field = fields_dict[fieldname]
        if fieldname in params_dict and params_dict[fieldname] != '' and params_dict[fieldname] != []:
            or_query = None

            if type(search_field) == type(list()):
                field_list = search_field
                search_operator = "__icontains"
                fixed_filters = None
                multiple_values = False
                custom_query_method = None
                value_mapper = None

            else: 
                if search_field.get('ignore', False):
                    continue

                field_list = search_field['fields']
                search_operator = search_field.get('operator', None)
                fixed_filters = search_field.get('fixed_filters', None)
                multiple_values = search_field.get('multiple', False)
                custom_query_method =  search_field.get('custom_query', None)
                value_mapper =  search_field.get('value_mapper', None)

            for model_field in field_list:

                if multiple_values:
                    if hasattr(params_dict, "getlist"):
                        request_field_value = params_dict.getlist(fieldname)
                    elif type(params_dict[fieldname]) == list:
                        request_field_value = params_dict[fieldname]
                    else:
                        request_field_value = [params_dict[fieldname]]
                    if value_mapper:
                        request_field_value = [value_mapper(value) for value in request_field_value]
                else:
                    request_field_value = params_dict[fieldname] if not value_mapper else value_mapper(params_dict[fieldname])

                if not custom_query_method:
                    fieldname_key = model_field + search_operator
                    filter_dict = { fieldname_key : request_field_value}
                    if not or_query:
                        or_query = Q(**filter_dict)
                    else:
                        or_query = or_query | Q(**filter_dict)
                else:
                    if not request:
                        cf = custom_query_method(model_field, request_field_value, params_dict)
                    else:
                        cf = custom_query_method(model_field, request_field_value, request)

                    if not or_query:
                        or_query = cf
                    else:
                        or_query = or_query | cf

            fixed_filters_q = Q()
            if fixed_filters:
                if callable(fixed_filters):
                    fixed_filters_q = fixed_filters(params_dict)
                elif type(fixed_filters) is dict:
                    fixed_filters_q = Q(**fixed_filters)

            and_query = and_query & or_query
            and_query = and_query & fixed_filters_q


    return and_query



class BaseFilter(object):
    
    search_fields  = {}


    @classmethod
    def build_q(cls, params, request=None):
        return build_q(cls.get_search_fields(), params, request)


    @classmethod
    def get_search_fields(cls):
       
        sfdict = {}
        for klass in tuple(cls.__bases__) + (cls, ):
            if hasattr(klass, 'search_fields'):
                sfdict.update(klass.search_fields)
        return sfdict