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


class DashboardsApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def clone_dashboard(self, body, **kwargs):  # noqa: E501
        """clone_dashboard  # noqa: E501

        Clone a dashboard.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.clone_dashboard(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CloneDashboardRequestBody body: Clone a Dashboard (required)
        :param str account_id:
        :return: ClonedDashboardResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.clone_dashboard_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.clone_dashboard_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def clone_dashboard_with_http_info(self, body, **kwargs):  # noqa: E501
        """clone_dashboard  # noqa: E501

        Clone a dashboard.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.clone_dashboard_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CloneDashboardRequestBody body: Clone a Dashboard (required)
        :param str account_id:
        :return: ClonedDashboardResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'account_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method clone_dashboard" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `clone_dashboard`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501

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
            '/dashboard/clone', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ClonedDashboardResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_dashboard(self, body, folder_id, **kwargs):  # noqa: E501
        """delete_dashboard  # noqa: E501

        Delete a dashboard.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_dashboard(body, folder_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param DeleteDashboardRequest body: Delete a Dashboard by ID. (required)
        :param str folder_id: (required)
        :param str account_id:
        :return: DeleteDashboardResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_dashboard_with_http_info(body, folder_id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_dashboard_with_http_info(body, folder_id, **kwargs)  # noqa: E501
            return data

    def delete_dashboard_with_http_info(self, body, folder_id, **kwargs):  # noqa: E501
        """delete_dashboard  # noqa: E501

        Delete a dashboard.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_dashboard_with_http_info(body, folder_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param DeleteDashboardRequest body: Delete a Dashboard by ID. (required)
        :param str folder_id: (required)
        :param str account_id:
        :return: DeleteDashboardResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'folder_id', 'account_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_dashboard" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `delete_dashboard`")  # noqa: E501
        # verify the required parameter 'folder_id' is set
        if ('folder_id' not in params or
                params['folder_id'] is None):
            raise ValueError("Missing the required parameter `folder_id` when calling `delete_dashboard`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501
        if 'folder_id' in params:
            query_params.append(('folderId', params['folder_id']))  # noqa: E501

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
            '/dashboard/remove', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DeleteDashboardResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_dashboard(self, dashboard_id, **kwargs):  # noqa: E501
        """get_dashboard  # noqa: E501

        Get all details of a dashboard by ID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_dashboard(dashboard_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str dashboard_id: (required)
        :param str account_id:
        :return: GetDashboardResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_dashboard_with_http_info(dashboard_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_dashboard_with_http_info(dashboard_id, **kwargs)  # noqa: E501
            return data

    def get_dashboard_with_http_info(self, dashboard_id, **kwargs):  # noqa: E501
        """get_dashboard  # noqa: E501

        Get all details of a dashboard by ID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_dashboard_with_http_info(dashboard_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str dashboard_id: (required)
        :param str account_id:
        :return: GetDashboardResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['dashboard_id', 'account_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_dashboard" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'dashboard_id' is set
        if ('dashboard_id' not in params or
                params['dashboard_id'] is None):
            raise ValueError("Missing the required parameter `dashboard_id` when calling `get_dashboard`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'dashboard_id' in params:
            path_params['dashboard_id'] = params['dashboard_id']  # noqa: E501

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
            '/dashboard/dashboards/{dashboard_id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetDashboardResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_dashboard_data(self, dashboard_id, file_type, **kwargs):  # noqa: E501
        """Download data within a Dashboard  # noqa: E501

        Download the data of all tiles within a Dashboard.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_dashboard_data(dashboard_id, file_type, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str dashboard_id: (required)
        :param str file_type: (required)
        :param str filters:
        :return: DashboardDownloadResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_dashboard_data_with_http_info(dashboard_id, file_type, **kwargs)  # noqa: E501
        else:
            (data) = self.get_dashboard_data_with_http_info(dashboard_id, file_type, **kwargs)  # noqa: E501
            return data

    def get_dashboard_data_with_http_info(self, dashboard_id, file_type, **kwargs):  # noqa: E501
        """Download data within a Dashboard  # noqa: E501

        Download the data of all tiles within a Dashboard.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_dashboard_data_with_http_info(dashboard_id, file_type, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str dashboard_id: (required)
        :param str file_type: (required)
        :param str filters:
        :return: DashboardDownloadResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['dashboard_id', 'file_type', 'filters']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_dashboard_data" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'dashboard_id' is set
        if ('dashboard_id' not in params or
                params['dashboard_id'] is None):
            raise ValueError("Missing the required parameter `dashboard_id` when calling `get_dashboard_data`")  # noqa: E501
        # verify the required parameter 'file_type' is set
        if ('file_type' not in params or
                params['file_type'] is None):
            raise ValueError("Missing the required parameter `file_type` when calling `get_dashboard_data`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'dashboard_id' in params:
            path_params['dashboard_id'] = params['dashboard_id']  # noqa: E501

        query_params = []
        if 'file_type' in params:
            query_params.append(('file_type', params['file_type']))  # noqa: E501
        if 'filters' in params:
            query_params.append(('filters', params['filters']))  # noqa: E501

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
            '/dashboard/api/dashboards/{dashboard_id}/download', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DashboardDownloadResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_dashboard_download_csv(self, dashboard_id, **kwargs):  # noqa: E501
        """Download a Dashboard CSV  # noqa: E501

        Download a Dashboard in CSV format.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_dashboard_download_csv(dashboard_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str dashboard_id: (required)
        :param str account_id:
        :param str filters:
        :param bool expanded_tables:
        :return: DownloadCsvDashboardResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_dashboard_download_csv_with_http_info(dashboard_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_dashboard_download_csv_with_http_info(dashboard_id, **kwargs)  # noqa: E501
            return data

    def get_dashboard_download_csv_with_http_info(self, dashboard_id, **kwargs):  # noqa: E501
        """Download a Dashboard CSV  # noqa: E501

        Download a Dashboard in CSV format.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_dashboard_download_csv_with_http_info(dashboard_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str dashboard_id: (required)
        :param str account_id:
        :param str filters:
        :param bool expanded_tables:
        :return: DownloadCsvDashboardResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['dashboard_id', 'account_id', 'filters', 'expanded_tables']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_dashboard_download_csv" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'dashboard_id' is set
        if ('dashboard_id' not in params or
                params['dashboard_id'] is None):
            raise ValueError("Missing the required parameter `dashboard_id` when calling `get_dashboard_download_csv`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'dashboard_id' in params:
            path_params['dashboard_id'] = params['dashboard_id']  # noqa: E501

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501
        if 'filters' in params:
            query_params.append(('filters', params['filters']))  # noqa: E501
        if 'expanded_tables' in params:
            query_params.append(('expanded_tables', params['expanded_tables']))  # noqa: E501

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
            '/dashboard/download/dashboards/{dashboard_id}/csv', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DownloadCsvDashboardResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_dashboard_download_pdf(self, dashboard_id, **kwargs):  # noqa: E501
        """Download a Dashboard PDF  # noqa: E501

        Download a Dashboard in PDF format.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_dashboard_download_pdf(dashboard_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str dashboard_id: (required)
        :param str account_id:
        :param str filters:
        :param bool expanded_tables:
        :param bool landscape:
        :param str paper_size:
        :param str style:
        :return: DownloadPdfDashboardResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_dashboard_download_pdf_with_http_info(dashboard_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_dashboard_download_pdf_with_http_info(dashboard_id, **kwargs)  # noqa: E501
            return data

    def get_dashboard_download_pdf_with_http_info(self, dashboard_id, **kwargs):  # noqa: E501
        """Download a Dashboard PDF  # noqa: E501

        Download a Dashboard in PDF format.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_dashboard_download_pdf_with_http_info(dashboard_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str dashboard_id: (required)
        :param str account_id:
        :param str filters:
        :param bool expanded_tables:
        :param bool landscape:
        :param str paper_size:
        :param str style:
        :return: DownloadPdfDashboardResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['dashboard_id', 'account_id', 'filters', 'expanded_tables', 'landscape', 'paper_size', 'style']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_dashboard_download_pdf" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'dashboard_id' is set
        if ('dashboard_id' not in params or
                params['dashboard_id'] is None):
            raise ValueError("Missing the required parameter `dashboard_id` when calling `get_dashboard_download_pdf`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'dashboard_id' in params:
            path_params['dashboard_id'] = params['dashboard_id']  # noqa: E501

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501
        if 'filters' in params:
            query_params.append(('filters', params['filters']))  # noqa: E501
        if 'expanded_tables' in params:
            query_params.append(('expanded_tables', params['expanded_tables']))  # noqa: E501
        if 'landscape' in params:
            query_params.append(('landscape', params['landscape']))  # noqa: E501
        if 'paper_size' in params:
            query_params.append(('paper_size', params['paper_size']))  # noqa: E501
        if 'style' in params:
            query_params.append(('style', params['style']))  # noqa: E501

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
            '/dashboard/download/dashboards/{dashboard_id}/pdf', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DownloadPdfDashboardResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_dashboard_elements(self, dashboard_id, **kwargs):  # noqa: E501
        """get_dashboard_elements  # noqa: E501

        Get all elements within a dashboard by ID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_dashboard_elements(dashboard_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str dashboard_id: (required)
        :param str account_id:
        :return: GetDashboardElementsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_dashboard_elements_with_http_info(dashboard_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_dashboard_elements_with_http_info(dashboard_id, **kwargs)  # noqa: E501
            return data

    def get_dashboard_elements_with_http_info(self, dashboard_id, **kwargs):  # noqa: E501
        """get_dashboard_elements  # noqa: E501

        Get all elements within a dashboard by ID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_dashboard_elements_with_http_info(dashboard_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str dashboard_id: (required)
        :param str account_id:
        :return: GetDashboardElementsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['dashboard_id', 'account_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_dashboard_elements" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'dashboard_id' is set
        if ('dashboard_id' not in params or
                params['dashboard_id'] is None):
            raise ValueError("Missing the required parameter `dashboard_id` when calling `get_dashboard_elements`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'dashboard_id' in params:
            path_params['dashboard_id'] = params['dashboard_id']  # noqa: E501

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
            '/dashboard/dashboards/{dashboard_id}/elements', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetDashboardElementsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_dashboard_filters(self, dashboard_id, **kwargs):  # noqa: E501
        """get_dashboard_filters  # noqa: E501

        Get all filters within a dashboard by ID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_dashboard_filters(dashboard_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str dashboard_id: (required)
        :param str account_id:
        :return: GetDashboardFiltersResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_dashboard_filters_with_http_info(dashboard_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_dashboard_filters_with_http_info(dashboard_id, **kwargs)  # noqa: E501
            return data

    def get_dashboard_filters_with_http_info(self, dashboard_id, **kwargs):  # noqa: E501
        """get_dashboard_filters  # noqa: E501

        Get all filters within a dashboard by ID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_dashboard_filters_with_http_info(dashboard_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str dashboard_id: (required)
        :param str account_id:
        :return: GetDashboardFiltersResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['dashboard_id', 'account_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_dashboard_filters" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'dashboard_id' is set
        if ('dashboard_id' not in params or
                params['dashboard_id'] is None):
            raise ValueError("Missing the required parameter `dashboard_id` when calling `get_dashboard_filters`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'dashboard_id' in params:
            path_params['dashboard_id'] = params['dashboard_id']  # noqa: E501

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
            '/dashboard/dashboards/{dashboard_id}/filters', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetDashboardFiltersResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def schedules_run_once(self, body, **kwargs):  # noqa: E501
        """Runs a schedule delivery once that is then immediately sent via email to recipients  # noqa: E501

        Run a schedule delivery once  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.schedules_run_once(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ScheduleReportRequestBody body: Run a Dashboard Schedule Delivery once (required)
        :param str account_id:
        :return: ScheduleReportResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.schedules_run_once_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.schedules_run_once_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def schedules_run_once_with_http_info(self, body, **kwargs):  # noqa: E501
        """Runs a schedule delivery once that is then immediately sent via email to recipients  # noqa: E501

        Run a schedule delivery once  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.schedules_run_once_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ScheduleReportRequestBody body: Run a Dashboard Schedule Delivery once (required)
        :param str account_id:
        :return: ScheduleReportResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'account_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method schedules_run_once" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `schedules_run_once`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501

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
            '/dashboard/schedules/run_once', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ScheduleReportResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_dashboard(self, body, **kwargs):  # noqa: E501
        """update_dashboard  # noqa: E501

        Update a dashboards name, tags or folder.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_dashboard(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateDashboardRequest body: Update dashboard fields. (required)
        :param str account_id:
        :return: UpdateDashboardResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_dashboard_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.update_dashboard_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def update_dashboard_with_http_info(self, body, **kwargs):  # noqa: E501
        """update_dashboard  # noqa: E501

        Update a dashboards name, tags or folder.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_dashboard_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateDashboardRequest body: Update dashboard fields. (required)
        :param str account_id:
        :return: UpdateDashboardResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'account_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_dashboard" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update_dashboard`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501

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
            '/dashboard/', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UpdateDashboardResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_dashboard_filter(self, body, dashboard_id, filter_id, **kwargs):  # noqa: E501
        """update_dashboard_filter  # noqa: E501

        Update a specific filter within a dashboard by ID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_dashboard_filter(body, dashboard_id, filter_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateDashboardFilterRequest body: (required)
        :param str dashboard_id: (required)
        :param str filter_id: (required)
        :return: GetDashboardFilterResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_dashboard_filter_with_http_info(body, dashboard_id, filter_id, **kwargs)  # noqa: E501
        else:
            (data) = self.update_dashboard_filter_with_http_info(body, dashboard_id, filter_id, **kwargs)  # noqa: E501
            return data

    def update_dashboard_filter_with_http_info(self, body, dashboard_id, filter_id, **kwargs):  # noqa: E501
        """update_dashboard_filter  # noqa: E501

        Update a specific filter within a dashboard by ID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_dashboard_filter_with_http_info(body, dashboard_id, filter_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateDashboardFilterRequest body: (required)
        :param str dashboard_id: (required)
        :param str filter_id: (required)
        :return: GetDashboardFilterResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'dashboard_id', 'filter_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_dashboard_filter" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update_dashboard_filter`")  # noqa: E501
        # verify the required parameter 'dashboard_id' is set
        if ('dashboard_id' not in params or
                params['dashboard_id'] is None):
            raise ValueError("Missing the required parameter `dashboard_id` when calling `update_dashboard_filter`")  # noqa: E501
        # verify the required parameter 'filter_id' is set
        if ('filter_id' not in params or
                params['filter_id'] is None):
            raise ValueError("Missing the required parameter `filter_id` when calling `update_dashboard_filter`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'dashboard_id' in params:
            path_params['dashboard_id'] = params['dashboard_id']  # noqa: E501
        if 'filter_id' in params:
            path_params['filter_id'] = params['filter_id']  # noqa: E501

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
            '/dashboard/dashboards/{dashboard_id}/filters/{filter_id}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetDashboardFilterResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
