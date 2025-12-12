import inspect
import io
import os
import logging
import posixpath
from urllib.parse import urljoin
import requests
from .models import OpenAPI3DataAccess
from .utils import call_restful_api
from prance import ResolvingParser


def recursion_limit_handler_void(limit, refstring, recursions):
    return {}


# the noice factory method
def build_web_service_client(service_documentation, resource_name=None) -> type:
    parser = ResolvingParser(
        service_documentation, recursion_limit_handler=recursion_limit_handler_void
    )
    parser.parse()
    specification = parser.specification
    return build_access_class(specification, resource_name)


class ApplicationServer:
    def __init__(self, url, description):
        self.url = url
        self.description = description

    def call_function(self, function_name, **kwargs):
        service_url = self.url + function_name
        return call_restful_api(url=service_url, **kwargs)


class ApplicationServerPool:
    def __init__(self, specification_servers=[], base_address=""):
        self.servers = []
        self.preferred_server = None
        self._dead_servers = set()
        # import appservers from the OpenAPI specification
        if specification_servers is not None:
            # beware the base address here: some openapi specs have only
            # relative addresses, so with urljoin we try to combine them
            # with an absolute address. Urljoin is smart enough to tell
            # if the server url is already an absolute one and in such a
            # case it ignores the base address.
            self.servers = [
                ApplicationServer(
                    urljoin(base_address, server.get("url")), server.get("description")
                )
                for server in specification_servers
            ]
            self.preferred_server = self.servers[0] if len(self.servers) > 0 else None
            self.check_servers()

    def call_function(self, **kwargs):
        unavailable_servers = set()
        try:
            return self.preferred_server.call_function(**kwargs)
        except requests.exceptions.HTTPError as e:
            unavailable_servers.add(self.preferred_server)
            # find an available server
            response = None
            for s in self.servers:
                if (s not in self._dead_servers) and (s not in unavailable_servers):
                    try:
                        response = s.call_function(**kwargs)
                        self.preferred_server = s
                        return response
                    except:
                        unavailable_servers.add(s)
            logging.error(
                "Request to "
                + kwargs.get("function_name")
                + " cannot be satisfied on any server"
            )

    def check_servers(self):
        for s in self.servers:
            resp = requests.get(s.url)
            if 200 <= resp.status_code < 300:
                logging.info(f"{s.url} is online")
            else:
                self._dead_servers.add(s)
                logging.warning(f"{s.url} fails with HTTP status {resp.status_code}")


def _to_parameter_name(par_name):
    """Given a string, it returns a version of it that can be used as a Python parameter name"""
    return par_name.translate({ord(c): "_" for c in "/!@#*+-%&|[]()$ \r\n\t"})


def _remove_duplicates(elements: list[inspect.Parameter]):
    """monkey-patch solution to remove duplicate entries from the
    signature parameters list without destroying its ordering"""
    keys = set()
    out_els = []
    for e in elements:
        if e.name not in keys:
            out_els.append(e)
            keys.add(e.name)
    return out_els


def _build_translation_tables(*args):
    """given any collection of strings, it evaluates sanitized versions of said strings
    and returns two dictionaries containing the translation mapping:
    original string -> sanitized string
    and
    sanitized string -> original string"""
    ab = {}
    ba = {}
    for d in args:
        for k in d:
            san_k = _to_parameter_name(k)
            ab[k] = san_k
            ba[san_k] = k
    return ab, ba


