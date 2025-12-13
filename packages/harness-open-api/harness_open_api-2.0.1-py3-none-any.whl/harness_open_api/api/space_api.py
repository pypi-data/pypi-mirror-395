# coding: utf-8

"""
    Harness NextGen Software Delivery Platform API Reference

    The Harness Software Delivery Platform uses OpenAPI Specification v3.0. Harness constantly improves these APIs. Please be aware that some improvements could cause breaking changes. # Introduction     The Harness API allows you to integrate and use all the services and modules we provide on the Harness Platform. If you use client-side SDKs, Harness functionality can be integrated with your client-side automation, helping you reduce manual efforts and deploy code faster.    For more information about how Harness works, read our [documentation](https://developer.harness.io/docs/getting-started) or visit the [Harness Developer Hub](https://developer.harness.io/).  ## How it works    The Harness API is a RESTful API that uses standard HTTP verbs. You can send requests in JSON, YAML, or form-data format. The format of the response matches the format of your request. You must send a single request at a time and ensure that you include your authentication key. For more information about this, go to [Authentication](#section/Introduction/Authentication).  ## Get started    Before you start integrating, get to know our API better by reading the following topics:    * [Harness key concepts](https://developer.harness.io/docs/getting-started/learn-harness-key-concepts/)   * [Authentication](#section/Introduction/Authentication)   * [Requests and responses](#section/Introduction/Requests-and-Responses)   * [Common Parameters](#section/Introduction/Common-Parameters-Beta)   * [Status Codes](#section/Introduction/Status-Codes)   * [Errors](#tag/Error-Response)   * [Versioning](#section/Introduction/Versioning-Beta)   * [Pagination](/#section/Introduction/Pagination-Beta)    The methods you need to integrate with depend on the functionality you want to use. Work with  your Harness Solutions Engineer to determine which methods you need.  ## Authentication  To authenticate with the Harness API, you need to:   1. Generate an API token on the Harness Platform.   2. Send the API token you generate in the `x-api-key` header in each request.  ### Generate an API token  To generate an API token, complete the following steps:   1. Go to the [Harness Platform](https://app.harness.io/).   2. On the left-hand navigation, click **My Profile**.   3. Click **+API Key**, enter a name for your key and then click **Save**.   4. Within the API Key tile, click **+Token**.   5. Enter a name for your token and click **Generate Token**. **Important**: Make sure to save your token securely. Harness does not store the API token for future reference, so make sure to save your token securely before you leave the page.  ### Send the API token in your requests  Send the token you created in the Harness Platform in the x-api-key header. For example:   `x-api-key: YOUR_API_KEY_HERE`  ## Requests and Responses    The structure for each request and response is outlined in the API documentation. We have examples in JSON and YAML for every request and response. You can use our online editor to test the examples.  ## Common Parameters [Beta]  | Field Name | Type    | Default | Description    | |------------|---------|---------|----------------| | identifier | string  | none    | URL-friendly version of the name, used to identify a resource within it's scope and so needs to be unique within the scope.                                                                                                            | | name       | string  | none    | Human-friendly name for the resource.                                                                                       | | org        | string  | none    | Limit to provided org identifiers.                                                                                                                     | | project    | string  | none    | Limit to provided project identifiers.                                                                                                                 | | description| string  | none    | More information about the specific resource.                                                                                    | | tags       | map[string]string  | none    | List of labels applied to the resource.                                                                                                                         | | order      | string  | desc    | Order to use when sorting the specified fields. Type: enum(asc,desc).                                                                                                                                     | | sort       | string  | none    | Fields on which to sort. Note: Specify the fields that you want to use for sorting. When doing so, consider the operational overhead of sorting fields. | | limit      | int     | 30      | Pagination: Number of items to return.                                                                                                                 | | page       | int     | 1       | Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page.                  | | created    | int64   | none    | Unix timestamp that shows when the resource was created (in milliseconds).                                                               | | updated    | int64   | none    | Unix timestamp that shows when the resource was last edited (in milliseconds).                                                           |   ## Status Codes    Harness uses conventional HTTP status codes to indicate the status of an API request.    Generally, 2xx responses are reserved for success and 4xx status codes are reserved for failures. A 5xx response code indicates an error on the Harness server.    | Error Code  | Description |   |-------------|-------------|   | 200         |     OK      |   | 201         |   Created   |   | 202         |   Accepted  |   | 204         |  No Content |   | 400         | Bad Request |   | 401         | Unauthorized |   | 403         | Forbidden |   | 412         | Precondition Failed |   | 415         | Unsupported Media Type |   | 500         | Server Error |    To view our error response structures, go [here](#tag/Error-Response).  ## Versioning [Beta]  ### Harness Version   The current version of our Beta APIs is yet to be announced. The version number will use the date-header format and will be valid only for our Beta APIs.  ### Generation   All our beta APIs are versioned as a Generation, and this version is included in the path to every API resource. For example, v1 beta APIs begin with `app.harness.io/v1/`, where v1 is the API Generation.    The version number represents the core API and does not change frequently. The version number changes only if there is a significant departure from the basic underpinnings of the existing API. For example, when Harness performs a system-wide refactoring of core concepts or resources.  ## Pagination [Beta]  We use pagination to place limits on the number of responses associated with list endpoints. Pagination is achieved by the use of limit query parameters. The limit defaults to 30. Its maximum value is 100.  Following are the pagination headers supported in the response bodies of paginated APIs:   1. X-Total-Elements : Indicates the total number of entries in a paginated response.   2. X-Page-Number : Indicates the page number currently returned for a paginated response.   3. X-Page-Size : Indicates the number of entries per page for a paginated response.  For example:    ``` X-Total-Elements : 30 X-Page-Number : 0 X-Page-Size : 10   ```   # noqa: E501

    OpenAPI spec version: 1.0
    Contact: contact@harness.io
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from harness_open_api.api_client import ApiClient


class SpaceApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def find_space_label(self, space_ref, key, **kwargs):  # noqa: E501
        """find_space_label  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_space_label(space_ref, key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: (required)
        :param str key: (required)
        :param bool include_values: The result should include label values.
        :return: RegistryTypesLabelWithValues
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.find_space_label_with_http_info(space_ref, key, **kwargs)  # noqa: E501
        else:
            (data) = self.find_space_label_with_http_info(space_ref, key, **kwargs)  # noqa: E501
            return data

    def find_space_label_with_http_info(self, space_ref, key, **kwargs):  # noqa: E501
        """find_space_label  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_space_label_with_http_info(space_ref, key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: (required)
        :param str key: (required)
        :param bool include_values: The result should include label values.
        :return: RegistryTypesLabelWithValues
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['space_ref', 'key', 'include_values']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method find_space_label" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'space_ref' is set
        if ('space_ref' not in params or
                params['space_ref'] is None):
            raise ValueError("Missing the required parameter `space_ref` when calling `find_space_label`")  # noqa: E501
        # verify the required parameter 'key' is set
        if ('key' not in params or
                params['key'] is None):
            raise ValueError("Missing the required parameter `key` when calling `find_space_label`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'space_ref' in params:
            path_params['space_ref'] = params['space_ref']  # noqa: E501
        if 'key' in params:
            path_params['key'] = params['key']  # noqa: E501

        query_params = []
        if 'include_values' in params:
            query_params.append(('include_values', params['include_values']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/har/api/v1/spaces/{space_ref}/labels/{key}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RegistryTypesLabelWithValues',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def registrydefine_space_label(self, space_ref, **kwargs):  # noqa: E501
        """registrydefine_space_label  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.registrydefine_space_label(space_ref, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: (required)
        :param SpaceRefLabelsBody1 body:
        :return: RegistryTypesLabel
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.registrydefine_space_label_with_http_info(space_ref, **kwargs)  # noqa: E501
        else:
            (data) = self.registrydefine_space_label_with_http_info(space_ref, **kwargs)  # noqa: E501
            return data

    def registrydefine_space_label_with_http_info(self, space_ref, **kwargs):  # noqa: E501
        """registrydefine_space_label  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.registrydefine_space_label_with_http_info(space_ref, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: (required)
        :param SpaceRefLabelsBody1 body:
        :return: RegistryTypesLabel
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['space_ref', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method registrydefine_space_label" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'space_ref' is set
        if ('space_ref' not in params or
                params['space_ref'] is None):
            raise ValueError("Missing the required parameter `space_ref` when calling `registrydefine_space_label`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'space_ref' in params:
            path_params['space_ref'] = params['space_ref']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/har/api/v1/spaces/{space_ref}/labels', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RegistryTypesLabel',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def registrydefine_space_label_value(self, space_ref, key, **kwargs):  # noqa: E501
        """registrydefine_space_label_value  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.registrydefine_space_label_value(space_ref, key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: (required)
        :param str key: (required)
        :param KeyValuesBody2 body:
        :return: TypesLabelValue
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.registrydefine_space_label_value_with_http_info(space_ref, key, **kwargs)  # noqa: E501
        else:
            (data) = self.registrydefine_space_label_value_with_http_info(space_ref, key, **kwargs)  # noqa: E501
            return data

    def registrydefine_space_label_value_with_http_info(self, space_ref, key, **kwargs):  # noqa: E501
        """registrydefine_space_label_value  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.registrydefine_space_label_value_with_http_info(space_ref, key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: (required)
        :param str key: (required)
        :param KeyValuesBody2 body:
        :return: TypesLabelValue
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['space_ref', 'key', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method registrydefine_space_label_value" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'space_ref' is set
        if ('space_ref' not in params or
                params['space_ref'] is None):
            raise ValueError("Missing the required parameter `space_ref` when calling `registrydefine_space_label_value`")  # noqa: E501
        # verify the required parameter 'key' is set
        if ('key' not in params or
                params['key'] is None):
            raise ValueError("Missing the required parameter `key` when calling `registrydefine_space_label_value`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'space_ref' in params:
            path_params['space_ref'] = params['space_ref']  # noqa: E501
        if 'key' in params:
            path_params['key'] = params['key']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/har/api/v1/spaces/{space_ref}/labels/{key}/values', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesLabelValue',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def registrydelete_space_label(self, space_ref, key, **kwargs):  # noqa: E501
        """registrydelete_space_label  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.registrydelete_space_label(space_ref, key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: (required)
        :param str key: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.registrydelete_space_label_with_http_info(space_ref, key, **kwargs)  # noqa: E501
        else:
            (data) = self.registrydelete_space_label_with_http_info(space_ref, key, **kwargs)  # noqa: E501
            return data

    def registrydelete_space_label_with_http_info(self, space_ref, key, **kwargs):  # noqa: E501
        """registrydelete_space_label  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.registrydelete_space_label_with_http_info(space_ref, key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: (required)
        :param str key: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['space_ref', 'key']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method registrydelete_space_label" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'space_ref' is set
        if ('space_ref' not in params or
                params['space_ref'] is None):
            raise ValueError("Missing the required parameter `space_ref` when calling `registrydelete_space_label`")  # noqa: E501
        # verify the required parameter 'key' is set
        if ('key' not in params or
                params['key'] is None):
            raise ValueError("Missing the required parameter `key` when calling `registrydelete_space_label`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'space_ref' in params:
            path_params['space_ref'] = params['space_ref']  # noqa: E501
        if 'key' in params:
            path_params['key'] = params['key']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/har/api/v1/spaces/{space_ref}/labels/{key}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def registrydelete_space_label_value(self, space_ref, key, value, **kwargs):  # noqa: E501
        """registrydelete_space_label_value  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.registrydelete_space_label_value(space_ref, key, value, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: (required)
        :param str key: (required)
        :param str value: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.registrydelete_space_label_value_with_http_info(space_ref, key, value, **kwargs)  # noqa: E501
        else:
            (data) = self.registrydelete_space_label_value_with_http_info(space_ref, key, value, **kwargs)  # noqa: E501
            return data

    def registrydelete_space_label_value_with_http_info(self, space_ref, key, value, **kwargs):  # noqa: E501
        """registrydelete_space_label_value  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.registrydelete_space_label_value_with_http_info(space_ref, key, value, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: (required)
        :param str key: (required)
        :param str value: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['space_ref', 'key', 'value']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method registrydelete_space_label_value" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'space_ref' is set
        if ('space_ref' not in params or
                params['space_ref'] is None):
            raise ValueError("Missing the required parameter `space_ref` when calling `registrydelete_space_label_value`")  # noqa: E501
        # verify the required parameter 'key' is set
        if ('key' not in params or
                params['key'] is None):
            raise ValueError("Missing the required parameter `key` when calling `registrydelete_space_label_value`")  # noqa: E501
        # verify the required parameter 'value' is set
        if ('value' not in params or
                params['value'] is None):
            raise ValueError("Missing the required parameter `value` when calling `registrydelete_space_label_value`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'space_ref' in params:
            path_params['space_ref'] = params['space_ref']  # noqa: E501
        if 'key' in params:
            path_params['key'] = params['key']  # noqa: E501
        if 'value' in params:
            path_params['value'] = params['value']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/har/api/v1/spaces/{space_ref}/labels/{key}/values/{value}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def registrylist_space_label_values(self, space_ref, key, **kwargs):  # noqa: E501
        """registrylist_space_label_values  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.registrylist_space_label_values(space_ref, key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: (required)
        :param str key: (required)
        :return: list[TypesLabelValue]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.registrylist_space_label_values_with_http_info(space_ref, key, **kwargs)  # noqa: E501
        else:
            (data) = self.registrylist_space_label_values_with_http_info(space_ref, key, **kwargs)  # noqa: E501
            return data

    def registrylist_space_label_values_with_http_info(self, space_ref, key, **kwargs):  # noqa: E501
        """registrylist_space_label_values  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.registrylist_space_label_values_with_http_info(space_ref, key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: (required)
        :param str key: (required)
        :return: list[TypesLabelValue]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['space_ref', 'key']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method registrylist_space_label_values" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'space_ref' is set
        if ('space_ref' not in params or
                params['space_ref'] is None):
            raise ValueError("Missing the required parameter `space_ref` when calling `registrylist_space_label_values`")  # noqa: E501
        # verify the required parameter 'key' is set
        if ('key' not in params or
                params['key'] is None):
            raise ValueError("Missing the required parameter `key` when calling `registrylist_space_label_values`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'space_ref' in params:
            path_params['space_ref'] = params['space_ref']  # noqa: E501
        if 'key' in params:
            path_params['key'] = params['key']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/har/api/v1/spaces/{space_ref}/labels/{key}/values', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[TypesLabelValue]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def registrylist_space_labels(self, space_ref, **kwargs):  # noqa: E501
        """registrylist_space_labels  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.registrylist_space_labels(space_ref, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: (required)
        :param int page: The page to return.
        :param int limit: The maximum number of results to return.
        :param bool inherited: The result should inherit entities from parent spaces.
        :param str query: The substring which is used to filter the labels by their key.
        :return: list[RegistryTypesLabel]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.registrylist_space_labels_with_http_info(space_ref, **kwargs)  # noqa: E501
        else:
            (data) = self.registrylist_space_labels_with_http_info(space_ref, **kwargs)  # noqa: E501
            return data

    def registrylist_space_labels_with_http_info(self, space_ref, **kwargs):  # noqa: E501
        """registrylist_space_labels  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.registrylist_space_labels_with_http_info(space_ref, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: (required)
        :param int page: The page to return.
        :param int limit: The maximum number of results to return.
        :param bool inherited: The result should inherit entities from parent spaces.
        :param str query: The substring which is used to filter the labels by their key.
        :return: list[RegistryTypesLabel]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['space_ref', 'page', 'limit', 'inherited', 'query']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method registrylist_space_labels" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'space_ref' is set
        if ('space_ref' not in params or
                params['space_ref'] is None):
            raise ValueError("Missing the required parameter `space_ref` when calling `registrylist_space_labels`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'space_ref' in params:
            path_params['space_ref'] = params['space_ref']  # noqa: E501

        query_params = []
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'inherited' in params:
            query_params.append(('inherited', params['inherited']))  # noqa: E501
        if 'query' in params:
            query_params.append(('query', params['query']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/har/api/v1/spaces/{space_ref}/labels', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[RegistryTypesLabel]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def registrysave_space_label(self, space_ref, **kwargs):  # noqa: E501
        """registrysave_space_label  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.registrysave_space_label(space_ref, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: (required)
        :param SpaceRefLabelsBody body:
        :return: RegistryTypesLabelWithValues
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.registrysave_space_label_with_http_info(space_ref, **kwargs)  # noqa: E501
        else:
            (data) = self.registrysave_space_label_with_http_info(space_ref, **kwargs)  # noqa: E501
            return data

    def registrysave_space_label_with_http_info(self, space_ref, **kwargs):  # noqa: E501
        """registrysave_space_label  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.registrysave_space_label_with_http_info(space_ref, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: (required)
        :param SpaceRefLabelsBody body:
        :return: RegistryTypesLabelWithValues
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['space_ref', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method registrysave_space_label" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'space_ref' is set
        if ('space_ref' not in params or
                params['space_ref'] is None):
            raise ValueError("Missing the required parameter `space_ref` when calling `registrysave_space_label`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'space_ref' in params:
            path_params['space_ref'] = params['space_ref']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/har/api/v1/spaces/{space_ref}/labels', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RegistryTypesLabelWithValues',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def registryupdate_space_label(self, space_ref, key, **kwargs):  # noqa: E501
        """registryupdate_space_label  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.registryupdate_space_label(space_ref, key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: (required)
        :param str key: (required)
        :param LabelsKeyBody2 body:
        :return: RegistryTypesLabel
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.registryupdate_space_label_with_http_info(space_ref, key, **kwargs)  # noqa: E501
        else:
            (data) = self.registryupdate_space_label_with_http_info(space_ref, key, **kwargs)  # noqa: E501
            return data

    def registryupdate_space_label_with_http_info(self, space_ref, key, **kwargs):  # noqa: E501
        """registryupdate_space_label  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.registryupdate_space_label_with_http_info(space_ref, key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: (required)
        :param str key: (required)
        :param LabelsKeyBody2 body:
        :return: RegistryTypesLabel
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['space_ref', 'key', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method registryupdate_space_label" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'space_ref' is set
        if ('space_ref' not in params or
                params['space_ref'] is None):
            raise ValueError("Missing the required parameter `space_ref` when calling `registryupdate_space_label`")  # noqa: E501
        # verify the required parameter 'key' is set
        if ('key' not in params or
                params['key'] is None):
            raise ValueError("Missing the required parameter `key` when calling `registryupdate_space_label`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'space_ref' in params:
            path_params['space_ref'] = params['space_ref']  # noqa: E501
        if 'key' in params:
            path_params['key'] = params['key']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/har/api/v1/spaces/{space_ref}/labels/{key}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RegistryTypesLabel',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def registryupdate_space_label_value(self, space_ref, key, value, **kwargs):  # noqa: E501
        """registryupdate_space_label_value  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.registryupdate_space_label_value(space_ref, key, value, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: (required)
        :param str key: (required)
        :param str value: (required)
        :param ValuesValueBody2 body:
        :return: TypesLabelValue
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.registryupdate_space_label_value_with_http_info(space_ref, key, value, **kwargs)  # noqa: E501
        else:
            (data) = self.registryupdate_space_label_value_with_http_info(space_ref, key, value, **kwargs)  # noqa: E501
            return data

    def registryupdate_space_label_value_with_http_info(self, space_ref, key, value, **kwargs):  # noqa: E501
        """registryupdate_space_label_value  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.registryupdate_space_label_value_with_http_info(space_ref, key, value, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: (required)
        :param str key: (required)
        :param str value: (required)
        :param ValuesValueBody2 body:
        :return: TypesLabelValue
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['space_ref', 'key', 'value', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method registryupdate_space_label_value" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'space_ref' is set
        if ('space_ref' not in params or
                params['space_ref'] is None):
            raise ValueError("Missing the required parameter `space_ref` when calling `registryupdate_space_label_value`")  # noqa: E501
        # verify the required parameter 'key' is set
        if ('key' not in params or
                params['key'] is None):
            raise ValueError("Missing the required parameter `key` when calling `registryupdate_space_label_value`")  # noqa: E501
        # verify the required parameter 'value' is set
        if ('value' not in params or
                params['value'] is None):
            raise ValueError("Missing the required parameter `value` when calling `registryupdate_space_label_value`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'space_ref' in params:
            path_params['space_ref'] = params['space_ref']  # noqa: E501
        if 'key' in params:
            path_params['key'] = params['key']  # noqa: E501
        if 'value' in params:
            path_params['value'] = params['value']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/har/api/v1/spaces/{space_ref}/labels/{key}/values/{value}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesLabelValue',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
