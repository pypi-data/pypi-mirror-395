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


class AccountBannerApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def banners_allowed(self, **kwargs):  # noqa: E501
        """Check for a current account max 5 banners are enabled or not  # noqa: E501

        Check for a current account max 5 banners are enabled or not.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.banners_allowed(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: bool
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.banners_allowed_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.banners_allowed_with_http_info(**kwargs)  # noqa: E501
            return data

    def banners_allowed_with_http_info(self, **kwargs):  # noqa: E501
        """Check for a current account max 5 banners are enabled or not  # noqa: E501

        Check for a current account max 5 banners are enabled or not.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.banners_allowed_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: bool
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method banners_allowed" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/banners/allowed', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='bool',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_account_scoped_banners(self, **kwargs):  # noqa: E501
        """Creates a new Banner in account scope  # noqa: E501

        Creates a new Banner in Account Scope.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_account_scoped_banners(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param BannerDTO body:
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: BannerResponseDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_account_scoped_banners_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.create_account_scoped_banners_with_http_info(**kwargs)  # noqa: E501
            return data

    def create_account_scoped_banners_with_http_info(self, **kwargs):  # noqa: E501
        """Creates a new Banner in account scope  # noqa: E501

        Creates a new Banner in Account Scope.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_account_scoped_banners_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param BannerDTO body:
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: BannerResponseDTO
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
                    " to method create_account_scoped_banners" % key
                )
            params[key] = val
        del params['kwargs']

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
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/banners', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='BannerResponseDTO',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_account_scoped_banner(self, banner, **kwargs):  # noqa: E501
        """Deletes the specified Banner in account scope  # noqa: E501

        Deletes the specified Banner in account scope  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_account_scoped_banner(banner, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str banner: Identifier field of the Banner (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_account_scoped_banner_with_http_info(banner, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_account_scoped_banner_with_http_info(banner, **kwargs)  # noqa: E501
            return data

    def delete_account_scoped_banner_with_http_info(self, banner, **kwargs):  # noqa: E501
        """Deletes the specified Banner in account scope  # noqa: E501

        Deletes the specified Banner in account scope  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_account_scoped_banner_with_http_info(banner, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str banner: Identifier field of the Banner (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['banner', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_account_scoped_banner" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'banner' is set
        if ('banner' not in params or
                params['banner'] is None):
            raise ValueError("Missing the required parameter `banner` when calling `delete_account_scoped_banner`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'banner' in params:
            path_params['banner'] = params['banner']  # noqa: E501

        query_params = []

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/banners/{banner}', 'DELETE',
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

    def get_account_scoped_active_banners(self, **kwargs):  # noqa: E501
        """Return Active Banners  # noqa: E501

        This API endpoint will return max 5 banners as that is the enabled banners count.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_account_scoped_active_banners(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :param str search_term: This would be used to filter resources having attributes matching with search term.
        :param int page: Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page 
        :param int limit: Number of items to return per page.
        :param str sort: Parameter on the basis of which sorting is done.
        :param str order: Order on the basis of which sorting is done.
        :return: list[BannerResponseDTO]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_account_scoped_active_banners_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_account_scoped_active_banners_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_account_scoped_active_banners_with_http_info(self, **kwargs):  # noqa: E501
        """Return Active Banners  # noqa: E501

        This API endpoint will return max 5 banners as that is the enabled banners count.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_account_scoped_active_banners_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :param str search_term: This would be used to filter resources having attributes matching with search term.
        :param int page: Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page 
        :param int limit: Number of items to return per page.
        :param str sort: Parameter on the basis of which sorting is done.
        :param str order: Order on the basis of which sorting is done.
        :return: list[BannerResponseDTO]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['harness_account', 'search_term', 'page', 'limit', 'sort', 'order']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_account_scoped_active_banners" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'search_term' in params:
            query_params.append(('search_term', params['search_term']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501
        if 'order' in params:
            query_params.append(('order', params['order']))  # noqa: E501

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/banners/active', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[BannerResponseDTO]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_account_scoped_banners(self, **kwargs):  # noqa: E501
        """Retrieves the list of Banners in account scope  # noqa: E501

        Retrieves the list of Banners in account scope  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_account_scoped_banners(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :param str search_term: This would be used to filter resources having attributes matching with search term.
        :param int page: Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page 
        :param int limit: Number of items to return per page.
        :param str sort: Parameter on the basis of which sorting is done.
        :param str order: Order on the basis of which sorting is done.
        :param str enabled: Show banners with enabled field filtering
        :return: list[BannerResponseDTO]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_account_scoped_banners_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_account_scoped_banners_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_account_scoped_banners_with_http_info(self, **kwargs):  # noqa: E501
        """Retrieves the list of Banners in account scope  # noqa: E501

        Retrieves the list of Banners in account scope  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_account_scoped_banners_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :param str search_term: This would be used to filter resources having attributes matching with search term.
        :param int page: Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page 
        :param int limit: Number of items to return per page.
        :param str sort: Parameter on the basis of which sorting is done.
        :param str order: Order on the basis of which sorting is done.
        :param str enabled: Show banners with enabled field filtering
        :return: list[BannerResponseDTO]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['harness_account', 'search_term', 'page', 'limit', 'sort', 'order', 'enabled']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_account_scoped_banners" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'search_term' in params:
            query_params.append(('search_term', params['search_term']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501
        if 'order' in params:
            query_params.append(('order', params['order']))  # noqa: E501
        if 'enabled' in params:
            query_params.append(('enabled', params['enabled']))  # noqa: E501

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/banners', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[BannerResponseDTO]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_account_scoped_banner(self, banner, **kwargs):  # noqa: E501
        """Updates the specified Banner in account scope  # noqa: E501

        Updates the specified Banner in account scope  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_account_scoped_banner(banner, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str banner: Identifier field of the Banner (required)
        :param BannerDTO body: Request body when updating respective Banner.
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: BannerResponseDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_account_scoped_banner_with_http_info(banner, **kwargs)  # noqa: E501
        else:
            (data) = self.update_account_scoped_banner_with_http_info(banner, **kwargs)  # noqa: E501
            return data

    def update_account_scoped_banner_with_http_info(self, banner, **kwargs):  # noqa: E501
        """Updates the specified Banner in account scope  # noqa: E501

        Updates the specified Banner in account scope  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_account_scoped_banner_with_http_info(banner, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str banner: Identifier field of the Banner (required)
        :param BannerDTO body: Request body when updating respective Banner.
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: BannerResponseDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['banner', 'body', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_account_scoped_banner" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'banner' is set
        if ('banner' not in params or
                params['banner'] is None):
            raise ValueError("Missing the required parameter `banner` when calling `update_account_scoped_banner`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'banner' in params:
            path_params['banner'] = params['banner']  # noqa: E501

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
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/banners/{banner}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='BannerResponseDTO',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def validate_account_scoped_banner_identifier(self, banner_id, **kwargs):  # noqa: E501
        """Validate if the specified Banner identifier is available for use in account scope  # noqa: E501

        Validate if the specified BannerDTO identifier is available for use in account scope  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.validate_account_scoped_banner_identifier(banner_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str banner_id: Identifier field of the BannerDTO (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: bool
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.validate_account_scoped_banner_identifier_with_http_info(banner_id, **kwargs)  # noqa: E501
        else:
            (data) = self.validate_account_scoped_banner_identifier_with_http_info(banner_id, **kwargs)  # noqa: E501
            return data

    def validate_account_scoped_banner_identifier_with_http_info(self, banner_id, **kwargs):  # noqa: E501
        """Validate if the specified Banner identifier is available for use in account scope  # noqa: E501

        Validate if the specified BannerDTO identifier is available for use in account scope  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.validate_account_scoped_banner_identifier_with_http_info(banner_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str banner_id: Identifier field of the BannerDTO (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: bool
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['banner_id', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method validate_account_scoped_banner_identifier" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'banner_id' is set
        if ('banner_id' not in params or
                params['banner_id'] is None):
            raise ValueError("Missing the required parameter `banner_id` when calling `validate_account_scoped_banner_identifier`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'banner_id' in params:
            path_params['bannerId'] = params['banner_id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/banners/validate-unique-identifier/{bannerId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='bool',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