def build_caller_function(
    function_name,
    method,
    params,
    route_parameters,
    content_parameters,
    default_headers,
    request_content_type,
    response_content_type,
    docstring="",
):
    """Creates a class method to call a REST service.
    The otuput callable object must be placed inside an object with
    a *servers* attribute that exposes a *call_function* method, because the generated callable
    will only parse parameters and send them to that function in that attribute"""
    # let's build a translation dictionary for parameter names
    # we need this because stuff like 'Content-Type' is legit HTTP parameter name
    # but it wuld not work as a Python variable name, hence the need for
    # a name conversion
    par_ab, par_ba = _build_translation_tables(
        params, route_parameters, content_parameters, default_headers
    )

    # in the method signature, we'll put the *sanitized* version of the names (so par_ab[par_name])
    # but then in the actual request dictionary, we should send the original parameter name (so par_ba[par_name])
    # gogadget closure
    def caller_function(
        self, **kwargs
    ):  # the only way to dynamically build a method's signature is to use **kwargs and then do some deep black magic with inspect
        # build request parameters
        # query/form parmaters
        request_paramaters = {
            p: (kwargs[par_ab.get(p)] if (par_ab.get(p) in kwargs) else v)
            for p, v in params.items()
        }
        # route parameters
        path_params = {
            p: (kwargs[par_ab.get(p)] if (par_ab.get(p) in kwargs) else v)
            for p, v in route_parameters.items()
        }
        # the idea here is that if the user wants to send a payload they manually built, they always can
        if "data" in kwargs:
            request_payload = kwargs.get("data")
        else:  # otherwise we'll cobble one together from the specification
            request_payload = {
                p: (kwargs[par_ab.get(p)] if (par_ab.get(p) in kwargs) else v)
                for p, v in content_parameters.items()
            }
        # build request headers
        # print(request_payload)
        request_headers = {
            p: (kwargs[par_ab.get(p)] if (par_ab.get(p) in kwargs) else v)
            for p, v in default_headers.items()
        }
        # now the ApplicationServerPool object should handle the request
        return self.servers.call_function(
            function_name=function_name,
            data=request_payload,
            params=request_paramaters,
            path_params=path_params,
            headers=request_headers,
            files=kwargs.get("files"),
            method=method,
            additional_headers=kwargs.get("additional_headers"),
            payload_content_type=request_content_type,
            expected_response_content_type=response_content_type,
        )

    # adding docstring
    caller_function.__doc__ = docstring
    # and signature
    signature_params = [
        inspect.Parameter(name="self", kind=inspect.Parameter.POSITIONAL_ONLY)
    ]
    signature_params = signature_params + [
        inspect.Parameter(
            name=par_ab.get(p), default=v, kind=inspect.Parameter.KEYWORD_ONLY
        )
        for p, v in params.items()
    ]
    signature_params = signature_params + [
        inspect.Parameter(
            name=par_ab.get(p), default=v, kind=inspect.Parameter.KEYWORD_ONLY
        )
        for p, v in route_parameters.items()
    ]
    signature_params = signature_params + [
        inspect.Parameter(
            name=par_ab.get(p), default=v, kind=inspect.Parameter.KEYWORD_ONLY
        )
        for p, v in content_parameters.items()
    ]
    signature_params = signature_params + [
        inspect.Parameter(
            name=par_ab.get(p), default=v, kind=inspect.Parameter.KEYWORD_ONLY
        )
        for p, v in default_headers.items()
    ]
    signature_params.append(
        inspect.Parameter(
            name="data", default=None, kind=inspect.Parameter.KEYWORD_ONLY
        )
    )
    signature_params.append(
        inspect.Parameter(
            name="files", default=None, kind=inspect.Parameter.KEYWORD_ONLY
        )
    )
    signature_params.append(
        inspect.Parameter(
            name="additional_headers",
            default=None,
            kind=inspect.Parameter.KEYWORD_ONLY,
            annotation=dict,
        )
    )
    # soooo, sometimes some paramters may appear twice becasue of weird specifciations...
    # therefore we need to turn signature params into a set and then back into a list
    # signature_params= list(set(signature_params))
    # UPDATE: that was a very bad idea, becasue it messed up parameters order
    # so in the end I had to write a fugly monkey patch method to fix the problem
    signature_params = _remove_duplicates(signature_params)
    # print(signature_params)
    caller_function.__signature__ = inspect.Signature(parameters=signature_params)
    return caller_function


def _sanitize(url_string):
    """Removes characters that cannot be into a function's name"""
    return url_string.translate({ord(c): None for c in "/!@#*+-%&|[]{}()$ \r\n\t"})


def parse_parameters(parameter_list: list):
    """parses the contents object in the OpenAPI specification
    to extrace content parameters and their default values. Plus docstrings"""
    params = {}
    path_params = {}  # inside the parameters object there may be path parameters too!
    header_params = {}  # and stuff that goes in the header too!
    docstring = ""
    for param_dict in parameter_list:
        name = param_dict.get("name")
        param_type = param_dict.get(
            "in"
        )  # this is the rat bastard telling where to shove the parameter
        # these are the schema informations
        if isinstance(param_dict.get("schema"), dict):
            description = param_dict.get("schema").get("description")
            default = param_dict.get("schema").get("default")
            par_type = param_dict.get("schema").get("type")
        else:
            description = ""
            default = None
            par_type = "any"
        # put things in the correct bin
        if param_type == "header":
            header_params[name] = default
        elif param_type == "path":
            path_params[name] = default
        else:
            params[name] = default
            # assembling the docstring
        docstring = (
            docstring
            + str(name)
            + ":"
            + str(par_type)
            + " "
            + "default = "
            + str(default)
            + "\n\t"
            + str(description)
            + "\n"
        )
    return params, header_params, path_params, docstring


