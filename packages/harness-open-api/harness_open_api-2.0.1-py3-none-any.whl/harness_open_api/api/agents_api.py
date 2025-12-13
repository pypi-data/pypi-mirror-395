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


class AgentsApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def agent_service_for_server_create(self, body, **kwargs):  # noqa: E501
        """agent_service_for_server_create  # noqa: E501

        Create agent.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_create(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1Agent body: (required)
        :return: V1Agent
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.agent_service_for_server_create_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.agent_service_for_server_create_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def agent_service_for_server_create_with_http_info(self, body, **kwargs):  # noqa: E501
        """agent_service_for_server_create  # noqa: E501

        Create agent.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_create_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1Agent body: (required)
        :return: V1Agent
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method agent_service_for_server_create" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `agent_service_for_server_create`")  # noqa: E501

        collection_formats = {}

        path_params = {}

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
            '/gitops/api/v1/agents', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='V1Agent',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def agent_service_for_server_delete(self, identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_delete  # noqa: E501

        Delete agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_delete(identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str identifier: (required)
        :param str account_identifier: Account Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str org_identifier: Organization Identifier for the Entity.
        :param str name:
        :param str type:
        :param list[str] tags:
        :param str search_term:
        :param int page_size:
        :param int page_index:
        :param str scope:
        :param str dr_identifier:
        :param str sort_by:
        :param str sort_order:
        :param bool metadata_only:
        :param bool ignore_scope:
        :param str connected_status:
        :param str health_status:
        :param bool with_credentials: Applicable when trying to retrieve an agent. Set to true to include the credentials for the agent in the response. (Private key may not be included in response if agent is already connected to harness). NOTE: Setting this to true requires the user to have edit permissions on Agent.
        :param bool include_secondary:
        :return: V1Agent
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.agent_service_for_server_delete_with_http_info(identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.agent_service_for_server_delete_with_http_info(identifier, **kwargs)  # noqa: E501
            return data

    def agent_service_for_server_delete_with_http_info(self, identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_delete  # noqa: E501

        Delete agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_delete_with_http_info(identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str identifier: (required)
        :param str account_identifier: Account Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str org_identifier: Organization Identifier for the Entity.
        :param str name:
        :param str type:
        :param list[str] tags:
        :param str search_term:
        :param int page_size:
        :param int page_index:
        :param str scope:
        :param str dr_identifier:
        :param str sort_by:
        :param str sort_order:
        :param bool metadata_only:
        :param bool ignore_scope:
        :param str connected_status:
        :param str health_status:
        :param bool with_credentials: Applicable when trying to retrieve an agent. Set to true to include the credentials for the agent in the response. (Private key may not be included in response if agent is already connected to harness). NOTE: Setting this to true requires the user to have edit permissions on Agent.
        :param bool include_secondary:
        :return: V1Agent
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['identifier', 'account_identifier', 'project_identifier', 'org_identifier', 'name', 'type', 'tags', 'search_term', 'page_size', 'page_index', 'scope', 'dr_identifier', 'sort_by', 'sort_order', 'metadata_only', 'ignore_scope', 'connected_status', 'health_status', 'with_credentials', 'include_secondary']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method agent_service_for_server_delete" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `agent_service_for_server_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'name' in params:
            query_params.append(('name', params['name']))  # noqa: E501
        if 'type' in params:
            query_params.append(('type', params['type']))  # noqa: E501
        if 'tags' in params:
            query_params.append(('tags', params['tags']))  # noqa: E501
            collection_formats['tags'] = 'multi'  # noqa: E501
        if 'search_term' in params:
            query_params.append(('searchTerm', params['search_term']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('pageSize', params['page_size']))  # noqa: E501
        if 'page_index' in params:
            query_params.append(('pageIndex', params['page_index']))  # noqa: E501
        if 'scope' in params:
            query_params.append(('scope', params['scope']))  # noqa: E501
        if 'dr_identifier' in params:
            query_params.append(('drIdentifier', params['dr_identifier']))  # noqa: E501
        if 'sort_by' in params:
            query_params.append(('sortBy', params['sort_by']))  # noqa: E501
        if 'sort_order' in params:
            query_params.append(('sortOrder', params['sort_order']))  # noqa: E501
        if 'metadata_only' in params:
            query_params.append(('metadataOnly', params['metadata_only']))  # noqa: E501
        if 'ignore_scope' in params:
            query_params.append(('ignoreScope', params['ignore_scope']))  # noqa: E501
        if 'connected_status' in params:
            query_params.append(('connectedStatus', params['connected_status']))  # noqa: E501
        if 'health_status' in params:
            query_params.append(('healthStatus', params['health_status']))  # noqa: E501
        if 'with_credentials' in params:
            query_params.append(('withCredentials', params['with_credentials']))  # noqa: E501
        if 'include_secondary' in params:
            query_params.append(('includeSecondary', params['include_secondary']))  # noqa: E501

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
            '/gitops/api/v1/agents/{identifier}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='V1Agent',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def agent_service_for_server_get(self, identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_get  # noqa: E501

        Get agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_get(identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str identifier: (required)
        :param str account_identifier: Account Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str org_identifier: Organization Identifier for the Entity.
        :param str name:
        :param str type:
        :param list[str] tags:
        :param str search_term:
        :param int page_size:
        :param int page_index:
        :param str scope:
        :param str dr_identifier:
        :param str sort_by:
        :param str sort_order:
        :param bool metadata_only:
        :param bool ignore_scope:
        :param str connected_status:
        :param str health_status:
        :param bool with_credentials: Applicable when trying to retrieve an agent. Set to true to include the credentials for the agent in the response. (Private key may not be included in response if agent is already connected to harness). NOTE: Setting this to true requires the user to have edit permissions on Agent.
        :param bool include_secondary:
        :return: V1Agent
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.agent_service_for_server_get_with_http_info(identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.agent_service_for_server_get_with_http_info(identifier, **kwargs)  # noqa: E501
            return data

    def agent_service_for_server_get_with_http_info(self, identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_get  # noqa: E501

        Get agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_get_with_http_info(identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str identifier: (required)
        :param str account_identifier: Account Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str org_identifier: Organization Identifier for the Entity.
        :param str name:
        :param str type:
        :param list[str] tags:
        :param str search_term:
        :param int page_size:
        :param int page_index:
        :param str scope:
        :param str dr_identifier:
        :param str sort_by:
        :param str sort_order:
        :param bool metadata_only:
        :param bool ignore_scope:
        :param str connected_status:
        :param str health_status:
        :param bool with_credentials: Applicable when trying to retrieve an agent. Set to true to include the credentials for the agent in the response. (Private key may not be included in response if agent is already connected to harness). NOTE: Setting this to true requires the user to have edit permissions on Agent.
        :param bool include_secondary:
        :return: V1Agent
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['identifier', 'account_identifier', 'project_identifier', 'org_identifier', 'name', 'type', 'tags', 'search_term', 'page_size', 'page_index', 'scope', 'dr_identifier', 'sort_by', 'sort_order', 'metadata_only', 'ignore_scope', 'connected_status', 'health_status', 'with_credentials', 'include_secondary']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method agent_service_for_server_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `agent_service_for_server_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'name' in params:
            query_params.append(('name', params['name']))  # noqa: E501
        if 'type' in params:
            query_params.append(('type', params['type']))  # noqa: E501
        if 'tags' in params:
            query_params.append(('tags', params['tags']))  # noqa: E501
            collection_formats['tags'] = 'multi'  # noqa: E501
        if 'search_term' in params:
            query_params.append(('searchTerm', params['search_term']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('pageSize', params['page_size']))  # noqa: E501
        if 'page_index' in params:
            query_params.append(('pageIndex', params['page_index']))  # noqa: E501
        if 'scope' in params:
            query_params.append(('scope', params['scope']))  # noqa: E501
        if 'dr_identifier' in params:
            query_params.append(('drIdentifier', params['dr_identifier']))  # noqa: E501
        if 'sort_by' in params:
            query_params.append(('sortBy', params['sort_by']))  # noqa: E501
        if 'sort_order' in params:
            query_params.append(('sortOrder', params['sort_order']))  # noqa: E501
        if 'metadata_only' in params:
            query_params.append(('metadataOnly', params['metadata_only']))  # noqa: E501
        if 'ignore_scope' in params:
            query_params.append(('ignoreScope', params['ignore_scope']))  # noqa: E501
        if 'connected_status' in params:
            query_params.append(('connectedStatus', params['connected_status']))  # noqa: E501
        if 'health_status' in params:
            query_params.append(('healthStatus', params['health_status']))  # noqa: E501
        if 'with_credentials' in params:
            query_params.append(('withCredentials', params['with_credentials']))  # noqa: E501
        if 'include_secondary' in params:
            query_params.append(('includeSecondary', params['include_secondary']))  # noqa: E501

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
            '/gitops/api/v1/agents/{identifier}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='V1Agent',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def agent_service_for_server_get_deploy_helm_chart(self, agent_identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_get_deploy_helm_chart  # noqa: E501

        GetDeployHelmChart returns the Helm Chart for deploying the agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_get_deploy_helm_chart(agent_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str agent_identifier: Agent identifier for entity. (required)
        :param str account_identifier: Account Identifier for the Entity.
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str namespace:
        :param str disaster_recovery_identifier: Disaster Recovery Identifier for entity.
        :param bool skip_crds:
        :param str ca_data: Certificate chain for the agent, must be base64 encoded.
        :param str proxy_http:
        :param str proxy_https:
        :param str proxy_username:
        :param str proxy_password:
        :param bool proxy_skip_ssl_verify:
        :param str private_key:
        :param bool argocd_settings_enable_helm_path_traversal: Controls the Environment variable HELM_SECRETS_VALUES_ALLOW_PATH_TRAVERSAL to allow or deny dot-dot-slash values file paths. Disabled by default for security reasons. This config is pushed as an env variable to the repo-server.
        :param bool argocd_settings_force_enable_in_cluster: For a Namespaced gitops agent, incluster is disabled by default. (controlled through variable `cluster.inclusterEnabled` in argocd-cm configmap. NOTE that you will have to manually restrict your namespaced agent's scope to its own cluster since this essentially makes the namespaced agent have access to incluster completely including creating clusterroles.
        :return: StreamResultOfV1DownloadResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.agent_service_for_server_get_deploy_helm_chart_with_http_info(agent_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.agent_service_for_server_get_deploy_helm_chart_with_http_info(agent_identifier, **kwargs)  # noqa: E501
            return data

    def agent_service_for_server_get_deploy_helm_chart_with_http_info(self, agent_identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_get_deploy_helm_chart  # noqa: E501

        GetDeployHelmChart returns the Helm Chart for deploying the agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_get_deploy_helm_chart_with_http_info(agent_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str agent_identifier: Agent identifier for entity. (required)
        :param str account_identifier: Account Identifier for the Entity.
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str namespace:
        :param str disaster_recovery_identifier: Disaster Recovery Identifier for entity.
        :param bool skip_crds:
        :param str ca_data: Certificate chain for the agent, must be base64 encoded.
        :param str proxy_http:
        :param str proxy_https:
        :param str proxy_username:
        :param str proxy_password:
        :param bool proxy_skip_ssl_verify:
        :param str private_key:
        :param bool argocd_settings_enable_helm_path_traversal: Controls the Environment variable HELM_SECRETS_VALUES_ALLOW_PATH_TRAVERSAL to allow or deny dot-dot-slash values file paths. Disabled by default for security reasons. This config is pushed as an env variable to the repo-server.
        :param bool argocd_settings_force_enable_in_cluster: For a Namespaced gitops agent, incluster is disabled by default. (controlled through variable `cluster.inclusterEnabled` in argocd-cm configmap. NOTE that you will have to manually restrict your namespaced agent's scope to its own cluster since this essentially makes the namespaced agent have access to incluster completely including creating clusterroles.
        :return: StreamResultOfV1DownloadResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['agent_identifier', 'account_identifier', 'org_identifier', 'project_identifier', 'namespace', 'disaster_recovery_identifier', 'skip_crds', 'ca_data', 'proxy_http', 'proxy_https', 'proxy_username', 'proxy_password', 'proxy_skip_ssl_verify', 'private_key', 'argocd_settings_enable_helm_path_traversal', 'argocd_settings_force_enable_in_cluster']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method agent_service_for_server_get_deploy_helm_chart" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'agent_identifier' is set
        if ('agent_identifier' not in params or
                params['agent_identifier'] is None):
            raise ValueError("Missing the required parameter `agent_identifier` when calling `agent_service_for_server_get_deploy_helm_chart`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'agent_identifier' in params:
            path_params['agentIdentifier'] = params['agent_identifier']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'namespace' in params:
            query_params.append(('namespace', params['namespace']))  # noqa: E501
        if 'disaster_recovery_identifier' in params:
            query_params.append(('disasterRecoveryIdentifier', params['disaster_recovery_identifier']))  # noqa: E501
        if 'skip_crds' in params:
            query_params.append(('skipCrds', params['skip_crds']))  # noqa: E501
        if 'ca_data' in params:
            query_params.append(('caData', params['ca_data']))  # noqa: E501
        if 'proxy_http' in params:
            query_params.append(('proxy.http', params['proxy_http']))  # noqa: E501
        if 'proxy_https' in params:
            query_params.append(('proxy.https', params['proxy_https']))  # noqa: E501
        if 'proxy_username' in params:
            query_params.append(('proxy.username', params['proxy_username']))  # noqa: E501
        if 'proxy_password' in params:
            query_params.append(('proxy.password', params['proxy_password']))  # noqa: E501
        if 'proxy_skip_ssl_verify' in params:
            query_params.append(('proxy.skipSSLVerify', params['proxy_skip_ssl_verify']))  # noqa: E501
        if 'private_key' in params:
            query_params.append(('privateKey', params['private_key']))  # noqa: E501
        if 'argocd_settings_enable_helm_path_traversal' in params:
            query_params.append(('argocdSettings.enableHelmPathTraversal', params['argocd_settings_enable_helm_path_traversal']))  # noqa: E501
        if 'argocd_settings_force_enable_in_cluster' in params:
            query_params.append(('argocdSettings.forceEnableInCluster', params['argocd_settings_force_enable_in_cluster']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/octet-stream'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/gitops/api/v1/agents/{agentIdentifier}/helm-chart', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='StreamResultOfV1DownloadResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def agent_service_for_server_get_deploy_overrides(self, agent_identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_get_deploy_overrides  # noqa: E501

        GetDeployOverrides returns the Helm Chart overrides for the agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_get_deploy_overrides(agent_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str agent_identifier: Agent identifier for entity. (required)
        :param str account_identifier: Account Identifier for the Entity.
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str namespace:
        :param str disaster_recovery_identifier: Disaster Recovery Identifier for entity.
        :param bool skip_crds:
        :param str ca_data: Certificate chain for the agent, must be base64 encoded.
        :param str proxy_http:
        :param str proxy_https:
        :param str proxy_username:
        :param str proxy_password:
        :param bool proxy_skip_ssl_verify:
        :param str private_key:
        :param bool argocd_settings_enable_helm_path_traversal: Controls the Environment variable HELM_SECRETS_VALUES_ALLOW_PATH_TRAVERSAL to allow or deny dot-dot-slash values file paths. Disabled by default for security reasons. This config is pushed as an env variable to the repo-server.
        :param bool argocd_settings_force_enable_in_cluster: For a Namespaced gitops agent, incluster is disabled by default. (controlled through variable `cluster.inclusterEnabled` in argocd-cm configmap. NOTE that you will have to manually restrict your namespaced agent's scope to its own cluster since this essentially makes the namespaced agent have access to incluster completely including creating clusterroles.
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.agent_service_for_server_get_deploy_overrides_with_http_info(agent_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.agent_service_for_server_get_deploy_overrides_with_http_info(agent_identifier, **kwargs)  # noqa: E501
            return data

    def agent_service_for_server_get_deploy_overrides_with_http_info(self, agent_identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_get_deploy_overrides  # noqa: E501

        GetDeployOverrides returns the Helm Chart overrides for the agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_get_deploy_overrides_with_http_info(agent_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str agent_identifier: Agent identifier for entity. (required)
        :param str account_identifier: Account Identifier for the Entity.
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str namespace:
        :param str disaster_recovery_identifier: Disaster Recovery Identifier for entity.
        :param bool skip_crds:
        :param str ca_data: Certificate chain for the agent, must be base64 encoded.
        :param str proxy_http:
        :param str proxy_https:
        :param str proxy_username:
        :param str proxy_password:
        :param bool proxy_skip_ssl_verify:
        :param str private_key:
        :param bool argocd_settings_enable_helm_path_traversal: Controls the Environment variable HELM_SECRETS_VALUES_ALLOW_PATH_TRAVERSAL to allow or deny dot-dot-slash values file paths. Disabled by default for security reasons. This config is pushed as an env variable to the repo-server.
        :param bool argocd_settings_force_enable_in_cluster: For a Namespaced gitops agent, incluster is disabled by default. (controlled through variable `cluster.inclusterEnabled` in argocd-cm configmap. NOTE that you will have to manually restrict your namespaced agent's scope to its own cluster since this essentially makes the namespaced agent have access to incluster completely including creating clusterroles.
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['agent_identifier', 'account_identifier', 'org_identifier', 'project_identifier', 'namespace', 'disaster_recovery_identifier', 'skip_crds', 'ca_data', 'proxy_http', 'proxy_https', 'proxy_username', 'proxy_password', 'proxy_skip_ssl_verify', 'private_key', 'argocd_settings_enable_helm_path_traversal', 'argocd_settings_force_enable_in_cluster']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method agent_service_for_server_get_deploy_overrides" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'agent_identifier' is set
        if ('agent_identifier' not in params or
                params['agent_identifier'] is None):
            raise ValueError("Missing the required parameter `agent_identifier` when calling `agent_service_for_server_get_deploy_overrides`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'agent_identifier' in params:
            path_params['agentIdentifier'] = params['agent_identifier']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'namespace' in params:
            query_params.append(('namespace', params['namespace']))  # noqa: E501
        if 'disaster_recovery_identifier' in params:
            query_params.append(('disasterRecoveryIdentifier', params['disaster_recovery_identifier']))  # noqa: E501
        if 'skip_crds' in params:
            query_params.append(('skipCrds', params['skip_crds']))  # noqa: E501
        if 'ca_data' in params:
            query_params.append(('caData', params['ca_data']))  # noqa: E501
        if 'proxy_http' in params:
            query_params.append(('proxy.http', params['proxy_http']))  # noqa: E501
        if 'proxy_https' in params:
            query_params.append(('proxy.https', params['proxy_https']))  # noqa: E501
        if 'proxy_username' in params:
            query_params.append(('proxy.username', params['proxy_username']))  # noqa: E501
        if 'proxy_password' in params:
            query_params.append(('proxy.password', params['proxy_password']))  # noqa: E501
        if 'proxy_skip_ssl_verify' in params:
            query_params.append(('proxy.skipSSLVerify', params['proxy_skip_ssl_verify']))  # noqa: E501
        if 'private_key' in params:
            query_params.append(('privateKey', params['private_key']))  # noqa: E501
        if 'argocd_settings_enable_helm_path_traversal' in params:
            query_params.append(('argocdSettings.enableHelmPathTraversal', params['argocd_settings_enable_helm_path_traversal']))  # noqa: E501
        if 'argocd_settings_force_enable_in_cluster' in params:
            query_params.append(('argocdSettings.forceEnableInCluster', params['argocd_settings_force_enable_in_cluster']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/yaml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/gitops/api/v1/agents/{agentIdentifier}/helm-overrides', 'GET',
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

    def agent_service_for_server_get_deploy_yaml(self, agent_identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_get_deploy_yaml  # noqa: E501

        GetDeployYaml returns deployment yamls for agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_get_deploy_yaml(agent_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str agent_identifier: Agent identifier for entity. (required)
        :param str account_identifier: Account Identifier for the Entity.
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str namespace:
        :param str disaster_recovery_identifier: Disaster Recovery Identifier for entity.
        :param bool skip_crds:
        :param str ca_data: Certificate chain for the agent, must be base64 encoded.
        :param str proxy_http:
        :param str proxy_https:
        :param str proxy_username:
        :param str proxy_password:
        :param bool proxy_skip_ssl_verify:
        :param str private_key:
        :param bool argocd_settings_enable_helm_path_traversal: Controls the Environment variable HELM_SECRETS_VALUES_ALLOW_PATH_TRAVERSAL to allow or deny dot-dot-slash values file paths. Disabled by default for security reasons. This config is pushed as an env variable to the repo-server.
        :param bool argocd_settings_force_enable_in_cluster: For a Namespaced gitops agent, incluster is disabled by default. (controlled through variable `cluster.inclusterEnabled` in argocd-cm configmap. NOTE that you will have to manually restrict your namespaced agent's scope to its own cluster since this essentially makes the namespaced agent have access to incluster completely including creating clusterroles.
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.agent_service_for_server_get_deploy_yaml_with_http_info(agent_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.agent_service_for_server_get_deploy_yaml_with_http_info(agent_identifier, **kwargs)  # noqa: E501
            return data

    def agent_service_for_server_get_deploy_yaml_with_http_info(self, agent_identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_get_deploy_yaml  # noqa: E501

        GetDeployYaml returns deployment yamls for agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_get_deploy_yaml_with_http_info(agent_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str agent_identifier: Agent identifier for entity. (required)
        :param str account_identifier: Account Identifier for the Entity.
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str namespace:
        :param str disaster_recovery_identifier: Disaster Recovery Identifier for entity.
        :param bool skip_crds:
        :param str ca_data: Certificate chain for the agent, must be base64 encoded.
        :param str proxy_http:
        :param str proxy_https:
        :param str proxy_username:
        :param str proxy_password:
        :param bool proxy_skip_ssl_verify:
        :param str private_key:
        :param bool argocd_settings_enable_helm_path_traversal: Controls the Environment variable HELM_SECRETS_VALUES_ALLOW_PATH_TRAVERSAL to allow or deny dot-dot-slash values file paths. Disabled by default for security reasons. This config is pushed as an env variable to the repo-server.
        :param bool argocd_settings_force_enable_in_cluster: For a Namespaced gitops agent, incluster is disabled by default. (controlled through variable `cluster.inclusterEnabled` in argocd-cm configmap. NOTE that you will have to manually restrict your namespaced agent's scope to its own cluster since this essentially makes the namespaced agent have access to incluster completely including creating clusterroles.
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['agent_identifier', 'account_identifier', 'org_identifier', 'project_identifier', 'namespace', 'disaster_recovery_identifier', 'skip_crds', 'ca_data', 'proxy_http', 'proxy_https', 'proxy_username', 'proxy_password', 'proxy_skip_ssl_verify', 'private_key', 'argocd_settings_enable_helm_path_traversal', 'argocd_settings_force_enable_in_cluster']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method agent_service_for_server_get_deploy_yaml" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'agent_identifier' is set
        if ('agent_identifier' not in params or
                params['agent_identifier'] is None):
            raise ValueError("Missing the required parameter `agent_identifier` when calling `agent_service_for_server_get_deploy_yaml`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'agent_identifier' in params:
            path_params['agentIdentifier'] = params['agent_identifier']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'namespace' in params:
            query_params.append(('namespace', params['namespace']))  # noqa: E501
        if 'disaster_recovery_identifier' in params:
            query_params.append(('disasterRecoveryIdentifier', params['disaster_recovery_identifier']))  # noqa: E501
        if 'skip_crds' in params:
            query_params.append(('skipCrds', params['skip_crds']))  # noqa: E501
        if 'ca_data' in params:
            query_params.append(('caData', params['ca_data']))  # noqa: E501
        if 'proxy_http' in params:
            query_params.append(('proxy.http', params['proxy_http']))  # noqa: E501
        if 'proxy_https' in params:
            query_params.append(('proxy.https', params['proxy_https']))  # noqa: E501
        if 'proxy_username' in params:
            query_params.append(('proxy.username', params['proxy_username']))  # noqa: E501
        if 'proxy_password' in params:
            query_params.append(('proxy.password', params['proxy_password']))  # noqa: E501
        if 'proxy_skip_ssl_verify' in params:
            query_params.append(('proxy.skipSSLVerify', params['proxy_skip_ssl_verify']))  # noqa: E501
        if 'private_key' in params:
            query_params.append(('privateKey', params['private_key']))  # noqa: E501
        if 'argocd_settings_enable_helm_path_traversal' in params:
            query_params.append(('argocdSettings.enableHelmPathTraversal', params['argocd_settings_enable_helm_path_traversal']))  # noqa: E501
        if 'argocd_settings_force_enable_in_cluster' in params:
            query_params.append(('argocdSettings.forceEnableInCluster', params['argocd_settings_force_enable_in_cluster']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/yaml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/gitops/api/v1/agents/{agentIdentifier}/deploy.yaml', 'GET',
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

    def agent_service_for_server_get_operator_yaml(self, agent_identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_get_operator_yaml  # noqa: E501

        GetOperatorYaml returns operator yaml for deploying the agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_get_operator_yaml(agent_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str agent_identifier: Agent identifier for entity. (required)
        :param str account_identifier: Account Identifier for the Entity.
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str namespace:
        :param str disaster_recovery_identifier: Disaster Recovery Identifier for entity.
        :param bool skip_crds:
        :param str ca_data: Certificate chain for the agent, must be base64 encoded.
        :param str proxy_http:
        :param str proxy_https:
        :param str proxy_username:
        :param str proxy_password:
        :param bool proxy_skip_ssl_verify:
        :param str private_key:
        :param bool argocd_settings_enable_helm_path_traversal: Controls the Environment variable HELM_SECRETS_VALUES_ALLOW_PATH_TRAVERSAL to allow or deny dot-dot-slash values file paths. Disabled by default for security reasons. This config is pushed as an env variable to the repo-server.
        :param bool argocd_settings_force_enable_in_cluster: For a Namespaced gitops agent, incluster is disabled by default. (controlled through variable `cluster.inclusterEnabled` in argocd-cm configmap. NOTE that you will have to manually restrict your namespaced agent's scope to its own cluster since this essentially makes the namespaced agent have access to incluster completely including creating clusterroles.
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.agent_service_for_server_get_operator_yaml_with_http_info(agent_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.agent_service_for_server_get_operator_yaml_with_http_info(agent_identifier, **kwargs)  # noqa: E501
            return data

    def agent_service_for_server_get_operator_yaml_with_http_info(self, agent_identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_get_operator_yaml  # noqa: E501

        GetOperatorYaml returns operator yaml for deploying the agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_get_operator_yaml_with_http_info(agent_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str agent_identifier: Agent identifier for entity. (required)
        :param str account_identifier: Account Identifier for the Entity.
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str namespace:
        :param str disaster_recovery_identifier: Disaster Recovery Identifier for entity.
        :param bool skip_crds:
        :param str ca_data: Certificate chain for the agent, must be base64 encoded.
        :param str proxy_http:
        :param str proxy_https:
        :param str proxy_username:
        :param str proxy_password:
        :param bool proxy_skip_ssl_verify:
        :param str private_key:
        :param bool argocd_settings_enable_helm_path_traversal: Controls the Environment variable HELM_SECRETS_VALUES_ALLOW_PATH_TRAVERSAL to allow or deny dot-dot-slash values file paths. Disabled by default for security reasons. This config is pushed as an env variable to the repo-server.
        :param bool argocd_settings_force_enable_in_cluster: For a Namespaced gitops agent, incluster is disabled by default. (controlled through variable `cluster.inclusterEnabled` in argocd-cm configmap. NOTE that you will have to manually restrict your namespaced agent's scope to its own cluster since this essentially makes the namespaced agent have access to incluster completely including creating clusterroles.
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['agent_identifier', 'account_identifier', 'org_identifier', 'project_identifier', 'namespace', 'disaster_recovery_identifier', 'skip_crds', 'ca_data', 'proxy_http', 'proxy_https', 'proxy_username', 'proxy_password', 'proxy_skip_ssl_verify', 'private_key', 'argocd_settings_enable_helm_path_traversal', 'argocd_settings_force_enable_in_cluster']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method agent_service_for_server_get_operator_yaml" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'agent_identifier' is set
        if ('agent_identifier' not in params or
                params['agent_identifier'] is None):
            raise ValueError("Missing the required parameter `agent_identifier` when calling `agent_service_for_server_get_operator_yaml`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'agent_identifier' in params:
            path_params['agentIdentifier'] = params['agent_identifier']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'namespace' in params:
            query_params.append(('namespace', params['namespace']))  # noqa: E501
        if 'disaster_recovery_identifier' in params:
            query_params.append(('disasterRecoveryIdentifier', params['disaster_recovery_identifier']))  # noqa: E501
        if 'skip_crds' in params:
            query_params.append(('skipCrds', params['skip_crds']))  # noqa: E501
        if 'ca_data' in params:
            query_params.append(('caData', params['ca_data']))  # noqa: E501
        if 'proxy_http' in params:
            query_params.append(('proxy.http', params['proxy_http']))  # noqa: E501
        if 'proxy_https' in params:
            query_params.append(('proxy.https', params['proxy_https']))  # noqa: E501
        if 'proxy_username' in params:
            query_params.append(('proxy.username', params['proxy_username']))  # noqa: E501
        if 'proxy_password' in params:
            query_params.append(('proxy.password', params['proxy_password']))  # noqa: E501
        if 'proxy_skip_ssl_verify' in params:
            query_params.append(('proxy.skipSSLVerify', params['proxy_skip_ssl_verify']))  # noqa: E501
        if 'private_key' in params:
            query_params.append(('privateKey', params['private_key']))  # noqa: E501
        if 'argocd_settings_enable_helm_path_traversal' in params:
            query_params.append(('argocdSettings.enableHelmPathTraversal', params['argocd_settings_enable_helm_path_traversal']))  # noqa: E501
        if 'argocd_settings_force_enable_in_cluster' in params:
            query_params.append(('argocdSettings.forceEnableInCluster', params['argocd_settings_force_enable_in_cluster']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/yaml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/gitops/api/v1/agents/{agentIdentifier}/operator/yaml', 'GET',
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

    def agent_service_for_server_list(self, **kwargs):  # noqa: E501
        """agent_service_for_server_list  # noqa: E501

        List agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_list(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str org_identifier: Organization Identifier for the Entity.
        :param str identifier:
        :param str name:
        :param str type:
        :param list[str] tags:
        :param str search_term:
        :param int page_size:
        :param int page_index:
        :param str scope:
        :param str dr_identifier:
        :param str sort_by:
        :param str sort_order:
        :param bool metadata_only:
        :param bool ignore_scope:
        :param str connected_status:
        :param str health_status:
        :param bool with_credentials: Applicable when trying to retrieve an agent. Set to true to include the credentials for the agent in the response. (Private key may not be included in response if agent is already connected to harness). NOTE: Setting this to true requires the user to have edit permissions on Agent.
        :param bool include_secondary:
        :return: V1AgentList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.agent_service_for_server_list_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.agent_service_for_server_list_with_http_info(**kwargs)  # noqa: E501
            return data

    def agent_service_for_server_list_with_http_info(self, **kwargs):  # noqa: E501
        """agent_service_for_server_list  # noqa: E501

        List agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_list_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str org_identifier: Organization Identifier for the Entity.
        :param str identifier:
        :param str name:
        :param str type:
        :param list[str] tags:
        :param str search_term:
        :param int page_size:
        :param int page_index:
        :param str scope:
        :param str dr_identifier:
        :param str sort_by:
        :param str sort_order:
        :param bool metadata_only:
        :param bool ignore_scope:
        :param str connected_status:
        :param str health_status:
        :param bool with_credentials: Applicable when trying to retrieve an agent. Set to true to include the credentials for the agent in the response. (Private key may not be included in response if agent is already connected to harness). NOTE: Setting this to true requires the user to have edit permissions on Agent.
        :param bool include_secondary:
        :return: V1AgentList
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'project_identifier', 'org_identifier', 'identifier', 'name', 'type', 'tags', 'search_term', 'page_size', 'page_index', 'scope', 'dr_identifier', 'sort_by', 'sort_order', 'metadata_only', 'ignore_scope', 'connected_status', 'health_status', 'with_credentials', 'include_secondary']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method agent_service_for_server_list" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'identifier' in params:
            query_params.append(('identifier', params['identifier']))  # noqa: E501
        if 'name' in params:
            query_params.append(('name', params['name']))  # noqa: E501
        if 'type' in params:
            query_params.append(('type', params['type']))  # noqa: E501
        if 'tags' in params:
            query_params.append(('tags', params['tags']))  # noqa: E501
            collection_formats['tags'] = 'multi'  # noqa: E501
        if 'search_term' in params:
            query_params.append(('searchTerm', params['search_term']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('pageSize', params['page_size']))  # noqa: E501
        if 'page_index' in params:
            query_params.append(('pageIndex', params['page_index']))  # noqa: E501
        if 'scope' in params:
            query_params.append(('scope', params['scope']))  # noqa: E501
        if 'dr_identifier' in params:
            query_params.append(('drIdentifier', params['dr_identifier']))  # noqa: E501
        if 'sort_by' in params:
            query_params.append(('sortBy', params['sort_by']))  # noqa: E501
        if 'sort_order' in params:
            query_params.append(('sortOrder', params['sort_order']))  # noqa: E501
        if 'metadata_only' in params:
            query_params.append(('metadataOnly', params['metadata_only']))  # noqa: E501
        if 'ignore_scope' in params:
            query_params.append(('ignoreScope', params['ignore_scope']))  # noqa: E501
        if 'connected_status' in params:
            query_params.append(('connectedStatus', params['connected_status']))  # noqa: E501
        if 'health_status' in params:
            query_params.append(('healthStatus', params['health_status']))  # noqa: E501
        if 'with_credentials' in params:
            query_params.append(('withCredentials', params['with_credentials']))  # noqa: E501
        if 'include_secondary' in params:
            query_params.append(('includeSecondary', params['include_secondary']))  # noqa: E501

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
            '/gitops/api/v1/agents', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='V1AgentList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def agent_service_for_server_list_namespaces(self, **kwargs):  # noqa: E501
        """agent_service_for_server_list_namespaces  # noqa: E501

        Get agent namespaces.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_list_namespaces(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str org_identifier: Organization Identifier for the Entity.
        :param str identifier:
        :param str name:
        :param str type:
        :param list[str] tags:
        :param str search_term:
        :param int page_size:
        :param int page_index:
        :param str scope:
        :param str dr_identifier:
        :param str sort_by:
        :param str sort_order:
        :param bool metadata_only:
        :param bool ignore_scope:
        :param str connected_status:
        :param str health_status:
        :param bool with_credentials: Applicable when trying to retrieve an agent. Set to true to include the credentials for the agent in the response. (Private key may not be included in response if agent is already connected to harness). NOTE: Setting this to true requires the user to have edit permissions on Agent.
        :param bool include_secondary:
        :return: Gitopsservicev1NamespaceList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.agent_service_for_server_list_namespaces_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.agent_service_for_server_list_namespaces_with_http_info(**kwargs)  # noqa: E501
            return data

    def agent_service_for_server_list_namespaces_with_http_info(self, **kwargs):  # noqa: E501
        """agent_service_for_server_list_namespaces  # noqa: E501

        Get agent namespaces.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_list_namespaces_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str org_identifier: Organization Identifier for the Entity.
        :param str identifier:
        :param str name:
        :param str type:
        :param list[str] tags:
        :param str search_term:
        :param int page_size:
        :param int page_index:
        :param str scope:
        :param str dr_identifier:
        :param str sort_by:
        :param str sort_order:
        :param bool metadata_only:
        :param bool ignore_scope:
        :param str connected_status:
        :param str health_status:
        :param bool with_credentials: Applicable when trying to retrieve an agent. Set to true to include the credentials for the agent in the response. (Private key may not be included in response if agent is already connected to harness). NOTE: Setting this to true requires the user to have edit permissions on Agent.
        :param bool include_secondary:
        :return: Gitopsservicev1NamespaceList
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'project_identifier', 'org_identifier', 'identifier', 'name', 'type', 'tags', 'search_term', 'page_size', 'page_index', 'scope', 'dr_identifier', 'sort_by', 'sort_order', 'metadata_only', 'ignore_scope', 'connected_status', 'health_status', 'with_credentials', 'include_secondary']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method agent_service_for_server_list_namespaces" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'identifier' in params:
            query_params.append(('identifier', params['identifier']))  # noqa: E501
        if 'name' in params:
            query_params.append(('name', params['name']))  # noqa: E501
        if 'type' in params:
            query_params.append(('type', params['type']))  # noqa: E501
        if 'tags' in params:
            query_params.append(('tags', params['tags']))  # noqa: E501
            collection_formats['tags'] = 'multi'  # noqa: E501
        if 'search_term' in params:
            query_params.append(('searchTerm', params['search_term']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('pageSize', params['page_size']))  # noqa: E501
        if 'page_index' in params:
            query_params.append(('pageIndex', params['page_index']))  # noqa: E501
        if 'scope' in params:
            query_params.append(('scope', params['scope']))  # noqa: E501
        if 'dr_identifier' in params:
            query_params.append(('drIdentifier', params['dr_identifier']))  # noqa: E501
        if 'sort_by' in params:
            query_params.append(('sortBy', params['sort_by']))  # noqa: E501
        if 'sort_order' in params:
            query_params.append(('sortOrder', params['sort_order']))  # noqa: E501
        if 'metadata_only' in params:
            query_params.append(('metadataOnly', params['metadata_only']))  # noqa: E501
        if 'ignore_scope' in params:
            query_params.append(('ignoreScope', params['ignore_scope']))  # noqa: E501
        if 'connected_status' in params:
            query_params.append(('connectedStatus', params['connected_status']))  # noqa: E501
        if 'health_status' in params:
            query_params.append(('healthStatus', params['health_status']))  # noqa: E501
        if 'with_credentials' in params:
            query_params.append(('withCredentials', params['with_credentials']))  # noqa: E501
        if 'include_secondary' in params:
            query_params.append(('includeSecondary', params['include_secondary']))  # noqa: E501

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
            '/gitops/api/v1/agents/ns', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Gitopsservicev1NamespaceList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def agent_service_for_server_list_tags(self, **kwargs):  # noqa: E501
        """agent_service_for_server_list_tags  # noqa: E501

        Get agent tags.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_list_tags(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str org_identifier: Organization Identifier for the Entity.
        :param str identifier:
        :param str name:
        :param str type:
        :param list[str] tags:
        :param str search_term:
        :param int page_size:
        :param int page_index:
        :param str scope:
        :param str dr_identifier:
        :param str sort_by:
        :param str sort_order:
        :param bool metadata_only:
        :param bool ignore_scope:
        :param str connected_status:
        :param str health_status:
        :param bool with_credentials: Applicable when trying to retrieve an agent. Set to true to include the credentials for the agent in the response. (Private key may not be included in response if agent is already connected to harness). NOTE: Setting this to true requires the user to have edit permissions on Agent.
        :param bool include_secondary:
        :return: V1TagMap
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.agent_service_for_server_list_tags_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.agent_service_for_server_list_tags_with_http_info(**kwargs)  # noqa: E501
            return data

    def agent_service_for_server_list_tags_with_http_info(self, **kwargs):  # noqa: E501
        """agent_service_for_server_list_tags  # noqa: E501

        Get agent tags.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_list_tags_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str org_identifier: Organization Identifier for the Entity.
        :param str identifier:
        :param str name:
        :param str type:
        :param list[str] tags:
        :param str search_term:
        :param int page_size:
        :param int page_index:
        :param str scope:
        :param str dr_identifier:
        :param str sort_by:
        :param str sort_order:
        :param bool metadata_only:
        :param bool ignore_scope:
        :param str connected_status:
        :param str health_status:
        :param bool with_credentials: Applicable when trying to retrieve an agent. Set to true to include the credentials for the agent in the response. (Private key may not be included in response if agent is already connected to harness). NOTE: Setting this to true requires the user to have edit permissions on Agent.
        :param bool include_secondary:
        :return: V1TagMap
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'project_identifier', 'org_identifier', 'identifier', 'name', 'type', 'tags', 'search_term', 'page_size', 'page_index', 'scope', 'dr_identifier', 'sort_by', 'sort_order', 'metadata_only', 'ignore_scope', 'connected_status', 'health_status', 'with_credentials', 'include_secondary']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method agent_service_for_server_list_tags" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'identifier' in params:
            query_params.append(('identifier', params['identifier']))  # noqa: E501
        if 'name' in params:
            query_params.append(('name', params['name']))  # noqa: E501
        if 'type' in params:
            query_params.append(('type', params['type']))  # noqa: E501
        if 'tags' in params:
            query_params.append(('tags', params['tags']))  # noqa: E501
            collection_formats['tags'] = 'multi'  # noqa: E501
        if 'search_term' in params:
            query_params.append(('searchTerm', params['search_term']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('pageSize', params['page_size']))  # noqa: E501
        if 'page_index' in params:
            query_params.append(('pageIndex', params['page_index']))  # noqa: E501
        if 'scope' in params:
            query_params.append(('scope', params['scope']))  # noqa: E501
        if 'dr_identifier' in params:
            query_params.append(('drIdentifier', params['dr_identifier']))  # noqa: E501
        if 'sort_by' in params:
            query_params.append(('sortBy', params['sort_by']))  # noqa: E501
        if 'sort_order' in params:
            query_params.append(('sortOrder', params['sort_order']))  # noqa: E501
        if 'metadata_only' in params:
            query_params.append(('metadataOnly', params['metadata_only']))  # noqa: E501
        if 'ignore_scope' in params:
            query_params.append(('ignoreScope', params['ignore_scope']))  # noqa: E501
        if 'connected_status' in params:
            query_params.append(('connectedStatus', params['connected_status']))  # noqa: E501
        if 'health_status' in params:
            query_params.append(('healthStatus', params['health_status']))  # noqa: E501
        if 'with_credentials' in params:
            query_params.append(('withCredentials', params['with_credentials']))  # noqa: E501
        if 'include_secondary' in params:
            query_params.append(('includeSecondary', params['include_secondary']))  # noqa: E501

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
            '/gitops/api/v1/agents/tags', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='V1TagMap',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def agent_service_for_server_list_versions(self, **kwargs):  # noqa: E501
        """agent_service_for_server_list_versions  # noqa: E501

        Get agent versions.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_list_versions(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str org_identifier: Organization Identifier for the Entity.
        :param str identifier:
        :param str name:
        :param str type:
        :param list[str] tags:
        :param str search_term:
        :param int page_size:
        :param int page_index:
        :param str scope:
        :param str dr_identifier:
        :param str sort_by:
        :param str sort_order:
        :param bool metadata_only:
        :param bool ignore_scope:
        :param str connected_status:
        :param str health_status:
        :param bool with_credentials: Applicable when trying to retrieve an agent. Set to true to include the credentials for the agent in the response. (Private key may not be included in response if agent is already connected to harness). NOTE: Setting this to true requires the user to have edit permissions on Agent.
        :param bool include_secondary:
        :return: V1VersionList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.agent_service_for_server_list_versions_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.agent_service_for_server_list_versions_with_http_info(**kwargs)  # noqa: E501
            return data

    def agent_service_for_server_list_versions_with_http_info(self, **kwargs):  # noqa: E501
        """agent_service_for_server_list_versions  # noqa: E501

        Get agent versions.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_list_versions_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str org_identifier: Organization Identifier for the Entity.
        :param str identifier:
        :param str name:
        :param str type:
        :param list[str] tags:
        :param str search_term:
        :param int page_size:
        :param int page_index:
        :param str scope:
        :param str dr_identifier:
        :param str sort_by:
        :param str sort_order:
        :param bool metadata_only:
        :param bool ignore_scope:
        :param str connected_status:
        :param str health_status:
        :param bool with_credentials: Applicable when trying to retrieve an agent. Set to true to include the credentials for the agent in the response. (Private key may not be included in response if agent is already connected to harness). NOTE: Setting this to true requires the user to have edit permissions on Agent.
        :param bool include_secondary:
        :return: V1VersionList
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'project_identifier', 'org_identifier', 'identifier', 'name', 'type', 'tags', 'search_term', 'page_size', 'page_index', 'scope', 'dr_identifier', 'sort_by', 'sort_order', 'metadata_only', 'ignore_scope', 'connected_status', 'health_status', 'with_credentials', 'include_secondary']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method agent_service_for_server_list_versions" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'identifier' in params:
            query_params.append(('identifier', params['identifier']))  # noqa: E501
        if 'name' in params:
            query_params.append(('name', params['name']))  # noqa: E501
        if 'type' in params:
            query_params.append(('type', params['type']))  # noqa: E501
        if 'tags' in params:
            query_params.append(('tags', params['tags']))  # noqa: E501
            collection_formats['tags'] = 'multi'  # noqa: E501
        if 'search_term' in params:
            query_params.append(('searchTerm', params['search_term']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('pageSize', params['page_size']))  # noqa: E501
        if 'page_index' in params:
            query_params.append(('pageIndex', params['page_index']))  # noqa: E501
        if 'scope' in params:
            query_params.append(('scope', params['scope']))  # noqa: E501
        if 'dr_identifier' in params:
            query_params.append(('drIdentifier', params['dr_identifier']))  # noqa: E501
        if 'sort_by' in params:
            query_params.append(('sortBy', params['sort_by']))  # noqa: E501
        if 'sort_order' in params:
            query_params.append(('sortOrder', params['sort_order']))  # noqa: E501
        if 'metadata_only' in params:
            query_params.append(('metadataOnly', params['metadata_only']))  # noqa: E501
        if 'ignore_scope' in params:
            query_params.append(('ignoreScope', params['ignore_scope']))  # noqa: E501
        if 'connected_status' in params:
            query_params.append(('connectedStatus', params['connected_status']))  # noqa: E501
        if 'health_status' in params:
            query_params.append(('healthStatus', params['health_status']))  # noqa: E501
        if 'with_credentials' in params:
            query_params.append(('withCredentials', params['with_credentials']))  # noqa: E501
        if 'include_secondary' in params:
            query_params.append(('includeSecondary', params['include_secondary']))  # noqa: E501

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
            '/gitops/api/v1/agents/versions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='V1VersionList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def agent_service_for_server_post_deploy_helm_chart(self, body, agent_identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_post_deploy_helm_chart  # noqa: E501

        PostDeployHelmChart returns the Helm Chart for deploying the agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_post_deploy_helm_chart(body, agent_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1AgentYamlQuery body: (required)
        :param str agent_identifier: Agent identifier for entity. (required)
        :return: StreamResultOfV1DownloadResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.agent_service_for_server_post_deploy_helm_chart_with_http_info(body, agent_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.agent_service_for_server_post_deploy_helm_chart_with_http_info(body, agent_identifier, **kwargs)  # noqa: E501
            return data

    def agent_service_for_server_post_deploy_helm_chart_with_http_info(self, body, agent_identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_post_deploy_helm_chart  # noqa: E501

        PostDeployHelmChart returns the Helm Chart for deploying the agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_post_deploy_helm_chart_with_http_info(body, agent_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1AgentYamlQuery body: (required)
        :param str agent_identifier: Agent identifier for entity. (required)
        :return: StreamResultOfV1DownloadResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'agent_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method agent_service_for_server_post_deploy_helm_chart" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `agent_service_for_server_post_deploy_helm_chart`")  # noqa: E501
        # verify the required parameter 'agent_identifier' is set
        if ('agent_identifier' not in params or
                params['agent_identifier'] is None):
            raise ValueError("Missing the required parameter `agent_identifier` when calling `agent_service_for_server_post_deploy_helm_chart`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'agent_identifier' in params:
            path_params['agentIdentifier'] = params['agent_identifier']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/octet-stream'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/gitops/api/v1/agents/{agentIdentifier}/deployment-spec/helm', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='StreamResultOfV1DownloadResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def agent_service_for_server_post_deploy_overrides(self, body, agent_identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_post_deploy_overrides  # noqa: E501

        PostDeployOverrides returns the Helm Chart overrides for deploying the agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_post_deploy_overrides(body, agent_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1AgentYamlQuery body: (required)
        :param str agent_identifier: Agent identifier for entity. (required)
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.agent_service_for_server_post_deploy_overrides_with_http_info(body, agent_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.agent_service_for_server_post_deploy_overrides_with_http_info(body, agent_identifier, **kwargs)  # noqa: E501
            return data

    def agent_service_for_server_post_deploy_overrides_with_http_info(self, body, agent_identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_post_deploy_overrides  # noqa: E501

        PostDeployOverrides returns the Helm Chart overrides for deploying the agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_post_deploy_overrides_with_http_info(body, agent_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1AgentYamlQuery body: (required)
        :param str agent_identifier: Agent identifier for entity. (required)
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'agent_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method agent_service_for_server_post_deploy_overrides" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `agent_service_for_server_post_deploy_overrides`")  # noqa: E501
        # verify the required parameter 'agent_identifier' is set
        if ('agent_identifier' not in params or
                params['agent_identifier'] is None):
            raise ValueError("Missing the required parameter `agent_identifier` when calling `agent_service_for_server_post_deploy_overrides`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'agent_identifier' in params:
            path_params['agentIdentifier'] = params['agent_identifier']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/yaml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/gitops/api/v1/agents/{agentIdentifier}/helm-overrides', 'POST',
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

    def agent_service_for_server_post_deploy_yaml(self, body, agent_identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_post_deploy_yaml  # noqa: E501

        PostDeployYaml returns deployment yamls for agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_post_deploy_yaml(body, agent_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1AgentYamlQuery body: (required)
        :param str agent_identifier: Agent identifier for entity. (required)
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.agent_service_for_server_post_deploy_yaml_with_http_info(body, agent_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.agent_service_for_server_post_deploy_yaml_with_http_info(body, agent_identifier, **kwargs)  # noqa: E501
            return data

    def agent_service_for_server_post_deploy_yaml_with_http_info(self, body, agent_identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_post_deploy_yaml  # noqa: E501

        PostDeployYaml returns deployment yamls for agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_post_deploy_yaml_with_http_info(body, agent_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1AgentYamlQuery body: (required)
        :param str agent_identifier: Agent identifier for entity. (required)
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'agent_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method agent_service_for_server_post_deploy_yaml" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `agent_service_for_server_post_deploy_yaml`")  # noqa: E501
        # verify the required parameter 'agent_identifier' is set
        if ('agent_identifier' not in params or
                params['agent_identifier'] is None):
            raise ValueError("Missing the required parameter `agent_identifier` when calling `agent_service_for_server_post_deploy_yaml`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'agent_identifier' in params:
            path_params['agentIdentifier'] = params['agent_identifier']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/yaml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/gitops/api/v1/agents/{agentIdentifier}/deployment-spec/yaml', 'POST',
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

    def agent_service_for_server_post_operator_yaml(self, body, agent_identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_post_operator_yaml  # noqa: E501

        PostOperatorYaml returns operator yaml for deploying the agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_post_operator_yaml(body, agent_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1AgentYamlQuery body: (required)
        :param str agent_identifier: Agent identifier for entity. (required)
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.agent_service_for_server_post_operator_yaml_with_http_info(body, agent_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.agent_service_for_server_post_operator_yaml_with_http_info(body, agent_identifier, **kwargs)  # noqa: E501
            return data

    def agent_service_for_server_post_operator_yaml_with_http_info(self, body, agent_identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_post_operator_yaml  # noqa: E501

        PostOperatorYaml returns operator yaml for deploying the agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_post_operator_yaml_with_http_info(body, agent_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1AgentYamlQuery body: (required)
        :param str agent_identifier: Agent identifier for entity. (required)
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'agent_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method agent_service_for_server_post_operator_yaml" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `agent_service_for_server_post_operator_yaml`")  # noqa: E501
        # verify the required parameter 'agent_identifier' is set
        if ('agent_identifier' not in params or
                params['agent_identifier'] is None):
            raise ValueError("Missing the required parameter `agent_identifier` when calling `agent_service_for_server_post_operator_yaml`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'agent_identifier' in params:
            path_params['agentIdentifier'] = params['agent_identifier']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/yaml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/gitops/api/v1/agents/{agentIdentifier}/operator/yaml', 'POST',
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

    def agent_service_for_server_regenerate_credentials(self, identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_regenerate_credentials  # noqa: E501

        Regenerate credentials for agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_regenerate_credentials(identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str identifier: (required)
        :return: V1Agent
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.agent_service_for_server_regenerate_credentials_with_http_info(identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.agent_service_for_server_regenerate_credentials_with_http_info(identifier, **kwargs)  # noqa: E501
            return data

    def agent_service_for_server_regenerate_credentials_with_http_info(self, identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_regenerate_credentials  # noqa: E501

        Regenerate credentials for agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_regenerate_credentials_with_http_info(identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str identifier: (required)
        :return: V1Agent
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method agent_service_for_server_regenerate_credentials" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `agent_service_for_server_regenerate_credentials`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

        query_params = []

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
            '/gitops/api/v1/agents/{identifier}/credentials', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='V1Agent',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def agent_service_for_server_scale(self, body, identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_scale  # noqa: E501

        Scale the Hosted agent.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_scale(body, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1AgentScaleRequest body: (required)
        :param str identifier: (required)
        :return: V1Agent
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.agent_service_for_server_scale_with_http_info(body, identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.agent_service_for_server_scale_with_http_info(body, identifier, **kwargs)  # noqa: E501
            return data

    def agent_service_for_server_scale_with_http_info(self, body, identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_scale  # noqa: E501

        Scale the Hosted agent.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_scale_with_http_info(body, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1AgentScaleRequest body: (required)
        :param str identifier: (required)
        :return: V1Agent
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method agent_service_for_server_scale" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `agent_service_for_server_scale`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `agent_service_for_server_scale`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

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
            '/gitops/api/v1/agents/{identifier}/scale', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='V1Agent',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def agent_service_for_server_search(self, body, **kwargs):  # noqa: E501
        """agent_service_for_server_search  # noqa: E501

        Search agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_search(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1AgentQuery body: (required)
        :return: V1AgentList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.agent_service_for_server_search_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.agent_service_for_server_search_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def agent_service_for_server_search_with_http_info(self, body, **kwargs):  # noqa: E501
        """agent_service_for_server_search  # noqa: E501

        Search agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_search_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1AgentQuery body: (required)
        :return: V1AgentList
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method agent_service_for_server_search" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `agent_service_for_server_search`")  # noqa: E501

        collection_formats = {}

        path_params = {}

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
            '/gitops/api/v1/agents/search', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='V1AgentList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def agent_service_for_server_set_primary_node(self, body, agent_identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_set_primary_node  # noqa: E501

        Set primary disaster recovery node.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_set_primary_node(body, agent_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1AgentSetPrimaryNodeRequest body: (required)
        :param str agent_identifier: Agent identifier for entity. (required)
        :return: V1Agent
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.agent_service_for_server_set_primary_node_with_http_info(body, agent_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.agent_service_for_server_set_primary_node_with_http_info(body, agent_identifier, **kwargs)  # noqa: E501
            return data

    def agent_service_for_server_set_primary_node_with_http_info(self, body, agent_identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_set_primary_node  # noqa: E501

        Set primary disaster recovery node.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_set_primary_node_with_http_info(body, agent_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1AgentSetPrimaryNodeRequest body: (required)
        :param str agent_identifier: Agent identifier for entity. (required)
        :return: V1Agent
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'agent_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method agent_service_for_server_set_primary_node" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `agent_service_for_server_set_primary_node`")  # noqa: E501
        # verify the required parameter 'agent_identifier' is set
        if ('agent_identifier' not in params or
                params['agent_identifier'] is None):
            raise ValueError("Missing the required parameter `agent_identifier` when calling `agent_service_for_server_set_primary_node`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'agent_identifier' in params:
            path_params['agentIdentifier'] = params['agent_identifier']  # noqa: E501

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
            '/gitops/api/v1/agents/{agentIdentifier}/primaryNode', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='V1Agent',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def agent_service_for_server_unique(self, identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_unique  # noqa: E501

        Unique returns unique agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_unique(identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str identifier: (required)
        :param str account_identifier: Account Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str org_identifier: Organization Identifier for the Entity.
        :param str name:
        :param str type:
        :param list[str] tags:
        :param str search_term:
        :param int page_size:
        :param int page_index:
        :param str scope:
        :param str dr_identifier:
        :param str sort_by:
        :param str sort_order:
        :param bool metadata_only:
        :param bool ignore_scope:
        :param str connected_status:
        :param str health_status:
        :param bool with_credentials: Applicable when trying to retrieve an agent. Set to true to include the credentials for the agent in the response. (Private key may not be included in response if agent is already connected to harness). NOTE: Setting this to true requires the user to have edit permissions on Agent.
        :param bool include_secondary:
        :return: V1UniqueMessage
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.agent_service_for_server_unique_with_http_info(identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.agent_service_for_server_unique_with_http_info(identifier, **kwargs)  # noqa: E501
            return data

    def agent_service_for_server_unique_with_http_info(self, identifier, **kwargs):  # noqa: E501
        """agent_service_for_server_unique  # noqa: E501

        Unique returns unique agents.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_unique_with_http_info(identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str identifier: (required)
        :param str account_identifier: Account Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str org_identifier: Organization Identifier for the Entity.
        :param str name:
        :param str type:
        :param list[str] tags:
        :param str search_term:
        :param int page_size:
        :param int page_index:
        :param str scope:
        :param str dr_identifier:
        :param str sort_by:
        :param str sort_order:
        :param bool metadata_only:
        :param bool ignore_scope:
        :param str connected_status:
        :param str health_status:
        :param bool with_credentials: Applicable when trying to retrieve an agent. Set to true to include the credentials for the agent in the response. (Private key may not be included in response if agent is already connected to harness). NOTE: Setting this to true requires the user to have edit permissions on Agent.
        :param bool include_secondary:
        :return: V1UniqueMessage
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['identifier', 'account_identifier', 'project_identifier', 'org_identifier', 'name', 'type', 'tags', 'search_term', 'page_size', 'page_index', 'scope', 'dr_identifier', 'sort_by', 'sort_order', 'metadata_only', 'ignore_scope', 'connected_status', 'health_status', 'with_credentials', 'include_secondary']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method agent_service_for_server_unique" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `agent_service_for_server_unique`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'name' in params:
            query_params.append(('name', params['name']))  # noqa: E501
        if 'type' in params:
            query_params.append(('type', params['type']))  # noqa: E501
        if 'tags' in params:
            query_params.append(('tags', params['tags']))  # noqa: E501
            collection_formats['tags'] = 'multi'  # noqa: E501
        if 'search_term' in params:
            query_params.append(('searchTerm', params['search_term']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('pageSize', params['page_size']))  # noqa: E501
        if 'page_index' in params:
            query_params.append(('pageIndex', params['page_index']))  # noqa: E501
        if 'scope' in params:
            query_params.append(('scope', params['scope']))  # noqa: E501
        if 'dr_identifier' in params:
            query_params.append(('drIdentifier', params['dr_identifier']))  # noqa: E501
        if 'sort_by' in params:
            query_params.append(('sortBy', params['sort_by']))  # noqa: E501
        if 'sort_order' in params:
            query_params.append(('sortOrder', params['sort_order']))  # noqa: E501
        if 'metadata_only' in params:
            query_params.append(('metadataOnly', params['metadata_only']))  # noqa: E501
        if 'ignore_scope' in params:
            query_params.append(('ignoreScope', params['ignore_scope']))  # noqa: E501
        if 'connected_status' in params:
            query_params.append(('connectedStatus', params['connected_status']))  # noqa: E501
        if 'health_status' in params:
            query_params.append(('healthStatus', params['health_status']))  # noqa: E501
        if 'with_credentials' in params:
            query_params.append(('withCredentials', params['with_credentials']))  # noqa: E501
        if 'include_secondary' in params:
            query_params.append(('includeSecondary', params['include_secondary']))  # noqa: E501

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
            '/gitops/api/v1/agents/{identifier}/unique', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='V1UniqueMessage',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def agent_service_for_server_update(self, body, agent_identifier, **kwargs):  # noqa: E501
        """Update agents.  # noqa: E501

        This API can be used to update an agent's details in Harness. The following fields will be updated to the new values in the body - \"tags\", \"metadata\"(all nested fields in metadata will be replaced with new provided values including empty/nil values if they're sent), \"description\", \"type\".  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_update(body, agent_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1Agent body: (required)
        :param str agent_identifier: The gitops-server generated ID for this gitops-agent (required)
        :return: V1Agent
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.agent_service_for_server_update_with_http_info(body, agent_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.agent_service_for_server_update_with_http_info(body, agent_identifier, **kwargs)  # noqa: E501
            return data

    def agent_service_for_server_update_with_http_info(self, body, agent_identifier, **kwargs):  # noqa: E501
        """Update agents.  # noqa: E501

        This API can be used to update an agent's details in Harness. The following fields will be updated to the new values in the body - \"tags\", \"metadata\"(all nested fields in metadata will be replaced with new provided values including empty/nil values if they're sent), \"description\", \"type\".  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.agent_service_for_server_update_with_http_info(body, agent_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1Agent body: (required)
        :param str agent_identifier: The gitops-server generated ID for this gitops-agent (required)
        :return: V1Agent
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'agent_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method agent_service_for_server_update" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `agent_service_for_server_update`")  # noqa: E501
        # verify the required parameter 'agent_identifier' is set
        if ('agent_identifier' not in params or
                params['agent_identifier'] is None):
            raise ValueError("Missing the required parameter `agent_identifier` when calling `agent_service_for_server_update`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'agent_identifier' in params:
            path_params['agent.identifier'] = params['agent_identifier']  # noqa: E501

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
            '/gitops/api/v1/agents/{agent.identifier}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='V1Agent',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def version_upgrade_service_upgrade_available_v2(self, **kwargs):  # noqa: E501
        """version_upgrade_service_upgrade_available_v2  # noqa: E501

        Check for version updates.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.version_upgrade_service_upgrade_available_v2(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str existing_version: Current Agent Version
        :return: V1VersionUpgradeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.version_upgrade_service_upgrade_available_v2_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.version_upgrade_service_upgrade_available_v2_with_http_info(**kwargs)  # noqa: E501
            return data

    def version_upgrade_service_upgrade_available_v2_with_http_info(self, **kwargs):  # noqa: E501
        """version_upgrade_service_upgrade_available_v2  # noqa: E501

        Check for version updates.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.version_upgrade_service_upgrade_available_v2_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str existing_version: Current Agent Version
        :return: V1VersionUpgradeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['existing_version']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method version_upgrade_service_upgrade_available_v2" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'existing_version' in params:
            query_params.append(('existingVersion', params['existing_version']))  # noqa: E501

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
            '/gitops/api/v2/versions/agents/upgrade-available', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='V1VersionUpgradeResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
