from io import StringIO
import io
import json
import requests
import logging
from retry import retry
import pandas as pd
from pandas.core.common import standardize_mapping
from pandas.core.dtypes.cast import maybe_box_native # this is because of Scalars in dataframes...

# list of file-like objects for parsing purposes
FILE_LIKE_OBJECTS = [io.TextIOBase, io.BufferedIOBase, io.RawIOBase, io.IOBase]

def _parse_response_format(response:requests.Response, content_type:str):
    '''Helper function that tries to parse exacly one MIME type'''
    #print('Content Type is ' + content_type)
    if content_type in ['json', 'application/json']:
            return response.json()
    elif content_type.startswith('text'):
        if content_type in ['text/csv', 'csv']:
            # special case: we are receiving a CSV string!
            try:
                return pd.read_csv(StringIO(response.text))
            except:
                logging.warning('Not able to parse CSV content, returning text data')
                return response.text
        else: 
                return response.text
    else:
        logging.warning('Unknown content type, returning bytes data')
        return response.content

def parse_response(response:requests.Response, expected_content_type:str|list = 'json'):
    '''
    Tries its best to parse a requests response object into a 
    manageable data structure
    
    Parameters
    ----------
    response: requests.Response
        whatever the call to the Web service returned
    
    expected_content_type: str or list
        the expected content type, it should be a MIME type like 'application/json'
        or 'text/csv'. It's the type the method will try to parse if no explicit
        indication is included in the response headers. You can also pass down a list
        of MIME types and the function will try to parse find which one works. 
        Default value: json
    '''
    # if content type is explicitly declared, we'll try to use it
    declared_content_type = response.headers.get('content-type')
    if declared_content_type:
        content_type = declared_content_type
    else:
        # otherwise we'll use the expected one passed as a parameter
        content_type = expected_content_type
    # if we have a list of possible formats, we'll try to parse them
    # all until we find the one that actually matches the data
    if isinstance(content_type, list):
        for c_t in content_type:
            try:
                return _parse_response_format(response, c_t)
            except:
                # wrong format, let's fail silently then
                logging.warning(f'Response is not a valid {c_t}')
    else:            
        try:
            return _parse_response_format(response, content_type)
        except Exception as e:
            #print(e)
            logging.warning('Not able to parse response content, returning bytes data')
            try:
                return response.content
            except:
                raise IOError('Unable to read server response')

def prepare_payload(payload, content_type='application/json'):
    '''
    Tries its best to prepare an object to be sent as request 
    payload
    
    Parameters
    ----------
    payload: obj 
        whatever object you intend to send
    
    content_type: str
        the expected content type, it should be a MIME type like 'application/json'
        or 'text/csv'. It's the type the method will try to encode. Default value: json
    '''
    if payload is None:
        return None
    # serialize payload in an appropriate way
    if content_type in ['application/json', 'json']:
        # if the user already converted the payload to a JSON string *somehow*
        # we'll just pass that down, otherwise, we'll floss it with the JSON DUMPS
        # method
        if isinstance(payload, str):
            return payload
        return json.dumps(payload)
    elif content_type.startswith('text'):
        return str(payload)
    elif content_type in ['application/octet-stream', 'stream', 'binary']:
        # is the object a string? And if yes, is it a path?
        if isinstance(payload, str):
            # three options: it's a path or  it's already a binary encoded octet stream. Or the user
            # is an asshole and passed down something nonsensical.
            # let's try to open the string as if were a file
            try:
                with open(payload, 'rb') as f:
                    return f.read()
            except:
                # if anything goes badly, then probably the user already
                # dumped that to a bytes string and we'll just send that
                return payload
        # is payload a file-like object?
        if any([isinstance(payload, t) for t in FILE_LIKE_OBJECTS]):
            return payload.read()
    # if everything fails, we just send out an empty object.
    # yes, so it'll fail silently. Is it evil? Indeed... but
    # we revel in reseachers' tears.
    return None

