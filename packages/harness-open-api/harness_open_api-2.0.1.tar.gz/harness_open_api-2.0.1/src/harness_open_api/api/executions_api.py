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


class ExecutionsApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def executions_create_execution(self, body, harness_account, org, project, **kwargs):  # noqa: E501
        """Create execution  # noqa: E501

        Create a new execution.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.executions_create_execution(body, harness_account, org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateExecutionRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :return: CreateExecutionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.executions_create_execution_with_http_info(body, harness_account, org, project, **kwargs)  # noqa: E501
        else:
            (data) = self.executions_create_execution_with_http_info(body, harness_account, org, project, **kwargs)  # noqa: E501
            return data

    def executions_create_execution_with_http_info(self, body, harness_account, org, project, **kwargs):  # noqa: E501
        """Create execution  # noqa: E501

        Create a new execution.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.executions_create_execution_with_http_info(body, harness_account, org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateExecutionRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :return: CreateExecutionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account', 'org', 'project']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method executions_create_execution" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `executions_create_execution`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `executions_create_execution`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `executions_create_execution`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `executions_create_execution`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/executions', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CreateExecutionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def executions_list_cost_changes(self, org, project, pipeline_execution_id, harness_account, **kwargs):  # noqa: E501
        """List cost changes  # noqa: E501

        List cost changes from the latest plan and last applied state for the current execution.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.executions_list_cost_changes(org, project, pipeline_execution_id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str pipeline_execution_id: Pipeline execution ID (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str pipeline_stage_id:
        :return: ListCostChangesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.executions_list_cost_changes_with_http_info(org, project, pipeline_execution_id, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.executions_list_cost_changes_with_http_info(org, project, pipeline_execution_id, harness_account, **kwargs)  # noqa: E501
            return data

    def executions_list_cost_changes_with_http_info(self, org, project, pipeline_execution_id, harness_account, **kwargs):  # noqa: E501
        """List cost changes  # noqa: E501

        List cost changes from the latest plan and last applied state for the current execution.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.executions_list_cost_changes_with_http_info(org, project, pipeline_execution_id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str pipeline_execution_id: Pipeline execution ID (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str pipeline_stage_id:
        :return: ListCostChangesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'pipeline_execution_id', 'harness_account', 'pipeline_stage_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method executions_list_cost_changes" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `executions_list_cost_changes`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `executions_list_cost_changes`")  # noqa: E501
        # verify the required parameter 'pipeline_execution_id' is set
        if ('pipeline_execution_id' not in params or
                params['pipeline_execution_id'] is None):
            raise ValueError("Missing the required parameter `pipeline_execution_id` when calling `executions_list_cost_changes`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `executions_list_cost_changes`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'pipeline_execution_id' in params:
            path_params['pipeline_execution_id'] = params['pipeline_execution_id']  # noqa: E501

        query_params = []
        if 'pipeline_stage_id' in params:
            query_params.append(('pipeline_stage_id', params['pipeline_stage_id']))  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/executions/{pipeline_execution_id}/cost-changes', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ListCostChangesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def executions_list_cost_changes_all_stages(self, org, project, pipeline_execution_id, harness_account, **kwargs):  # noqa: E501
        """List cost changes for all stages  # noqa: E501

        List cost changes for all stages from the latest plan and last applied state for the current execution.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.executions_list_cost_changes_all_stages(org, project, pipeline_execution_id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str pipeline_execution_id: Pipeline execution ID (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: ChangedCostsCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.executions_list_cost_changes_all_stages_with_http_info(org, project, pipeline_execution_id, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.executions_list_cost_changes_all_stages_with_http_info(org, project, pipeline_execution_id, harness_account, **kwargs)  # noqa: E501
            return data

    def executions_list_cost_changes_all_stages_with_http_info(self, org, project, pipeline_execution_id, harness_account, **kwargs):  # noqa: E501
        """List cost changes for all stages  # noqa: E501

        List cost changes for all stages from the latest plan and last applied state for the current execution.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.executions_list_cost_changes_all_stages_with_http_info(org, project, pipeline_execution_id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str pipeline_execution_id: Pipeline execution ID (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: ChangedCostsCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'pipeline_execution_id', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method executions_list_cost_changes_all_stages" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `executions_list_cost_changes_all_stages`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `executions_list_cost_changes_all_stages`")  # noqa: E501
        # verify the required parameter 'pipeline_execution_id' is set
        if ('pipeline_execution_id' not in params or
                params['pipeline_execution_id'] is None):
            raise ValueError("Missing the required parameter `pipeline_execution_id` when calling `executions_list_cost_changes_all_stages`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `executions_list_cost_changes_all_stages`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'pipeline_execution_id' in params:
            path_params['pipeline_execution_id'] = params['pipeline_execution_id']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/executions/{pipeline_execution_id}/cost-changes-all-stages', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ChangedCostsCollection',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def executions_list_executions(self, org, project, harness_account, **kwargs):  # noqa: E501
        """List executions  # noqa: E501

        List all executions.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.executions_list_executions(org, project, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :param str workspace: Workspace identifier
        :param str pipeline_execution_id: Pipeline identifier
        :param list[str] status: Status of the execution
        :param str pipeline_name: Pipeline name
        :param int start_time: Specify the start time for the query
        :param int end_time: Specify the end time limit for the query
        :return: ExecutionResourceCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.executions_list_executions_with_http_info(org, project, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.executions_list_executions_with_http_info(org, project, harness_account, **kwargs)  # noqa: E501
            return data

    def executions_list_executions_with_http_info(self, org, project, harness_account, **kwargs):  # noqa: E501
        """List executions  # noqa: E501

        List all executions.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.executions_list_executions_with_http_info(org, project, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :param str workspace: Workspace identifier
        :param str pipeline_execution_id: Pipeline identifier
        :param list[str] status: Status of the execution
        :param str pipeline_name: Pipeline name
        :param int start_time: Specify the start time for the query
        :param int end_time: Specify the end time limit for the query
        :return: ExecutionResourceCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'harness_account', 'limit', 'page', 'workspace', 'pipeline_execution_id', 'status', 'pipeline_name', 'start_time', 'end_time']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method executions_list_executions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `executions_list_executions`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `executions_list_executions`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `executions_list_executions`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501

        query_params = []
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'workspace' in params:
            query_params.append(('workspace', params['workspace']))  # noqa: E501
        if 'pipeline_execution_id' in params:
            query_params.append(('pipeline_execution_id', params['pipeline_execution_id']))  # noqa: E501
        if 'status' in params:
            query_params.append(('status', params['status']))  # noqa: E501
            collection_formats['status'] = 'multi'  # noqa: E501
        if 'pipeline_name' in params:
            query_params.append(('pipeline_name', params['pipeline_name']))  # noqa: E501
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
            '/iacm/api/orgs/{org}/projects/{project}/executions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ExecutionResourceCollection',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def executions_list_resource_changes(self, org, project, pipeline_execution_id, harness_account, **kwargs):  # noqa: E501
        """List resource changes  # noqa: E501

        List resource changes from the latest plan and state for this execution.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.executions_list_resource_changes(org, project, pipeline_execution_id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str pipeline_execution_id: Pipeline execution ID (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param bool exclude_state: When true, exclude values from the state in the response
        :param str pipeline_stage_id:
        :return: ListResourceChangesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.executions_list_resource_changes_with_http_info(org, project, pipeline_execution_id, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.executions_list_resource_changes_with_http_info(org, project, pipeline_execution_id, harness_account, **kwargs)  # noqa: E501
            return data

    def executions_list_resource_changes_with_http_info(self, org, project, pipeline_execution_id, harness_account, **kwargs):  # noqa: E501
        """List resource changes  # noqa: E501

        List resource changes from the latest plan and state for this execution.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.executions_list_resource_changes_with_http_info(org, project, pipeline_execution_id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str pipeline_execution_id: Pipeline execution ID (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param bool exclude_state: When true, exclude values from the state in the response
        :param str pipeline_stage_id:
        :return: ListResourceChangesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'pipeline_execution_id', 'harness_account', 'exclude_state', 'pipeline_stage_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method executions_list_resource_changes" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `executions_list_resource_changes`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `executions_list_resource_changes`")  # noqa: E501
        # verify the required parameter 'pipeline_execution_id' is set
        if ('pipeline_execution_id' not in params or
                params['pipeline_execution_id'] is None):
            raise ValueError("Missing the required parameter `pipeline_execution_id` when calling `executions_list_resource_changes`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `executions_list_resource_changes`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'pipeline_execution_id' in params:
            path_params['pipeline_execution_id'] = params['pipeline_execution_id']  # noqa: E501

        query_params = []
        if 'exclude_state' in params:
            query_params.append(('exclude_state', params['exclude_state']))  # noqa: E501
        if 'pipeline_stage_id' in params:
            query_params.append(('pipeline_stage_id', params['pipeline_stage_id']))  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/executions/{pipeline_execution_id}/resource-changes', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ListResourceChangesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def executions_list_resource_changes_all_stages(self, org, project, pipeline_execution_id, harness_account, **kwargs):  # noqa: E501
        """List resource changes for all stages  # noqa: E501

        List resource changes for all stages from the latest plan and state for this execution.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.executions_list_resource_changes_all_stages(org, project, pipeline_execution_id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str pipeline_execution_id: Pipeline execution ID (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param bool exclude_state: When true, exclude values from the state in the response
        :return: ChangedResourcesCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.executions_list_resource_changes_all_stages_with_http_info(org, project, pipeline_execution_id, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.executions_list_resource_changes_all_stages_with_http_info(org, project, pipeline_execution_id, harness_account, **kwargs)  # noqa: E501
            return data

    def executions_list_resource_changes_all_stages_with_http_info(self, org, project, pipeline_execution_id, harness_account, **kwargs):  # noqa: E501
        """List resource changes for all stages  # noqa: E501

        List resource changes for all stages from the latest plan and state for this execution.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.executions_list_resource_changes_all_stages_with_http_info(org, project, pipeline_execution_id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str pipeline_execution_id: Pipeline execution ID (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param bool exclude_state: When true, exclude values from the state in the response
        :return: ChangedResourcesCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'pipeline_execution_id', 'harness_account', 'exclude_state']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method executions_list_resource_changes_all_stages" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `executions_list_resource_changes_all_stages`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `executions_list_resource_changes_all_stages`")  # noqa: E501
        # verify the required parameter 'pipeline_execution_id' is set
        if ('pipeline_execution_id' not in params or
                params['pipeline_execution_id'] is None):
            raise ValueError("Missing the required parameter `pipeline_execution_id` when calling `executions_list_resource_changes_all_stages`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `executions_list_resource_changes_all_stages`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'pipeline_execution_id' in params:
            path_params['pipeline_execution_id'] = params['pipeline_execution_id']  # noqa: E501

        query_params = []
        if 'exclude_state' in params:
            query_params.append(('exclude_state', params['exclude_state']))  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/executions/{pipeline_execution_id}/resource-changes-all-stages', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ChangedResourcesCollection',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def executions_modify_execution(self, body, harness_account, org, project, pipeline_execution_id, pipeline_stage_id, **kwargs):  # noqa: E501
        """Update execution  # noqa: E501

        Modify an individual execution by adding audit data.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.executions_modify_execution(body, harness_account, org, project, pipeline_execution_id, pipeline_stage_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateExecutionRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str pipeline_execution_id: Pipeline execution ID (required)
        :param str pipeline_stage_id: Pipeline execution stage ID (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.executions_modify_execution_with_http_info(body, harness_account, org, project, pipeline_execution_id, pipeline_stage_id, **kwargs)  # noqa: E501
        else:
            (data) = self.executions_modify_execution_with_http_info(body, harness_account, org, project, pipeline_execution_id, pipeline_stage_id, **kwargs)  # noqa: E501
            return data

    def executions_modify_execution_with_http_info(self, body, harness_account, org, project, pipeline_execution_id, pipeline_stage_id, **kwargs):  # noqa: E501
        """Update execution  # noqa: E501

        Modify an individual execution by adding audit data.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.executions_modify_execution_with_http_info(body, harness_account, org, project, pipeline_execution_id, pipeline_stage_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateExecutionRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str pipeline_execution_id: Pipeline execution ID (required)
        :param str pipeline_stage_id: Pipeline execution stage ID (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account', 'org', 'project', 'pipeline_execution_id', 'pipeline_stage_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method executions_modify_execution" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `executions_modify_execution`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `executions_modify_execution`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `executions_modify_execution`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `executions_modify_execution`")  # noqa: E501
        # verify the required parameter 'pipeline_execution_id' is set
        if ('pipeline_execution_id' not in params or
                params['pipeline_execution_id'] is None):
            raise ValueError("Missing the required parameter `pipeline_execution_id` when calling `executions_modify_execution`")  # noqa: E501
        # verify the required parameter 'pipeline_stage_id' is set
        if ('pipeline_stage_id' not in params or
                params['pipeline_stage_id'] is None):
            raise ValueError("Missing the required parameter `pipeline_stage_id` when calling `executions_modify_execution`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'pipeline_execution_id' in params:
            path_params['pipeline_execution_id'] = params['pipeline_execution_id']  # noqa: E501
        if 'pipeline_stage_id' in params:
            path_params['pipeline_stage_id'] = params['pipeline_stage_id']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/executions/{pipeline_execution_id}/{pipeline_stage_id}/audit-event', 'POST',
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

    def executions_show_execution(self, org, project, pipeline_execution_id, pipeline_stage_id, harness_account, **kwargs):  # noqa: E501
        """Show execution  # noqa: E501

        Show an individual execution.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.executions_show_execution(org, project, pipeline_execution_id, pipeline_stage_id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str pipeline_execution_id: Pipeline execution ID (required)
        :param str pipeline_stage_id: Pipeline execution stage ID (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: ShowExecutionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.executions_show_execution_with_http_info(org, project, pipeline_execution_id, pipeline_stage_id, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.executions_show_execution_with_http_info(org, project, pipeline_execution_id, pipeline_stage_id, harness_account, **kwargs)  # noqa: E501
            return data

    def executions_show_execution_with_http_info(self, org, project, pipeline_execution_id, pipeline_stage_id, harness_account, **kwargs):  # noqa: E501
        """Show execution  # noqa: E501

        Show an individual execution.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.executions_show_execution_with_http_info(org, project, pipeline_execution_id, pipeline_stage_id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str pipeline_execution_id: Pipeline execution ID (required)
        :param str pipeline_stage_id: Pipeline execution stage ID (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: ShowExecutionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'pipeline_execution_id', 'pipeline_stage_id', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method executions_show_execution" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `executions_show_execution`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `executions_show_execution`")  # noqa: E501
        # verify the required parameter 'pipeline_execution_id' is set
        if ('pipeline_execution_id' not in params or
                params['pipeline_execution_id'] is None):
            raise ValueError("Missing the required parameter `pipeline_execution_id` when calling `executions_show_execution`")  # noqa: E501
        # verify the required parameter 'pipeline_stage_id' is set
        if ('pipeline_stage_id' not in params or
                params['pipeline_stage_id'] is None):
            raise ValueError("Missing the required parameter `pipeline_stage_id` when calling `executions_show_execution`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `executions_show_execution`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'pipeline_execution_id' in params:
            path_params['pipeline_execution_id'] = params['pipeline_execution_id']  # noqa: E501
        if 'pipeline_stage_id' in params:
            path_params['pipeline_stage_id'] = params['pipeline_stage_id']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/executions/{pipeline_execution_id}/{pipeline_stage_id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ShowExecutionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
