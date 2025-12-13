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


class ExternalDataProviderApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def add_new_external_data_file_metadata(self, body, account_identifier, **kwargs):  # noqa: E501
        """Add a new external data file metadata  # noqa: E501

        Add a new external data file metadata  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.add_new_external_data_file_metadata(body, account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateExternalDataFilesDTO body: Request body containing external data object (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :return: ResponseDTOExternalDataFiles
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.add_new_external_data_file_metadata_with_http_info(body, account_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.add_new_external_data_file_metadata_with_http_info(body, account_identifier, **kwargs)  # noqa: E501
            return data

    def add_new_external_data_file_metadata_with_http_info(self, body, account_identifier, **kwargs):  # noqa: E501
        """Add a new external data file metadata  # noqa: E501

        Add a new external data file metadata  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.add_new_external_data_file_metadata_with_http_info(body, account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateExternalDataFilesDTO body: Request body containing external data object (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :return: ResponseDTOExternalDataFiles
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'account_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method add_new_external_data_file_metadata" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `add_new_external_data_file_metadata`")  # noqa: E501
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `add_new_external_data_file_metadata`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/yaml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/ccm/api/externaldata/filesinfo', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ResponseDTOExternalDataFiles',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def ccmdelete_provider(self, account_identifier, provider_id, **kwargs):  # noqa: E501
        """Delete a provider  # noqa: E501

        Delete a external data provider given a idD.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ccmdelete_provider(account_identifier, provider_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str provider_id: Unique identifier for the rule (required)
        :return: ResponseDTOBoolean
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ccmdelete_provider_with_http_info(account_identifier, provider_id, **kwargs)  # noqa: E501
        else:
            (data) = self.ccmdelete_provider_with_http_info(account_identifier, provider_id, **kwargs)  # noqa: E501
            return data

    def ccmdelete_provider_with_http_info(self, account_identifier, provider_id, **kwargs):  # noqa: E501
        """Delete a provider  # noqa: E501

        Delete a external data provider given a idD.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ccmdelete_provider_with_http_info(account_identifier, provider_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str provider_id: Unique identifier for the rule (required)
        :return: ResponseDTOBoolean
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'provider_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method ccmdelete_provider" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `ccmdelete_provider`")  # noqa: E501
        # verify the required parameter 'provider_id' is set
        if ('provider_id' not in params or
                params['provider_id'] is None):
            raise ValueError("Missing the required parameter `provider_id` when calling `ccmdelete_provider`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'provider_id' in params:
            path_params['providerId'] = params['provider_id']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/yaml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/ccm/api/externaldata/provider/{providerId}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ResponseDTOBoolean',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_external_data_provider(self, body, account_identifier, **kwargs):  # noqa: E501
        """Create External Data Provider  # noqa: E501

        Create External Data Provider  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_external_data_provider(body, account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateExternalDataProviderDTO body: Create External Data Provider Request (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :return: ResponseDTOExternalDataProvider
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_external_data_provider_with_http_info(body, account_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.create_external_data_provider_with_http_info(body, account_identifier, **kwargs)  # noqa: E501
            return data

    def create_external_data_provider_with_http_info(self, body, account_identifier, **kwargs):  # noqa: E501
        """Create External Data Provider  # noqa: E501

        Create External Data Provider  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_external_data_provider_with_http_info(body, account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateExternalDataProviderDTO body: Create External Data Provider Request (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :return: ResponseDTOExternalDataProvider
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'account_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_external_data_provider" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_external_data_provider`")  # noqa: E501
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `create_external_data_provider`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/yaml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/ccm/api/externaldata/provider', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ResponseDTOExternalDataProvider',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_datafile_and_metadata(self, account_identifier, file_id, **kwargs):  # noqa: E501
        """Delete data file and related metadata  # noqa: E501

        Delete data file and related metadata given an id.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_datafile_and_metadata(account_identifier, file_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str file_id: Unique identifier for the data file (required)
        :return: ResponseDTOBoolean
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_datafile_and_metadata_with_http_info(account_identifier, file_id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_datafile_and_metadata_with_http_info(account_identifier, file_id, **kwargs)  # noqa: E501
            return data

    def delete_datafile_and_metadata_with_http_info(self, account_identifier, file_id, **kwargs):  # noqa: E501
        """Delete data file and related metadata  # noqa: E501

        Delete data file and related metadata given an id.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_datafile_and_metadata_with_http_info(account_identifier, file_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str file_id: Unique identifier for the data file (required)
        :return: ResponseDTOBoolean
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'file_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_datafile_and_metadata" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `delete_datafile_and_metadata`")  # noqa: E501
        # verify the required parameter 'file_id' is set
        if ('file_id' not in params or
                params['file_id'] is None):
            raise ValueError("Missing the required parameter `file_id` when calling `delete_datafile_and_metadata`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'file_id' in params:
            path_params['fileId'] = params['file_id']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/yaml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/ccm/api/externaldata/filesinfo/{fileId}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ResponseDTOBoolean',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_providers(self, account_identifier, **kwargs):  # noqa: E501
        """get all external data providers  # noqa: E501

        get providers   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_providers(account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :return: ResponseDTOListExternalDataProvider
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_providers_with_http_info(account_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.get_providers_with_http_info(account_identifier, **kwargs)  # noqa: E501
            return data

    def get_providers_with_http_info(self, account_identifier, **kwargs):  # noqa: E501
        """get all external data providers  # noqa: E501

        get providers   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_providers_with_http_info(account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :return: ResponseDTOListExternalDataProvider
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_providers" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `get_providers`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/yaml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/ccm/api/externaldata/provider/list', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ResponseDTOListExternalDataProvider',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_signed_url(self, account_identifier, provider_id, invoice_period, object_name, **kwargs):  # noqa: E501
        """Get a signed url  # noqa: E501

        Get a signed url to upload external cost data.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_signed_url(account_identifier, provider_id, invoice_period, object_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier (required)
        :param str provider_id: Unique identifier for the provider (required)
        :param str invoice_period: Invoice period in format YYYYMMDD-YYYYMMDD (required)
        :param str object_name: Name of the object to upload (required)
        :return: ResponseDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_signed_url_with_http_info(account_identifier, provider_id, invoice_period, object_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_signed_url_with_http_info(account_identifier, provider_id, invoice_period, object_name, **kwargs)  # noqa: E501
            return data

    def get_signed_url_with_http_info(self, account_identifier, provider_id, invoice_period, object_name, **kwargs):  # noqa: E501
        """Get a signed url  # noqa: E501

        Get a signed url to upload external cost data.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_signed_url_with_http_info(account_identifier, provider_id, invoice_period, object_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier (required)
        :param str provider_id: Unique identifier for the provider (required)
        :param str invoice_period: Invoice period in format YYYYMMDD-YYYYMMDD (required)
        :param str object_name: Name of the object to upload (required)
        :return: ResponseDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'provider_id', 'invoice_period', 'object_name']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_signed_url" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `get_signed_url`")  # noqa: E501
        # verify the required parameter 'provider_id' is set
        if ('provider_id' not in params or
                params['provider_id'] is None):
            raise ValueError("Missing the required parameter `provider_id` when calling `get_signed_url`")  # noqa: E501
        # verify the required parameter 'invoice_period' is set
        if ('invoice_period' not in params or
                params['invoice_period'] is None):
            raise ValueError("Missing the required parameter `invoice_period` when calling `get_signed_url`")  # noqa: E501
        # verify the required parameter 'object_name' is set
        if ('object_name' not in params or
                params['object_name'] is None):
            raise ValueError("Missing the required parameter `object_name` when calling `get_signed_url`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'provider_id' in params:
            query_params.append(('providerId', params['provider_id']))  # noqa: E501
        if 'invoice_period' in params:
            query_params.append(('invoicePeriod', params['invoice_period']))  # noqa: E501
        if 'object_name' in params:
            query_params.append(('objectName', params['object_name']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/yaml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/ccm/api/externaldata/signedurl', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ResponseDTO',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_providers_file_info(self, body, account_identifier, **kwargs):  # noqa: E501
        """get all files info for list of providers  # noqa: E501

        listProvidersFileInfo  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_providers_file_info(body, account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ExternalDataProviderList body: Request body containing external data object (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :return: ResponseDTOMapStringListExternalDataFiles
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_providers_file_info_with_http_info(body, account_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.list_providers_file_info_with_http_info(body, account_identifier, **kwargs)  # noqa: E501
            return data

    def list_providers_file_info_with_http_info(self, body, account_identifier, **kwargs):  # noqa: E501
        """get all files info for list of providers  # noqa: E501

        listProvidersFileInfo  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_providers_file_info_with_http_info(body, account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ExternalDataProviderList body: Request body containing external data object (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :return: ResponseDTOMapStringListExternalDataFiles
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'account_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_providers_file_info" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `list_providers_file_info`")  # noqa: E501
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `list_providers_file_info`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/yaml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/ccm/api/externaldata/provider/filesinfo', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ResponseDTOMapStringListExternalDataFiles',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def trigger_data_ingestion(self, body, account_identifier, **kwargs):  # noqa: E501
        """Trigger data ingestion  # noqa: E501

        Trigger data ingestion  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.trigger_data_ingestion(body, account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ExternalDataIngestionRequest body: Request body containing list of invoice months for a provider (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :return: ResponseDTOExternalDataFiles
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.trigger_data_ingestion_with_http_info(body, account_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.trigger_data_ingestion_with_http_info(body, account_identifier, **kwargs)  # noqa: E501
            return data

    def trigger_data_ingestion_with_http_info(self, body, account_identifier, **kwargs):  # noqa: E501
        """Trigger data ingestion  # noqa: E501

        Trigger data ingestion  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.trigger_data_ingestion_with_http_info(body, account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ExternalDataIngestionRequest body: Request body containing list of invoice months for a provider (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :return: ResponseDTOExternalDataFiles
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'account_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method trigger_data_ingestion" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `trigger_data_ingestion`")  # noqa: E501
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `trigger_data_ingestion`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/yaml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/ccm/api/externaldata/dataingestion', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ResponseDTOExternalDataFiles',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_file_meta_data(self, body, account_identifier, file_id, **kwargs):  # noqa: E501
        """Update file metadata  # noqa: E501

        Update file metadata  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_file_meta_data(body, account_identifier, file_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateExternalDataFilesDTO body: Request body containing fileMetaData object (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str file_id: Unique identifier for the rule (required)
        :return: ResponseDTOExternalDataFiles
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_file_meta_data_with_http_info(body, account_identifier, file_id, **kwargs)  # noqa: E501
        else:
            (data) = self.update_file_meta_data_with_http_info(body, account_identifier, file_id, **kwargs)  # noqa: E501
            return data

    def update_file_meta_data_with_http_info(self, body, account_identifier, file_id, **kwargs):  # noqa: E501
        """Update file metadata  # noqa: E501

        Update file metadata  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_file_meta_data_with_http_info(body, account_identifier, file_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateExternalDataFilesDTO body: Request body containing fileMetaData object (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str file_id: Unique identifier for the rule (required)
        :return: ResponseDTOExternalDataFiles
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'account_identifier', 'file_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_file_meta_data" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update_file_meta_data`")  # noqa: E501
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `update_file_meta_data`")  # noqa: E501
        # verify the required parameter 'file_id' is set
        if ('file_id' not in params or
                params['file_id'] is None):
            raise ValueError("Missing the required parameter `file_id` when calling `update_file_meta_data`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'file_id' in params:
            path_params['fileId'] = params['file_id']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/yaml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/ccm/api/externaldata/filesinfo/{fileId}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ResponseDTOExternalDataFiles',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
