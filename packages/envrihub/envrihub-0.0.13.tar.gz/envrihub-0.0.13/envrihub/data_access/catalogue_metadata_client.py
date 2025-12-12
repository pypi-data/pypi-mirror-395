import inspect

from .models import RESTfulAPIDataAccess
from .utils import call_restful_api

def _sanitize_base_url(url):
    # the base URL as registered in the COS looks like this:
    # https://www.marinespecies.org/rest/AphiaAttributesByAphiaID/{id}{?include_inherited}
    # so it can have both route and query parameters in it. When you see something like }{ 
    # it is likely route paramters are over
    if '}{' in url:
        return url.split('}{', 1)[0] + '}'
    else:
        return url



def build_epos_catalogue_metadata_access(base_url:str, parameters:list, content_type:str='application/json', description = '', service_name = 'Service')->type:
    '''builds a class with custom access method inheriting from RESTfulAPIDataAccess'''
    # build the access method's docstring
    docstring = description + '\n\nParameters\n----------\n'
    for par in parameters:
        docstring = docstring +  str(par.get('name')) + ': ' + 'default = ' + str(par.get('defaultValue')) + '\n\t' + str(par.get('label')) + '\n'
    # build the access method
    access_method = build_access_function(base_url, params=parameters, response_content_type=content_type, docstring = docstring)
    # and poop out the class
    return type(service_name, tuple([RESTfulAPIDataAccess]), {'access':access_method})

def build_access_function(base_url, params,  response_content_type,
                         docstring):
    ## parameters is a list of objects like this
    '''
    {'defaultValue': 'false',
    'label': 'CategoryID',
    'name': 'include_inherited',
    'required': False,
    'type': 'boolean'}
    '''
    # we need to translate it into a dictionary of parameter name -> default value pairs
    pardict = {par.get('name'):par.get('defaultValue') for par in params}
    # then the base_url can contain a mixture of query and route parameters, we have to fix that
    base_url = _sanitize_base_url(base_url)
    # gogadget closure
    def access(self, **kwargs): # the only way to dynamically build a method's signature is to use **kwargs and then do some deep black magic with inspect
        # build request parameters
        #print(kwargs)
        request_paramaters = {p:(kwargs[p] if (p in kwargs) else v) for p, v in pardict.items()}
        # the following is because of URL parameters
        try:
            query_url = base_url.format(**request_paramaters)
        except:
            query_url = base_url
        # now the ApplicationServerPool object should handle the request
        return call_restful_api(url = query_url, params = request_paramaters, headers = {},
                             method='GET', additional_headers= kwargs.get('additional_headers'),
                                expected_response_content_type = response_content_type)
    # adding docstring
    access.__doc__ = docstring
    # and signature
    signature_params = [inspect.Parameter(name="self", kind = inspect.Parameter.POSITIONAL_ONLY)]
    signature_params = signature_params + [inspect.Parameter(name=p, default = v, kind = inspect.Parameter.KEYWORD_ONLY) for p, v in pardict.items()]
    signature_params.append(inspect.Parameter(name='additional_headers', default = None, kind = inspect.Parameter.KEYWORD_ONLY, annotation=dict))
    #print(signature_params)
    access.__signature__ = inspect.Signature(parameters=signature_params)
    return access