def build_access_class(
    specification: dict, resource_name=None, base_address=""
) -> type:
    if resource_name is None:
        resource_name = _sanitize(specification.get("info").get("title"))
    class_methods = {}
    servers = ApplicationServerPool(specification.get("servers"), base_address)
    # now we have to go through the paths dictionary
    # which is made of abominations like this
    # {
    #  '/address': {'post': {...}, 'get':{...},
    #   ...
    # }
    for url, methods in specification.get("paths").items():
        supported_methods = ",".join([x for x in methods])
        logging.info(f"Operation: {url}, methods: {supported_methods}")
        for method, specs in methods.items():
            # here are the GET/POST/PUT/whatever variants
            # the possible responses are in the 'responses' object, which is an interable
            # likely there will be some error codes and somewhere a 200-OK one
            response_content_type = None
            if specs.get("responses"):
                for response, content in specs.get("responses").items():
                    if response in ["200", "201", "202"]:
                        # the content we are looking for! But beware: multiple response formats might be acceptable!
                        response_content_type = []
                        if isinstance(content.get("content"), dict):
                            for content_type, notes in content.get("content").items():
                                response_content_type.append(content_type)
                        # if the list has only one element, then we'll just pass down that one element
                        if len(response_content_type) == 1:
                            response_content_type = response_content_type[0]

            description = specs["description"] if specs.get("description") else ""
            docstring = description + "\n\nParameters\n----------\n"
            # here let's parse the GET http parameters
            params = {}
            path_params = (
                {}
            )  # inside the parameters object there may be path parameters too!
            header_params = {}  # and stuff that goes in the header too!
            if isinstance(specs.get("parameters"), list):
                params, header_params, path_params, param_docstring = parse_parameters(
                    specs.get("parameters")
                )
                docstring = docstring + param_docstring
            # now for the headers
            default_headers = {}
            # TODO read specification for headers, they should be in the *security*
            # section of the open API spec.
            # here, if any, the parameters to be structured into a JSON payload
            default_headers = default_headers | header_params
            content_parameters = {}
            request_content_type = None
            if isinstance(specs.get("requestBody"), dict):
                contents = specs.get("requestBody").get("content")
                if isinstance(contents, dict):
                    # let's get through all the stuff you can shove in the request body
                    for request_content_type, content_info in contents.items():
                        default_headers["Content-Type"] = request_content_type
                        content_parameters = {}
                        # of course we do that only if we are dealing with a dictionary-like payload
                        if (request_content_type == "application/json") and (
                            isinstance(content_info.get("schema"), dict)
                        ):
                            if isinstance(
                                content_info.get("schema").get("properties"), dict
                            ):
                                for name, req_param in (
                                    content_info.get("schema").get("properties").items()
                                ):

                                    description = req_param.get("description")
                                    default = req_param.get("default")
                                    par_type = req_param.get("type")
                                    docstring = (
                                        docstring
                                        + str(name)
                                        + ":"
                                        + str(par_type)
                                        + " "
                                        + "default = "
                                        + str(default)
                                        + "\n\t"
                                        + str(description)
                                        + "\n"
                                    )
                                    content_parameters[name] = default
                    content_slug = request_content_type.split("/")[-1]
                    # format the name method so that it looks like get_function_json
                    method_name = (
                        f"{method}_{_sanitize(url)}"
                        if len(methods) > 1
                        else _sanitize(url)
                    )
                    method_name = (
                        f"{method_name}_{content_slug}"
                        if len(contents) > 1
                        else method_name
                    )
                    class_methods[method_name] = build_caller_function(
                        url,
                        method,
                        params,
                        route_parameters=path_params,
                        content_parameters=content_parameters,
                        default_headers=default_headers,
                        request_content_type=request_content_type,
                        response_content_type=response_content_type,
                        docstring=docstring,
                    )
            else:
                # let's build a method with no content parameters then
                method_name = (
                    f"{method}_{_sanitize(url)}" if len(methods) > 1 else _sanitize(url)
                )
                class_methods[method_name] = build_caller_function(
                    url,
                    method,
                    params,
                    path_params,
                    content_parameters,
                    default_headers,
                    request_content_type,
                    response_content_type,
                    docstring,
                )
    # now we have the methods in a dictionary
    # we can build the access object as a new dedicated class
    return type(
        resource_name, (OpenAPI3DataAccess,), {"servers": servers, **class_methods}
    )
