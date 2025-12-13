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


class FrontendApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def frontend_all_issues_details(self, account_id, org_id, project_id, issue_id, **kwargs):  # noqa: E501
        """frontend_all_issues_details  # noqa: E501

        Provides issue details for a project's latest baseline scans  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_all_issues_details(account_id, org_id, project_id, issue_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param str issue_id: The ID of the Security Issue (required)
        :param str exemption_statuses:
        :param str search:
        :param int page: Page number to fetch (starting from 0)
        :param int page_size: Number of results per page
        :return: FrontendAllIssuesDetailsResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.frontend_all_issues_details_with_http_info(account_id, org_id, project_id, issue_id, **kwargs)  # noqa: E501
        else:
            (data) = self.frontend_all_issues_details_with_http_info(account_id, org_id, project_id, issue_id, **kwargs)  # noqa: E501
            return data

    def frontend_all_issues_details_with_http_info(self, account_id, org_id, project_id, issue_id, **kwargs):  # noqa: E501
        """frontend_all_issues_details  # noqa: E501

        Provides issue details for a project's latest baseline scans  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_all_issues_details_with_http_info(account_id, org_id, project_id, issue_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param str issue_id: The ID of the Security Issue (required)
        :param str exemption_statuses:
        :param str search:
        :param int page: Page number to fetch (starting from 0)
        :param int page_size: Number of results per page
        :return: FrontendAllIssuesDetailsResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'org_id', 'project_id', 'issue_id', 'exemption_statuses', 'search', 'page', 'page_size']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method frontend_all_issues_details" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `frontend_all_issues_details`")  # noqa: E501
        # verify the required parameter 'org_id' is set
        if ('org_id' not in params or
                params['org_id'] is None):
            raise ValueError("Missing the required parameter `org_id` when calling `frontend_all_issues_details`")  # noqa: E501
        # verify the required parameter 'project_id' is set
        if ('project_id' not in params or
                params['project_id'] is None):
            raise ValueError("Missing the required parameter `project_id` when calling `frontend_all_issues_details`")  # noqa: E501
        # verify the required parameter 'issue_id' is set
        if ('issue_id' not in params or
                params['issue_id'] is None):
            raise ValueError("Missing the required parameter `issue_id` when calling `frontend_all_issues_details`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'issue_id' in params:
            path_params['issueId'] = params['issue_id']  # noqa: E501

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501
        if 'org_id' in params:
            query_params.append(('orgId', params['org_id']))  # noqa: E501
        if 'project_id' in params:
            query_params.append(('projectId', params['project_id']))  # noqa: E501
        if 'exemption_statuses' in params:
            query_params.append(('exemptionStatuses', params['exemption_statuses']))  # noqa: E501
        if 'search' in params:
            query_params.append(('search', params['search']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('pageSize', params['page_size']))  # noqa: E501

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
            '/sto/api/v2/frontend/all-issues/issues/{issueId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FrontendAllIssuesDetailsResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def frontend_all_issues_filters(self, account_id, org_id, project_id, **kwargs):  # noqa: E501
        """frontend_all_issues_filters  # noqa: E501

        Provide list of filters for a projects latest baseline scans  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_all_issues_filters(account_id, org_id, project_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :return: FrontendAllIssuesFiltersResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.frontend_all_issues_filters_with_http_info(account_id, org_id, project_id, **kwargs)  # noqa: E501
        else:
            (data) = self.frontend_all_issues_filters_with_http_info(account_id, org_id, project_id, **kwargs)  # noqa: E501
            return data

    def frontend_all_issues_filters_with_http_info(self, account_id, org_id, project_id, **kwargs):  # noqa: E501
        """frontend_all_issues_filters  # noqa: E501

        Provide list of filters for a projects latest baseline scans  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_all_issues_filters_with_http_info(account_id, org_id, project_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :return: FrontendAllIssuesFiltersResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'org_id', 'project_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method frontend_all_issues_filters" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `frontend_all_issues_filters`")  # noqa: E501
        # verify the required parameter 'org_id' is set
        if ('org_id' not in params or
                params['org_id'] is None):
            raise ValueError("Missing the required parameter `org_id` when calling `frontend_all_issues_filters`")  # noqa: E501
        # verify the required parameter 'project_id' is set
        if ('project_id' not in params or
                params['project_id'] is None):
            raise ValueError("Missing the required parameter `project_id` when calling `frontend_all_issues_filters`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501
        if 'org_id' in params:
            query_params.append(('orgId', params['org_id']))  # noqa: E501
        if 'project_id' in params:
            query_params.append(('projectId', params['project_id']))  # noqa: E501

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
            '/sto/api/v2/frontend/all-issues/filters', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FrontendAllIssuesFiltersResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def frontend_all_issues_list(self, account_id, org_id, project_id, **kwargs):  # noqa: E501
        """frontend_all_issues_list  # noqa: E501

        Provides a paginated list of issues for a project found in the latest baseline scans  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_all_issues_list(account_id, org_id, project_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param int page: Page number to fetch (starting from 0)
        :param int page_size: Number of results per page
        :param str target_ids:
        :param str target_types:
        :param str pipeline_ids:
        :param str scan_tools:
        :param str severity_codes:
        :param str exemption_statuses:
        :param str search:
        :param str issue_types:
        :param str statuses:
        :return: FrontendAllIssuesListResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.frontend_all_issues_list_with_http_info(account_id, org_id, project_id, **kwargs)  # noqa: E501
        else:
            (data) = self.frontend_all_issues_list_with_http_info(account_id, org_id, project_id, **kwargs)  # noqa: E501
            return data

    def frontend_all_issues_list_with_http_info(self, account_id, org_id, project_id, **kwargs):  # noqa: E501
        """frontend_all_issues_list  # noqa: E501

        Provides a paginated list of issues for a project found in the latest baseline scans  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_all_issues_list_with_http_info(account_id, org_id, project_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param int page: Page number to fetch (starting from 0)
        :param int page_size: Number of results per page
        :param str target_ids:
        :param str target_types:
        :param str pipeline_ids:
        :param str scan_tools:
        :param str severity_codes:
        :param str exemption_statuses:
        :param str search:
        :param str issue_types:
        :param str statuses:
        :return: FrontendAllIssuesListResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'org_id', 'project_id', 'page', 'page_size', 'target_ids', 'target_types', 'pipeline_ids', 'scan_tools', 'severity_codes', 'exemption_statuses', 'search', 'issue_types', 'statuses']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method frontend_all_issues_list" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `frontend_all_issues_list`")  # noqa: E501
        # verify the required parameter 'org_id' is set
        if ('org_id' not in params or
                params['org_id'] is None):
            raise ValueError("Missing the required parameter `org_id` when calling `frontend_all_issues_list`")  # noqa: E501
        # verify the required parameter 'project_id' is set
        if ('project_id' not in params or
                params['project_id'] is None):
            raise ValueError("Missing the required parameter `project_id` when calling `frontend_all_issues_list`")  # noqa: E501

        collection_formats = {}

        path_params = {}

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
        if 'target_ids' in params:
            query_params.append(('targetIds', params['target_ids']))  # noqa: E501
        if 'target_types' in params:
            query_params.append(('targetTypes', params['target_types']))  # noqa: E501
        if 'pipeline_ids' in params:
            query_params.append(('pipelineIds', params['pipeline_ids']))  # noqa: E501
        if 'scan_tools' in params:
            query_params.append(('scanTools', params['scan_tools']))  # noqa: E501
        if 'severity_codes' in params:
            query_params.append(('severityCodes', params['severity_codes']))  # noqa: E501
        if 'exemption_statuses' in params:
            query_params.append(('exemptionStatuses', params['exemption_statuses']))  # noqa: E501
        if 'search' in params:
            query_params.append(('search', params['search']))  # noqa: E501
        if 'issue_types' in params:
            query_params.append(('issueTypes', params['issue_types']))  # noqa: E501
        if 'statuses' in params:
            query_params.append(('statuses', params['statuses']))  # noqa: E501

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
            '/sto/api/v2/frontend/all-issues/issues', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FrontendAllIssuesListResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def frontend_all_issues_occurrence_details(self, account_id, org_id, project_id, issue_id, target_id, **kwargs):  # noqa: E501
        """frontend_all_issues_occurrence_details  # noqa: E501

        Provide list of filters for the latest scans of a baseline  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_all_issues_occurrence_details(account_id, org_id, project_id, issue_id, target_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param str issue_id: The ID of the Security Issue (required)
        :param str target_id: Associated Target ID (required)
        :param int page: Page number to fetch (starting from 0)
        :param int page_size: Number of results per page
        :param str exemption_statuses:
        :param str search:
        :return: FrontendAllIssuesOccurrenceDetailsResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.frontend_all_issues_occurrence_details_with_http_info(account_id, org_id, project_id, issue_id, target_id, **kwargs)  # noqa: E501
        else:
            (data) = self.frontend_all_issues_occurrence_details_with_http_info(account_id, org_id, project_id, issue_id, target_id, **kwargs)  # noqa: E501
            return data

    def frontend_all_issues_occurrence_details_with_http_info(self, account_id, org_id, project_id, issue_id, target_id, **kwargs):  # noqa: E501
        """frontend_all_issues_occurrence_details  # noqa: E501

        Provide list of filters for the latest scans of a baseline  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_all_issues_occurrence_details_with_http_info(account_id, org_id, project_id, issue_id, target_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param str issue_id: The ID of the Security Issue (required)
        :param str target_id: Associated Target ID (required)
        :param int page: Page number to fetch (starting from 0)
        :param int page_size: Number of results per page
        :param str exemption_statuses:
        :param str search:
        :return: FrontendAllIssuesOccurrenceDetailsResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'org_id', 'project_id', 'issue_id', 'target_id', 'page', 'page_size', 'exemption_statuses', 'search']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method frontend_all_issues_occurrence_details" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `frontend_all_issues_occurrence_details`")  # noqa: E501
        # verify the required parameter 'org_id' is set
        if ('org_id' not in params or
                params['org_id'] is None):
            raise ValueError("Missing the required parameter `org_id` when calling `frontend_all_issues_occurrence_details`")  # noqa: E501
        # verify the required parameter 'project_id' is set
        if ('project_id' not in params or
                params['project_id'] is None):
            raise ValueError("Missing the required parameter `project_id` when calling `frontend_all_issues_occurrence_details`")  # noqa: E501
        # verify the required parameter 'issue_id' is set
        if ('issue_id' not in params or
                params['issue_id'] is None):
            raise ValueError("Missing the required parameter `issue_id` when calling `frontend_all_issues_occurrence_details`")  # noqa: E501
        # verify the required parameter 'target_id' is set
        if ('target_id' not in params or
                params['target_id'] is None):
            raise ValueError("Missing the required parameter `target_id` when calling `frontend_all_issues_occurrence_details`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'issue_id' in params:
            path_params['issueId'] = params['issue_id']  # noqa: E501
        if 'target_id' in params:
            path_params['targetId'] = params['target_id']  # noqa: E501

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
        if 'exemption_statuses' in params:
            query_params.append(('exemptionStatuses', params['exemption_statuses']))  # noqa: E501
        if 'search' in params:
            query_params.append(('search', params['search']))  # noqa: E501

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
            '/sto/api/v2/frontend/all-issues/issues/{issueId}/targets/{targetId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FrontendAllIssuesOccurrenceDetailsResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def frontend_execution_issue_counts(self, account_id, org_id, project_id, execution_ids, **kwargs):  # noqa: E501
        """frontend_execution_issue_counts  # noqa: E501

        Returns counts of active Security Issues for one or more Pipeline Executions  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_execution_issue_counts(account_id, org_id, project_id, execution_ids, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param str execution_ids: Comma-separated list of Harness Execution IDs for which to count Security Issues (required)
        :return: dict(str, IssueCounts)
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.frontend_execution_issue_counts_with_http_info(account_id, org_id, project_id, execution_ids, **kwargs)  # noqa: E501
        else:
            (data) = self.frontend_execution_issue_counts_with_http_info(account_id, org_id, project_id, execution_ids, **kwargs)  # noqa: E501
            return data

    def frontend_execution_issue_counts_with_http_info(self, account_id, org_id, project_id, execution_ids, **kwargs):  # noqa: E501
        """frontend_execution_issue_counts  # noqa: E501

        Returns counts of active Security Issues for one or more Pipeline Executions  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_execution_issue_counts_with_http_info(account_id, org_id, project_id, execution_ids, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param str execution_ids: Comma-separated list of Harness Execution IDs for which to count Security Issues (required)
        :return: dict(str, IssueCounts)
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'org_id', 'project_id', 'execution_ids']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method frontend_execution_issue_counts" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `frontend_execution_issue_counts`")  # noqa: E501
        # verify the required parameter 'org_id' is set
        if ('org_id' not in params or
                params['org_id'] is None):
            raise ValueError("Missing the required parameter `org_id` when calling `frontend_execution_issue_counts`")  # noqa: E501
        # verify the required parameter 'project_id' is set
        if ('project_id' not in params or
                params['project_id'] is None):
            raise ValueError("Missing the required parameter `project_id` when calling `frontend_execution_issue_counts`")  # noqa: E501
        # verify the required parameter 'execution_ids' is set
        if ('execution_ids' not in params or
                params['execution_ids'] is None):
            raise ValueError("Missing the required parameter `execution_ids` when calling `frontend_execution_issue_counts`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501
        if 'org_id' in params:
            query_params.append(('orgId', params['org_id']))  # noqa: E501
        if 'project_id' in params:
            query_params.append(('projectId', params['project_id']))  # noqa: E501
        if 'execution_ids' in params:
            query_params.append(('executionIds', params['execution_ids']))  # noqa: E501

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
            '/sto/api/v2/frontend/issue-counts', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='dict(str, IssueCounts)',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def frontend_expiring_exemptions(self, account_id, org_id, project_id, execution_id, **kwargs):  # noqa: E501
        """frontend_expiring_exemptions  # noqa: E501

        Returns issue summaries that are going to expire  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_expiring_exemptions(account_id, org_id, project_id, execution_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param str execution_id: Harness pipeline execution ID (required)
        :param int days: Number of days of Baseline Issue counts to return
        :return: FrontendExpiringExemptionsResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.frontend_expiring_exemptions_with_http_info(account_id, org_id, project_id, execution_id, **kwargs)  # noqa: E501
        else:
            (data) = self.frontend_expiring_exemptions_with_http_info(account_id, org_id, project_id, execution_id, **kwargs)  # noqa: E501
            return data

    def frontend_expiring_exemptions_with_http_info(self, account_id, org_id, project_id, execution_id, **kwargs):  # noqa: E501
        """frontend_expiring_exemptions  # noqa: E501

        Returns issue summaries that are going to expire  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_expiring_exemptions_with_http_info(account_id, org_id, project_id, execution_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param str execution_id: Harness pipeline execution ID (required)
        :param int days: Number of days of Baseline Issue counts to return
        :return: FrontendExpiringExemptionsResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'org_id', 'project_id', 'execution_id', 'days']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method frontend_expiring_exemptions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `frontend_expiring_exemptions`")  # noqa: E501
        # verify the required parameter 'org_id' is set
        if ('org_id' not in params or
                params['org_id'] is None):
            raise ValueError("Missing the required parameter `org_id` when calling `frontend_expiring_exemptions`")  # noqa: E501
        # verify the required parameter 'project_id' is set
        if ('project_id' not in params or
                params['project_id'] is None):
            raise ValueError("Missing the required parameter `project_id` when calling `frontend_expiring_exemptions`")  # noqa: E501
        # verify the required parameter 'execution_id' is set
        if ('execution_id' not in params or
                params['execution_id'] is None):
            raise ValueError("Missing the required parameter `execution_id` when calling `frontend_expiring_exemptions`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'execution_id' in params:
            path_params['executionId'] = params['execution_id']  # noqa: E501

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501
        if 'org_id' in params:
            query_params.append(('orgId', params['org_id']))  # noqa: E501
        if 'project_id' in params:
            query_params.append(('projectId', params['project_id']))  # noqa: E501
        if 'days' in params:
            query_params.append(('days', params['days']))  # noqa: E501

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
            '/sto/api/v2/frontend/expiring-exemptions/{executionId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FrontendExpiringExemptionsResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def frontend_global_exemptions(self, body, account_id, status, **kwargs):  # noqa: E501
        """frontend_global_exemptions  # noqa: E501

        Provides data needed by the Global Exemptions Security Review page  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_global_exemptions(body, account_id, status, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param GlobalExemptionsRequestBody body: (required)
        :param str account_id: Harness Account ID (required)
        :param str status: Exemption status (required)
        :param str x_api_key: Harness personal or service access token
        :param str org_id: Harness Organization ID
        :param str project_id: Harness Project ID
        :param int page: Page number to fetch (starting from 0)
        :param int page_size: Number of results per page
        :param str search:
        :return: FrontendSecurityReviewResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.frontend_global_exemptions_with_http_info(body, account_id, status, **kwargs)  # noqa: E501
        else:
            (data) = self.frontend_global_exemptions_with_http_info(body, account_id, status, **kwargs)  # noqa: E501
            return data

    def frontend_global_exemptions_with_http_info(self, body, account_id, status, **kwargs):  # noqa: E501
        """frontend_global_exemptions  # noqa: E501

        Provides data needed by the Global Exemptions Security Review page  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_global_exemptions_with_http_info(body, account_id, status, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param GlobalExemptionsRequestBody body: (required)
        :param str account_id: Harness Account ID (required)
        :param str status: Exemption status (required)
        :param str x_api_key: Harness personal or service access token
        :param str org_id: Harness Organization ID
        :param str project_id: Harness Project ID
        :param int page: Page number to fetch (starting from 0)
        :param int page_size: Number of results per page
        :param str search:
        :return: FrontendSecurityReviewResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'account_id', 'status', 'x_api_key', 'org_id', 'project_id', 'page', 'page_size', 'search']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method frontend_global_exemptions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `frontend_global_exemptions`")  # noqa: E501
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `frontend_global_exemptions`")  # noqa: E501
        # verify the required parameter 'status' is set
        if ('status' not in params or
                params['status'] is None):
            raise ValueError("Missing the required parameter `status` when calling `frontend_global_exemptions`")  # noqa: E501

        collection_formats = {}

        path_params = {}

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
        if 'status' in params:
            query_params.append(('status', params['status']))  # noqa: E501
        if 'search' in params:
            query_params.append(('search', params['search']))  # noqa: E501

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
            '/sto/api/v2/frontend/exemptions', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FrontendSecurityReviewResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def frontend_impacted_targets_for_exemption(self, account_id, exemption_id, **kwargs):  # noqa: E501
        """frontend_impacted_targets_for_exemption  # noqa: E501

        Returns a list of impacted target details for an exemption id  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_impacted_targets_for_exemption(account_id, exemption_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str exemption_id: ID of Security Test Exemption (required)
        :param str org_id: Harness Organization ID
        :param str project_id: Harness Project ID
        :param int page: Page number to fetch (starting from 0)
        :param int page_size: Number of results per page
        :param str search:
        :return: FrontendImpactedTargetsForExemptionResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.frontend_impacted_targets_for_exemption_with_http_info(account_id, exemption_id, **kwargs)  # noqa: E501
        else:
            (data) = self.frontend_impacted_targets_for_exemption_with_http_info(account_id, exemption_id, **kwargs)  # noqa: E501
            return data

    def frontend_impacted_targets_for_exemption_with_http_info(self, account_id, exemption_id, **kwargs):  # noqa: E501
        """frontend_impacted_targets_for_exemption  # noqa: E501

        Returns a list of impacted target details for an exemption id  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_impacted_targets_for_exemption_with_http_info(account_id, exemption_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str exemption_id: ID of Security Test Exemption (required)
        :param str org_id: Harness Organization ID
        :param str project_id: Harness Project ID
        :param int page: Page number to fetch (starting from 0)
        :param int page_size: Number of results per page
        :param str search:
        :return: FrontendImpactedTargetsForExemptionResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'exemption_id', 'org_id', 'project_id', 'page', 'page_size', 'search']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method frontend_impacted_targets_for_exemption" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `frontend_impacted_targets_for_exemption`")  # noqa: E501
        # verify the required parameter 'exemption_id' is set
        if ('exemption_id' not in params or
                params['exemption_id'] is None):
            raise ValueError("Missing the required parameter `exemption_id` when calling `frontend_impacted_targets_for_exemption`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'exemption_id' in params:
            path_params['exemptionId'] = params['exemption_id']  # noqa: E501

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
            '/sto/api/v2/frontend/exemption/{exemptionId}/targets', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FrontendImpactedTargetsForExemptionResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def frontend_issue_for_exemption(self, account_id, exemption_id, **kwargs):  # noqa: E501
        """frontend_issue_for_exemption  # noqa: E501

        Returns a specific issue exemption  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_issue_for_exemption(account_id, exemption_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str exemption_id: ID of Security Test Exemption (required)
        :param str org_id: Harness Organization ID
        :param str project_id: Harness Project ID
        :param str target_id: Harness STO Target ID
        :param int page: Page number to fetch (starting from 0)
        :param int page_size: Number of results per page
        :return: FrontendIssueForExemptionResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.frontend_issue_for_exemption_with_http_info(account_id, exemption_id, **kwargs)  # noqa: E501
        else:
            (data) = self.frontend_issue_for_exemption_with_http_info(account_id, exemption_id, **kwargs)  # noqa: E501
            return data

    def frontend_issue_for_exemption_with_http_info(self, account_id, exemption_id, **kwargs):  # noqa: E501
        """frontend_issue_for_exemption  # noqa: E501

        Returns a specific issue exemption  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_issue_for_exemption_with_http_info(account_id, exemption_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str exemption_id: ID of Security Test Exemption (required)
        :param str org_id: Harness Organization ID
        :param str project_id: Harness Project ID
        :param str target_id: Harness STO Target ID
        :param int page: Page number to fetch (starting from 0)
        :param int page_size: Number of results per page
        :return: FrontendIssueForExemptionResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'exemption_id', 'org_id', 'project_id', 'target_id', 'page', 'page_size']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method frontend_issue_for_exemption" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `frontend_issue_for_exemption`")  # noqa: E501
        # verify the required parameter 'exemption_id' is set
        if ('exemption_id' not in params or
                params['exemption_id'] is None):
            raise ValueError("Missing the required parameter `exemption_id` when calling `frontend_issue_for_exemption`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'exemption_id' in params:
            path_params['exemptionId'] = params['exemption_id']  # noqa: E501

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501
        if 'org_id' in params:
            query_params.append(('orgId', params['org_id']))  # noqa: E501
        if 'project_id' in params:
            query_params.append(('projectId', params['project_id']))  # noqa: E501
        if 'target_id' in params:
            query_params.append(('targetId', params['target_id']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('pageSize', params['page_size']))  # noqa: E501

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
            '/sto/api/v2/frontend/issue-exemption/{exemptionId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FrontendIssueForExemptionResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def frontend_issue_severity_change(self, account_id, org_id, project_id, issue_id, exemption_id, **kwargs):  # noqa: E501
        """frontend_issue_severity_change  # noqa: E501

        Provides the severity change for an issue when approving occurrence level exemption  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_issue_severity_change(account_id, org_id, project_id, issue_id, exemption_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param str issue_id: The ID of the Security Issue (required)
        :param str exemption_id: ID of Security Test Exemption (required)
        :param str scan_id: The Security Scan execution that detected this Security Issue
        :return: FrontendIssueSeverityChangeResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.frontend_issue_severity_change_with_http_info(account_id, org_id, project_id, issue_id, exemption_id, **kwargs)  # noqa: E501
        else:
            (data) = self.frontend_issue_severity_change_with_http_info(account_id, org_id, project_id, issue_id, exemption_id, **kwargs)  # noqa: E501
            return data

    def frontend_issue_severity_change_with_http_info(self, account_id, org_id, project_id, issue_id, exemption_id, **kwargs):  # noqa: E501
        """frontend_issue_severity_change  # noqa: E501

        Provides the severity change for an issue when approving occurrence level exemption  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_issue_severity_change_with_http_info(account_id, org_id, project_id, issue_id, exemption_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param str issue_id: The ID of the Security Issue (required)
        :param str exemption_id: ID of Security Test Exemption (required)
        :param str scan_id: The Security Scan execution that detected this Security Issue
        :return: FrontendIssueSeverityChangeResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'org_id', 'project_id', 'issue_id', 'exemption_id', 'scan_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method frontend_issue_severity_change" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `frontend_issue_severity_change`")  # noqa: E501
        # verify the required parameter 'org_id' is set
        if ('org_id' not in params or
                params['org_id'] is None):
            raise ValueError("Missing the required parameter `org_id` when calling `frontend_issue_severity_change`")  # noqa: E501
        # verify the required parameter 'project_id' is set
        if ('project_id' not in params or
                params['project_id'] is None):
            raise ValueError("Missing the required parameter `project_id` when calling `frontend_issue_severity_change`")  # noqa: E501
        # verify the required parameter 'issue_id' is set
        if ('issue_id' not in params or
                params['issue_id'] is None):
            raise ValueError("Missing the required parameter `issue_id` when calling `frontend_issue_severity_change`")  # noqa: E501
        # verify the required parameter 'exemption_id' is set
        if ('exemption_id' not in params or
                params['exemption_id'] is None):
            raise ValueError("Missing the required parameter `exemption_id` when calling `frontend_issue_severity_change`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'exemption_id' in params:
            path_params['exemptionId'] = params['exemption_id']  # noqa: E501

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501
        if 'org_id' in params:
            query_params.append(('orgId', params['org_id']))  # noqa: E501
        if 'project_id' in params:
            query_params.append(('projectId', params['project_id']))  # noqa: E501
        if 'scan_id' in params:
            query_params.append(('scanId', params['scan_id']))  # noqa: E501
        if 'issue_id' in params:
            query_params.append(('issueId', params['issue_id']))  # noqa: E501

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
            '/sto/api/v2/frontend/exemption/{exemptionId}/issue-severity-change', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FrontendIssueSeverityChangeResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def frontend_overview_baselines(self, account_id, org_id, project_id, **kwargs):  # noqa: E501
        """frontend_overview_baselines  # noqa: E501

        Provides baseline execution data needed by the Overview page  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_overview_baselines(account_id, org_id, project_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :return: FrontendOverviewBaselinesResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.frontend_overview_baselines_with_http_info(account_id, org_id, project_id, **kwargs)  # noqa: E501
        else:
            (data) = self.frontend_overview_baselines_with_http_info(account_id, org_id, project_id, **kwargs)  # noqa: E501
            return data

    def frontend_overview_baselines_with_http_info(self, account_id, org_id, project_id, **kwargs):  # noqa: E501
        """frontend_overview_baselines  # noqa: E501

        Provides baseline execution data needed by the Overview page  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_overview_baselines_with_http_info(account_id, org_id, project_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :return: FrontendOverviewBaselinesResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'org_id', 'project_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method frontend_overview_baselines" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `frontend_overview_baselines`")  # noqa: E501
        # verify the required parameter 'org_id' is set
        if ('org_id' not in params or
                params['org_id'] is None):
            raise ValueError("Missing the required parameter `org_id` when calling `frontend_overview_baselines`")  # noqa: E501
        # verify the required parameter 'project_id' is set
        if ('project_id' not in params or
                params['project_id'] is None):
            raise ValueError("Missing the required parameter `project_id` when calling `frontend_overview_baselines`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501
        if 'org_id' in params:
            query_params.append(('orgId', params['org_id']))  # noqa: E501
        if 'project_id' in params:
            query_params.append(('projectId', params['project_id']))  # noqa: E501

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
            '/sto/api/v2/frontend/overview/baselines', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FrontendOverviewBaselinesResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def frontend_overview_historical_counts(self, account_id, org_id, project_id, **kwargs):  # noqa: E501
        """frontend_overview_historical_counts  # noqa: E501

        Provides historical issue data needed by the Overview page  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_overview_historical_counts(account_id, org_id, project_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param int days: Number of days of Baseline Issue counts to return
        :return: FrontendOverviewHistoricalCountsResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.frontend_overview_historical_counts_with_http_info(account_id, org_id, project_id, **kwargs)  # noqa: E501
        else:
            (data) = self.frontend_overview_historical_counts_with_http_info(account_id, org_id, project_id, **kwargs)  # noqa: E501
            return data

    def frontend_overview_historical_counts_with_http_info(self, account_id, org_id, project_id, **kwargs):  # noqa: E501
        """frontend_overview_historical_counts  # noqa: E501

        Provides historical issue data needed by the Overview page  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_overview_historical_counts_with_http_info(account_id, org_id, project_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param int days: Number of days of Baseline Issue counts to return
        :return: FrontendOverviewHistoricalCountsResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'org_id', 'project_id', 'days']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method frontend_overview_historical_counts" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `frontend_overview_historical_counts`")  # noqa: E501
        # verify the required parameter 'org_id' is set
        if ('org_id' not in params or
                params['org_id'] is None):
            raise ValueError("Missing the required parameter `org_id` when calling `frontend_overview_historical_counts`")  # noqa: E501
        # verify the required parameter 'project_id' is set
        if ('project_id' not in params or
                params['project_id'] is None):
            raise ValueError("Missing the required parameter `project_id` when calling `frontend_overview_historical_counts`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501
        if 'org_id' in params:
            query_params.append(('orgId', params['org_id']))  # noqa: E501
        if 'project_id' in params:
            query_params.append(('projectId', params['project_id']))  # noqa: E501
        if 'days' in params:
            query_params.append(('days', params['days']))  # noqa: E501

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
            '/sto/api/v2/frontend/overview/historical-counts', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FrontendOverviewHistoricalCountsResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def frontend_pipeline_security_issues(self, account_id, org_id, project_id, execution_id, **kwargs):  # noqa: E501
        """frontend_pipeline_security_issues  # noqa: E501

        Provide issue data needed by the PipelineSecurityView  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_pipeline_security_issues(account_id, org_id, project_id, execution_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param str execution_id: Harness Execution ID (required)
        :param int page_existing: Page number to fetch (starting from 0)
        :param int page_size_existing: Number of results per page
        :param int page_new: Page number to fetch (starting from 0)
        :param int page_size_new: Number of results per page
        :param str stages:
        :param str steps:
        :param str target_ids:
        :param str target_types:
        :param str product_names:
        :param str severity_codes:
        :param bool include_exempted:
        :param str search:
        :param str issue_types:
        :param str status:
        :param str origins:
        :param str origin_statuses:
        :return: FrontendPipelineSecurityIssuesResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.frontend_pipeline_security_issues_with_http_info(account_id, org_id, project_id, execution_id, **kwargs)  # noqa: E501
        else:
            (data) = self.frontend_pipeline_security_issues_with_http_info(account_id, org_id, project_id, execution_id, **kwargs)  # noqa: E501
            return data

    def frontend_pipeline_security_issues_with_http_info(self, account_id, org_id, project_id, execution_id, **kwargs):  # noqa: E501
        """frontend_pipeline_security_issues  # noqa: E501

        Provide issue data needed by the PipelineSecurityView  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_pipeline_security_issues_with_http_info(account_id, org_id, project_id, execution_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param str execution_id: Harness Execution ID (required)
        :param int page_existing: Page number to fetch (starting from 0)
        :param int page_size_existing: Number of results per page
        :param int page_new: Page number to fetch (starting from 0)
        :param int page_size_new: Number of results per page
        :param str stages:
        :param str steps:
        :param str target_ids:
        :param str target_types:
        :param str product_names:
        :param str severity_codes:
        :param bool include_exempted:
        :param str search:
        :param str issue_types:
        :param str status:
        :param str origins:
        :param str origin_statuses:
        :return: FrontendPipelineSecurityIssuesResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'org_id', 'project_id', 'execution_id', 'page_existing', 'page_size_existing', 'page_new', 'page_size_new', 'stages', 'steps', 'target_ids', 'target_types', 'product_names', 'severity_codes', 'include_exempted', 'search', 'issue_types', 'status', 'origins', 'origin_statuses']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method frontend_pipeline_security_issues" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `frontend_pipeline_security_issues`")  # noqa: E501
        # verify the required parameter 'org_id' is set
        if ('org_id' not in params or
                params['org_id'] is None):
            raise ValueError("Missing the required parameter `org_id` when calling `frontend_pipeline_security_issues`")  # noqa: E501
        # verify the required parameter 'project_id' is set
        if ('project_id' not in params or
                params['project_id'] is None):
            raise ValueError("Missing the required parameter `project_id` when calling `frontend_pipeline_security_issues`")  # noqa: E501
        # verify the required parameter 'execution_id' is set
        if ('execution_id' not in params or
                params['execution_id'] is None):
            raise ValueError("Missing the required parameter `execution_id` when calling `frontend_pipeline_security_issues`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501
        if 'org_id' in params:
            query_params.append(('orgId', params['org_id']))  # noqa: E501
        if 'project_id' in params:
            query_params.append(('projectId', params['project_id']))  # noqa: E501
        if 'execution_id' in params:
            query_params.append(('executionId', params['execution_id']))  # noqa: E501
        if 'page_existing' in params:
            query_params.append(('pageExisting', params['page_existing']))  # noqa: E501
        if 'page_size_existing' in params:
            query_params.append(('pageSizeExisting', params['page_size_existing']))  # noqa: E501
        if 'page_new' in params:
            query_params.append(('pageNew', params['page_new']))  # noqa: E501
        if 'page_size_new' in params:
            query_params.append(('pageSizeNew', params['page_size_new']))  # noqa: E501
        if 'stages' in params:
            query_params.append(('stages', params['stages']))  # noqa: E501
        if 'steps' in params:
            query_params.append(('steps', params['steps']))  # noqa: E501
        if 'target_ids' in params:
            query_params.append(('targetIds', params['target_ids']))  # noqa: E501
        if 'target_types' in params:
            query_params.append(('targetTypes', params['target_types']))  # noqa: E501
        if 'product_names' in params:
            query_params.append(('productNames', params['product_names']))  # noqa: E501
        if 'severity_codes' in params:
            query_params.append(('severityCodes', params['severity_codes']))  # noqa: E501
        if 'include_exempted' in params:
            query_params.append(('includeExempted', params['include_exempted']))  # noqa: E501
        if 'search' in params:
            query_params.append(('search', params['search']))  # noqa: E501
        if 'issue_types' in params:
            query_params.append(('issueTypes', params['issue_types']))  # noqa: E501
        if 'status' in params:
            query_params.append(('status', params['status']))  # noqa: E501
        if 'origins' in params:
            query_params.append(('origins', params['origins']))  # noqa: E501
        if 'origin_statuses' in params:
            query_params.append(('originStatuses', params['origin_statuses']))  # noqa: E501

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
            '/sto/api/v2/frontend/pipeline-security/issues', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FrontendPipelineSecurityIssuesResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def frontend_pipeline_security_issues_csv(self, account_id, org_id, project_id, execution_id, **kwargs):  # noqa: E501
        """Export security issues data  # noqa: E501

        Export pipeline security issues as JSON data for CSV generation  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_pipeline_security_issues_csv(account_id, org_id, project_id, execution_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param str execution_id: Harness Execution ID (required)
        :param int page_existing: Page number to fetch (starting from 0)
        :param int page_size_existing: Number of results per page
        :param int page_new: Page number to fetch (starting from 0)
        :param int page_size_new: Number of results per page
        :param str stages:
        :param str steps:
        :param str target_ids:
        :param str target_types:
        :param str product_names:
        :param str severity_codes:
        :param bool include_exempted:
        :param str search:
        :param str issue_types:
        :param str status:
        :param str origins:
        :param str origin_statuses:
        :return: ExportPipelineSecurityIssuesCSVResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.frontend_pipeline_security_issues_csv_with_http_info(account_id, org_id, project_id, execution_id, **kwargs)  # noqa: E501
        else:
            (data) = self.frontend_pipeline_security_issues_csv_with_http_info(account_id, org_id, project_id, execution_id, **kwargs)  # noqa: E501
            return data

    def frontend_pipeline_security_issues_csv_with_http_info(self, account_id, org_id, project_id, execution_id, **kwargs):  # noqa: E501
        """Export security issues data  # noqa: E501

        Export pipeline security issues as JSON data for CSV generation  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_pipeline_security_issues_csv_with_http_info(account_id, org_id, project_id, execution_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param str execution_id: Harness Execution ID (required)
        :param int page_existing: Page number to fetch (starting from 0)
        :param int page_size_existing: Number of results per page
        :param int page_new: Page number to fetch (starting from 0)
        :param int page_size_new: Number of results per page
        :param str stages:
        :param str steps:
        :param str target_ids:
        :param str target_types:
        :param str product_names:
        :param str severity_codes:
        :param bool include_exempted:
        :param str search:
        :param str issue_types:
        :param str status:
        :param str origins:
        :param str origin_statuses:
        :return: ExportPipelineSecurityIssuesCSVResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'org_id', 'project_id', 'execution_id', 'page_existing', 'page_size_existing', 'page_new', 'page_size_new', 'stages', 'steps', 'target_ids', 'target_types', 'product_names', 'severity_codes', 'include_exempted', 'search', 'issue_types', 'status', 'origins', 'origin_statuses']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method frontend_pipeline_security_issues_csv" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `frontend_pipeline_security_issues_csv`")  # noqa: E501
        # verify the required parameter 'org_id' is set
        if ('org_id' not in params or
                params['org_id'] is None):
            raise ValueError("Missing the required parameter `org_id` when calling `frontend_pipeline_security_issues_csv`")  # noqa: E501
        # verify the required parameter 'project_id' is set
        if ('project_id' not in params or
                params['project_id'] is None):
            raise ValueError("Missing the required parameter `project_id` when calling `frontend_pipeline_security_issues_csv`")  # noqa: E501
        # verify the required parameter 'execution_id' is set
        if ('execution_id' not in params or
                params['execution_id'] is None):
            raise ValueError("Missing the required parameter `execution_id` when calling `frontend_pipeline_security_issues_csv`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501
        if 'org_id' in params:
            query_params.append(('orgId', params['org_id']))  # noqa: E501
        if 'project_id' in params:
            query_params.append(('projectId', params['project_id']))  # noqa: E501
        if 'execution_id' in params:
            query_params.append(('executionId', params['execution_id']))  # noqa: E501
        if 'page_existing' in params:
            query_params.append(('pageExisting', params['page_existing']))  # noqa: E501
        if 'page_size_existing' in params:
            query_params.append(('pageSizeExisting', params['page_size_existing']))  # noqa: E501
        if 'page_new' in params:
            query_params.append(('pageNew', params['page_new']))  # noqa: E501
        if 'page_size_new' in params:
            query_params.append(('pageSizeNew', params['page_size_new']))  # noqa: E501
        if 'stages' in params:
            query_params.append(('stages', params['stages']))  # noqa: E501
        if 'steps' in params:
            query_params.append(('steps', params['steps']))  # noqa: E501
        if 'target_ids' in params:
            query_params.append(('targetIds', params['target_ids']))  # noqa: E501
        if 'target_types' in params:
            query_params.append(('targetTypes', params['target_types']))  # noqa: E501
        if 'product_names' in params:
            query_params.append(('productNames', params['product_names']))  # noqa: E501
        if 'severity_codes' in params:
            query_params.append(('severityCodes', params['severity_codes']))  # noqa: E501
        if 'include_exempted' in params:
            query_params.append(('includeExempted', params['include_exempted']))  # noqa: E501
        if 'search' in params:
            query_params.append(('search', params['search']))  # noqa: E501
        if 'issue_types' in params:
            query_params.append(('issueTypes', params['issue_types']))  # noqa: E501
        if 'status' in params:
            query_params.append(('status', params['status']))  # noqa: E501
        if 'origins' in params:
            query_params.append(('origins', params['origins']))  # noqa: E501
        if 'origin_statuses' in params:
            query_params.append(('originStatuses', params['origin_statuses']))  # noqa: E501

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
            '/sto/api/v2/frontend/pipeline-security/issues/csv', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ExportPipelineSecurityIssuesCSVResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def frontend_pipeline_security_steps(self, account_id, org_id, project_id, execution_id, **kwargs):  # noqa: E501
        """frontend_pipeline_security_steps  # noqa: E501

        Provide step data needed by the PipelineSecurityView  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_pipeline_security_steps(account_id, org_id, project_id, execution_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param str execution_id: Harness Execution ID (required)
        :return: FrontendPipelineSecurityStepsResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.frontend_pipeline_security_steps_with_http_info(account_id, org_id, project_id, execution_id, **kwargs)  # noqa: E501
        else:
            (data) = self.frontend_pipeline_security_steps_with_http_info(account_id, org_id, project_id, execution_id, **kwargs)  # noqa: E501
            return data

    def frontend_pipeline_security_steps_with_http_info(self, account_id, org_id, project_id, execution_id, **kwargs):  # noqa: E501
        """frontend_pipeline_security_steps  # noqa: E501

        Provide step data needed by the PipelineSecurityView  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_pipeline_security_steps_with_http_info(account_id, org_id, project_id, execution_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param str execution_id: Harness Execution ID (required)
        :return: FrontendPipelineSecurityStepsResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'org_id', 'project_id', 'execution_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method frontend_pipeline_security_steps" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `frontend_pipeline_security_steps`")  # noqa: E501
        # verify the required parameter 'org_id' is set
        if ('org_id' not in params or
                params['org_id'] is None):
            raise ValueError("Missing the required parameter `org_id` when calling `frontend_pipeline_security_steps`")  # noqa: E501
        # verify the required parameter 'project_id' is set
        if ('project_id' not in params or
                params['project_id'] is None):
            raise ValueError("Missing the required parameter `project_id` when calling `frontend_pipeline_security_steps`")  # noqa: E501
        # verify the required parameter 'execution_id' is set
        if ('execution_id' not in params or
                params['execution_id'] is None):
            raise ValueError("Missing the required parameter `execution_id` when calling `frontend_pipeline_security_steps`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501
        if 'org_id' in params:
            query_params.append(('orgId', params['org_id']))  # noqa: E501
        if 'project_id' in params:
            query_params.append(('projectId', params['project_id']))  # noqa: E501
        if 'execution_id' in params:
            query_params.append(('executionId', params['execution_id']))  # noqa: E501

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
            '/sto/api/v2/frontend/pipeline-security/steps', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FrontendPipelineSecurityStepsResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def frontend_security_review(self, account_id, org_id, project_id, status, **kwargs):  # noqa: E501
        """frontend_security_review  # noqa: E501

        Provides data needed by the Security Review page  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_security_review(account_id, org_id, project_id, status, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param str status: Exemption status (required)
        :param int page: Page number to fetch (starting from 0)
        :param int page_size: Number of results per page
        :param str search:
        :return: FrontendSecurityReviewResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.frontend_security_review_with_http_info(account_id, org_id, project_id, status, **kwargs)  # noqa: E501
        else:
            (data) = self.frontend_security_review_with_http_info(account_id, org_id, project_id, status, **kwargs)  # noqa: E501
            return data

    def frontend_security_review_with_http_info(self, account_id, org_id, project_id, status, **kwargs):  # noqa: E501
        """frontend_security_review  # noqa: E501

        Provides data needed by the Security Review page  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_security_review_with_http_info(account_id, org_id, project_id, status, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param str status: Exemption status (required)
        :param int page: Page number to fetch (starting from 0)
        :param int page_size: Number of results per page
        :param str search:
        :return: FrontendSecurityReviewResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'org_id', 'project_id', 'status', 'page', 'page_size', 'search']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method frontend_security_review" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `frontend_security_review`")  # noqa: E501
        # verify the required parameter 'org_id' is set
        if ('org_id' not in params or
                params['org_id'] is None):
            raise ValueError("Missing the required parameter `org_id` when calling `frontend_security_review`")  # noqa: E501
        # verify the required parameter 'project_id' is set
        if ('project_id' not in params or
                params['project_id'] is None):
            raise ValueError("Missing the required parameter `project_id` when calling `frontend_security_review`")  # noqa: E501
        # verify the required parameter 'status' is set
        if ('status' not in params or
                params['status'] is None):
            raise ValueError("Missing the required parameter `status` when calling `frontend_security_review`")  # noqa: E501

        collection_formats = {}

        path_params = {}

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
        if 'status' in params:
            query_params.append(('status', params['status']))  # noqa: E501
        if 'search' in params:
            query_params.append(('search', params['search']))  # noqa: E501

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
            '/sto/api/v2/frontend/security-review', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FrontendSecurityReviewResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def frontend_test_targets(self, account_id, org_id, project_id, **kwargs):  # noqa: E501
        """frontend_test_targets  # noqa: E501

        Provides data needed by the Test Targets page  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_test_targets(account_id, org_id, project_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param int page: Page number to fetch (starting from 0)
        :param int page_size: Number of results per page
        :param str search:
        :param str target_id: Associated Target ID
        :return: FrontendTestTargetsResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.frontend_test_targets_with_http_info(account_id, org_id, project_id, **kwargs)  # noqa: E501
        else:
            (data) = self.frontend_test_targets_with_http_info(account_id, org_id, project_id, **kwargs)  # noqa: E501
            return data

    def frontend_test_targets_with_http_info(self, account_id, org_id, project_id, **kwargs):  # noqa: E501
        """frontend_test_targets  # noqa: E501

        Provides data needed by the Test Targets page  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_test_targets_with_http_info(account_id, org_id, project_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param int page: Page number to fetch (starting from 0)
        :param int page_size: Number of results per page
        :param str search:
        :param str target_id: Associated Target ID
        :return: FrontendTestTargetsResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'org_id', 'project_id', 'page', 'page_size', 'search', 'target_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method frontend_test_targets" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `frontend_test_targets`")  # noqa: E501
        # verify the required parameter 'org_id' is set
        if ('org_id' not in params or
                params['org_id'] is None):
            raise ValueError("Missing the required parameter `org_id` when calling `frontend_test_targets`")  # noqa: E501
        # verify the required parameter 'project_id' is set
        if ('project_id' not in params or
                params['project_id'] is None):
            raise ValueError("Missing the required parameter `project_id` when calling `frontend_test_targets`")  # noqa: E501

        collection_formats = {}

        path_params = {}

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
        if 'target_id' in params:
            query_params.append(('targetId', params['target_id']))  # noqa: E501

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
            '/sto/api/v2/frontend/test-targets', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FrontendTestTargetsResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def frontend_update_test_target_variants(self, body, account_id, org_id, project_id, target_id, **kwargs):  # noqa: E501
        """frontend_update_test_target_variants  # noqa: E501

        Updates statuses for a list of Test Target Variants  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_update_test_target_variants(body, account_id, org_id, project_id, target_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateTestTargetVariantsRequestBody body: (required)
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param str target_id: Associated Target ID (required)
        :return: StoStatus
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.frontend_update_test_target_variants_with_http_info(body, account_id, org_id, project_id, target_id, **kwargs)  # noqa: E501
        else:
            (data) = self.frontend_update_test_target_variants_with_http_info(body, account_id, org_id, project_id, target_id, **kwargs)  # noqa: E501
            return data

    def frontend_update_test_target_variants_with_http_info(self, body, account_id, org_id, project_id, target_id, **kwargs):  # noqa: E501
        """frontend_update_test_target_variants  # noqa: E501

        Updates statuses for a list of Test Target Variants  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.frontend_update_test_target_variants_with_http_info(body, account_id, org_id, project_id, target_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateTestTargetVariantsRequestBody body: (required)
        :param str account_id: Harness Account ID (required)
        :param str org_id: Harness Organization ID (required)
        :param str project_id: Harness Project ID (required)
        :param str target_id: Associated Target ID (required)
        :return: StoStatus
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'account_id', 'org_id', 'project_id', 'target_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method frontend_update_test_target_variants" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `frontend_update_test_target_variants`")  # noqa: E501
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `frontend_update_test_target_variants`")  # noqa: E501
        # verify the required parameter 'org_id' is set
        if ('org_id' not in params or
                params['org_id'] is None):
            raise ValueError("Missing the required parameter `org_id` when calling `frontend_update_test_target_variants`")  # noqa: E501
        # verify the required parameter 'project_id' is set
        if ('project_id' not in params or
                params['project_id'] is None):
            raise ValueError("Missing the required parameter `project_id` when calling `frontend_update_test_target_variants`")  # noqa: E501
        # verify the required parameter 'target_id' is set
        if ('target_id' not in params or
                params['target_id'] is None):
            raise ValueError("Missing the required parameter `target_id` when calling `frontend_update_test_target_variants`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'target_id' in params:
            path_params['targetId'] = params['target_id']  # noqa: E501

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501
        if 'org_id' in params:
            query_params.append(('orgId', params['org_id']))  # noqa: E501
        if 'project_id' in params:
            query_params.append(('projectId', params['project_id']))  # noqa: E501

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
            '/sto/api/v2/frontend/test-targets/{targetId}/variants/status', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='StoStatus',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
