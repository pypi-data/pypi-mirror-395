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


class ProviderRegistryApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def provider_registry_create_provider(self, type, harness_account, **kwargs):  # noqa: E501
        """Create provider  # noqa: E501

        Create a provider  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_create_provider(type, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str type: Provider type (required)
        :param str harness_account: Account ID (required)
        :return: AnsibleDataInfo
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.provider_registry_create_provider_with_http_info(type, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.provider_registry_create_provider_with_http_info(type, harness_account, **kwargs)  # noqa: E501
            return data

    def provider_registry_create_provider_with_http_info(self, type, harness_account, **kwargs):  # noqa: E501
        """Create provider  # noqa: E501

        Create a provider  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_create_provider_with_http_info(type, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str type: Provider type (required)
        :param str harness_account: Account ID (required)
        :return: AnsibleDataInfo
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['type', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method provider_registry_create_provider" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'type' is set
        if ('type' not in params or
                params['type'] is None):
            raise ValueError("Missing the required parameter `type` when calling `provider_registry_create_provider`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `provider_registry_create_provider`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'type' in params:
            path_params['type'] = params['type']  # noqa: E501

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
            '/iacm/api/providers/{type}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AnsibleDataInfo',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def provider_registry_create_provider_version(self, body, harness_account, id, **kwargs):  # noqa: E501
        """Create provider version  # noqa: E501

        Create a provider version  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_create_provider_version(body, harness_account, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateProviderVersionRequestBody body: (required)
        :param str harness_account: Account ID (required)
        :param str id: Provider ID (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.provider_registry_create_provider_version_with_http_info(body, harness_account, id, **kwargs)  # noqa: E501
        else:
            (data) = self.provider_registry_create_provider_version_with_http_info(body, harness_account, id, **kwargs)  # noqa: E501
            return data

    def provider_registry_create_provider_version_with_http_info(self, body, harness_account, id, **kwargs):  # noqa: E501
        """Create provider version  # noqa: E501

        Create a provider version  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_create_provider_version_with_http_info(body, harness_account, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateProviderVersionRequestBody body: (required)
        :param str harness_account: Account ID (required)
        :param str id: Provider ID (required)
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
                    " to method provider_registry_create_provider_version" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `provider_registry_create_provider_version`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `provider_registry_create_provider_version`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `provider_registry_create_provider_version`")  # noqa: E501

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
            '/iacm/api/providers/{id}/version', 'POST',
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

    def provider_registry_delete_file(self, id, version, filename, harness_account, **kwargs):  # noqa: E501
        """Delete file from a non synced provider version  # noqa: E501

        Delete a file from a non synced provider version  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_delete_file(id, version, filename, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: Provider ID (required)
        :param str version: Provider version (required)
        :param str filename: File name (required)
        :param str harness_account: Account ID (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.provider_registry_delete_file_with_http_info(id, version, filename, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.provider_registry_delete_file_with_http_info(id, version, filename, harness_account, **kwargs)  # noqa: E501
            return data

    def provider_registry_delete_file_with_http_info(self, id, version, filename, harness_account, **kwargs):  # noqa: E501
        """Delete file from a non synced provider version  # noqa: E501

        Delete a file from a non synced provider version  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_delete_file_with_http_info(id, version, filename, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: Provider ID (required)
        :param str version: Provider version (required)
        :param str filename: File name (required)
        :param str harness_account: Account ID (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'version', 'filename', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method provider_registry_delete_file" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `provider_registry_delete_file`")  # noqa: E501
        # verify the required parameter 'version' is set
        if ('version' not in params or
                params['version'] is None):
            raise ValueError("Missing the required parameter `version` when calling `provider_registry_delete_file`")  # noqa: E501
        # verify the required parameter 'filename' is set
        if ('filename' not in params or
                params['filename'] is None):
            raise ValueError("Missing the required parameter `filename` when calling `provider_registry_delete_file`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `provider_registry_delete_file`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501
        if 'version' in params:
            path_params['version'] = params['version']  # noqa: E501
        if 'filename' in params:
            path_params['filename'] = params['filename']  # noqa: E501

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
            '/iacm/api/providers/{id}/version/{version}/file/{filename}', 'DELETE',
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

    def provider_registry_delete_provider(self, id, harness_account, **kwargs):  # noqa: E501
        """Delete provider  # noqa: E501

        Deletes a provider  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_delete_provider(id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: Provider ID (required)
        :param str harness_account: Account name (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.provider_registry_delete_provider_with_http_info(id, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.provider_registry_delete_provider_with_http_info(id, harness_account, **kwargs)  # noqa: E501
            return data

    def provider_registry_delete_provider_with_http_info(self, id, harness_account, **kwargs):  # noqa: E501
        """Delete provider  # noqa: E501

        Deletes a provider  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_delete_provider_with_http_info(id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: Provider ID (required)
        :param str harness_account: Account name (required)
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
                    " to method provider_registry_delete_provider" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `provider_registry_delete_provider`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `provider_registry_delete_provider`")  # noqa: E501

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
            '/iacm/api/providers/{id}', 'DELETE',
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

    def provider_registry_delete_provider_version(self, id, version, harness_account, **kwargs):  # noqa: E501
        """Delete provider version  # noqa: E501

        Delete a provider version  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_delete_provider_version(id, version, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: Provider ID (required)
        :param str version: Provider version (required)
        :param str harness_account: Account ID (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.provider_registry_delete_provider_version_with_http_info(id, version, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.provider_registry_delete_provider_version_with_http_info(id, version, harness_account, **kwargs)  # noqa: E501
            return data

    def provider_registry_delete_provider_version_with_http_info(self, id, version, harness_account, **kwargs):  # noqa: E501
        """Delete provider version  # noqa: E501

        Delete a provider version  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_delete_provider_version_with_http_info(id, version, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: Provider ID (required)
        :param str version: Provider version (required)
        :param str harness_account: Account ID (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'version', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method provider_registry_delete_provider_version" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `provider_registry_delete_provider_version`")  # noqa: E501
        # verify the required parameter 'version' is set
        if ('version' not in params or
                params['version'] is None):
            raise ValueError("Missing the required parameter `version` when calling `provider_registry_delete_provider_version`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `provider_registry_delete_provider_version`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501
        if 'version' in params:
            path_params['version'] = params['version']  # noqa: E501

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
            '/iacm/api/providers/{id}/version/{version}', 'DELETE',
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

    def provider_registry_delete_signing_key(self, id, harness_account, **kwargs):  # noqa: E501
        """Delete a signing key for a provider  # noqa: E501

        Delete a signing key for a provider  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_delete_signing_key(id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: id of the key in the db (required)
        :param str harness_account: Account ID (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.provider_registry_delete_signing_key_with_http_info(id, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.provider_registry_delete_signing_key_with_http_info(id, harness_account, **kwargs)  # noqa: E501
            return data

    def provider_registry_delete_signing_key_with_http_info(self, id, harness_account, **kwargs):  # noqa: E501
        """Delete a signing key for a provider  # noqa: E501

        Delete a signing key for a provider  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_delete_signing_key_with_http_info(id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: id of the key in the db (required)
        :param str harness_account: Account ID (required)
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
                    " to method provider_registry_delete_signing_key" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `provider_registry_delete_signing_key`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `provider_registry_delete_signing_key`")  # noqa: E501

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
            '/iacm/api/providers/keys/{id}', 'DELETE',
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

    def provider_registry_get_file(self, token, account, type, version, os, arch, filetype, **kwargs):  # noqa: E501
        """Get provider file  # noqa: E501

        Download a provider file (binary, checksums, or signature)  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_get_file(token, account, type, version, os, arch, filetype, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str token: Token to access the file (required)
        :param str account: Account identifier (required)
        :param str type: Provider type (required)
        :param str version: Provider version (required)
        :param str os: Operating system (required)
        :param str arch: Architecture (required)
        :param str filetype: Type of file to download (required)
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.provider_registry_get_file_with_http_info(token, account, type, version, os, arch, filetype, **kwargs)  # noqa: E501
        else:
            (data) = self.provider_registry_get_file_with_http_info(token, account, type, version, os, arch, filetype, **kwargs)  # noqa: E501
            return data

    def provider_registry_get_file_with_http_info(self, token, account, type, version, os, arch, filetype, **kwargs):  # noqa: E501
        """Get provider file  # noqa: E501

        Download a provider file (binary, checksums, or signature)  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_get_file_with_http_info(token, account, type, version, os, arch, filetype, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str token: Token to access the file (required)
        :param str account: Account identifier (required)
        :param str type: Provider type (required)
        :param str version: Provider version (required)
        :param str os: Operating system (required)
        :param str arch: Architecture (required)
        :param str filetype: Type of file to download (required)
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['token', 'account', 'type', 'version', 'os', 'arch', 'filetype']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method provider_registry_get_file" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'token' is set
        if ('token' not in params or
                params['token'] is None):
            raise ValueError("Missing the required parameter `token` when calling `provider_registry_get_file`")  # noqa: E501
        # verify the required parameter 'account' is set
        if ('account' not in params or
                params['account'] is None):
            raise ValueError("Missing the required parameter `account` when calling `provider_registry_get_file`")  # noqa: E501
        # verify the required parameter 'type' is set
        if ('type' not in params or
                params['type'] is None):
            raise ValueError("Missing the required parameter `type` when calling `provider_registry_get_file`")  # noqa: E501
        # verify the required parameter 'version' is set
        if ('version' not in params or
                params['version'] is None):
            raise ValueError("Missing the required parameter `version` when calling `provider_registry_get_file`")  # noqa: E501
        # verify the required parameter 'os' is set
        if ('os' not in params or
                params['os'] is None):
            raise ValueError("Missing the required parameter `os` when calling `provider_registry_get_file`")  # noqa: E501
        # verify the required parameter 'arch' is set
        if ('arch' not in params or
                params['arch'] is None):
            raise ValueError("Missing the required parameter `arch` when calling `provider_registry_get_file`")  # noqa: E501
        # verify the required parameter 'filetype' is set
        if ('filetype' not in params or
                params['filetype'] is None):
            raise ValueError("Missing the required parameter `filetype` when calling `provider_registry_get_file`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'account' in params:
            path_params['account'] = params['account']  # noqa: E501
        if 'type' in params:
            path_params['type'] = params['type']  # noqa: E501
        if 'version' in params:
            path_params['version'] = params['version']  # noqa: E501
        if 'os' in params:
            path_params['os'] = params['os']  # noqa: E501
        if 'arch' in params:
            path_params['arch'] = params['arch']  # noqa: E501
        if 'filetype' in params:
            path_params['filetype'] = params['filetype']  # noqa: E501

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
            '/iacm/provider/account/{account}/{type}/{version}/download/{os}/{arch}/{filetype}', 'GET',
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

    def provider_registry_get_provider(self, id, harness_account, **kwargs):  # noqa: E501
        """Get provider  # noqa: E501

        Gets a provider by ID  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_get_provider(id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: Provider ID (required)
        :param str harness_account: Account name (required)
        :return: IaCMGetProviderResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.provider_registry_get_provider_with_http_info(id, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.provider_registry_get_provider_with_http_info(id, harness_account, **kwargs)  # noqa: E501
            return data

    def provider_registry_get_provider_with_http_info(self, id, harness_account, **kwargs):  # noqa: E501
        """Get provider  # noqa: E501

        Gets a provider by ID  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_get_provider_with_http_info(id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: Provider ID (required)
        :param str harness_account: Account name (required)
        :return: IaCMGetProviderResponse
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
                    " to method provider_registry_get_provider" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `provider_registry_get_provider`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `provider_registry_get_provider`")  # noqa: E501

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
            '/iacm/api/providers/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='IaCMGetProviderResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def provider_registry_get_provider_download(self, account, type, version, os, arch, **kwargs):  # noqa: E501
        """Get provider download information  # noqa: E501

        Returns download information for a specific provider version and platform  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_get_provider_download(account, type, version, os, arch, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account: Account that owns the provider (required)
        :param str type: Provider type (required)
        :param str version: Provider version (required)
        :param str os: Operating system (required)
        :param str arch: Architecture (required)
        :return: GetProviderDownloadResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.provider_registry_get_provider_download_with_http_info(account, type, version, os, arch, **kwargs)  # noqa: E501
        else:
            (data) = self.provider_registry_get_provider_download_with_http_info(account, type, version, os, arch, **kwargs)  # noqa: E501
            return data

    def provider_registry_get_provider_download_with_http_info(self, account, type, version, os, arch, **kwargs):  # noqa: E501
        """Get provider download information  # noqa: E501

        Returns download information for a specific provider version and platform  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_get_provider_download_with_http_info(account, type, version, os, arch, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account: Account that owns the provider (required)
        :param str type: Provider type (required)
        :param str version: Provider version (required)
        :param str os: Operating system (required)
        :param str arch: Architecture (required)
        :return: GetProviderDownloadResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account', 'type', 'version', 'os', 'arch']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method provider_registry_get_provider_download" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account' is set
        if ('account' not in params or
                params['account'] is None):
            raise ValueError("Missing the required parameter `account` when calling `provider_registry_get_provider_download`")  # noqa: E501
        # verify the required parameter 'type' is set
        if ('type' not in params or
                params['type'] is None):
            raise ValueError("Missing the required parameter `type` when calling `provider_registry_get_provider_download`")  # noqa: E501
        # verify the required parameter 'version' is set
        if ('version' not in params or
                params['version'] is None):
            raise ValueError("Missing the required parameter `version` when calling `provider_registry_get_provider_download`")  # noqa: E501
        # verify the required parameter 'os' is set
        if ('os' not in params or
                params['os'] is None):
            raise ValueError("Missing the required parameter `os` when calling `provider_registry_get_provider_download`")  # noqa: E501
        # verify the required parameter 'arch' is set
        if ('arch' not in params or
                params['arch'] is None):
            raise ValueError("Missing the required parameter `arch` when calling `provider_registry_get_provider_download`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'account' in params:
            path_params['account'] = params['account']  # noqa: E501
        if 'type' in params:
            path_params['type'] = params['type']  # noqa: E501
        if 'version' in params:
            path_params['version'] = params['version']  # noqa: E501
        if 'os' in params:
            path_params['os'] = params['os']  # noqa: E501
        if 'arch' in params:
            path_params['arch'] = params['arch']  # noqa: E501

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
            '/iacm/provider/account/{account}/{type}/{version}/download/{os}/{arch}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetProviderDownloadResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def provider_registry_get_provider_version(self, id, version, harness_account, **kwargs):  # noqa: E501
        """Get provider version  # noqa: E501

        Get a provider version  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_get_provider_version(id, version, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: Provider ID (required)
        :param str version: Provider version (required)
        :param str harness_account: Account ID (required)
        :return: GetProviderVersionResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.provider_registry_get_provider_version_with_http_info(id, version, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.provider_registry_get_provider_version_with_http_info(id, version, harness_account, **kwargs)  # noqa: E501
            return data

    def provider_registry_get_provider_version_with_http_info(self, id, version, harness_account, **kwargs):  # noqa: E501
        """Get provider version  # noqa: E501

        Get a provider version  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_get_provider_version_with_http_info(id, version, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: Provider ID (required)
        :param str version: Provider version (required)
        :param str harness_account: Account ID (required)
        :return: GetProviderVersionResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'version', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method provider_registry_get_provider_version" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `provider_registry_get_provider_version`")  # noqa: E501
        # verify the required parameter 'version' is set
        if ('version' not in params or
                params['version'] is None):
            raise ValueError("Missing the required parameter `version` when calling `provider_registry_get_provider_version`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `provider_registry_get_provider_version`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501
        if 'version' in params:
            path_params['version'] = params['version']  # noqa: E501

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
            '/iacm/api/providers/{id}/version/{version}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetProviderVersionResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def provider_registry_list_provider_versions(self, account, type, **kwargs):  # noqa: E501
        """List provider versions  # noqa: E501

        Lists available versions for a provider  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_list_provider_versions(account, type, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account: Account that owns the provider (required)
        :param str type: Provider type (required)
        :return: ListProviderVersionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.provider_registry_list_provider_versions_with_http_info(account, type, **kwargs)  # noqa: E501
        else:
            (data) = self.provider_registry_list_provider_versions_with_http_info(account, type, **kwargs)  # noqa: E501
            return data

    def provider_registry_list_provider_versions_with_http_info(self, account, type, **kwargs):  # noqa: E501
        """List provider versions  # noqa: E501

        Lists available versions for a provider  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_list_provider_versions_with_http_info(account, type, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account: Account that owns the provider (required)
        :param str type: Provider type (required)
        :return: ListProviderVersionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account', 'type']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method provider_registry_list_provider_versions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account' is set
        if ('account' not in params or
                params['account'] is None):
            raise ValueError("Missing the required parameter `account` when calling `provider_registry_list_provider_versions`")  # noqa: E501
        # verify the required parameter 'type' is set
        if ('type' not in params or
                params['type'] is None):
            raise ValueError("Missing the required parameter `type` when calling `provider_registry_list_provider_versions`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'account' in params:
            path_params['account'] = params['account']  # noqa: E501
        if 'type' in params:
            path_params['type'] = params['type']  # noqa: E501

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
            '/iacm/provider/account/{account}/{type}/versions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ListProviderVersionsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def provider_registry_list_providers(self, harness_account, **kwargs):  # noqa: E501
        """List providers  # noqa: E501

        Lists all providers for an account  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_list_providers(harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Account name (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :param str search_term: Filter results by partial name match
        :param str sort: Sort order for results
        :return: ProviderCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.provider_registry_list_providers_with_http_info(harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.provider_registry_list_providers_with_http_info(harness_account, **kwargs)  # noqa: E501
            return data

    def provider_registry_list_providers_with_http_info(self, harness_account, **kwargs):  # noqa: E501
        """List providers  # noqa: E501

        Lists all providers for an account  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_list_providers_with_http_info(harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Account name (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :param str search_term: Filter results by partial name match
        :param str sort: Sort order for results
        :return: ProviderCollection
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
                    " to method provider_registry_list_providers" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `provider_registry_list_providers`")  # noqa: E501

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
            '/iacm/api/providers', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ProviderCollection',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def provider_registry_list_signing_keys(self, harness_account, **kwargs):  # noqa: E501
        """List signing keys  # noqa: E501

        List all GPG signing keys for an account  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_list_signing_keys(harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Account ID (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :param str search_term: Filter results by partial name match
        :param str sort: Sort order for results
        :return: SigningKeyCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.provider_registry_list_signing_keys_with_http_info(harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.provider_registry_list_signing_keys_with_http_info(harness_account, **kwargs)  # noqa: E501
            return data

    def provider_registry_list_signing_keys_with_http_info(self, harness_account, **kwargs):  # noqa: E501
        """List signing keys  # noqa: E501

        List all GPG signing keys for an account  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_list_signing_keys_with_http_info(harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Account ID (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :param str search_term: Filter results by partial name match
        :param str sort: Sort order for results
        :return: SigningKeyCollection
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
                    " to method provider_registry_list_signing_keys" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `provider_registry_list_signing_keys`")  # noqa: E501

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
            '/iacm/api/providers/keys', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SigningKeyCollection',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def provider_registry_post_files(self, id, version, harness_account, content_disposition, **kwargs):  # noqa: E501
        """Upload files  # noqa: E501

        Upload files to the provider registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_post_files(id, version, harness_account, content_disposition, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: Provider ID (required)
        :param str version: Provider version (required)
        :param str harness_account: Account ID (required)
        :param str content_disposition: Content-Disposition header (required)
        :return: PostFilesResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.provider_registry_post_files_with_http_info(id, version, harness_account, content_disposition, **kwargs)  # noqa: E501
        else:
            (data) = self.provider_registry_post_files_with_http_info(id, version, harness_account, content_disposition, **kwargs)  # noqa: E501
            return data

    def provider_registry_post_files_with_http_info(self, id, version, harness_account, content_disposition, **kwargs):  # noqa: E501
        """Upload files  # noqa: E501

        Upload files to the provider registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_post_files_with_http_info(id, version, harness_account, content_disposition, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: Provider ID (required)
        :param str version: Provider version (required)
        :param str harness_account: Account ID (required)
        :param str content_disposition: Content-Disposition header (required)
        :return: PostFilesResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'version', 'harness_account', 'content_disposition']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method provider_registry_post_files" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `provider_registry_post_files`")  # noqa: E501
        # verify the required parameter 'version' is set
        if ('version' not in params or
                params['version'] is None):
            raise ValueError("Missing the required parameter `version` when calling `provider_registry_post_files`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `provider_registry_post_files`")  # noqa: E501
        # verify the required parameter 'content_disposition' is set
        if ('content_disposition' not in params or
                params['content_disposition'] is None):
            raise ValueError("Missing the required parameter `content_disposition` when calling `provider_registry_post_files`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501
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
            ['application/json', 'application/vnd.goa.error'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/providers/{id}/version/{version}/files', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='PostFilesResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def provider_registry_publish_provider_version(self, id, version, harness_account, **kwargs):  # noqa: E501
        """Publish a provider version  # noqa: E501

        Publish a provider version  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_publish_provider_version(id, version, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: Provider ID (required)
        :param str version: Provider version (required)
        :param str harness_account: Account ID (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.provider_registry_publish_provider_version_with_http_info(id, version, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.provider_registry_publish_provider_version_with_http_info(id, version, harness_account, **kwargs)  # noqa: E501
            return data

    def provider_registry_publish_provider_version_with_http_info(self, id, version, harness_account, **kwargs):  # noqa: E501
        """Publish a provider version  # noqa: E501

        Publish a provider version  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_publish_provider_version_with_http_info(id, version, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: Provider ID (required)
        :param str version: Provider version (required)
        :param str harness_account: Account ID (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'version', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method provider_registry_publish_provider_version" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `provider_registry_publish_provider_version`")  # noqa: E501
        # verify the required parameter 'version' is set
        if ('version' not in params or
                params['version'] is None):
            raise ValueError("Missing the required parameter `version` when calling `provider_registry_publish_provider_version`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `provider_registry_publish_provider_version`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501
        if 'version' in params:
            path_params['version'] = params['version']  # noqa: E501

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
            '/iacm/api/providers/{id}/version/{version}/publish', 'POST',
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

    def provider_registry_update_provider_version(self, body, harness_account, id, version, **kwargs):  # noqa: E501
        """Update provider version  # noqa: E501

        Update a provider version  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_update_provider_version(body, harness_account, id, version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateProviderVersionRequestBody body: (required)
        :param str harness_account: Account ID (required)
        :param str id: Provider ID (required)
        :param str version: Provider version (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.provider_registry_update_provider_version_with_http_info(body, harness_account, id, version, **kwargs)  # noqa: E501
        else:
            (data) = self.provider_registry_update_provider_version_with_http_info(body, harness_account, id, version, **kwargs)  # noqa: E501
            return data

    def provider_registry_update_provider_version_with_http_info(self, body, harness_account, id, version, **kwargs):  # noqa: E501
        """Update provider version  # noqa: E501

        Update a provider version  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_update_provider_version_with_http_info(body, harness_account, id, version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateProviderVersionRequestBody body: (required)
        :param str harness_account: Account ID (required)
        :param str id: Provider ID (required)
        :param str version: Provider version (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account', 'id', 'version']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method provider_registry_update_provider_version" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `provider_registry_update_provider_version`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `provider_registry_update_provider_version`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `provider_registry_update_provider_version`")  # noqa: E501
        # verify the required parameter 'version' is set
        if ('version' not in params or
                params['version'] is None):
            raise ValueError("Missing the required parameter `version` when calling `provider_registry_update_provider_version`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501
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
            '/iacm/api/providers/{id}/version/{version}', 'PUT',
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

    def provider_registry_update_signing_key(self, body, harness_account, id, **kwargs):  # noqa: E501
        """Update a signing key for a provider  # noqa: E501

        Update a signing key for a provider  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_update_signing_key(body, harness_account, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UploadSigningKeyRequest body: (required)
        :param str harness_account: Account ID (required)
        :param str id: id of the key in the db (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.provider_registry_update_signing_key_with_http_info(body, harness_account, id, **kwargs)  # noqa: E501
        else:
            (data) = self.provider_registry_update_signing_key_with_http_info(body, harness_account, id, **kwargs)  # noqa: E501
            return data

    def provider_registry_update_signing_key_with_http_info(self, body, harness_account, id, **kwargs):  # noqa: E501
        """Update a signing key for a provider  # noqa: E501

        Update a signing key for a provider  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_update_signing_key_with_http_info(body, harness_account, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UploadSigningKeyRequest body: (required)
        :param str harness_account: Account ID (required)
        :param str id: id of the key in the db (required)
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
                    " to method provider_registry_update_signing_key" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `provider_registry_update_signing_key`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `provider_registry_update_signing_key`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `provider_registry_update_signing_key`")  # noqa: E501

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
            '/iacm/api/providers/keys/{id}', 'PUT',
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

    def provider_registry_upload_signing_key(self, body, harness_account, **kwargs):  # noqa: E501
        """Upload signing key  # noqa: E501

        Upload a GPG signing key for an account  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_upload_signing_key(body, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UploadSigningKeyRequest body: (required)
        :param str harness_account: Account ID (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.provider_registry_upload_signing_key_with_http_info(body, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.provider_registry_upload_signing_key_with_http_info(body, harness_account, **kwargs)  # noqa: E501
            return data

    def provider_registry_upload_signing_key_with_http_info(self, body, harness_account, **kwargs):  # noqa: E501
        """Upload signing key  # noqa: E501

        Upload a GPG signing key for an account  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.provider_registry_upload_signing_key_with_http_info(body, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UploadSigningKeyRequest body: (required)
        :param str harness_account: Account ID (required)
        :return: None
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
                    " to method provider_registry_upload_signing_key" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `provider_registry_upload_signing_key`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `provider_registry_upload_signing_key`")  # noqa: E501

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
            ['application/vnd.goa.error'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/providers/keys', 'POST',
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
