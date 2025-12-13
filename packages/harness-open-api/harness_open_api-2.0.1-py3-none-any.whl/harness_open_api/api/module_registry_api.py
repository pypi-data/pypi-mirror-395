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


class ModuleRegistryApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def module_registry_create_module(self, body, harness_account, **kwargs):  # noqa: E501
        """Create module  # noqa: E501

        Create a new module in the module registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_create_module(body, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateModuleRequest body: (required)
        :param str harness_account: account that owns the module (required)
        :return: ModuleRegistryCreateModuleResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.module_registry_create_module_with_http_info(body, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.module_registry_create_module_with_http_info(body, harness_account, **kwargs)  # noqa: E501
            return data

    def module_registry_create_module_with_http_info(self, body, harness_account, **kwargs):  # noqa: E501
        """Create module  # noqa: E501

        Create a new module in the module registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_create_module_with_http_info(body, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateModuleRequest body: (required)
        :param str harness_account: account that owns the module (required)
        :return: ModuleRegistryCreateModuleResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method module_registry_create_module" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `module_registry_create_module`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `module_registry_create_module`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/vnd.goa.error'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/modules', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ModuleRegistryCreateModuleResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def module_registry_create_module_execution(self, body, module_id, **kwargs):  # noqa: E501
        """Create a new module execution  # noqa: E501

        Create a new module execution.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_create_module_execution(body, module_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateModuleExecutionRequest body: (required)
        :param str module_id: The unique identifier for the associated module (required)
        :return: CreateModuleExecutionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.module_registry_create_module_execution_with_http_info(body, module_id, **kwargs)  # noqa: E501
        else:
            (data) = self.module_registry_create_module_execution_with_http_info(body, module_id, **kwargs)  # noqa: E501
            return data

    def module_registry_create_module_execution_with_http_info(self, body, module_id, **kwargs):  # noqa: E501
        """Create a new module execution  # noqa: E501

        Create a new module execution.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_create_module_execution_with_http_info(body, module_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateModuleExecutionRequest body: (required)
        :param str module_id: The unique identifier for the associated module (required)
        :return: CreateModuleExecutionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'module_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method module_registry_create_module_execution" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `module_registry_create_module_execution`")  # noqa: E501
        # verify the required parameter 'module_id' is set
        if ('module_id' not in params or
                params['module_id'] is None):
            raise ValueError("Missing the required parameter `module_id` when calling `module_registry_create_module_execution`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'module_id' in params:
            path_params['moduleId'] = params['module_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/vnd.goa.error'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/modules/{moduleId}/executions', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CreateModuleExecutionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def module_registry_create_testing_pipelines(self, body, harness_account, id, **kwargs):  # noqa: E501
        """Create testing pipeline  # noqa: E501

        Create a new testing pipeline for a given module  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_create_testing_pipelines(body, harness_account, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateTestingPipelineRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str id: module id (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.module_registry_create_testing_pipelines_with_http_info(body, harness_account, id, **kwargs)  # noqa: E501
        else:
            (data) = self.module_registry_create_testing_pipelines_with_http_info(body, harness_account, id, **kwargs)  # noqa: E501
            return data

    def module_registry_create_testing_pipelines_with_http_info(self, body, harness_account, id, **kwargs):  # noqa: E501
        """Create testing pipeline  # noqa: E501

        Create a new testing pipeline for a given module  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_create_testing_pipelines_with_http_info(body, harness_account, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateTestingPipelineRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str id: module id (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account', 'id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method module_registry_create_testing_pipelines" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `module_registry_create_testing_pipelines`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `module_registry_create_testing_pipelines`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `module_registry_create_testing_pipelines`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/vnd.goa.error'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/modules/{id}/pipeline', 'POST',
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

    def module_registry_delete_module(self, id, harness_account, **kwargs):  # noqa: E501
        """Delete module  # noqa: E501

        Delete a module from the module registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_delete_module(id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: id (required)
        :param str harness_account: account name (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.module_registry_delete_module_with_http_info(id, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.module_registry_delete_module_with_http_info(id, harness_account, **kwargs)  # noqa: E501
            return data

    def module_registry_delete_module_with_http_info(self, id, harness_account, **kwargs):  # noqa: E501
        """Delete module  # noqa: E501

        Delete a module from the module registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_delete_module_with_http_info(id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: id (required)
        :param str harness_account: account name (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method module_registry_delete_module" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `module_registry_delete_module`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `module_registry_delete_module`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/vnd.goa.error'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/modules/{id}', 'DELETE',
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

    def module_registry_disable_testing(self, id, harness_account, **kwargs):  # noqa: E501
        """Disable testing  # noqa: E501

        Disable testing for a module  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_disable_testing(id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: module id (required)
        :param str harness_account: account name (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.module_registry_disable_testing_with_http_info(id, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.module_registry_disable_testing_with_http_info(id, harness_account, **kwargs)  # noqa: E501
            return data

    def module_registry_disable_testing_with_http_info(self, id, harness_account, **kwargs):  # noqa: E501
        """Disable testing  # noqa: E501

        Disable testing for a module  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_disable_testing_with_http_info(id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: module id (required)
        :param str harness_account: account name (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method module_registry_disable_testing" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `module_registry_disable_testing`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `module_registry_disable_testing`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/vnd.goa.error'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/modules/{id}/testing', 'DELETE',
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

    def module_registry_download(self, account, name, system, version, **kwargs):  # noqa: E501
        """Download module  # noqa: E501

        Download a module given a specific version  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_download(account, name, system, version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account: account name (required)
        :param str name: module name (required)
        :param str system: system name (required)
        :param str version: version of the module (required)
        :return: DownloadModuleResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.module_registry_download_with_http_info(account, name, system, version, **kwargs)  # noqa: E501
        else:
            (data) = self.module_registry_download_with_http_info(account, name, system, version, **kwargs)  # noqa: E501
            return data

    def module_registry_download_with_http_info(self, account, name, system, version, **kwargs):  # noqa: E501
        """Download module  # noqa: E501

        Download a module given a specific version  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_download_with_http_info(account, name, system, version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account: account name (required)
        :param str name: module name (required)
        :param str system: system name (required)
        :param str version: version of the module (required)
        :return: DownloadModuleResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account', 'name', 'system', 'version']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method module_registry_download" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account' is set
        if ('account' not in params or
                params['account'] is None):
            raise ValueError("Missing the required parameter `account` when calling `module_registry_download`")  # noqa: E501
        # verify the required parameter 'name' is set
        if ('name' not in params or
                params['name'] is None):
            raise ValueError("Missing the required parameter `name` when calling `module_registry_download`")  # noqa: E501
        # verify the required parameter 'system' is set
        if ('system' not in params or
                params['system'] is None):
            raise ValueError("Missing the required parameter `system` when calling `module_registry_download`")  # noqa: E501
        # verify the required parameter 'version' is set
        if ('version' not in params or
                params['version'] is None):
            raise ValueError("Missing the required parameter `version` when calling `module_registry_download`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'account' in params:
            path_params['account'] = params['account']  # noqa: E501
        if 'name' in params:
            path_params['name'] = params['name']  # noqa: E501
        if 'system' in params:
            path_params['system'] = params['system']  # noqa: E501
        if 'version' in params:
            path_params['version'] = params['version']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/vnd.goa.error'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/registry/account/{account}/{name}/{system}/{version}/download', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DownloadModuleResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def module_registry_enable_testing(self, body, harness_account, id, **kwargs):  # noqa: E501
        """Enable testing  # noqa: E501

        Enable testing for a module  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_enable_testing(body, harness_account, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param EnableTestingRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str id: module id (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.module_registry_enable_testing_with_http_info(body, harness_account, id, **kwargs)  # noqa: E501
        else:
            (data) = self.module_registry_enable_testing_with_http_info(body, harness_account, id, **kwargs)  # noqa: E501
            return data

    def module_registry_enable_testing_with_http_info(self, body, harness_account, id, **kwargs):  # noqa: E501
        """Enable testing  # noqa: E501

        Enable testing for a module  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_enable_testing_with_http_info(body, harness_account, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param EnableTestingRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str id: module id (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account', 'id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method module_registry_enable_testing" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `module_registry_enable_testing`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `module_registry_enable_testing`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `module_registry_enable_testing`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/vnd.goa.error'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/modules/{id}/testing', 'POST',
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

    def module_registry_get_module(self, token, account, name, system, version, **kwargs):  # noqa: E501
        """Download module file tarball  # noqa: E501

        Download a module given a specific version  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_get_module(token, account, name, system, version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str token: token for authentication (required)
        :param str account: account name (required)
        :param str name: module name (required)
        :param str system: system name (required)
        :param str version: version of the module (required)
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.module_registry_get_module_with_http_info(token, account, name, system, version, **kwargs)  # noqa: E501
        else:
            (data) = self.module_registry_get_module_with_http_info(token, account, name, system, version, **kwargs)  # noqa: E501
            return data

    def module_registry_get_module_with_http_info(self, token, account, name, system, version, **kwargs):  # noqa: E501
        """Download module file tarball  # noqa: E501

        Download a module given a specific version  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_get_module_with_http_info(token, account, name, system, version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str token: token for authentication (required)
        :param str account: account name (required)
        :param str name: module name (required)
        :param str system: system name (required)
        :param str version: version of the module (required)
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['token', 'account', 'name', 'system', 'version']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method module_registry_get_module" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'token' is set
        if ('token' not in params or
                params['token'] is None):
            raise ValueError("Missing the required parameter `token` when calling `module_registry_get_module`")  # noqa: E501
        # verify the required parameter 'account' is set
        if ('account' not in params or
                params['account'] is None):
            raise ValueError("Missing the required parameter `account` when calling `module_registry_get_module`")  # noqa: E501
        # verify the required parameter 'name' is set
        if ('name' not in params or
                params['name'] is None):
            raise ValueError("Missing the required parameter `name` when calling `module_registry_get_module`")  # noqa: E501
        # verify the required parameter 'system' is set
        if ('system' not in params or
                params['system'] is None):
            raise ValueError("Missing the required parameter `system` when calling `module_registry_get_module`")  # noqa: E501
        # verify the required parameter 'version' is set
        if ('version' not in params or
                params['version'] is None):
            raise ValueError("Missing the required parameter `version` when calling `module_registry_get_module`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'account' in params:
            path_params['account'] = params['account']  # noqa: E501
        if 'name' in params:
            path_params['name'] = params['name']  # noqa: E501
        if 'system' in params:
            path_params['system'] = params['system']  # noqa: E501
        if 'version' in params:
            path_params['version'] = params['version']  # noqa: E501

        query_params = []
        if 'token' in params:
            query_params.append(('token', params['token']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/vnd.goa.error'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/registry/account/{account}/{name}/{system}/{version}/download/file', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='str',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def module_registry_list_connectors(self, harness_account, **kwargs):  # noqa: E501
        """List connectors  # noqa: E501

        List all connectors from the module registry for a specific account  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_list_connectors(harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: account name (required)
        :param str org: organization name
        :param str project: project name
        :return: list[str]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.module_registry_list_connectors_with_http_info(harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.module_registry_list_connectors_with_http_info(harness_account, **kwargs)  # noqa: E501
            return data

    def module_registry_list_connectors_with_http_info(self, harness_account, **kwargs):  # noqa: E501
        """List connectors  # noqa: E501

        List all connectors from the module registry for a specific account  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_list_connectors_with_http_info(harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: account name (required)
        :param str org: organization name
        :param str project: project name
        :return: list[str]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['harness_account', 'org', 'project']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method module_registry_list_connectors" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `module_registry_list_connectors`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'org' in params:
            query_params.append(('org', params['org']))  # noqa: E501
        if 'project' in params:
            query_params.append(('project', params['project']))  # noqa: E501

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/vnd.goa.error'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/modules/connectors', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[str]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def module_registry_list_metadata_by_module(self, version, module_id, harness_account, **kwargs):  # noqa: E501
        """List module metadata  # noqa: E501

        List the module metadata from the module registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_list_metadata_by_module(version, module_id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str version: version of the module (required)
        :param str module_id: module id (required)
        :param str harness_account: account name (required)
        :param str submodule: submodule name
        :return: ListModuleMetadataResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.module_registry_list_metadata_by_module_with_http_info(version, module_id, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.module_registry_list_metadata_by_module_with_http_info(version, module_id, harness_account, **kwargs)  # noqa: E501
            return data

    def module_registry_list_metadata_by_module_with_http_info(self, version, module_id, harness_account, **kwargs):  # noqa: E501
        """List module metadata  # noqa: E501

        List the module metadata from the module registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_list_metadata_by_module_with_http_info(version, module_id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str version: version of the module (required)
        :param str module_id: module id (required)
        :param str harness_account: account name (required)
        :param str submodule: submodule name
        :return: ListModuleMetadataResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['version', 'module_id', 'harness_account', 'submodule']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method module_registry_list_metadata_by_module" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'version' is set
        if ('version' not in params or
                params['version'] is None):
            raise ValueError("Missing the required parameter `version` when calling `module_registry_list_metadata_by_module`")  # noqa: E501
        # verify the required parameter 'module_id' is set
        if ('module_id' not in params or
                params['module_id'] is None):
            raise ValueError("Missing the required parameter `module_id` when calling `module_registry_list_metadata_by_module`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `module_registry_list_metadata_by_module`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'module_id' in params:
            path_params['module_id'] = params['module_id']  # noqa: E501

        query_params = []
        if 'version' in params:
            query_params.append(('version', params['version']))  # noqa: E501
        if 'submodule' in params:
            query_params.append(('submodule', params['submodule']))  # noqa: E501

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/vnd.goa.error'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/modules/{module_id}/metadata', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ListModuleMetadataResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def module_registry_list_module_executions_id(self, module_id, harness_account, **kwargs):  # noqa: E501
        """List executions for a specific module  # noqa: E501

        List all module executions for a module.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_list_module_executions_id(module_id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str module_id: Module identifier (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :param str pipeline_execution_id: Pipeline identifier
        :param list[str] status: Status of the execution
        :param int start_time: Specify the start time for the query
        :param int end_time: Specify the end time limit for the query
        :return: ModuleExecutionResourceCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.module_registry_list_module_executions_id_with_http_info(module_id, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.module_registry_list_module_executions_id_with_http_info(module_id, harness_account, **kwargs)  # noqa: E501
            return data

    def module_registry_list_module_executions_id_with_http_info(self, module_id, harness_account, **kwargs):  # noqa: E501
        """List executions for a specific module  # noqa: E501

        List all module executions for a module.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_list_module_executions_id_with_http_info(module_id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str module_id: Module identifier (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :param str pipeline_execution_id: Pipeline identifier
        :param list[str] status: Status of the execution
        :param int start_time: Specify the start time for the query
        :param int end_time: Specify the end time limit for the query
        :return: ModuleExecutionResourceCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['module_id', 'harness_account', 'limit', 'page', 'pipeline_execution_id', 'status', 'start_time', 'end_time']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method module_registry_list_module_executions_id" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'module_id' is set
        if ('module_id' not in params or
                params['module_id'] is None):
            raise ValueError("Missing the required parameter `module_id` when calling `module_registry_list_module_executions_id`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `module_registry_list_module_executions_id`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'module_id' in params:
            path_params['moduleId'] = params['module_id']  # noqa: E501

        query_params = []
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'pipeline_execution_id' in params:
            query_params.append(('pipeline_execution_id', params['pipeline_execution_id']))  # noqa: E501
        if 'status' in params:
            query_params.append(('status', params['status']))  # noqa: E501
            collection_formats['status'] = 'multi'  # noqa: E501
        if 'start_time' in params:
            query_params.append(('start_time', params['start_time']))  # noqa: E501
        if 'end_time' in params:
            query_params.append(('end_time', params['end_time']))  # noqa: E501

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/vnd.goa.error'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/modules/{moduleId}/executions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ModuleExecutionResourceCollection',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def module_registry_list_module_tags_by_id(self, id, harness_account, **kwargs):  # noqa: E501
        """List module tags  # noqa: E501

        List the module tags from the module registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_list_module_tags_by_id(id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: module id (required)
        :param str harness_account: account name (required)
        :return: list[str]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.module_registry_list_module_tags_by_id_with_http_info(id, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.module_registry_list_module_tags_by_id_with_http_info(id, harness_account, **kwargs)  # noqa: E501
            return data

    def module_registry_list_module_tags_by_id_with_http_info(self, id, harness_account, **kwargs):  # noqa: E501
        """List module tags  # noqa: E501

        List the module tags from the module registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_list_module_tags_by_id_with_http_info(id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: module id (required)
        :param str harness_account: account name (required)
        :return: list[str]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method module_registry_list_module_tags_by_id" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `module_registry_list_module_tags_by_id`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `module_registry_list_module_tags_by_id`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/vnd.goa.error'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/modules/{id}/tags', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[str]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def module_registry_list_modules_by_account(self, harness_account, **kwargs):  # noqa: E501
        """List modules  # noqa: E501

        List all modules from the module registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_list_modules_by_account(harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: account name (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :param str search_term: Filter results by partial name match
        :param str sort: Sort order for results
        :return: ModuleResourceCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.module_registry_list_modules_by_account_with_http_info(harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.module_registry_list_modules_by_account_with_http_info(harness_account, **kwargs)  # noqa: E501
            return data

    def module_registry_list_modules_by_account_with_http_info(self, harness_account, **kwargs):  # noqa: E501
        """List modules  # noqa: E501

        List all modules from the module registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_list_modules_by_account_with_http_info(harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: account name (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :param str search_term: Filter results by partial name match
        :param str sort: Sort order for results
        :return: ModuleResourceCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['harness_account', 'limit', 'page', 'search_term', 'sort']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method module_registry_list_modules_by_account" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `module_registry_list_modules_by_account`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'search_term' in params:
            query_params.append(('searchTerm', params['search_term']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/vnd.goa.error'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/modules', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ModuleResourceCollection',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def module_registry_list_modules_by_id(self, id, harness_account, **kwargs):  # noqa: E501
        """List module by id  # noqa: E501

        List a module from the module registry by ID  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_list_modules_by_id(id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: module id (required)
        :param str harness_account: account name (required)
        :return: ListModuleByIDResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.module_registry_list_modules_by_id_with_http_info(id, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.module_registry_list_modules_by_id_with_http_info(id, harness_account, **kwargs)  # noqa: E501
            return data

    def module_registry_list_modules_by_id_with_http_info(self, id, harness_account, **kwargs):  # noqa: E501
        """List module by id  # noqa: E501

        List a module from the module registry by ID  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_list_modules_by_id_with_http_info(id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: module id (required)
        :param str harness_account: account name (required)
        :return: ListModuleByIDResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method module_registry_list_modules_by_id" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `module_registry_list_modules_by_id`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `module_registry_list_modules_by_id`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/vnd.goa.error'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/modules/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ListModuleByIDResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def module_registry_list_readme_by_id(self, version, module_id, harness_account, **kwargs):  # noqa: E501
        """List module readme  # noqa: E501

        List the module readme from the module registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_list_readme_by_id(version, module_id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str version: version of the module (required)
        :param str module_id: module id (required)
        :param str harness_account: account name (required)
        :param str submodule: submodule name
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.module_registry_list_readme_by_id_with_http_info(version, module_id, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.module_registry_list_readme_by_id_with_http_info(version, module_id, harness_account, **kwargs)  # noqa: E501
            return data

    def module_registry_list_readme_by_id_with_http_info(self, version, module_id, harness_account, **kwargs):  # noqa: E501
        """List module readme  # noqa: E501

        List the module readme from the module registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_list_readme_by_id_with_http_info(version, module_id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str version: version of the module (required)
        :param str module_id: module id (required)
        :param str harness_account: account name (required)
        :param str submodule: submodule name
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['version', 'module_id', 'harness_account', 'submodule']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method module_registry_list_readme_by_id" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'version' is set
        if ('version' not in params or
                params['version'] is None):
            raise ValueError("Missing the required parameter `version` when calling `module_registry_list_readme_by_id`")  # noqa: E501
        # verify the required parameter 'module_id' is set
        if ('module_id' not in params or
                params['module_id'] is None):
            raise ValueError("Missing the required parameter `module_id` when calling `module_registry_list_readme_by_id`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `module_registry_list_readme_by_id`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'module_id' in params:
            path_params['module_id'] = params['module_id']  # noqa: E501

        query_params = []
        if 'version' in params:
            query_params.append(('version', params['version']))  # noqa: E501
        if 'submodule' in params:
            query_params.append(('submodule', params['submodule']))  # noqa: E501

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/vnd.goa.error'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/modules/{module_id}/readme', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='str',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def module_registry_list_versions(self, account, name, system, **kwargs):  # noqa: E501
        """List module versions  # noqa: E501

        list-module-versions returns an array of versions for a given module  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_list_versions(account, name, system, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account: account name (required)
        :param str name: module name (required)
        :param str system: system name (required)
        :return: ListModuleVersionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.module_registry_list_versions_with_http_info(account, name, system, **kwargs)  # noqa: E501
        else:
            (data) = self.module_registry_list_versions_with_http_info(account, name, system, **kwargs)  # noqa: E501
            return data

    def module_registry_list_versions_with_http_info(self, account, name, system, **kwargs):  # noqa: E501
        """List module versions  # noqa: E501

        list-module-versions returns an array of versions for a given module  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_list_versions_with_http_info(account, name, system, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account: account name (required)
        :param str name: module name (required)
        :param str system: system name (required)
        :return: ListModuleVersionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account', 'name', 'system']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method module_registry_list_versions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account' is set
        if ('account' not in params or
                params['account'] is None):
            raise ValueError("Missing the required parameter `account` when calling `module_registry_list_versions`")  # noqa: E501
        # verify the required parameter 'name' is set
        if ('name' not in params or
                params['name'] is None):
            raise ValueError("Missing the required parameter `name` when calling `module_registry_list_versions`")  # noqa: E501
        # verify the required parameter 'system' is set
        if ('system' not in params or
                params['system'] is None):
            raise ValueError("Missing the required parameter `system` when calling `module_registry_list_versions`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'account' in params:
            path_params['account'] = params['account']  # noqa: E501
        if 'name' in params:
            path_params['name'] = params['name']  # noqa: E501
        if 'system' in params:
            path_params['system'] = params['system']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/vnd.goa.error'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/registry/account/{account}/{name}/{system}/versions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ListModuleVersionsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def module_registry_module_parsed_data(self, body, harness_account, name, system, version, **kwargs):  # noqa: E501
        """Create module data  # noqa: E501

        Create a new module in the module registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_module_parsed_data(body, harness_account, name, system, version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateModuleDataRequest body: (required)
        :param str harness_account: account name (required)
        :param str name: module name (required)
        :param str system: system name (required)
        :param str version: version of the module (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.module_registry_module_parsed_data_with_http_info(body, harness_account, name, system, version, **kwargs)  # noqa: E501
        else:
            (data) = self.module_registry_module_parsed_data_with_http_info(body, harness_account, name, system, version, **kwargs)  # noqa: E501
            return data

    def module_registry_module_parsed_data_with_http_info(self, body, harness_account, name, system, version, **kwargs):  # noqa: E501
        """Create module data  # noqa: E501

        Create a new module in the module registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_module_parsed_data_with_http_info(body, harness_account, name, system, version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateModuleDataRequest body: (required)
        :param str harness_account: account name (required)
        :param str name: module name (required)
        :param str system: system name (required)
        :param str version: version of the module (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account', 'name', 'system', 'version']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method module_registry_module_parsed_data" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `module_registry_module_parsed_data`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `module_registry_module_parsed_data`")  # noqa: E501
        # verify the required parameter 'name' is set
        if ('name' not in params or
                params['name'] is None):
            raise ValueError("Missing the required parameter `name` when calling `module_registry_module_parsed_data`")  # noqa: E501
        # verify the required parameter 'system' is set
        if ('system' not in params or
                params['system'] is None):
            raise ValueError("Missing the required parameter `system` when calling `module_registry_module_parsed_data`")  # noqa: E501
        # verify the required parameter 'version' is set
        if ('version' not in params or
                params['version'] is None):
            raise ValueError("Missing the required parameter `version` when calling `module_registry_module_parsed_data`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'name' in params:
            path_params['name'] = params['name']  # noqa: E501
        if 'system' in params:
            path_params['system'] = params['system']  # noqa: E501
        if 'version' in params:
            path_params['version'] = params['version']  # noqa: E501

        query_params = []

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/vnd.goa.error'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/modules/{name}/{system}/{version}/metadata', 'POST',
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

    def module_registry_post_module_artifact(self, name, system, version, harness_account, content_disposition, **kwargs):  # noqa: E501
        """Upload module artifact files  # noqa: E501

        Upload module artifact to the module registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_post_module_artifact(name, system, version, harness_account, content_disposition, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name: Module artifact name (required)
        :param str system: Module artifact system (required)
        :param str version: version of the module (required)
        :param str harness_account: Account ID (required)
        :param str content_disposition: Content-Disposition header (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.module_registry_post_module_artifact_with_http_info(name, system, version, harness_account, content_disposition, **kwargs)  # noqa: E501
        else:
            (data) = self.module_registry_post_module_artifact_with_http_info(name, system, version, harness_account, content_disposition, **kwargs)  # noqa: E501
            return data

    def module_registry_post_module_artifact_with_http_info(self, name, system, version, harness_account, content_disposition, **kwargs):  # noqa: E501
        """Upload module artifact files  # noqa: E501

        Upload module artifact to the module registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_post_module_artifact_with_http_info(name, system, version, harness_account, content_disposition, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name: Module artifact name (required)
        :param str system: Module artifact system (required)
        :param str version: version of the module (required)
        :param str harness_account: Account ID (required)
        :param str content_disposition: Content-Disposition header (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['name', 'system', 'version', 'harness_account', 'content_disposition']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method module_registry_post_module_artifact" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if ('name' not in params or
                params['name'] is None):
            raise ValueError("Missing the required parameter `name` when calling `module_registry_post_module_artifact`")  # noqa: E501
        # verify the required parameter 'system' is set
        if ('system' not in params or
                params['system'] is None):
            raise ValueError("Missing the required parameter `system` when calling `module_registry_post_module_artifact`")  # noqa: E501
        # verify the required parameter 'version' is set
        if ('version' not in params or
                params['version'] is None):
            raise ValueError("Missing the required parameter `version` when calling `module_registry_post_module_artifact`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `module_registry_post_module_artifact`")  # noqa: E501
        # verify the required parameter 'content_disposition' is set
        if ('content_disposition' not in params or
                params['content_disposition'] is None):
            raise ValueError("Missing the required parameter `content_disposition` when calling `module_registry_post_module_artifact`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'name' in params:
            path_params['name'] = params['name']  # noqa: E501
        if 'system' in params:
            path_params['system'] = params['system']  # noqa: E501
        if 'version' in params:
            path_params['version'] = params['version']  # noqa: E501

        query_params = []

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501
        if 'content_disposition' in params:
            header_params['Content-Disposition'] = params['content_disposition']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/vnd.goa.error'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/modules/{name}/{system}/{version}/upload', 'POST',
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

    def module_registry_post_module_readme(self, name, system, version, harness_account, **kwargs):  # noqa: E501
        """Create module readme  # noqa: E501

        Endpoint to push the Readme for a given module  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_post_module_readme(name, system, version, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name: module name (required)
        :param str system: system name (required)
        :param str version: version of the module (required)
        :param str harness_account: account name (required)
        :param str submodule_name: submodule name
        :param int content_length: Size in bytes of the readme
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.module_registry_post_module_readme_with_http_info(name, system, version, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.module_registry_post_module_readme_with_http_info(name, system, version, harness_account, **kwargs)  # noqa: E501
            return data

    def module_registry_post_module_readme_with_http_info(self, name, system, version, harness_account, **kwargs):  # noqa: E501
        """Create module readme  # noqa: E501

        Endpoint to push the Readme for a given module  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_post_module_readme_with_http_info(name, system, version, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name: module name (required)
        :param str system: system name (required)
        :param str version: version of the module (required)
        :param str harness_account: account name (required)
        :param str submodule_name: submodule name
        :param int content_length: Size in bytes of the readme
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['name', 'system', 'version', 'harness_account', 'submodule_name', 'content_length']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method module_registry_post_module_readme" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if ('name' not in params or
                params['name'] is None):
            raise ValueError("Missing the required parameter `name` when calling `module_registry_post_module_readme`")  # noqa: E501
        # verify the required parameter 'system' is set
        if ('system' not in params or
                params['system'] is None):
            raise ValueError("Missing the required parameter `system` when calling `module_registry_post_module_readme`")  # noqa: E501
        # verify the required parameter 'version' is set
        if ('version' not in params or
                params['version'] is None):
            raise ValueError("Missing the required parameter `version` when calling `module_registry_post_module_readme`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `module_registry_post_module_readme`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'name' in params:
            path_params['name'] = params['name']  # noqa: E501
        if 'system' in params:
            path_params['system'] = params['system']  # noqa: E501
        if 'version' in params:
            path_params['version'] = params['version']  # noqa: E501

        query_params = []
        if 'submodule_name' in params:
            query_params.append(('submoduleName', params['submodule_name']))  # noqa: E501

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501
        if 'content_length' in params:
            header_params['Content-Length'] = params['content_length']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/vnd.goa.error'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/modules/{name}/{system}/{version}/readme', 'POST',
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

    def module_registry_post_module_tags(self, body, harness_account, name, system, **kwargs):  # noqa: E501
        """Create module tags  # noqa: E501

        List all tags for a given module  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_post_module_tags(body, harness_account, name, system, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateModuleTagsRequest body: (required)
        :param str harness_account: account that owns the module (required)
        :param str name: module name (required)
        :param str system: system name (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.module_registry_post_module_tags_with_http_info(body, harness_account, name, system, **kwargs)  # noqa: E501
        else:
            (data) = self.module_registry_post_module_tags_with_http_info(body, harness_account, name, system, **kwargs)  # noqa: E501
            return data

    def module_registry_post_module_tags_with_http_info(self, body, harness_account, name, system, **kwargs):  # noqa: E501
        """Create module tags  # noqa: E501

        List all tags for a given module  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_post_module_tags_with_http_info(body, harness_account, name, system, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateModuleTagsRequest body: (required)
        :param str harness_account: account that owns the module (required)
        :param str name: module name (required)
        :param str system: system name (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account', 'name', 'system']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method module_registry_post_module_tags" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `module_registry_post_module_tags`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `module_registry_post_module_tags`")  # noqa: E501
        # verify the required parameter 'name' is set
        if ('name' not in params or
                params['name'] is None):
            raise ValueError("Missing the required parameter `name` when calling `module_registry_post_module_tags`")  # noqa: E501
        # verify the required parameter 'system' is set
        if ('system' not in params or
                params['system'] is None):
            raise ValueError("Missing the required parameter `system` when calling `module_registry_post_module_tags`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'name' in params:
            path_params['name'] = params['name']  # noqa: E501
        if 'system' in params:
            path_params['system'] = params['system']  # noqa: E501

        query_params = []

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/vnd.goa.error'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/modules/{name}/{system}/tags', 'POST',
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

    def module_registry_send_module_event(self, body, module_id, **kwargs):  # noqa: E501
        """Send an event related with a module execution  # noqa: E501

        Send an event related with a module execution  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_send_module_event(body, module_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param SendModuleEventRequest body: (required)
        :param str module_id: module id associated with this event (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.module_registry_send_module_event_with_http_info(body, module_id, **kwargs)  # noqa: E501
        else:
            (data) = self.module_registry_send_module_event_with_http_info(body, module_id, **kwargs)  # noqa: E501
            return data

    def module_registry_send_module_event_with_http_info(self, body, module_id, **kwargs):  # noqa: E501
        """Send an event related with a module execution  # noqa: E501

        Send an event related with a module execution  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_send_module_event_with_http_info(body, module_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param SendModuleEventRequest body: (required)
        :param str module_id: module id associated with this event (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'module_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method module_registry_send_module_event" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `module_registry_send_module_event`")  # noqa: E501
        # verify the required parameter 'module_id' is set
        if ('module_id' not in params or
                params['module_id'] is None):
            raise ValueError("Missing the required parameter `module_id` when calling `module_registry_send_module_event`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'module_id' in params:
            path_params['moduleId'] = params['module_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/vnd.goa.error'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/modules/{moduleId}/events', 'POST',
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

    def module_registry_sync_module_metadata(self, id, harness_account, **kwargs):  # noqa: E501
        """Sync module metadata  # noqa: E501

        Sync the module metadata from the module registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_sync_module_metadata(id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: id (required)
        :param str harness_account: account name (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.module_registry_sync_module_metadata_with_http_info(id, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.module_registry_sync_module_metadata_with_http_info(id, harness_account, **kwargs)  # noqa: E501
            return data

    def module_registry_sync_module_metadata_with_http_info(self, id, harness_account, **kwargs):  # noqa: E501
        """Sync module metadata  # noqa: E501

        Sync the module metadata from the module registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_sync_module_metadata_with_http_info(id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: id (required)
        :param str harness_account: account name (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method module_registry_sync_module_metadata" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `module_registry_sync_module_metadata`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `module_registry_sync_module_metadata`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/vnd.goa.error'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/modules/{id}/sync', 'POST',
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

    def module_registry_update_module(self, body, harness_account, id, **kwargs):  # noqa: E501
        """Update module  # noqa: E501

        Update a module in the module registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_update_module(body, harness_account, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateModuleRequest body: (required)
        :param str harness_account: account that owns the module (required)
        :param str id: module id (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.module_registry_update_module_with_http_info(body, harness_account, id, **kwargs)  # noqa: E501
        else:
            (data) = self.module_registry_update_module_with_http_info(body, harness_account, id, **kwargs)  # noqa: E501
            return data

    def module_registry_update_module_with_http_info(self, body, harness_account, id, **kwargs):  # noqa: E501
        """Update module  # noqa: E501

        Update a module in the module registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_update_module_with_http_info(body, harness_account, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateModuleRequest body: (required)
        :param str harness_account: account that owns the module (required)
        :param str id: module id (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account', 'id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method module_registry_update_module" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `module_registry_update_module`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `module_registry_update_module`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `module_registry_update_module`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/vnd.goa.error'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/modules/{id}', 'PUT',
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

    def module_registry_update_module_testing(self, body, harness_account, id, **kwargs):  # noqa: E501
        """Update module testing  # noqa: E501

        Update module testing metadata  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_update_module_testing(body, harness_account, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateTestingRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str id: module id (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.module_registry_update_module_testing_with_http_info(body, harness_account, id, **kwargs)  # noqa: E501
        else:
            (data) = self.module_registry_update_module_testing_with_http_info(body, harness_account, id, **kwargs)  # noqa: E501
            return data

    def module_registry_update_module_testing_with_http_info(self, body, harness_account, id, **kwargs):  # noqa: E501
        """Update module testing  # noqa: E501

        Update module testing metadata  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.module_registry_update_module_testing_with_http_info(body, harness_account, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateTestingRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str id: module id (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account', 'id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method module_registry_update_module_testing" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `module_registry_update_module_testing`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `module_registry_update_module_testing`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `module_registry_update_module_testing`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/vnd.goa.error'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/modules/{id}/testing', 'PUT',
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
