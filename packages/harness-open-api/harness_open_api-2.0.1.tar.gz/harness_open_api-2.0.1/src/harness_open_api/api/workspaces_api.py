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


class WorkspacesApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def workspaces_clone_workspace(self, body, harness_account, org, project, workspace, **kwargs):  # noqa: E501
        """Clone workspace  # noqa: E501

        Clone the given workspace with new name.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_clone_workspace(body, harness_account, org, project, workspace, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CloneWorkspaceRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: (required)
        :return: WorkspacesCreateWorkspaceResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_clone_workspace_with_http_info(body, harness_account, org, project, workspace, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_clone_workspace_with_http_info(body, harness_account, org, project, workspace, **kwargs)  # noqa: E501
            return data

    def workspaces_clone_workspace_with_http_info(self, body, harness_account, org, project, workspace, **kwargs):  # noqa: E501
        """Clone workspace  # noqa: E501

        Clone the given workspace with new name.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_clone_workspace_with_http_info(body, harness_account, org, project, workspace, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CloneWorkspaceRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: (required)
        :return: WorkspacesCreateWorkspaceResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account', 'org', 'project', 'workspace']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_clone_workspace" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `workspaces_clone_workspace`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_clone_workspace`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_clone_workspace`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_clone_workspace`")  # noqa: E501
        # verify the required parameter 'workspace' is set
        if ('workspace' not in params or
                params['workspace'] is None):
            raise ValueError("Missing the required parameter `workspace` when calling `workspaces_clone_workspace`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'workspace' in params:
            path_params['workspace'] = params['workspace']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/clone', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='WorkspacesCreateWorkspaceResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def workspaces_create_data(self, pipeline_id, stage_id, pipeline_execution_id, pipeline_stage_id, provisioner_type, data_type, org, project, workspace, harness_account, **kwargs):  # noqa: E501
        """Create data  # noqa: E501

        Store binary data generated by the provisioner, such as plans and state files.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_create_data(pipeline_id, stage_id, pipeline_execution_id, pipeline_stage_id, provisioner_type, data_type, org, project, workspace, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str pipeline_id: The unique identifier for the associated pipeline (required)
        :param str stage_id: The unique identifier for a stage (required)
        :param str pipeline_execution_id: The unique identifier for the associated pipeline execution (required)
        :param str pipeline_stage_id: The unique identifier for the associated pipeline execution stage (required)
        :param str provisioner_type: Type of provisioner that created the data (required)
        :param str data_type: Type of data stored (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace identifier (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str policy_action: Policy action used during OPA evaluation
        :param str stack_path: Optional path to the stack module
        :param int content_length: Size in bytes of the data.
        :return: CreateDataResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_create_data_with_http_info(pipeline_id, stage_id, pipeline_execution_id, pipeline_stage_id, provisioner_type, data_type, org, project, workspace, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_create_data_with_http_info(pipeline_id, stage_id, pipeline_execution_id, pipeline_stage_id, provisioner_type, data_type, org, project, workspace, harness_account, **kwargs)  # noqa: E501
            return data

    def workspaces_create_data_with_http_info(self, pipeline_id, stage_id, pipeline_execution_id, pipeline_stage_id, provisioner_type, data_type, org, project, workspace, harness_account, **kwargs):  # noqa: E501
        """Create data  # noqa: E501

        Store binary data generated by the provisioner, such as plans and state files.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_create_data_with_http_info(pipeline_id, stage_id, pipeline_execution_id, pipeline_stage_id, provisioner_type, data_type, org, project, workspace, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str pipeline_id: The unique identifier for the associated pipeline (required)
        :param str stage_id: The unique identifier for a stage (required)
        :param str pipeline_execution_id: The unique identifier for the associated pipeline execution (required)
        :param str pipeline_stage_id: The unique identifier for the associated pipeline execution stage (required)
        :param str provisioner_type: Type of provisioner that created the data (required)
        :param str data_type: Type of data stored (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace identifier (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str policy_action: Policy action used during OPA evaluation
        :param str stack_path: Optional path to the stack module
        :param int content_length: Size in bytes of the data.
        :return: CreateDataResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['pipeline_id', 'stage_id', 'pipeline_execution_id', 'pipeline_stage_id', 'provisioner_type', 'data_type', 'org', 'project', 'workspace', 'harness_account', 'policy_action', 'stack_path', 'content_length']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_create_data" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'pipeline_id' is set
        if ('pipeline_id' not in params or
                params['pipeline_id'] is None):
            raise ValueError("Missing the required parameter `pipeline_id` when calling `workspaces_create_data`")  # noqa: E501
        # verify the required parameter 'stage_id' is set
        if ('stage_id' not in params or
                params['stage_id'] is None):
            raise ValueError("Missing the required parameter `stage_id` when calling `workspaces_create_data`")  # noqa: E501
        # verify the required parameter 'pipeline_execution_id' is set
        if ('pipeline_execution_id' not in params or
                params['pipeline_execution_id'] is None):
            raise ValueError("Missing the required parameter `pipeline_execution_id` when calling `workspaces_create_data`")  # noqa: E501
        # verify the required parameter 'pipeline_stage_id' is set
        if ('pipeline_stage_id' not in params or
                params['pipeline_stage_id'] is None):
            raise ValueError("Missing the required parameter `pipeline_stage_id` when calling `workspaces_create_data`")  # noqa: E501
        # verify the required parameter 'provisioner_type' is set
        if ('provisioner_type' not in params or
                params['provisioner_type'] is None):
            raise ValueError("Missing the required parameter `provisioner_type` when calling `workspaces_create_data`")  # noqa: E501
        # verify the required parameter 'data_type' is set
        if ('data_type' not in params or
                params['data_type'] is None):
            raise ValueError("Missing the required parameter `data_type` when calling `workspaces_create_data`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_create_data`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_create_data`")  # noqa: E501
        # verify the required parameter 'workspace' is set
        if ('workspace' not in params or
                params['workspace'] is None):
            raise ValueError("Missing the required parameter `workspace` when calling `workspaces_create_data`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_create_data`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'workspace' in params:
            path_params['workspace'] = params['workspace']  # noqa: E501

        query_params = []
        if 'pipeline_id' in params:
            query_params.append(('pipeline_id', params['pipeline_id']))  # noqa: E501
        if 'stage_id' in params:
            query_params.append(('stage_id', params['stage_id']))  # noqa: E501
        if 'pipeline_execution_id' in params:
            query_params.append(('pipeline_execution_id', params['pipeline_execution_id']))  # noqa: E501
        if 'pipeline_stage_id' in params:
            query_params.append(('pipeline_stage_id', params['pipeline_stage_id']))  # noqa: E501
        if 'provisioner_type' in params:
            query_params.append(('provisioner_type', params['provisioner_type']))  # noqa: E501
        if 'data_type' in params:
            query_params.append(('data_type', params['data_type']))  # noqa: E501
        if 'policy_action' in params:
            query_params.append(('policy_action', params['policy_action']))  # noqa: E501
        if 'stack_path' in params:
            query_params.append(('stack_path', params['stack_path']))  # noqa: E501

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
            ['application/json', 'application/vnd.goa.error'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/data', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CreateDataResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def workspaces_create_remote_execution(self, body, harness_account, org, project, workspace, **kwargs):  # noqa: E501
        """Create remote execution  # noqa: E501

        Create a remote execution for a workspace.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_create_remote_execution(body, harness_account, org, project, workspace, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateRemoteExecutionRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: The workspace associated with the remote execution. (required)
        :return: CreateRemoteExecutionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_create_remote_execution_with_http_info(body, harness_account, org, project, workspace, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_create_remote_execution_with_http_info(body, harness_account, org, project, workspace, **kwargs)  # noqa: E501
            return data

    def workspaces_create_remote_execution_with_http_info(self, body, harness_account, org, project, workspace, **kwargs):  # noqa: E501
        """Create remote execution  # noqa: E501

        Create a remote execution for a workspace.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_create_remote_execution_with_http_info(body, harness_account, org, project, workspace, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateRemoteExecutionRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: The workspace associated with the remote execution. (required)
        :return: CreateRemoteExecutionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account', 'org', 'project', 'workspace']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_create_remote_execution" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `workspaces_create_remote_execution`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_create_remote_execution`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_create_remote_execution`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_create_remote_execution`")  # noqa: E501
        # verify the required parameter 'workspace' is set
        if ('workspace' not in params or
                params['workspace'] is None):
            raise ValueError("Missing the required parameter `workspace` when calling `workspaces_create_remote_execution`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'workspace' in params:
            path_params['workspace'] = params['workspace']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/remote-executions', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CreateRemoteExecutionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def workspaces_create_workspace(self, body, harness_account, org, project, **kwargs):  # noqa: E501
        """Create workspace  # noqa: E501

        Create a new workspace.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_create_workspace(body, harness_account, org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateWorkspaceRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :return: WorkspacesCreateWorkspaceResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_create_workspace_with_http_info(body, harness_account, org, project, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_create_workspace_with_http_info(body, harness_account, org, project, **kwargs)  # noqa: E501
            return data

    def workspaces_create_workspace_with_http_info(self, body, harness_account, org, project, **kwargs):  # noqa: E501
        """Create workspace  # noqa: E501

        Create a new workspace.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_create_workspace_with_http_info(body, harness_account, org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateWorkspaceRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :return: WorkspacesCreateWorkspaceResponseBody
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
                    " to method workspaces_create_workspace" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `workspaces_create_workspace`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_create_workspace`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_create_workspace`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_create_workspace`")  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='WorkspacesCreateWorkspaceResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def workspaces_delete_resources(self, body, harness_account, org, project, workspace, **kwargs):  # noqa: E501
        """Delete resources  # noqa: E501

        Deletes destroyed resources for a workspace.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_delete_resources(body, harness_account, org, project, workspace, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param DeleteResourcesRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace identifier (required)
        :return: DeleteResourcesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_delete_resources_with_http_info(body, harness_account, org, project, workspace, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_delete_resources_with_http_info(body, harness_account, org, project, workspace, **kwargs)  # noqa: E501
            return data

    def workspaces_delete_resources_with_http_info(self, body, harness_account, org, project, workspace, **kwargs):  # noqa: E501
        """Delete resources  # noqa: E501

        Deletes destroyed resources for a workspace.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_delete_resources_with_http_info(body, harness_account, org, project, workspace, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param DeleteResourcesRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace identifier (required)
        :return: DeleteResourcesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account', 'org', 'project', 'workspace']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_delete_resources" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `workspaces_delete_resources`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_delete_resources`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_delete_resources`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_delete_resources`")  # noqa: E501
        # verify the required parameter 'workspace' is set
        if ('workspace' not in params or
                params['workspace'] is None):
            raise ValueError("Missing the required parameter `workspace` when calling `workspaces_delete_resources`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'workspace' in params:
            path_params['workspace'] = params['workspace']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/resources', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DeleteResourcesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def workspaces_destroy_workspace(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """Destroy workspace  # noqa: E501

        Deletes the given workspace.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_destroy_workspace(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: Identifier is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_destroy_workspace_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_destroy_workspace_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
            return data

    def workspaces_destroy_workspace_with_http_info(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """Destroy workspace  # noqa: E501

        Deletes the given workspace.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_destroy_workspace_with_http_info(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: Identifier is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'identifier', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_destroy_workspace" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_destroy_workspace`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_destroy_workspace`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `workspaces_destroy_workspace`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_destroy_workspace`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/{identifier}', 'DELETE',
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

    def workspaces_download_remote_execution(self, org, project, workspace, id, harness_account, **kwargs):  # noqa: E501
        """Download remote execution  # noqa: E501

        Download the source code for the remote plan.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_download_remote_execution(org, project, workspace, id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace is the resource workspace this variable is associated with. (required)
        :param str id: The ID of the remote execution (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_download_remote_execution_with_http_info(org, project, workspace, id, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_download_remote_execution_with_http_info(org, project, workspace, id, harness_account, **kwargs)  # noqa: E501
            return data

    def workspaces_download_remote_execution_with_http_info(self, org, project, workspace, id, harness_account, **kwargs):  # noqa: E501
        """Download remote execution  # noqa: E501

        Download the source code for the remote plan.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_download_remote_execution_with_http_info(org, project, workspace, id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace is the resource workspace this variable is associated with. (required)
        :param str id: The ID of the remote execution (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'workspace', 'id', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_download_remote_execution" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_download_remote_execution`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_download_remote_execution`")  # noqa: E501
        # verify the required parameter 'workspace' is set
        if ('workspace' not in params or
                params['workspace'] is None):
            raise ValueError("Missing the required parameter `workspace` when calling `workspaces_download_remote_execution`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `workspaces_download_remote_execution`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_download_remote_execution`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'workspace' in params:
            path_params['workspace'] = params['workspace']  # noqa: E501
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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/remote-executions/{id}/download', 'GET',
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

    def workspaces_evaluate_data(self, policy_action, org, project, workspace, id, harness_account, **kwargs):  # noqa: E501
        """Evaluate data  # noqa: E501

        Evaluate policy against previously stored data, such as plans and state files.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_evaluate_data(policy_action, org, project, workspace, id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str policy_action: Policy action used during OPA evaluation (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace is the resource workspace this variable is associated with. (required)
        :param str id: The unique identifier for the data (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str pipeline_execution_id: Pipeline execution associated with this evaluation
        :return: EvaluateDataResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_evaluate_data_with_http_info(policy_action, org, project, workspace, id, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_evaluate_data_with_http_info(policy_action, org, project, workspace, id, harness_account, **kwargs)  # noqa: E501
            return data

    def workspaces_evaluate_data_with_http_info(self, policy_action, org, project, workspace, id, harness_account, **kwargs):  # noqa: E501
        """Evaluate data  # noqa: E501

        Evaluate policy against previously stored data, such as plans and state files.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_evaluate_data_with_http_info(policy_action, org, project, workspace, id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str policy_action: Policy action used during OPA evaluation (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace is the resource workspace this variable is associated with. (required)
        :param str id: The unique identifier for the data (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str pipeline_execution_id: Pipeline execution associated with this evaluation
        :return: EvaluateDataResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['policy_action', 'org', 'project', 'workspace', 'id', 'harness_account', 'pipeline_execution_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_evaluate_data" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'policy_action' is set
        if ('policy_action' not in params or
                params['policy_action'] is None):
            raise ValueError("Missing the required parameter `policy_action` when calling `workspaces_evaluate_data`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_evaluate_data`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_evaluate_data`")  # noqa: E501
        # verify the required parameter 'workspace' is set
        if ('workspace' not in params or
                params['workspace'] is None):
            raise ValueError("Missing the required parameter `workspace` when calling `workspaces_evaluate_data`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `workspaces_evaluate_data`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_evaluate_data`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'workspace' in params:
            path_params['workspace'] = params['workspace']  # noqa: E501
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'pipeline_execution_id' in params:
            query_params.append(('pipeline_execution_id', params['pipeline_execution_id']))  # noqa: E501
        if 'policy_action' in params:
            query_params.append(('policy_action', params['policy_action']))  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/data/{id}/evaluate-policy', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='EvaluateDataResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def workspaces_execute_remote_execution(self, org, project, workspace, id, harness_account, **kwargs):  # noqa: E501
        """execute-remote-execution workspaces  # noqa: E501

        Execute the remote execution  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_execute_remote_execution(org, project, workspace, id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace is the resource workspace this variable is associated with. (required)
        :param str id: The ID of the remote execution (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: RemoteExecution
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_execute_remote_execution_with_http_info(org, project, workspace, id, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_execute_remote_execution_with_http_info(org, project, workspace, id, harness_account, **kwargs)  # noqa: E501
            return data

    def workspaces_execute_remote_execution_with_http_info(self, org, project, workspace, id, harness_account, **kwargs):  # noqa: E501
        """execute-remote-execution workspaces  # noqa: E501

        Execute the remote execution  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_execute_remote_execution_with_http_info(org, project, workspace, id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace is the resource workspace this variable is associated with. (required)
        :param str id: The ID of the remote execution (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: RemoteExecution
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'workspace', 'id', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_execute_remote_execution" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_execute_remote_execution`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_execute_remote_execution`")  # noqa: E501
        # verify the required parameter 'workspace' is set
        if ('workspace' not in params or
                params['workspace'] is None):
            raise ValueError("Missing the required parameter `workspace` when calling `workspaces_execute_remote_execution`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `workspaces_execute_remote_execution`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_execute_remote_execution`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'workspace' in params:
            path_params['workspace'] = params['workspace']  # noqa: E501
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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/remote-executions/{id}/execute', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RemoteExecution',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def workspaces_find_remote_execution(self, org, project, workspace, id, harness_account, **kwargs):  # noqa: E501
        """Show remote execution  # noqa: E501

        Find remote execution  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_find_remote_execution(org, project, workspace, id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace is the resource workspace this variable is associated with. (required)
        :param str id: The ID of the remote execution (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: ShowRemoteExecutionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_find_remote_execution_with_http_info(org, project, workspace, id, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_find_remote_execution_with_http_info(org, project, workspace, id, harness_account, **kwargs)  # noqa: E501
            return data

    def workspaces_find_remote_execution_with_http_info(self, org, project, workspace, id, harness_account, **kwargs):  # noqa: E501
        """Show remote execution  # noqa: E501

        Find remote execution  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_find_remote_execution_with_http_info(org, project, workspace, id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace is the resource workspace this variable is associated with. (required)
        :param str id: The ID of the remote execution (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: ShowRemoteExecutionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'workspace', 'id', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_find_remote_execution" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_find_remote_execution`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_find_remote_execution`")  # noqa: E501
        # verify the required parameter 'workspace' is set
        if ('workspace' not in params or
                params['workspace'] is None):
            raise ValueError("Missing the required parameter `workspace` when calling `workspaces_find_remote_execution`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `workspaces_find_remote_execution`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_find_remote_execution`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'workspace' in params:
            path_params['workspace'] = params['workspace']  # noqa: E501
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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/remote-executions/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ShowRemoteExecutionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def workspaces_force_unlock_workspace(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """Force unlock workspace  # noqa: E501

        Force unlock a workspace.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_force_unlock_workspace(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: Identifier is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_force_unlock_workspace_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_force_unlock_workspace_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
            return data

    def workspaces_force_unlock_workspace_with_http_info(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """Force unlock workspace  # noqa: E501

        Force unlock a workspace.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_force_unlock_workspace_with_http_info(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: Identifier is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'identifier', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_force_unlock_workspace" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_force_unlock_workspace`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_force_unlock_workspace`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `workspaces_force_unlock_workspace`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_force_unlock_workspace`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/{identifier}/actions/force-unlock', 'POST',
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

    def workspaces_list_all_workspace_tags(self, org, project, harness_account, **kwargs):  # noqa: E501
        """List all workspace tags  # noqa: E501

        List all tags  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_list_all_workspace_tags(org, project, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: list[str]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_list_all_workspace_tags_with_http_info(org, project, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_list_all_workspace_tags_with_http_info(org, project, harness_account, **kwargs)  # noqa: E501
            return data

    def workspaces_list_all_workspace_tags_with_http_info(self, org, project, harness_account, **kwargs):  # noqa: E501
        """List all workspace tags  # noqa: E501

        List all tags  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_list_all_workspace_tags_with_http_info(org, project, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: list[str]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_list_all_workspace_tags" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_list_all_workspace_tags`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_list_all_workspace_tags`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_list_all_workspace_tags`")  # noqa: E501

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
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/vnd.goa.error'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/orgs/{org}/projects/{project}/tags', 'GET',
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

    def workspaces_list_associated_workspaces(self, template_id, harness_account, **kwargs):  # noqa: E501
        """List workspaces associated with a template ID  # noqa: E501

        Get all workspaces associated with a specific template ID  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_list_associated_workspaces(template_id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str template_id: Template identifier to filter workspaces (required)
        :param str harness_account: Account identifier. (required)
        :param str org: Organization identifier (required for 'org' and 'project' scope).
        :param str project: Project identifier (required for 'project' scope).
        :param str version: Template version associated with the workspace.
        :return: list[HarnessIacmWorkspaceTemplate]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_list_associated_workspaces_with_http_info(template_id, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_list_associated_workspaces_with_http_info(template_id, harness_account, **kwargs)  # noqa: E501
            return data

    def workspaces_list_associated_workspaces_with_http_info(self, template_id, harness_account, **kwargs):  # noqa: E501
        """List workspaces associated with a template ID  # noqa: E501

        Get all workspaces associated with a specific template ID  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_list_associated_workspaces_with_http_info(template_id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str template_id: Template identifier to filter workspaces (required)
        :param str harness_account: Account identifier. (required)
        :param str org: Organization identifier (required for 'org' and 'project' scope).
        :param str project: Project identifier (required for 'project' scope).
        :param str version: Template version associated with the workspace.
        :return: list[HarnessIacmWorkspaceTemplate]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['template_id', 'harness_account', 'org', 'project', 'version']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_list_associated_workspaces" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'template_id' is set
        if ('template_id' not in params or
                params['template_id'] is None):
            raise ValueError("Missing the required parameter `template_id` when calling `workspaces_list_associated_workspaces`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_list_associated_workspaces`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'template_id' in params:
            path_params['template_id'] = params['template_id']  # noqa: E501

        query_params = []
        if 'org' in params:
            query_params.append(('org', params['org']))  # noqa: E501
        if 'project' in params:
            query_params.append(('project', params['project']))  # noqa: E501
        if 'version' in params:
            query_params.append(('version', params['version']))  # noqa: E501

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
            '/iacm/api/workspace/templates/{template_id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[HarnessIacmWorkspaceTemplate]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def workspaces_list_data(self, org, project, workspace, harness_account, **kwargs):  # noqa: E501
        """List data  # noqa: E501

        List all stored data for a workspace.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_list_data(org, project, workspace, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace identifier (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str pipeline_execution_id: Filter by pipeline execution ID
        :param str pipeline_stage_id: Filter by pipeline execution stage ID
        :param str provisioner_type: Filter by provisioner type
        :param str data_type: Filter by data type
        :param str stack_path: Filter by stack path
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :return: WorkspaceDataResourceCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_list_data_with_http_info(org, project, workspace, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_list_data_with_http_info(org, project, workspace, harness_account, **kwargs)  # noqa: E501
            return data

    def workspaces_list_data_with_http_info(self, org, project, workspace, harness_account, **kwargs):  # noqa: E501
        """List data  # noqa: E501

        List all stored data for a workspace.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_list_data_with_http_info(org, project, workspace, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace identifier (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str pipeline_execution_id: Filter by pipeline execution ID
        :param str pipeline_stage_id: Filter by pipeline execution stage ID
        :param str provisioner_type: Filter by provisioner type
        :param str data_type: Filter by data type
        :param str stack_path: Filter by stack path
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :return: WorkspaceDataResourceCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'workspace', 'harness_account', 'pipeline_execution_id', 'pipeline_stage_id', 'provisioner_type', 'data_type', 'stack_path', 'limit', 'page']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_list_data" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_list_data`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_list_data`")  # noqa: E501
        # verify the required parameter 'workspace' is set
        if ('workspace' not in params or
                params['workspace'] is None):
            raise ValueError("Missing the required parameter `workspace` when calling `workspaces_list_data`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_list_data`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'workspace' in params:
            path_params['workspace'] = params['workspace']  # noqa: E501

        query_params = []
        if 'pipeline_execution_id' in params:
            query_params.append(('pipeline_execution_id', params['pipeline_execution_id']))  # noqa: E501
        if 'pipeline_stage_id' in params:
            query_params.append(('pipeline_stage_id', params['pipeline_stage_id']))  # noqa: E501
        if 'provisioner_type' in params:
            query_params.append(('provisioner_type', params['provisioner_type']))  # noqa: E501
        if 'data_type' in params:
            query_params.append(('data_type', params['data_type']))  # noqa: E501
        if 'stack_path' in params:
            query_params.append(('stack_path', params['stack_path']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/data', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='WorkspaceDataResourceCollection',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def workspaces_list_pipelines(self, org, project, workspace, harness_account, **kwargs):  # noqa: E501
        """List pipelines  # noqa: E501

        List the pipelines where the workspace is been used  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_list_pipelines(org, project, workspace, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace identifier (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :return: ListPipelinesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_list_pipelines_with_http_info(org, project, workspace, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_list_pipelines_with_http_info(org, project, workspace, harness_account, **kwargs)  # noqa: E501
            return data

    def workspaces_list_pipelines_with_http_info(self, org, project, workspace, harness_account, **kwargs):  # noqa: E501
        """List pipelines  # noqa: E501

        List the pipelines where the workspace is been used  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_list_pipelines_with_http_info(org, project, workspace, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace identifier (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :return: ListPipelinesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'workspace', 'harness_account', 'limit', 'page']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_list_pipelines" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_list_pipelines`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_list_pipelines`")  # noqa: E501
        # verify the required parameter 'workspace' is set
        if ('workspace' not in params or
                params['workspace'] is None):
            raise ValueError("Missing the required parameter `workspace` when calling `workspaces_list_pipelines`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_list_pipelines`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'workspace' in params:
            path_params['workspace'] = params['workspace']  # noqa: E501

        query_params = []
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/pipelines', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ListPipelinesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def workspaces_list_provisioners_ratio(self, org, project, harness_account, **kwargs):  # noqa: E501
        """List provisioners ratio  # noqa: E501

        Retrieves the ratio of provisioners used by workspaces  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_list_provisioners_ratio(org, project, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int start_time: Start time filter (Unix timestamp)
        :param int end_time: End time filter (Unix timestamp)
        :return: ListProvisionersRatioResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_list_provisioners_ratio_with_http_info(org, project, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_list_provisioners_ratio_with_http_info(org, project, harness_account, **kwargs)  # noqa: E501
            return data

    def workspaces_list_provisioners_ratio_with_http_info(self, org, project, harness_account, **kwargs):  # noqa: E501
        """List provisioners ratio  # noqa: E501

        Retrieves the ratio of provisioners used by workspaces  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_list_provisioners_ratio_with_http_info(org, project, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int start_time: Start time filter (Unix timestamp)
        :param int end_time: End time filter (Unix timestamp)
        :return: ListProvisionersRatioResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'harness_account', 'start_time', 'end_time']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_list_provisioners_ratio" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_list_provisioners_ratio`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_list_provisioners_ratio`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_list_provisioners_ratio`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501

        query_params = []
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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/provisioners-ratio', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ListProvisionersRatioResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def workspaces_list_resources(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """List resources  # noqa: E501

        List resources associated with this workspace.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_list_resources(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: Workspace identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param list[str] resource_types: Resource types to filter by.
        :return: ListResourcesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_list_resources_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_list_resources_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
            return data

    def workspaces_list_resources_with_http_info(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """List resources  # noqa: E501

        List resources associated with this workspace.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_list_resources_with_http_info(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: Workspace identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param list[str] resource_types: Resource types to filter by.
        :return: ListResourcesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'identifier', 'harness_account', 'resource_types']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_list_resources" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_list_resources`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_list_resources`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `workspaces_list_resources`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_list_resources`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

        query_params = []
        if 'resource_types' in params:
            query_params.append(('resource_types', params['resource_types']))  # noqa: E501
            collection_formats['resource_types'] = 'multi'  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/{identifier}/resources', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ListResourcesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def workspaces_list_workspace_modules(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """List modules  # noqa: E501

        List modules associated with this workspace.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_list_workspace_modules(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: Identifier is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: WorkspaceModuleCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_list_workspace_modules_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_list_workspace_modules_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
            return data

    def workspaces_list_workspace_modules_with_http_info(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """List modules  # noqa: E501

        List modules associated with this workspace.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_list_workspace_modules_with_http_info(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: Identifier is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: WorkspaceModuleCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'identifier', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_list_workspace_modules" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_list_workspace_modules`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_list_workspace_modules`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `workspaces_list_workspace_modules`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_list_workspace_modules`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/{identifier}/modules', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='WorkspaceModuleCollection',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def workspaces_list_workspace_resource_type_attributes(self, org, project, workspace, resource_type, harness_account, **kwargs):  # noqa: E501
        """List workspace resource type attributes  # noqa: E501

        Retrieves the resource type attributes used by workspaces  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_list_workspace_resource_type_attributes(org, project, workspace, resource_type, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace identifier (required)
        :param str resource_type: Resource type (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: list[str]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_list_workspace_resource_type_attributes_with_http_info(org, project, workspace, resource_type, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_list_workspace_resource_type_attributes_with_http_info(org, project, workspace, resource_type, harness_account, **kwargs)  # noqa: E501
            return data

    def workspaces_list_workspace_resource_type_attributes_with_http_info(self, org, project, workspace, resource_type, harness_account, **kwargs):  # noqa: E501
        """List workspace resource type attributes  # noqa: E501

        Retrieves the resource type attributes used by workspaces  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_list_workspace_resource_type_attributes_with_http_info(org, project, workspace, resource_type, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace identifier (required)
        :param str resource_type: Resource type (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: list[str]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'workspace', 'resource_type', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_list_workspace_resource_type_attributes" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_list_workspace_resource_type_attributes`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_list_workspace_resource_type_attributes`")  # noqa: E501
        # verify the required parameter 'workspace' is set
        if ('workspace' not in params or
                params['workspace'] is None):
            raise ValueError("Missing the required parameter `workspace` when calling `workspaces_list_workspace_resource_type_attributes`")  # noqa: E501
        # verify the required parameter 'resource_type' is set
        if ('resource_type' not in params or
                params['resource_type'] is None):
            raise ValueError("Missing the required parameter `resource_type` when calling `workspaces_list_workspace_resource_type_attributes`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_list_workspace_resource_type_attributes`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'workspace' in params:
            path_params['workspace'] = params['workspace']  # noqa: E501
        if 'resource_type' in params:
            path_params['resource_type'] = params['resource_type']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/resource-types/{resource_type}/attributes', 'GET',
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

    def workspaces_list_workspace_resource_types(self, org, project, workspace, harness_account, **kwargs):  # noqa: E501
        """List workspace resource types  # noqa: E501

        Retrieves the resource types used by workspaces  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_list_workspace_resource_types(org, project, workspace, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace identifier (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: list[str]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_list_workspace_resource_types_with_http_info(org, project, workspace, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_list_workspace_resource_types_with_http_info(org, project, workspace, harness_account, **kwargs)  # noqa: E501
            return data

    def workspaces_list_workspace_resource_types_with_http_info(self, org, project, workspace, harness_account, **kwargs):  # noqa: E501
        """List workspace resource types  # noqa: E501

        Retrieves the resource types used by workspaces  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_list_workspace_resource_types_with_http_info(org, project, workspace, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace identifier (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: list[str]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'workspace', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_list_workspace_resource_types" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_list_workspace_resource_types`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_list_workspace_resource_types`")  # noqa: E501
        # verify the required parameter 'workspace' is set
        if ('workspace' not in params or
                params['workspace'] is None):
            raise ValueError("Missing the required parameter `workspace` when calling `workspaces_list_workspace_resource_types`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_list_workspace_resource_types`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'workspace' in params:
            path_params['workspace'] = params['workspace']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/resource-types', 'GET',
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

    def workspaces_list_workspace_resource_types_and_attributes(self, org, project, workspace, harness_account, **kwargs):  # noqa: E501
        """Map of resource types and their attributes  # noqa: E501

        Retrieves the resource type attributes used by workspaces and attributes  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_list_workspace_resource_types_and_attributes(org, project, workspace, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace identifier (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: dict(str, list[str])
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_list_workspace_resource_types_and_attributes_with_http_info(org, project, workspace, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_list_workspace_resource_types_and_attributes_with_http_info(org, project, workspace, harness_account, **kwargs)  # noqa: E501
            return data

    def workspaces_list_workspace_resource_types_and_attributes_with_http_info(self, org, project, workspace, harness_account, **kwargs):  # noqa: E501
        """Map of resource types and their attributes  # noqa: E501

        Retrieves the resource type attributes used by workspaces and attributes  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_list_workspace_resource_types_and_attributes_with_http_info(org, project, workspace, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace identifier (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: dict(str, list[str])
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'workspace', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_list_workspace_resource_types_and_attributes" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_list_workspace_resource_types_and_attributes`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_list_workspace_resource_types_and_attributes`")  # noqa: E501
        # verify the required parameter 'workspace' is set
        if ('workspace' not in params or
                params['workspace'] is None):
            raise ValueError("Missing the required parameter `workspace` when calling `workspaces_list_workspace_resource_types_and_attributes`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_list_workspace_resource_types_and_attributes`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'workspace' in params:
            path_params['workspace'] = params['workspace']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/resource-types-and-attributes', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='dict(str, list[str])',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def workspaces_list_workspaces(self, org, project, harness_account, **kwargs):  # noqa: E501
        """List workspaces  # noqa: E501

        List all workspaces.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_list_workspaces(org, project, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :param str search_term: Filter results by partial name match
        :param str sort: Sort order for results
        :param list[str] status: Status of the execution
        :param list[str] tags: Comma separated list of tags to filter by
        :return: WorkspaceResourceSummaryCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_list_workspaces_with_http_info(org, project, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_list_workspaces_with_http_info(org, project, harness_account, **kwargs)  # noqa: E501
            return data

    def workspaces_list_workspaces_with_http_info(self, org, project, harness_account, **kwargs):  # noqa: E501
        """List workspaces  # noqa: E501

        List all workspaces.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_list_workspaces_with_http_info(org, project, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :param str search_term: Filter results by partial name match
        :param str sort: Sort order for results
        :param list[str] status: Status of the execution
        :param list[str] tags: Comma separated list of tags to filter by
        :return: WorkspaceResourceSummaryCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'harness_account', 'limit', 'page', 'search_term', 'sort', 'status', 'tags']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_list_workspaces" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_list_workspaces`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_list_workspaces`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_list_workspaces`")  # noqa: E501

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
        if 'search_term' in params:
            query_params.append(('searchTerm', params['search_term']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501
        if 'status' in params:
            query_params.append(('status', params['status']))  # noqa: E501
            collection_formats['status'] = 'multi'  # noqa: E501
        if 'tags' in params:
            query_params.append(('tags', params['tags']))  # noqa: E501
            collection_formats['tags'] = 'multi'  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='WorkspaceResourceSummaryCollection',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def workspaces_search_resources(self, body, harness_account, org, project, identifier, **kwargs):  # noqa: E501
        """List resources using selectors  # noqa: E501

        List resources for a workspace using selectors.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_search_resources(body, harness_account, org, project, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param SearchResourcesRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: Workspace identifier (required)
        :return: SearchResourcesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_search_resources_with_http_info(body, harness_account, org, project, identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_search_resources_with_http_info(body, harness_account, org, project, identifier, **kwargs)  # noqa: E501
            return data

    def workspaces_search_resources_with_http_info(self, body, harness_account, org, project, identifier, **kwargs):  # noqa: E501
        """List resources using selectors  # noqa: E501

        List resources for a workspace using selectors.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_search_resources_with_http_info(body, harness_account, org, project, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param SearchResourcesRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: Workspace identifier (required)
        :return: SearchResourcesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account', 'org', 'project', 'identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_search_resources" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `workspaces_search_resources`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_search_resources`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_search_resources`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_search_resources`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `workspaces_search_resources`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/{identifier}/resources/search', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SearchResourcesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def workspaces_send_event(self, body, harness_account, org, project, workspace, **kwargs):  # noqa: E501
        """Send event  # noqa: E501

        Store binary data generated by the provisioner, such as plans and state files.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_send_event(body, harness_account, org, project, workspace, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param SendEventRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace associated with this event (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_send_event_with_http_info(body, harness_account, org, project, workspace, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_send_event_with_http_info(body, harness_account, org, project, workspace, **kwargs)  # noqa: E501
            return data

    def workspaces_send_event_with_http_info(self, body, harness_account, org, project, workspace, **kwargs):  # noqa: E501
        """Send event  # noqa: E501

        Store binary data generated by the provisioner, such as plans and state files.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_send_event_with_http_info(body, harness_account, org, project, workspace, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param SendEventRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace associated with this event (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account', 'org', 'project', 'workspace']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_send_event" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `workspaces_send_event`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_send_event`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_send_event`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_send_event`")  # noqa: E501
        # verify the required parameter 'workspace' is set
        if ('workspace' not in params or
                params['workspace'] is None):
            raise ValueError("Missing the required parameter `workspace` when calling `workspaces_send_event`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'workspace' in params:
            path_params['workspace'] = params['workspace']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/events', 'POST',
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

    def workspaces_show_data(self, org, project, workspace, id, harness_account, **kwargs):  # noqa: E501
        """Show data  # noqa: E501

        Get binary data generated by the provisioner, such as plans and state files.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_show_data(org, project, workspace, id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace is the resource workspace this variable is associated with. (required)
        :param str id: The unique identifier for the data (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_show_data_with_http_info(org, project, workspace, id, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_show_data_with_http_info(org, project, workspace, id, harness_account, **kwargs)  # noqa: E501
            return data

    def workspaces_show_data_with_http_info(self, org, project, workspace, id, harness_account, **kwargs):  # noqa: E501
        """Show data  # noqa: E501

        Get binary data generated by the provisioner, such as plans and state files.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_show_data_with_http_info(org, project, workspace, id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace is the resource workspace this variable is associated with. (required)
        :param str id: The unique identifier for the data (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'workspace', 'id', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_show_data" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_show_data`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_show_data`")  # noqa: E501
        # verify the required parameter 'workspace' is set
        if ('workspace' not in params or
                params['workspace'] is None):
            raise ValueError("Missing the required parameter `workspace` when calling `workspaces_show_data`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `workspaces_show_data`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_show_data`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'workspace' in params:
            path_params['workspace'] = params['workspace']  # noqa: E501
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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/data/{id}', 'GET',
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

    def workspaces_show_workspace(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """Show workspace  # noqa: E501

        Show an individual workspace.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_show_workspace(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: Identifier is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: WorkspacesShowWorkspaceResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_show_workspace_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_show_workspace_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
            return data

    def workspaces_show_workspace_with_http_info(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """Show workspace  # noqa: E501

        Show an individual workspace.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_show_workspace_with_http_info(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: Identifier is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: WorkspacesShowWorkspaceResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'identifier', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_show_workspace" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_show_workspace`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_show_workspace`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `workspaces_show_workspace`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_show_workspace`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/{identifier}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='WorkspacesShowWorkspaceResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def workspaces_show_workspace_metrics(self, org, project, harness_account, **kwargs):  # noqa: E501
        """Show workspace metrics  # noqa: E501

        Show metrics for workspaces  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_show_workspace_metrics(org, project, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int start_time: Start time filter (Unix timestamp)
        :param int end_time: End time filter (Unix timestamp)
        :return: ShowWorkspaceMetricsRequest
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_show_workspace_metrics_with_http_info(org, project, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_show_workspace_metrics_with_http_info(org, project, harness_account, **kwargs)  # noqa: E501
            return data

    def workspaces_show_workspace_metrics_with_http_info(self, org, project, harness_account, **kwargs):  # noqa: E501
        """Show workspace metrics  # noqa: E501

        Show metrics for workspaces  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_show_workspace_metrics_with_http_info(org, project, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int start_time: Start time filter (Unix timestamp)
        :param int end_time: End time filter (Unix timestamp)
        :return: ShowWorkspaceMetricsRequest
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'harness_account', 'start_time', 'end_time']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_show_workspace_metrics" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_show_workspace_metrics`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_show_workspace_metrics`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_show_workspace_metrics`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501

        query_params = []
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
            '/iacm/api/orgs/{org}/projects/{project}/workspace-metrics', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ShowWorkspaceMetricsRequest',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def workspaces_update_resources(self, body, harness_account, org, project, workspace, **kwargs):  # noqa: E501
        """Update resources  # noqa: E501

        Updates resources for a workspace.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_update_resources(body, harness_account, org, project, workspace, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateResourcesRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace identifier (required)
        :return: UpdateResourcesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_update_resources_with_http_info(body, harness_account, org, project, workspace, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_update_resources_with_http_info(body, harness_account, org, project, workspace, **kwargs)  # noqa: E501
            return data

    def workspaces_update_resources_with_http_info(self, body, harness_account, org, project, workspace, **kwargs):  # noqa: E501
        """Update resources  # noqa: E501

        Updates resources for a workspace.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_update_resources_with_http_info(body, harness_account, org, project, workspace, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateResourcesRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace identifier (required)
        :return: UpdateResourcesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account', 'org', 'project', 'workspace']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_update_resources" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `workspaces_update_resources`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_update_resources`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_update_resources`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_update_resources`")  # noqa: E501
        # verify the required parameter 'workspace' is set
        if ('workspace' not in params or
                params['workspace'] is None):
            raise ValueError("Missing the required parameter `workspace` when calling `workspaces_update_resources`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'workspace' in params:
            path_params['workspace'] = params['workspace']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/resources', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UpdateResourcesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def workspaces_update_workspace(self, body, harness_account, org, project, identifier, **kwargs):  # noqa: E501
        """Update workspace  # noqa: E501

        Updates the given workspace with new info.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_update_workspace(body, harness_account, org, project, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateWorkspaceRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: Workspace identifier. (required)
        :return: UpdateWorkspaceResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_update_workspace_with_http_info(body, harness_account, org, project, identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_update_workspace_with_http_info(body, harness_account, org, project, identifier, **kwargs)  # noqa: E501
            return data

    def workspaces_update_workspace_with_http_info(self, body, harness_account, org, project, identifier, **kwargs):  # noqa: E501
        """Update workspace  # noqa: E501

        Updates the given workspace with new info.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_update_workspace_with_http_info(body, harness_account, org, project, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateWorkspaceRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: Workspace identifier. (required)
        :return: UpdateWorkspaceResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account', 'org', 'project', 'identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_update_workspace" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `workspaces_update_workspace`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_update_workspace`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_update_workspace`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_update_workspace`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `workspaces_update_workspace`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/{identifier}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UpdateWorkspaceResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def workspaces_upload_remote_execution(self, org, project, workspace, id, harness_account, content_digest, **kwargs):  # noqa: E501
        """Upload remote execution source  # noqa: E501

        Upload the source code for the remote execution.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_upload_remote_execution(org, project, workspace, id, harness_account, content_digest, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace is the resource workspace this variable is associated with. (required)
        :param str id: The ID of the remote execution (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str content_digest: Content-Digest header as defined in https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Digest. Sha256 is the only supported algorithm. (required)
        :param int content_length: Size in bytes of the source code.
        :return: UploadRemoteExecutionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.workspaces_upload_remote_execution_with_http_info(org, project, workspace, id, harness_account, content_digest, **kwargs)  # noqa: E501
        else:
            (data) = self.workspaces_upload_remote_execution_with_http_info(org, project, workspace, id, harness_account, content_digest, **kwargs)  # noqa: E501
            return data

    def workspaces_upload_remote_execution_with_http_info(self, org, project, workspace, id, harness_account, content_digest, **kwargs):  # noqa: E501
        """Upload remote execution source  # noqa: E501

        Upload the source code for the remote execution.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.workspaces_upload_remote_execution_with_http_info(org, project, workspace, id, harness_account, content_digest, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str workspace: Workspace is the resource workspace this variable is associated with. (required)
        :param str id: The ID of the remote execution (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str content_digest: Content-Digest header as defined in https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Digest. Sha256 is the only supported algorithm. (required)
        :param int content_length: Size in bytes of the source code.
        :return: UploadRemoteExecutionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'workspace', 'id', 'harness_account', 'content_digest', 'content_length']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workspaces_upload_remote_execution" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `workspaces_upload_remote_execution`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `workspaces_upload_remote_execution`")  # noqa: E501
        # verify the required parameter 'workspace' is set
        if ('workspace' not in params or
                params['workspace'] is None):
            raise ValueError("Missing the required parameter `workspace` when calling `workspaces_upload_remote_execution`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `workspaces_upload_remote_execution`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `workspaces_upload_remote_execution`")  # noqa: E501
        # verify the required parameter 'content_digest' is set
        if ('content_digest' not in params or
                params['content_digest'] is None):
            raise ValueError("Missing the required parameter `content_digest` when calling `workspaces_upload_remote_execution`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'workspace' in params:
            path_params['workspace'] = params['workspace']  # noqa: E501
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501
        if 'content_length' in params:
            header_params['Content-Length'] = params['content_length']  # noqa: E501
        if 'content_digest' in params:
            header_params['Content-Digest'] = params['content_digest']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/vnd.goa.error'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/orgs/{org}/projects/{project}/workspaces/{workspace}/remote-executions/{id}/upload', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UploadRemoteExecutionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
