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


class AnsibleApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def ansible_create_data(self, data_type, inventories, playbooks, org, project, harness_account, **kwargs):  # noqa: E501
        """Create data  # noqa: E501

        Store binary data generated by ansible.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_create_data(data_type, inventories, playbooks, org, project, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str data_type: Type of data stored (required)
        :param str inventories: Inventories associated with this event (required)
        :param str playbooks: Playbooks associated with this event (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str pipeline_id: The unique identifier for the associated pipeline
        :param str stage_id: The unique identifier for a stage
        :param str pipeline_execution_id: The unique identifier for the associated pipeline execution
        :param str pipeline_stage_id: The unique identifier for the associated pipeline execution stage
        :param int content_length: Size in bytes of the data.
        :return: CreateAnsibleDataResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_create_data_with_http_info(data_type, inventories, playbooks, org, project, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_create_data_with_http_info(data_type, inventories, playbooks, org, project, harness_account, **kwargs)  # noqa: E501
            return data

    def ansible_create_data_with_http_info(self, data_type, inventories, playbooks, org, project, harness_account, **kwargs):  # noqa: E501
        """Create data  # noqa: E501

        Store binary data generated by ansible.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_create_data_with_http_info(data_type, inventories, playbooks, org, project, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str data_type: Type of data stored (required)
        :param str inventories: Inventories associated with this event (required)
        :param str playbooks: Playbooks associated with this event (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str pipeline_id: The unique identifier for the associated pipeline
        :param str stage_id: The unique identifier for a stage
        :param str pipeline_execution_id: The unique identifier for the associated pipeline execution
        :param str pipeline_stage_id: The unique identifier for the associated pipeline execution stage
        :param int content_length: Size in bytes of the data.
        :return: CreateAnsibleDataResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['data_type', 'inventories', 'playbooks', 'org', 'project', 'harness_account', 'pipeline_id', 'stage_id', 'pipeline_execution_id', 'pipeline_stage_id', 'content_length']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method ansible_create_data" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'data_type' is set
        if ('data_type' not in params or
                params['data_type'] is None):
            raise ValueError("Missing the required parameter `data_type` when calling `ansible_create_data`")  # noqa: E501
        # verify the required parameter 'inventories' is set
        if ('inventories' not in params or
                params['inventories'] is None):
            raise ValueError("Missing the required parameter `inventories` when calling `ansible_create_data`")  # noqa: E501
        # verify the required parameter 'playbooks' is set
        if ('playbooks' not in params or
                params['playbooks'] is None):
            raise ValueError("Missing the required parameter `playbooks` when calling `ansible_create_data`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_create_data`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_create_data`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_create_data`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501

        query_params = []
        if 'pipeline_id' in params:
            query_params.append(('pipeline_id', params['pipeline_id']))  # noqa: E501
        if 'stage_id' in params:
            query_params.append(('stage_id', params['stage_id']))  # noqa: E501
        if 'pipeline_execution_id' in params:
            query_params.append(('pipeline_execution_id', params['pipeline_execution_id']))  # noqa: E501
        if 'pipeline_stage_id' in params:
            query_params.append(('pipeline_stage_id', params['pipeline_stage_id']))  # noqa: E501
        if 'data_type' in params:
            query_params.append(('data_type', params['data_type']))  # noqa: E501
        if 'inventories' in params:
            query_params.append(('inventories', params['inventories']))  # noqa: E501
        if 'playbooks' in params:
            query_params.append(('playbooks', params['playbooks']))  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/ansible/data', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CreateAnsibleDataResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def ansible_create_inventory(self, body, harness_account, org, project, **kwargs):  # noqa: E501
        """Create Ansible inventory  # noqa: E501

        Create a new inventory.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_create_inventory(body, harness_account, org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateInventoryRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :return: CreateInventoryResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_create_inventory_with_http_info(body, harness_account, org, project, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_create_inventory_with_http_info(body, harness_account, org, project, **kwargs)  # noqa: E501
            return data

    def ansible_create_inventory_with_http_info(self, body, harness_account, org, project, **kwargs):  # noqa: E501
        """Create Ansible inventory  # noqa: E501

        Create a new inventory.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_create_inventory_with_http_info(body, harness_account, org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateInventoryRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :return: CreateInventoryResponse
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
                    " to method ansible_create_inventory" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `ansible_create_inventory`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_create_inventory`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_create_inventory`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_create_inventory`")  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/ansible/inventory', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CreateInventoryResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def ansible_create_inventory_group(self, body, harness_account, org, project, inventory_identifier, **kwargs):  # noqa: E501
        """Create Ansible inventory group  # noqa: E501

        Create a new inventory group.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_create_inventory_group(body, harness_account, org, project, inventory_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateInventoryGroupRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str inventory_identifier: The unique identifier for this inventory (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_create_inventory_group_with_http_info(body, harness_account, org, project, inventory_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_create_inventory_group_with_http_info(body, harness_account, org, project, inventory_identifier, **kwargs)  # noqa: E501
            return data

    def ansible_create_inventory_group_with_http_info(self, body, harness_account, org, project, inventory_identifier, **kwargs):  # noqa: E501
        """Create Ansible inventory group  # noqa: E501

        Create a new inventory group.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_create_inventory_group_with_http_info(body, harness_account, org, project, inventory_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateInventoryGroupRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str inventory_identifier: The unique identifier for this inventory (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account', 'org', 'project', 'inventory_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method ansible_create_inventory_group" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `ansible_create_inventory_group`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_create_inventory_group`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_create_inventory_group`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_create_inventory_group`")  # noqa: E501
        # verify the required parameter 'inventory_identifier' is set
        if ('inventory_identifier' not in params or
                params['inventory_identifier'] is None):
            raise ValueError("Missing the required parameter `inventory_identifier` when calling `ansible_create_inventory_group`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'inventory_identifier' in params:
            path_params['inventory_identifier'] = params['inventory_identifier']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/ansible/inventory/{inventory_identifier}/groups', 'POST',
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

    def ansible_create_inventory_host(self, body, harness_account, org, project, identifier, **kwargs):  # noqa: E501
        """Create Ansible inventory host  # noqa: E501

        Create a new inventory host.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_create_inventory_host(body, harness_account, org, project, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateInventoryHostRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this inventory (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_create_inventory_host_with_http_info(body, harness_account, org, project, identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_create_inventory_host_with_http_info(body, harness_account, org, project, identifier, **kwargs)  # noqa: E501
            return data

    def ansible_create_inventory_host_with_http_info(self, body, harness_account, org, project, identifier, **kwargs):  # noqa: E501
        """Create Ansible inventory host  # noqa: E501

        Create a new inventory host.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_create_inventory_host_with_http_info(body, harness_account, org, project, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateInventoryHostRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this inventory (required)
        :return: None
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
                    " to method ansible_create_inventory_host" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `ansible_create_inventory_host`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_create_inventory_host`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_create_inventory_host`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_create_inventory_host`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `ansible_create_inventory_host`")  # noqa: E501

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
            ['application/vnd.goa.error'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/orgs/{org}/projects/{project}/ansible/inventory/{identifier}/hosts', 'POST',
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

    def ansible_create_inventory_vars(self, body, harness_account, org, project, identifier, **kwargs):  # noqa: E501
        """Create Ansible inventory variables  # noqa: E501

        Create new inventory variables.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_create_inventory_vars(body, harness_account, org, project, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateInventoryVarsRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this inventory (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_create_inventory_vars_with_http_info(body, harness_account, org, project, identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_create_inventory_vars_with_http_info(body, harness_account, org, project, identifier, **kwargs)  # noqa: E501
            return data

    def ansible_create_inventory_vars_with_http_info(self, body, harness_account, org, project, identifier, **kwargs):  # noqa: E501
        """Create Ansible inventory variables  # noqa: E501

        Create new inventory variables.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_create_inventory_vars_with_http_info(body, harness_account, org, project, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateInventoryVarsRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this inventory (required)
        :return: None
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
                    " to method ansible_create_inventory_vars" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `ansible_create_inventory_vars`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_create_inventory_vars`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_create_inventory_vars`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_create_inventory_vars`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `ansible_create_inventory_vars`")  # noqa: E501

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
            ['application/vnd.goa.error'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/orgs/{org}/projects/{project}/ansible/inventory/{identifier}/vars', 'POST',
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

    def ansible_create_playbook(self, body, harness_account, org, project, **kwargs):  # noqa: E501
        """Create Ansible playbook  # noqa: E501

        Create a new playbook.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_create_playbook(body, harness_account, org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreatePlaybookRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :return: CreatePlaybookResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_create_playbook_with_http_info(body, harness_account, org, project, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_create_playbook_with_http_info(body, harness_account, org, project, **kwargs)  # noqa: E501
            return data

    def ansible_create_playbook_with_http_info(self, body, harness_account, org, project, **kwargs):  # noqa: E501
        """Create Ansible playbook  # noqa: E501

        Create a new playbook.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_create_playbook_with_http_info(body, harness_account, org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreatePlaybookRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :return: CreatePlaybookResponse
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
                    " to method ansible_create_playbook" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `ansible_create_playbook`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_create_playbook`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_create_playbook`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_create_playbook`")  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/ansible/playbook', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CreatePlaybookResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def ansible_create_playbook_vars(self, body, harness_account, org, project, identifier, **kwargs):  # noqa: E501
        """Create dynamic Ansible playbook variable  # noqa: E501

        Create a new dynamic playbook variable.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_create_playbook_vars(body, harness_account, org, project, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreatePlaybookVarRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this inventory (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_create_playbook_vars_with_http_info(body, harness_account, org, project, identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_create_playbook_vars_with_http_info(body, harness_account, org, project, identifier, **kwargs)  # noqa: E501
            return data

    def ansible_create_playbook_vars_with_http_info(self, body, harness_account, org, project, identifier, **kwargs):  # noqa: E501
        """Create dynamic Ansible playbook variable  # noqa: E501

        Create a new dynamic playbook variable.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_create_playbook_vars_with_http_info(body, harness_account, org, project, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreatePlaybookVarRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this inventory (required)
        :return: None
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
                    " to method ansible_create_playbook_vars" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `ansible_create_playbook_vars`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_create_playbook_vars`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_create_playbook_vars`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_create_playbook_vars`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `ansible_create_playbook_vars`")  # noqa: E501

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
            ['application/vnd.goa.error'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/orgs/{org}/projects/{project}/ansible/playbook/{identifier}/vars', 'POST',
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

    def ansible_delete_inventory(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """Delete Ansible inventory  # noqa: E501

        Delete an existing inventory.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_delete_inventory(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this inventory (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_delete_inventory_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_delete_inventory_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
            return data

    def ansible_delete_inventory_with_http_info(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """Delete Ansible inventory  # noqa: E501

        Delete an existing inventory.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_delete_inventory_with_http_info(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this inventory (required)
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
                    " to method ansible_delete_inventory" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_delete_inventory`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_delete_inventory`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `ansible_delete_inventory`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_delete_inventory`")  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/ansible/inventory/{identifier}', 'DELETE',
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

    def ansible_delete_inventory_group(self, org, project, inventory_identifier, identifier, harness_account, **kwargs):  # noqa: E501
        """Delete Ansible inventory group  # noqa: E501

        Delete an existing inventory group.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_delete_inventory_group(org, project, inventory_identifier, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str inventory_identifier: The unique identifier for this inventory (required)
        :param str identifier: The identifier of the group (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_delete_inventory_group_with_http_info(org, project, inventory_identifier, identifier, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_delete_inventory_group_with_http_info(org, project, inventory_identifier, identifier, harness_account, **kwargs)  # noqa: E501
            return data

    def ansible_delete_inventory_group_with_http_info(self, org, project, inventory_identifier, identifier, harness_account, **kwargs):  # noqa: E501
        """Delete Ansible inventory group  # noqa: E501

        Delete an existing inventory group.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_delete_inventory_group_with_http_info(org, project, inventory_identifier, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str inventory_identifier: The unique identifier for this inventory (required)
        :param str identifier: The identifier of the group (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'inventory_identifier', 'identifier', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method ansible_delete_inventory_group" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_delete_inventory_group`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_delete_inventory_group`")  # noqa: E501
        # verify the required parameter 'inventory_identifier' is set
        if ('inventory_identifier' not in params or
                params['inventory_identifier'] is None):
            raise ValueError("Missing the required parameter `inventory_identifier` when calling `ansible_delete_inventory_group`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `ansible_delete_inventory_group`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_delete_inventory_group`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'inventory_identifier' in params:
            path_params['inventory_identifier'] = params['inventory_identifier']  # noqa: E501
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
            '/iacm/api/orgs/{org}/projects/{project}/ansible/inventory/{inventory_identifier}/groups/{identifier}', 'DELETE',
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

    def ansible_delete_inventory_host(self, org, project, inventory_identifier, host_address, harness_account, **kwargs):  # noqa: E501
        """Delete Ansible inventory host  # noqa: E501

        Delete a inventory host.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_delete_inventory_host(org, project, inventory_identifier, host_address, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str inventory_identifier: The unique identifier for this inventory (required)
        :param str host_address: Host address is the address of the host. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_delete_inventory_host_with_http_info(org, project, inventory_identifier, host_address, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_delete_inventory_host_with_http_info(org, project, inventory_identifier, host_address, harness_account, **kwargs)  # noqa: E501
            return data

    def ansible_delete_inventory_host_with_http_info(self, org, project, inventory_identifier, host_address, harness_account, **kwargs):  # noqa: E501
        """Delete Ansible inventory host  # noqa: E501

        Delete a inventory host.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_delete_inventory_host_with_http_info(org, project, inventory_identifier, host_address, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str inventory_identifier: The unique identifier for this inventory (required)
        :param str host_address: Host address is the address of the host. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'inventory_identifier', 'host_address', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method ansible_delete_inventory_host" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_delete_inventory_host`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_delete_inventory_host`")  # noqa: E501
        # verify the required parameter 'inventory_identifier' is set
        if ('inventory_identifier' not in params or
                params['inventory_identifier'] is None):
            raise ValueError("Missing the required parameter `inventory_identifier` when calling `ansible_delete_inventory_host`")  # noqa: E501
        # verify the required parameter 'host_address' is set
        if ('host_address' not in params or
                params['host_address'] is None):
            raise ValueError("Missing the required parameter `host_address` when calling `ansible_delete_inventory_host`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_delete_inventory_host`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'inventory_identifier' in params:
            path_params['inventory_identifier'] = params['inventory_identifier']  # noqa: E501
        if 'host_address' in params:
            path_params['host_address'] = params['host_address']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/ansible/inventory/{inventory_identifier}/hosts/{host_address}', 'DELETE',
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

    def ansible_delete_inventory_var(self, org, project, identifier, uuid, harness_account, **kwargs):  # noqa: E501
        """Delete Ansible inventory variable  # noqa: E501

        Delete a inventory variable.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_delete_inventory_var(org, project, identifier, uuid, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this inventory (required)
        :param str uuid: UUID is the unique identifier for the secret. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_delete_inventory_var_with_http_info(org, project, identifier, uuid, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_delete_inventory_var_with_http_info(org, project, identifier, uuid, harness_account, **kwargs)  # noqa: E501
            return data

    def ansible_delete_inventory_var_with_http_info(self, org, project, identifier, uuid, harness_account, **kwargs):  # noqa: E501
        """Delete Ansible inventory variable  # noqa: E501

        Delete a inventory variable.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_delete_inventory_var_with_http_info(org, project, identifier, uuid, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this inventory (required)
        :param str uuid: UUID is the unique identifier for the secret. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'identifier', 'uuid', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method ansible_delete_inventory_var" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_delete_inventory_var`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_delete_inventory_var`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `ansible_delete_inventory_var`")  # noqa: E501
        # verify the required parameter 'uuid' is set
        if ('uuid' not in params or
                params['uuid'] is None):
            raise ValueError("Missing the required parameter `uuid` when calling `ansible_delete_inventory_var`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_delete_inventory_var`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501
        if 'uuid' in params:
            path_params['uuid'] = params['uuid']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/ansible/inventory/{identifier}/vars/{uuid}', 'DELETE',
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

    def ansible_delete_inventory_vars(self, body, harness_account, org, project, identifier, **kwargs):  # noqa: E501
        """Delete Ansible inventory variables  # noqa: E501

        Delete inventory variables.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_delete_inventory_vars(body, harness_account, org, project, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param DeleteInventoryVarsRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this inventory (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_delete_inventory_vars_with_http_info(body, harness_account, org, project, identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_delete_inventory_vars_with_http_info(body, harness_account, org, project, identifier, **kwargs)  # noqa: E501
            return data

    def ansible_delete_inventory_vars_with_http_info(self, body, harness_account, org, project, identifier, **kwargs):  # noqa: E501
        """Delete Ansible inventory variables  # noqa: E501

        Delete inventory variables.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_delete_inventory_vars_with_http_info(body, harness_account, org, project, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param DeleteInventoryVarsRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this inventory (required)
        :return: None
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
                    " to method ansible_delete_inventory_vars" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `ansible_delete_inventory_vars`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_delete_inventory_vars`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_delete_inventory_vars`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_delete_inventory_vars`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `ansible_delete_inventory_vars`")  # noqa: E501

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
            ['application/vnd.goa.error'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/orgs/{org}/projects/{project}/ansible/inventory/{identifier}/vars', 'DELETE',
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

    def ansible_delete_playbook(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """Delete Ansible playbook  # noqa: E501

        Delete an existing playbook.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_delete_playbook(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this playbook (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_delete_playbook_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_delete_playbook_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
            return data

    def ansible_delete_playbook_with_http_info(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """Delete Ansible playbook  # noqa: E501

        Delete an existing playbook.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_delete_playbook_with_http_info(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this playbook (required)
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
                    " to method ansible_delete_playbook" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_delete_playbook`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_delete_playbook`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `ansible_delete_playbook`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_delete_playbook`")  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/ansible/playbook/{identifier}', 'DELETE',
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

    def ansible_delete_playbook_vars(self, body, harness_account, org, project, identifier, **kwargs):  # noqa: E501
        """Delete dynamic Ansible playbook variable  # noqa: E501

        Delete a dynamic playbook variable.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_delete_playbook_vars(body, harness_account, org, project, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param DeletePlaybookVarsRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this inventory (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_delete_playbook_vars_with_http_info(body, harness_account, org, project, identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_delete_playbook_vars_with_http_info(body, harness_account, org, project, identifier, **kwargs)  # noqa: E501
            return data

    def ansible_delete_playbook_vars_with_http_info(self, body, harness_account, org, project, identifier, **kwargs):  # noqa: E501
        """Delete dynamic Ansible playbook variable  # noqa: E501

        Delete a dynamic playbook variable.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_delete_playbook_vars_with_http_info(body, harness_account, org, project, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param DeletePlaybookVarsRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this inventory (required)
        :return: None
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
                    " to method ansible_delete_playbook_vars" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `ansible_delete_playbook_vars`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_delete_playbook_vars`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_delete_playbook_vars`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_delete_playbook_vars`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `ansible_delete_playbook_vars`")  # noqa: E501

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
            ['application/vnd.goa.error'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/orgs/{org}/projects/{project}/ansible/playbook/{identifier}/vars', 'DELETE',
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

    def ansible_list_ansible_activities(self, org, project, harness_account, **kwargs):  # noqa: E501
        """List Ansible Activities  # noqa: E501

        List all activities.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_list_ansible_activities(org, project, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :param str sort: Sort order for results
        :param str inventory_search_term: Search term to filter by inventory identifier
        :param str playbook_search_term: Search term to filter by playbook identifier
        :param str activity_type: Activity type filter
        :param str status: Activity status filter
        :return: AnsibleActivityResourceCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_list_ansible_activities_with_http_info(org, project, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_list_ansible_activities_with_http_info(org, project, harness_account, **kwargs)  # noqa: E501
            return data

    def ansible_list_ansible_activities_with_http_info(self, org, project, harness_account, **kwargs):  # noqa: E501
        """List Ansible Activities  # noqa: E501

        List all activities.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_list_ansible_activities_with_http_info(org, project, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :param str sort: Sort order for results
        :param str inventory_search_term: Search term to filter by inventory identifier
        :param str playbook_search_term: Search term to filter by playbook identifier
        :param str activity_type: Activity type filter
        :param str status: Activity status filter
        :return: AnsibleActivityResourceCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'harness_account', 'limit', 'page', 'sort', 'inventory_search_term', 'playbook_search_term', 'activity_type', 'status']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method ansible_list_ansible_activities" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_list_ansible_activities`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_list_ansible_activities`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_list_ansible_activities`")  # noqa: E501

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
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501
        if 'inventory_search_term' in params:
            query_params.append(('InventorySearchTerm', params['inventory_search_term']))  # noqa: E501
        if 'playbook_search_term' in params:
            query_params.append(('PlaybookSearchTerm', params['playbook_search_term']))  # noqa: E501
        if 'activity_type' in params:
            query_params.append(('activity_type', params['activity_type']))  # noqa: E501
        if 'status' in params:
            query_params.append(('status', params['status']))  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/ansible/activities', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AnsibleActivityResourceCollection',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def ansible_list_data(self, org, project, harness_account, **kwargs):  # noqa: E501
        """List data  # noqa: E501

        List all stored data for a inventory or playbook.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_list_data(org, project, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str inventory_search_term: Inventory search term
        :param str playbook_search_term: Playbook search term
        :param str pipeline_execution_id: Filter by pipeline execution ID
        :param str pipeline_stage_id: Filter by pipeline execution stage ID
        :param str data_type: Filter by data type
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :return: AnsibleDataResourceCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_list_data_with_http_info(org, project, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_list_data_with_http_info(org, project, harness_account, **kwargs)  # noqa: E501
            return data

    def ansible_list_data_with_http_info(self, org, project, harness_account, **kwargs):  # noqa: E501
        """List data  # noqa: E501

        List all stored data for a inventory or playbook.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_list_data_with_http_info(org, project, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str inventory_search_term: Inventory search term
        :param str playbook_search_term: Playbook search term
        :param str pipeline_execution_id: Filter by pipeline execution ID
        :param str pipeline_stage_id: Filter by pipeline execution stage ID
        :param str data_type: Filter by data type
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :return: AnsibleDataResourceCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'harness_account', 'inventory_search_term', 'playbook_search_term', 'pipeline_execution_id', 'pipeline_stage_id', 'data_type', 'limit', 'page']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method ansible_list_data" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_list_data`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_list_data`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_list_data`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501

        query_params = []
        if 'inventory_search_term' in params:
            query_params.append(('inventory_search_term', params['inventory_search_term']))  # noqa: E501
        if 'playbook_search_term' in params:
            query_params.append(('playbook_search_term', params['playbook_search_term']))  # noqa: E501
        if 'pipeline_execution_id' in params:
            query_params.append(('pipeline_execution_id', params['pipeline_execution_id']))  # noqa: E501
        if 'pipeline_stage_id' in params:
            query_params.append(('pipeline_stage_id', params['pipeline_stage_id']))  # noqa: E501
        if 'data_type' in params:
            query_params.append(('data_type', params['data_type']))  # noqa: E501
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
            '/iacm/api/orgs/{org}/projects/{project}/ansible/data', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AnsibleDataResourceCollection',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def ansible_list_inventory(self, org, project, harness_account, **kwargs):  # noqa: E501
        """List Ansible inventory  # noqa: E501

        List all inventories.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_list_inventory(org, project, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :param str search_term: Filter results by partial name match
        :param str sort: Sort order for results
        :param bool include_details: Include inventory details
        :return: InventoryDetailResourceCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_list_inventory_with_http_info(org, project, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_list_inventory_with_http_info(org, project, harness_account, **kwargs)  # noqa: E501
            return data

    def ansible_list_inventory_with_http_info(self, org, project, harness_account, **kwargs):  # noqa: E501
        """List Ansible inventory  # noqa: E501

        List all inventories.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_list_inventory_with_http_info(org, project, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :param str search_term: Filter results by partial name match
        :param str sort: Sort order for results
        :param bool include_details: Include inventory details
        :return: InventoryDetailResourceCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'harness_account', 'limit', 'page', 'search_term', 'sort', 'include_details']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method ansible_list_inventory" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_list_inventory`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_list_inventory`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_list_inventory`")  # noqa: E501

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
        if 'include_details' in params:
            query_params.append(('includeDetails', params['include_details']))  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/ansible/inventory', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InventoryDetailResourceCollection',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def ansible_list_playbooks(self, org, project, harness_account, **kwargs):  # noqa: E501
        """List Ansible playbooks  # noqa: E501

        List all playbooks.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_list_playbooks(org, project, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :param str search_term: Filter results by partial name match
        :param str sort: Sort order for results
        :return: PlaybookResourceCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_list_playbooks_with_http_info(org, project, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_list_playbooks_with_http_info(org, project, harness_account, **kwargs)  # noqa: E501
            return data

    def ansible_list_playbooks_with_http_info(self, org, project, harness_account, **kwargs):  # noqa: E501
        """List Ansible playbooks  # noqa: E501

        List all playbooks.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_list_playbooks_with_http_info(org, project, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :param str search_term: Filter results by partial name match
        :param str sort: Sort order for results
        :return: PlaybookResourceCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'harness_account', 'limit', 'page', 'search_term', 'sort']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method ansible_list_playbooks" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_list_playbooks`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_list_playbooks`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_list_playbooks`")  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/ansible/playbook', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='PlaybookResourceCollection',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def ansible_send_ansible_event(self, body, harness_account, org, project, **kwargs):  # noqa: E501
        """Send event  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_send_ansible_event(body, harness_account, org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param SendAnsibleEventRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_send_ansible_event_with_http_info(body, harness_account, org, project, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_send_ansible_event_with_http_info(body, harness_account, org, project, **kwargs)  # noqa: E501
            return data

    def ansible_send_ansible_event_with_http_info(self, body, harness_account, org, project, **kwargs):  # noqa: E501
        """Send event  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_send_ansible_event_with_http_info(body, harness_account, org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param SendAnsibleEventRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :return: None
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
                    " to method ansible_send_ansible_event" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `ansible_send_ansible_event`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_send_ansible_event`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_send_ansible_event`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_send_ansible_event`")  # noqa: E501

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
            ['application/vnd.goa.error'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/orgs/{org}/projects/{project}/ansible/events', 'POST',
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

    def ansible_show_ansible_activity(self, org, project, id, harness_account, **kwargs):  # noqa: E501
        """Show ansible activity  # noqa: E501

        Show an individual ansible activity.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_show_ansible_activity(org, project, id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str id: The unique ID for this activity (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: ShowAnsibleActivityResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_show_ansible_activity_with_http_info(org, project, id, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_show_ansible_activity_with_http_info(org, project, id, harness_account, **kwargs)  # noqa: E501
            return data

    def ansible_show_ansible_activity_with_http_info(self, org, project, id, harness_account, **kwargs):  # noqa: E501
        """Show ansible activity  # noqa: E501

        Show an individual ansible activity.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_show_ansible_activity_with_http_info(org, project, id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str id: The unique ID for this activity (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: ShowAnsibleActivityResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'id', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method ansible_show_ansible_activity" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_show_ansible_activity`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_show_ansible_activity`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `ansible_show_ansible_activity`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_show_ansible_activity`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
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
            '/iacm/api/orgs/{org}/projects/{project}/ansible/activities/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ShowAnsibleActivityResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def ansible_show_data(self, org, project, id, harness_account, **kwargs):  # noqa: E501
        """Show data  # noqa: E501

        Get binary data generated by the provisioner, such as plans and state files.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_show_data(org, project, id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str id: The unique identifier for the data (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_show_data_with_http_info(org, project, id, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_show_data_with_http_info(org, project, id, harness_account, **kwargs)  # noqa: E501
            return data

    def ansible_show_data_with_http_info(self, org, project, id, harness_account, **kwargs):  # noqa: E501
        """Show data  # noqa: E501

        Get binary data generated by the provisioner, such as plans and state files.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_show_data_with_http_info(org, project, id, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str id: The unique identifier for the data (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'id', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method ansible_show_data" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_show_data`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_show_data`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `ansible_show_data`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_show_data`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
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
            '/iacm/api/orgs/{org}/projects/{project}/ansible/data/{id}', 'GET',
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

    def ansible_show_inventory(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """Show Ansible inventory  # noqa: E501

        Show an individual inventory.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_show_inventory(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: Inventory identifier (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param bool use_arrays: Use arrays when displaying inventory data
        :return: ShowInventoryResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_show_inventory_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_show_inventory_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
            return data

    def ansible_show_inventory_with_http_info(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """Show Ansible inventory  # noqa: E501

        Show an individual inventory.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_show_inventory_with_http_info(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: Inventory identifier (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param bool use_arrays: Use arrays when displaying inventory data
        :return: ShowInventoryResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'identifier', 'harness_account', 'use_arrays']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method ansible_show_inventory" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_show_inventory`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_show_inventory`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `ansible_show_inventory`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_show_inventory`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

        query_params = []
        if 'use_arrays' in params:
            query_params.append(('useArrays', params['use_arrays']))  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/ansible/inventory/{identifier}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ShowInventoryResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def ansible_show_inventory_as_ansible(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """Show Ansible inventory as ansible compatible YAML  # noqa: E501

        Show an individual inventory as YAML.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_show_inventory_as_ansible(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this inventory (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: dict(str, object)
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_show_inventory_as_ansible_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_show_inventory_as_ansible_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
            return data

    def ansible_show_inventory_as_ansible_with_http_info(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """Show Ansible inventory as ansible compatible YAML  # noqa: E501

        Show an individual inventory as YAML.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_show_inventory_as_ansible_with_http_info(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this inventory (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: dict(str, object)
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
                    " to method ansible_show_inventory_as_ansible" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_show_inventory_as_ansible`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_show_inventory_as_ansible`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `ansible_show_inventory_as_ansible`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_show_inventory_as_ansible`")  # noqa: E501

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
            ['application/yaml', 'application/vnd.goa.error'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/orgs/{org}/projects/{project}/ansible/inventory/{identifier}/ansible', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='dict(str, object)',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def ansible_show_inventory_groups(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """Show Ansible inventory groups  # noqa: E501

        Show an individual inventory's groups.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_show_inventory_groups(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: Inventory identifier (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :return: ShowInventoryGroupsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_show_inventory_groups_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_show_inventory_groups_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
            return data

    def ansible_show_inventory_groups_with_http_info(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """Show Ansible inventory groups  # noqa: E501

        Show an individual inventory's groups.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_show_inventory_groups_with_http_info(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: Inventory identifier (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :return: ShowInventoryGroupsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'identifier', 'harness_account', 'limit', 'page']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method ansible_show_inventory_groups" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_show_inventory_groups`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_show_inventory_groups`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `ansible_show_inventory_groups`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_show_inventory_groups`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/ansible/inventory/{identifier}/groups', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ShowInventoryGroupsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def ansible_show_inventory_hosts(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """Show Ansible inventory hosts  # noqa: E501

        Show an individual inventory hosts.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_show_inventory_hosts(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: Inventory identifier (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :param str group: Filter results by group
        :return: ShowInventoryHostsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_show_inventory_hosts_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_show_inventory_hosts_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
            return data

    def ansible_show_inventory_hosts_with_http_info(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """Show Ansible inventory hosts  # noqa: E501

        Show an individual inventory hosts.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_show_inventory_hosts_with_http_info(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: Inventory identifier (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :param str group: Filter results by group
        :return: ShowInventoryHostsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'identifier', 'harness_account', 'limit', 'page', 'group']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method ansible_show_inventory_hosts" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_show_inventory_hosts`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_show_inventory_hosts`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `ansible_show_inventory_hosts`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_show_inventory_hosts`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

        query_params = []
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'group' in params:
            query_params.append(('group', params['group']))  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/ansible/inventory/{identifier}/hosts', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ShowInventoryHostsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def ansible_show_inventory_vars(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """Show Ansible inventory vars  # noqa: E501

        Show an individual inventory vars.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_show_inventory_vars(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: Inventory identifier (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :return: ShowInventoryVarsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_show_inventory_vars_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_show_inventory_vars_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
            return data

    def ansible_show_inventory_vars_with_http_info(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """Show Ansible inventory vars  # noqa: E501

        Show an individual inventory vars.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_show_inventory_vars_with_http_info(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: Inventory identifier (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :return: ShowInventoryVarsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'identifier', 'harness_account', 'limit', 'page']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method ansible_show_inventory_vars" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_show_inventory_vars`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_show_inventory_vars`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `ansible_show_inventory_vars`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_show_inventory_vars`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/ansible/inventory/{identifier}/vars', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ShowInventoryVarsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def ansible_show_playbook(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """Show Ansible playbook  # noqa: E501

        Show an individual playbook.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_show_playbook(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this playbook (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: ShowPlaybookResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_show_playbook_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_show_playbook_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
            return data

    def ansible_show_playbook_with_http_info(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """Show Ansible playbook  # noqa: E501

        Show an individual playbook.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_show_playbook_with_http_info(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this playbook (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :return: ShowPlaybookResponse
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
                    " to method ansible_show_playbook" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_show_playbook`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_show_playbook`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `ansible_show_playbook`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_show_playbook`")  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/ansible/playbook/{identifier}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ShowPlaybookResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def ansible_show_playbook_vars(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """Show Ansible playbook vars  # noqa: E501

        Show an individual playbook vars.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_show_playbook_vars(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: Playbook identifier (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :return: ShowPlaybookVarsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_show_playbook_vars_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_show_playbook_vars_with_http_info(org, project, identifier, harness_account, **kwargs)  # noqa: E501
            return data

    def ansible_show_playbook_vars_with_http_info(self, org, project, identifier, harness_account, **kwargs):  # noqa: E501
        """Show Ansible playbook vars  # noqa: E501

        Show an individual playbook vars.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_show_playbook_vars_with_http_info(org, project, identifier, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: Playbook identifier (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param int limit: Limit is the number of records to return for a page.
        :param int page: Page is the page number to return relative to the page 'limit'.
        :return: ShowPlaybookVarsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'identifier', 'harness_account', 'limit', 'page']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method ansible_show_playbook_vars" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_show_playbook_vars`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_show_playbook_vars`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `ansible_show_playbook_vars`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_show_playbook_vars`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/ansible/playbook/{identifier}/vars', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ShowPlaybookVarsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def ansible_update_inventory(self, body, harness_account, org, project, identifier, **kwargs):  # noqa: E501
        """Update Ansible inventory  # noqa: E501

        Update an existing inventory.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_update_inventory(body, harness_account, org, project, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateInventoryRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this inventory (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_update_inventory_with_http_info(body, harness_account, org, project, identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_update_inventory_with_http_info(body, harness_account, org, project, identifier, **kwargs)  # noqa: E501
            return data

    def ansible_update_inventory_with_http_info(self, body, harness_account, org, project, identifier, **kwargs):  # noqa: E501
        """Update Ansible inventory  # noqa: E501

        Update an existing inventory.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_update_inventory_with_http_info(body, harness_account, org, project, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateInventoryRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this inventory (required)
        :return: None
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
                    " to method ansible_update_inventory" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `ansible_update_inventory`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_update_inventory`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_update_inventory`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_update_inventory`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `ansible_update_inventory`")  # noqa: E501

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
            ['application/vnd.goa.error'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/orgs/{org}/projects/{project}/ansible/inventory/{identifier}', 'PUT',
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

    def ansible_update_inventory_group(self, body, harness_account, org, project, inventory_identifier, identifier, **kwargs):  # noqa: E501
        """Update Ansible inventory group  # noqa: E501

        Update an existing inventory group.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_update_inventory_group(body, harness_account, org, project, inventory_identifier, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateInventoryGroupRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str inventory_identifier: The unique identifier for this inventory (required)
        :param str identifier: The identifier of the group (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_update_inventory_group_with_http_info(body, harness_account, org, project, inventory_identifier, identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_update_inventory_group_with_http_info(body, harness_account, org, project, inventory_identifier, identifier, **kwargs)  # noqa: E501
            return data

    def ansible_update_inventory_group_with_http_info(self, body, harness_account, org, project, inventory_identifier, identifier, **kwargs):  # noqa: E501
        """Update Ansible inventory group  # noqa: E501

        Update an existing inventory group.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_update_inventory_group_with_http_info(body, harness_account, org, project, inventory_identifier, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateInventoryGroupRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str inventory_identifier: The unique identifier for this inventory (required)
        :param str identifier: The identifier of the group (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account', 'org', 'project', 'inventory_identifier', 'identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method ansible_update_inventory_group" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `ansible_update_inventory_group`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_update_inventory_group`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_update_inventory_group`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_update_inventory_group`")  # noqa: E501
        # verify the required parameter 'inventory_identifier' is set
        if ('inventory_identifier' not in params or
                params['inventory_identifier'] is None):
            raise ValueError("Missing the required parameter `inventory_identifier` when calling `ansible_update_inventory_group`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `ansible_update_inventory_group`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'inventory_identifier' in params:
            path_params['inventory_identifier'] = params['inventory_identifier']  # noqa: E501
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
            ['application/vnd.goa.error'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/orgs/{org}/projects/{project}/ansible/inventory/{inventory_identifier}/groups/{identifier}', 'PUT',
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

    def ansible_update_inventory_host(self, body, harness_account, org, project, inventory_identifier, host_address, **kwargs):  # noqa: E501
        """Update Ansible inventory host  # noqa: E501

        Update an existing inventory host.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_update_inventory_host(body, harness_account, org, project, inventory_identifier, host_address, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateInventoryHostRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str inventory_identifier: The unique identifier for this inventory (required)
        :param str host_address: Host address is the address of the host. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_update_inventory_host_with_http_info(body, harness_account, org, project, inventory_identifier, host_address, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_update_inventory_host_with_http_info(body, harness_account, org, project, inventory_identifier, host_address, **kwargs)  # noqa: E501
            return data

    def ansible_update_inventory_host_with_http_info(self, body, harness_account, org, project, inventory_identifier, host_address, **kwargs):  # noqa: E501
        """Update Ansible inventory host  # noqa: E501

        Update an existing inventory host.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_update_inventory_host_with_http_info(body, harness_account, org, project, inventory_identifier, host_address, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateInventoryHostRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str inventory_identifier: The unique identifier for this inventory (required)
        :param str host_address: Host address is the address of the host. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account', 'org', 'project', 'inventory_identifier', 'host_address']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method ansible_update_inventory_host" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `ansible_update_inventory_host`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_update_inventory_host`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_update_inventory_host`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_update_inventory_host`")  # noqa: E501
        # verify the required parameter 'inventory_identifier' is set
        if ('inventory_identifier' not in params or
                params['inventory_identifier'] is None):
            raise ValueError("Missing the required parameter `inventory_identifier` when calling `ansible_update_inventory_host`")  # noqa: E501
        # verify the required parameter 'host_address' is set
        if ('host_address' not in params or
                params['host_address'] is None):
            raise ValueError("Missing the required parameter `host_address` when calling `ansible_update_inventory_host`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'inventory_identifier' in params:
            path_params['inventory_identifier'] = params['inventory_identifier']  # noqa: E501
        if 'host_address' in params:
            path_params['host_address'] = params['host_address']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/ansible/inventory/{inventory_identifier}/hosts/{host_address}', 'PUT',
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

    def ansible_update_inventory_var(self, body, harness_account, org, project, identifier, uuid, **kwargs):  # noqa: E501
        """Update Ansible inventory variable  # noqa: E501

        Update an existing inventory variable.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_update_inventory_var(body, harness_account, org, project, identifier, uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateInventoryVarRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this inventory (required)
        :param str uuid: UUID is the unique identifier for the secret. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_update_inventory_var_with_http_info(body, harness_account, org, project, identifier, uuid, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_update_inventory_var_with_http_info(body, harness_account, org, project, identifier, uuid, **kwargs)  # noqa: E501
            return data

    def ansible_update_inventory_var_with_http_info(self, body, harness_account, org, project, identifier, uuid, **kwargs):  # noqa: E501
        """Update Ansible inventory variable  # noqa: E501

        Update an existing inventory variable.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_update_inventory_var_with_http_info(body, harness_account, org, project, identifier, uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateInventoryVarRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this inventory (required)
        :param str uuid: UUID is the unique identifier for the secret. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account', 'org', 'project', 'identifier', 'uuid']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method ansible_update_inventory_var" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `ansible_update_inventory_var`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_update_inventory_var`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_update_inventory_var`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_update_inventory_var`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `ansible_update_inventory_var`")  # noqa: E501
        # verify the required parameter 'uuid' is set
        if ('uuid' not in params or
                params['uuid'] is None):
            raise ValueError("Missing the required parameter `uuid` when calling `ansible_update_inventory_var`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501
        if 'uuid' in params:
            path_params['uuid'] = params['uuid']  # noqa: E501

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
            '/iacm/api/orgs/{org}/projects/{project}/ansible/inventory/{identifier}/vars/{uuid}', 'PUT',
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

    def ansible_update_inventory_vars(self, body, harness_account, org, project, identifier, **kwargs):  # noqa: E501
        """Update Ansible inventory variables  # noqa: E501

        Update existing inventory variables.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_update_inventory_vars(body, harness_account, org, project, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateInventoryVarsRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this inventory (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_update_inventory_vars_with_http_info(body, harness_account, org, project, identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_update_inventory_vars_with_http_info(body, harness_account, org, project, identifier, **kwargs)  # noqa: E501
            return data

    def ansible_update_inventory_vars_with_http_info(self, body, harness_account, org, project, identifier, **kwargs):  # noqa: E501
        """Update Ansible inventory variables  # noqa: E501

        Update existing inventory variables.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_update_inventory_vars_with_http_info(body, harness_account, org, project, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateInventoryVarsRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this inventory (required)
        :return: None
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
                    " to method ansible_update_inventory_vars" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `ansible_update_inventory_vars`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_update_inventory_vars`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_update_inventory_vars`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_update_inventory_vars`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `ansible_update_inventory_vars`")  # noqa: E501

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
            ['application/vnd.goa.error'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/orgs/{org}/projects/{project}/ansible/inventory/{identifier}/vars', 'PUT',
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

    def ansible_update_playbook(self, body, harness_account, org, project, identifier, **kwargs):  # noqa: E501
        """Update Ansible playbook  # noqa: E501

        Update an existing playbook.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_update_playbook(body, harness_account, org, project, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdatePlaybookRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this playbook (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_update_playbook_with_http_info(body, harness_account, org, project, identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_update_playbook_with_http_info(body, harness_account, org, project, identifier, **kwargs)  # noqa: E501
            return data

    def ansible_update_playbook_with_http_info(self, body, harness_account, org, project, identifier, **kwargs):  # noqa: E501
        """Update Ansible playbook  # noqa: E501

        Update an existing playbook.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_update_playbook_with_http_info(body, harness_account, org, project, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdatePlaybookRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this playbook (required)
        :return: None
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
                    " to method ansible_update_playbook" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `ansible_update_playbook`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_update_playbook`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_update_playbook`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_update_playbook`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `ansible_update_playbook`")  # noqa: E501

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
            ['application/vnd.goa.error'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/orgs/{org}/projects/{project}/ansible/playbook/{identifier}', 'PUT',
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

    def ansible_update_playbook_vars(self, body, harness_account, org, project, identifier, **kwargs):  # noqa: E501
        """Update dynamic Ansible playbook variable  # noqa: E501

        Update an existing dynamic playbook variable.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_update_playbook_vars(body, harness_account, org, project, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdatePlaybookVarsRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this inventory (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.ansible_update_playbook_vars_with_http_info(body, harness_account, org, project, identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.ansible_update_playbook_vars_with_http_info(body, harness_account, org, project, identifier, **kwargs)  # noqa: E501
            return data

    def ansible_update_playbook_vars_with_http_info(self, body, harness_account, org, project, identifier, **kwargs):  # noqa: E501
        """Update dynamic Ansible playbook variable  # noqa: E501

        Update an existing dynamic playbook variable.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ansible_update_playbook_vars_with_http_info(body, harness_account, org, project, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdatePlaybookVarsRequest body: (required)
        :param str harness_account: Account is the internal customer account ID. (required)
        :param str org: Org is the organisation identifier. (required)
        :param str project: Project is the project identifier. (required)
        :param str identifier: The unique identifier for this inventory (required)
        :return: None
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
                    " to method ansible_update_playbook_vars" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `ansible_update_playbook_vars`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `ansible_update_playbook_vars`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `ansible_update_playbook_vars`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `ansible_update_playbook_vars`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `ansible_update_playbook_vars`")  # noqa: E501

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
            ['application/vnd.goa.error'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/iacm/api/orgs/{org}/projects/{project}/ansible/playbook/{identifier}/vars', 'PUT',
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
