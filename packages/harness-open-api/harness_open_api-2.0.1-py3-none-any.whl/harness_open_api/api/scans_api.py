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


class ScansApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def scans_create_scan(self, body, account_id, **kwargs):  # noqa: E501
        """scans_create_scan  # noqa: E501

        Create a new Security Test Scan  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.scans_create_scan(body, account_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateScanRequestBody body: (required)
        :param str account_id: Harness Account ID (required)
        :param str x_api_key: Harness personal or service access token
        :param str x_harness_user_id: Harness User ID
        :return: ExemptionsCreateExemptionResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.scans_create_scan_with_http_info(body, account_id, **kwargs)  # noqa: E501
        else:
            (data) = self.scans_create_scan_with_http_info(body, account_id, **kwargs)  # noqa: E501
            return data

    def scans_create_scan_with_http_info(self, body, account_id, **kwargs):  # noqa: E501
        """scans_create_scan  # noqa: E501

        Create a new Security Test Scan  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.scans_create_scan_with_http_info(body, account_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateScanRequestBody body: (required)
        :param str account_id: Harness Account ID (required)
        :param str x_api_key: Harness personal or service access token
        :param str x_harness_user_id: Harness User ID
        :return: ExemptionsCreateExemptionResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'account_id', 'x_api_key', 'x_harness_user_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method scans_create_scan" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `scans_create_scan`")  # noqa: E501
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `scans_create_scan`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501

        header_params = {}
        if 'x_api_key' in params:
            header_params['X-Api-Key'] = params['x_api_key']  # noqa: E501
        if 'x_harness_user_id' in params:
            header_params['X-Harness-User-Id'] = params['x_harness_user_id']  # noqa: E501

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
            '/sto/api/v2/scans', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ExemptionsCreateExemptionResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def scans_delete_scan(self, account_id, id, **kwargs):  # noqa: E501
        """scans_delete_scan  # noqa: E501

        Delete an existing Security Test Scan  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.scans_delete_scan(account_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str id: The ID of the Security Test Scan to delete (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.scans_delete_scan_with_http_info(account_id, id, **kwargs)  # noqa: E501
        else:
            (data) = self.scans_delete_scan_with_http_info(account_id, id, **kwargs)  # noqa: E501
            return data

    def scans_delete_scan_with_http_info(self, account_id, id, **kwargs):  # noqa: E501
        """scans_delete_scan  # noqa: E501

        Delete an existing Security Test Scan  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.scans_delete_scan_with_http_info(account_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str id: The ID of the Security Test Scan to delete (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method scans_delete_scan" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `scans_delete_scan`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `scans_delete_scan`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501

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
            '/sto/api/v2/scans/{id}', 'DELETE',
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

    def scans_find_scan_by_id(self, account_id, id, **kwargs):  # noqa: E501
        """scans_find_scan_by_id  # noqa: E501

        Find Security Test Scan by ID  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.scans_find_scan_by_id(account_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str id: The ID of the Security Test Scan to retrieve (required)
        :param str x_api_key: Harness personal or service access token
        :return: Scan
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.scans_find_scan_by_id_with_http_info(account_id, id, **kwargs)  # noqa: E501
        else:
            (data) = self.scans_find_scan_by_id_with_http_info(account_id, id, **kwargs)  # noqa: E501
            return data

    def scans_find_scan_by_id_with_http_info(self, account_id, id, **kwargs):  # noqa: E501
        """scans_find_scan_by_id  # noqa: E501

        Find Security Test Scan by ID  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.scans_find_scan_by_id_with_http_info(account_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str id: The ID of the Security Test Scan to retrieve (required)
        :param str x_api_key: Harness personal or service access token
        :return: Scan
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'id', 'x_api_key']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method scans_find_scan_by_id" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `scans_find_scan_by_id`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `scans_find_scan_by_id`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501

        header_params = {}
        if 'x_api_key' in params:
            header_params['X-Api-Key'] = params['x_api_key']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/sto/api/v2/scans/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Scan',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def scans_list_scans(self, account_id, **kwargs):  # noqa: E501
        """scans_list_scans  # noqa: E501

        List a collection of Security Test Scans  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.scans_list_scans(account_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param int page: Page number to fetch (starting from 0)
        :param int page_size: Number of results per page
        :param str execution_id: Harness Execution ID
        :param str x_api_key: Harness personal or service access token
        :return: ScansListScansResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.scans_list_scans_with_http_info(account_id, **kwargs)  # noqa: E501
        else:
            (data) = self.scans_list_scans_with_http_info(account_id, **kwargs)  # noqa: E501
            return data

    def scans_list_scans_with_http_info(self, account_id, **kwargs):  # noqa: E501
        """scans_list_scans  # noqa: E501

        List a collection of Security Test Scans  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.scans_list_scans_with_http_info(account_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param int page: Page number to fetch (starting from 0)
        :param int page_size: Number of results per page
        :param str execution_id: Harness Execution ID
        :param str x_api_key: Harness personal or service access token
        :return: ScansListScansResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'page', 'page_size', 'execution_id', 'x_api_key']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method scans_list_scans" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `scans_list_scans`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('pageSize', params['page_size']))  # noqa: E501
        if 'execution_id' in params:
            query_params.append(('executionId', params['execution_id']))  # noqa: E501

        header_params = {}
        if 'x_api_key' in params:
            header_params['X-Api-Key'] = params['x_api_key']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/sto/api/v2/scans', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ScansListScansResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def scans_scan_issue(self, account_id, id, issue_id, **kwargs):  # noqa: E501
        """scans_scan_issue  # noqa: E501

        Returns a scan specific issue  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.scans_scan_issue(account_id, id, issue_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str id: The ID of the Security Test Scan (required)
        :param str issue_id: The ID of the Security Test Issue (required)
        :param str org_id: Harness Organization ID
        :param str project_id: Harness Project ID
        :param int page: Page number to fetch (starting from 0)
        :param int page_size: Number of results per page
        :param str sort: The field to sort by
        :param str order: The order to sort by
        :param str x_api_key: Harness personal or service access token
        :return: ScansScanIssueResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.scans_scan_issue_with_http_info(account_id, id, issue_id, **kwargs)  # noqa: E501
        else:
            (data) = self.scans_scan_issue_with_http_info(account_id, id, issue_id, **kwargs)  # noqa: E501
            return data

    def scans_scan_issue_with_http_info(self, account_id, id, issue_id, **kwargs):  # noqa: E501
        """scans_scan_issue  # noqa: E501

        Returns a scan specific issue  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.scans_scan_issue_with_http_info(account_id, id, issue_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str id: The ID of the Security Test Scan (required)
        :param str issue_id: The ID of the Security Test Issue (required)
        :param str org_id: Harness Organization ID
        :param str project_id: Harness Project ID
        :param int page: Page number to fetch (starting from 0)
        :param int page_size: Number of results per page
        :param str sort: The field to sort by
        :param str order: The order to sort by
        :param str x_api_key: Harness personal or service access token
        :return: ScansScanIssueResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'id', 'issue_id', 'org_id', 'project_id', 'page', 'page_size', 'sort', 'order', 'x_api_key']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method scans_scan_issue" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `scans_scan_issue`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `scans_scan_issue`")  # noqa: E501
        # verify the required parameter 'issue_id' is set
        if ('issue_id' not in params or
                params['issue_id'] is None):
            raise ValueError("Missing the required parameter `issue_id` when calling `scans_scan_issue`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501
        if 'issue_id' in params:
            path_params['issueId'] = params['issue_id']  # noqa: E501

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501
        if 'org_id' in params:
            query_params.append(('orgId', params['org_id']))  # noqa: E501
        if 'project_id' in params:
            query_params.append(('projectId', params['project_id']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('pageSize', params['page_size']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501
        if 'order' in params:
            query_params.append(('order', params['order']))  # noqa: E501

        header_params = {}
        if 'x_api_key' in params:
            header_params['X-Api-Key'] = params['x_api_key']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/sto/api/v2/scans/{id}/issue/{issueId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ScansScanIssueResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def scans_scan_issue_counts(self, account_id, org_id, project_id, id, **kwargs):  # noqa: E501
        """scans_scan_issue_counts  # noqa: E501

        Returns counts of active Security Issues for a Security Test Scan  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.scans_scan_issue_counts(account_id, org_id, project_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param str id: The ID of the Security Test Scan for which to count issues (required)
        :param str x_api_key: Harness personal or service access token
        :return: ScansScanIssueCountsResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.scans_scan_issue_counts_with_http_info(account_id, org_id, project_id, id, **kwargs)  # noqa: E501
        else:
            (data) = self.scans_scan_issue_counts_with_http_info(account_id, org_id, project_id, id, **kwargs)  # noqa: E501
            return data

    def scans_scan_issue_counts_with_http_info(self, account_id, org_id, project_id, id, **kwargs):  # noqa: E501
        """scans_scan_issue_counts  # noqa: E501

        Returns counts of active Security Issues for a Security Test Scan  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.scans_scan_issue_counts_with_http_info(account_id, org_id, project_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param str id: The ID of the Security Test Scan for which to count issues (required)
        :param str x_api_key: Harness personal or service access token
        :return: ScansScanIssueCountsResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'org_id', 'project_id', 'id', 'x_api_key']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method scans_scan_issue_counts" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `scans_scan_issue_counts`")  # noqa: E501
        # verify the required parameter 'org_id' is set
        if ('org_id' not in params or
                params['org_id'] is None):
            raise ValueError("Missing the required parameter `org_id` when calling `scans_scan_issue_counts`")  # noqa: E501
        # verify the required parameter 'project_id' is set
        if ('project_id' not in params or
                params['project_id'] is None):
            raise ValueError("Missing the required parameter `project_id` when calling `scans_scan_issue_counts`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `scans_scan_issue_counts`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501
        if 'org_id' in params:
            query_params.append(('orgId', params['org_id']))  # noqa: E501
        if 'project_id' in params:
            query_params.append(('projectId', params['project_id']))  # noqa: E501

        header_params = {}
        if 'x_api_key' in params:
            header_params['X-Api-Key'] = params['x_api_key']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/sto/api/v2/scans/{id}/issues/counts', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ScansScanIssueCountsResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def scans_scan_issue_occurrences(self, account_id, id, issue_id, **kwargs):  # noqa: E501
        """scans_scan_issue_occurrences  # noqa: E501

        Returns occurrences for a scan specific issue  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.scans_scan_issue_occurrences(account_id, id, issue_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str id: The ID of the Security Test Scan (required)
        :param str issue_id: The ID of the Security Test Issue (required)
        :param str org_id: Harness Organization ID
        :param str project_id: Harness Project ID
        :param int page: Page number to fetch (starting from 0)
        :param int page_size: Number of results per page
        :param str search:
        :param str exemption_status:
        :param str sort: The field to sort by
        :param str order: The order to sort by
        :param str exemption_id: ID of Security Test Exemption
        :param str x_api_key: Harness personal or service access token
        :return: ScansScanIssueResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.scans_scan_issue_occurrences_with_http_info(account_id, id, issue_id, **kwargs)  # noqa: E501
        else:
            (data) = self.scans_scan_issue_occurrences_with_http_info(account_id, id, issue_id, **kwargs)  # noqa: E501
            return data

    def scans_scan_issue_occurrences_with_http_info(self, account_id, id, issue_id, **kwargs):  # noqa: E501
        """scans_scan_issue_occurrences  # noqa: E501

        Returns occurrences for a scan specific issue  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.scans_scan_issue_occurrences_with_http_info(account_id, id, issue_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str id: The ID of the Security Test Scan (required)
        :param str issue_id: The ID of the Security Test Issue (required)
        :param str org_id: Harness Organization ID
        :param str project_id: Harness Project ID
        :param int page: Page number to fetch (starting from 0)
        :param int page_size: Number of results per page
        :param str search:
        :param str exemption_status:
        :param str sort: The field to sort by
        :param str order: The order to sort by
        :param str exemption_id: ID of Security Test Exemption
        :param str x_api_key: Harness personal or service access token
        :return: ScansScanIssueResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'id', 'issue_id', 'org_id', 'project_id', 'page', 'page_size', 'search', 'exemption_status', 'sort', 'order', 'exemption_id', 'x_api_key']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method scans_scan_issue_occurrences" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `scans_scan_issue_occurrences`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `scans_scan_issue_occurrences`")  # noqa: E501
        # verify the required parameter 'issue_id' is set
        if ('issue_id' not in params or
                params['issue_id'] is None):
            raise ValueError("Missing the required parameter `issue_id` when calling `scans_scan_issue_occurrences`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501
        if 'issue_id' in params:
            path_params['issueId'] = params['issue_id']  # noqa: E501

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501
        if 'org_id' in params:
            query_params.append(('orgId', params['org_id']))  # noqa: E501
        if 'project_id' in params:
            query_params.append(('projectId', params['project_id']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('pageSize', params['page_size']))  # noqa: E501
        if 'search' in params:
            query_params.append(('search', params['search']))  # noqa: E501
        if 'exemption_status' in params:
            query_params.append(('exemptionStatus', params['exemption_status']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501
        if 'order' in params:
            query_params.append(('order', params['order']))  # noqa: E501
        if 'exemption_id' in params:
            query_params.append(('exemptionId', params['exemption_id']))  # noqa: E501

        header_params = {}
        if 'x_api_key' in params:
            header_params['X-Api-Key'] = params['x_api_key']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/sto/api/v2/scans/{id}/issue/{issueId}/occurrences', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ScansScanIssueResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def scans_scan_issues(self, account_id, id, **kwargs):  # noqa: E501
        """scans_scan_issues  # noqa: E501

        List Issues by Scan ID  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.scans_scan_issues(account_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str id: The Scan ID (required)
        :param str exempted: Chooses whether to show exempted issues (\"only\"), or non-exempted issues (\"0\" or \"false\")
        :param str x_api_key: Harness personal or service access token
        :return: ScansScanIssuesResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.scans_scan_issues_with_http_info(account_id, id, **kwargs)  # noqa: E501
        else:
            (data) = self.scans_scan_issues_with_http_info(account_id, id, **kwargs)  # noqa: E501
            return data

    def scans_scan_issues_with_http_info(self, account_id, id, **kwargs):  # noqa: E501
        """scans_scan_issues  # noqa: E501

        List Issues by Scan ID  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.scans_scan_issues_with_http_info(account_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str id: The Scan ID (required)
        :param str exempted: Chooses whether to show exempted issues (\"only\"), or non-exempted issues (\"0\" or \"false\")
        :param str x_api_key: Harness personal or service access token
        :return: ScansScanIssuesResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'id', 'exempted', 'x_api_key']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method scans_scan_issues" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `scans_scan_issues`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `scans_scan_issues`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501
        if 'exempted' in params:
            query_params.append(('exempted', params['exempted']))  # noqa: E501

        header_params = {}
        if 'x_api_key' in params:
            header_params['X-Api-Key'] = params['x_api_key']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/sto/api/v2/scans/{id}/issues', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ScansScanIssuesResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def scans_update_scan(self, body, account_id, id, **kwargs):  # noqa: E501
        """scans_update_scan  # noqa: E501

        Update an existing Security Test Scan  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.scans_update_scan(body, account_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateScanRequestBody body: (required)
        :param str account_id: Harness Account ID (required)
        :param str id: The ID of the Security Test Scan to update (required)
        :param str x_api_key: Harness personal or service access token
        :return: Scan
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.scans_update_scan_with_http_info(body, account_id, id, **kwargs)  # noqa: E501
        else:
            (data) = self.scans_update_scan_with_http_info(body, account_id, id, **kwargs)  # noqa: E501
            return data

    def scans_update_scan_with_http_info(self, body, account_id, id, **kwargs):  # noqa: E501
        """scans_update_scan  # noqa: E501

        Update an existing Security Test Scan  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.scans_update_scan_with_http_info(body, account_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateScanRequestBody body: (required)
        :param str account_id: Harness Account ID (required)
        :param str id: The ID of the Security Test Scan to update (required)
        :param str x_api_key: Harness personal or service access token
        :return: Scan
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'account_id', 'id', 'x_api_key']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method scans_update_scan" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `scans_update_scan`")  # noqa: E501
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `scans_update_scan`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `scans_update_scan`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501

        header_params = {}
        if 'x_api_key' in params:
            header_params['X-Api-Key'] = params['x_api_key']  # noqa: E501

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
            '/sto/api/v2/scans/{id}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Scan',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