def call_restful_api(url, data:object=None, params:dict = {}, path_params ={}, headers:dict = {'Content-Type': 'application/json'}, files = None,
                     method:str='GET', additional_headers:dict= {}, payload_content_type:str ='application/json',
                     expected_response_content_type:str = 'application/json'):
    '''
    Calls a RESTful API
    Parameters
    ----------
    
    url: str 
        the URL of the API method to invoke, it can include parameters in curly braces, like
        /function/{par1}/{par2}
    data: object 
        an object to be sent as payload
    params:dict    
        a dictionary of parameters to be sent as query parameters
    path_params:dict
        if your URL has parameters in it, put the values in this dictionary
    headers:dict
        the key-value pairs to be sent as headers
    files: object
        an object to be sent as a multipart attachement
    method:str, default:'GET'
        the REST method to invoke
    additional_headers:dict, default:{}
        more header parameters. This dictionary will be merged with the *headers* one.
        what's the use of this? Well, let's say that some methods in this package really
        need it becasue of closures and decorators, but if you are not into such black
        magic, probably you'll never need to use this parameter.
    payload_content_type:str, default:'application/json'
        the type of content you are going to send, if any. It's how the payload will be serialized.
    expected_response_content_type:str default:'application/json'
        the type of content you expect to find in the service response. The method will
        try to parse this content type if no content-type header is in the service's response, 
        otherwise the content-type in the response will be considered. So, it's a monkey-patch
        to deal with services written by idiots.

        Returns:
            service response (str or dictionary): Web service response, either a dictionary or a string.
    
    '''
    # prepare the URL
    if len(path_params)>0:
        url = url.format(**path_params)
    # prepare the payload
    if method in ['post', 'POST', 'put', 'PUT']:
        payload = prepare_payload(data, payload_content_type)
    else:
        payload = None
    # assemble the headers
    if additional_headers is not None:
        # add the extra headers provided as a dictionary
        headers = {**headers, **additional_headers}
    response = None
    # invoke the Web Service
    if method in ['post', 'POST']:
        response = requests.post(url, params = params, data=payload, headers=headers, files = files)
    elif method in ['put', 'PUT']:
        response = requests.put(url, params = params, data=payload, headers=headers, files=files)
    elif method in ['delete', 'DELETE']:
        response = requests.delete(url, params = params, data=payload, headers=headers)
    else:
        response=requests.get(url, params = params, data=payload, headers=headers, files = files)
    if response.status_code in [200,201,202,203,204,205]: # the 20X status means 'success'
        return parse_response(response, expected_response_content_type)
    else:
        logging.error('Request to '+str(url) + ' failed with code ' + str(response.status_code))
        response.raise_for_status() # Raises an exception for 4xx and 5xx status codes
    return None


def dataframe_records_gen(df):
    '''
	Creates a *generator* object allowing us to read dataframe rows as dictionaries.
	We need to do this because the bult-in to_dic function returns a friggin' list with
	a list comprehension, which is likely to clog your memory if the dataframe is large
	'''
    columns = df.columns.tolist()
    into_c = standardize_mapping(dict)
    for row in df.itertuples(index=False, name=None):
        yield into_c(
            (k, maybe_box_native(v)) for k, v in dict(zip(columns, row)).items()
        )
		
def dataframe_records_gen_fast(df):
    '''
    This is like dataframe_records_gen, but waaaay faster and with a smaller memory footprint, BUT
	it's rather unsafe, as it does not check whether or not row items are Scalars and/or composite objects
	before trying to shove them into the dict. If your df has nothing fancy in it, this should not be a 
	dealbreaker, but if you do have some weird stuff in there, oh boy... You are in for a world of pain'''
    cols = list(df)
    col_arr_map = {col: df[col].astype(object).to_numpy() for col in cols}
    for i in range(len(df)):
        yield {col: col_arr_map[col][i] for col in cols}