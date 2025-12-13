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


class ServiceOverridesApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_service_override(self, body, account_identifier, **kwargs):  # noqa: E501
        """Create an ServiceOverride Entity  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_service_override(body, account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ServiceOverrideRequestV2 body: Details of the Service Override to be updated (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :return: ResponseDTOServiceOverrideResponseV2
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_service_override_with_http_info(body, account_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.create_service_override_with_http_info(body, account_identifier, **kwargs)  # noqa: E501
            return data

    def create_service_override_with_http_info(self, body, account_identifier, **kwargs):  # noqa: E501
        """Create an ServiceOverride Entity  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_service_override_with_http_info(body, account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ServiceOverrideRequestV2 body: Details of the Service Override to be updated (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :return: ResponseDTOServiceOverrideResponseV2
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
                    " to method create_service_override" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_service_override`")  # noqa: E501
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `create_service_override`")  # noqa: E501

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
            '/ng/api/serviceOverrides', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ResponseDTOServiceOverrideResponseV2',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_service_override1(self, identifier, account_identifier, **kwargs):  # noqa: E501
        """Delete a ServiceOverride entity  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_service_override1(identifier, account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str identifier: Service Overrides Identifier for Entity. (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: ResponseDTOBoolean
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_service_override1_with_http_info(identifier, account_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_service_override1_with_http_info(identifier, account_identifier, **kwargs)  # noqa: E501
            return data

    def delete_service_override1_with_http_info(self, identifier, account_identifier, **kwargs):  # noqa: E501
        """Delete a ServiceOverride entity  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_service_override1_with_http_info(identifier, account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str identifier: Service Overrides Identifier for Entity. (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: ResponseDTOBoolean
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['identifier', 'account_identifier', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_service_override1" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `delete_service_override1`")  # noqa: E501
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `delete_service_override1`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501

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
            '/ng/api/serviceOverrides/{identifier}', 'DELETE',
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

    def get_service_overrides(self, identifier, account_identifier, **kwargs):  # noqa: E501
        """Gets Service Overrides by Identifier  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_service_overrides(identifier, account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str identifier: Service Overrides Identifier for Entity. (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: ResponseDTOServiceOverrideResponseV2
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_service_overrides_with_http_info(identifier, account_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.get_service_overrides_with_http_info(identifier, account_identifier, **kwargs)  # noqa: E501
            return data

    def get_service_overrides_with_http_info(self, identifier, account_identifier, **kwargs):  # noqa: E501
        """Gets Service Overrides by Identifier  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_service_overrides_with_http_info(identifier, account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str identifier: Service Overrides Identifier for Entity. (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: ResponseDTOServiceOverrideResponseV2
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['identifier', 'account_identifier', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_service_overrides" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `get_service_overrides`")  # noqa: E501
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `get_service_overrides`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501

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
            '/ng/api/serviceOverrides/{identifier}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ResponseDTOServiceOverrideResponseV2',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def service_override_move_configs(self, account_identifier, **kwargs):  # noqa: E501
        """Move ServiceOverride YAML from inline to remote or remote to inline  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.service_override_move_configs(account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str connector_ref: Identifier of Connector needed for CRUD operations on the respective Entity
        :param str repo_name: Name of the repository.
        :param str branch: Name of the branch.
        :param str file_path: File Path of the Entity.
        :param str commit_msg: File Path of the Entity.
        :param bool is_new_branch: Checks the new branch
        :param str base_branch: Name of the default branch.
        :param bool is_harness_code_repo: Is Harness code repo enabled
        :param str move_config_type: Tells weather the entity has to be moved from inline to remote or remote to inline
        :param str environment_ref: Environment Reference for the Entity.
        :param str service_ref: Service Reference for Entity
        :param str infra_identifier: infraIdentifier
        :param str service_overrides_type: Type of the override which is based on source of overrides
        :param str identifier: Service Overrides Identifier for Entity.
        :return: ResponseDTOServiceOverrideMoveConfigResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.service_override_move_configs_with_http_info(account_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.service_override_move_configs_with_http_info(account_identifier, **kwargs)  # noqa: E501
            return data

    def service_override_move_configs_with_http_info(self, account_identifier, **kwargs):  # noqa: E501
        """Move ServiceOverride YAML from inline to remote or remote to inline  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.service_override_move_configs_with_http_info(account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str connector_ref: Identifier of Connector needed for CRUD operations on the respective Entity
        :param str repo_name: Name of the repository.
        :param str branch: Name of the branch.
        :param str file_path: File Path of the Entity.
        :param str commit_msg: File Path of the Entity.
        :param bool is_new_branch: Checks the new branch
        :param str base_branch: Name of the default branch.
        :param bool is_harness_code_repo: Is Harness code repo enabled
        :param str move_config_type: Tells weather the entity has to be moved from inline to remote or remote to inline
        :param str environment_ref: Environment Reference for the Entity.
        :param str service_ref: Service Reference for Entity
        :param str infra_identifier: infraIdentifier
        :param str service_overrides_type: Type of the override which is based on source of overrides
        :param str identifier: Service Overrides Identifier for Entity.
        :return: ResponseDTOServiceOverrideMoveConfigResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'org_identifier', 'project_identifier', 'connector_ref', 'repo_name', 'branch', 'file_path', 'commit_msg', 'is_new_branch', 'base_branch', 'is_harness_code_repo', 'move_config_type', 'environment_ref', 'service_ref', 'infra_identifier', 'service_overrides_type', 'identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method service_override_move_configs" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `service_override_move_configs`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'connector_ref' in params:
            query_params.append(('connectorRef', params['connector_ref']))  # noqa: E501
        if 'repo_name' in params:
            query_params.append(('repoName', params['repo_name']))  # noqa: E501
        if 'branch' in params:
            query_params.append(('branch', params['branch']))  # noqa: E501
        if 'file_path' in params:
            query_params.append(('filePath', params['file_path']))  # noqa: E501
        if 'commit_msg' in params:
            query_params.append(('commitMsg', params['commit_msg']))  # noqa: E501
        if 'is_new_branch' in params:
            query_params.append(('isNewBranch', params['is_new_branch']))  # noqa: E501
        if 'base_branch' in params:
            query_params.append(('baseBranch', params['base_branch']))  # noqa: E501
        if 'is_harness_code_repo' in params:
            query_params.append(('isHarnessCodeRepo', params['is_harness_code_repo']))  # noqa: E501
        if 'move_config_type' in params:
            query_params.append(('moveConfigType', params['move_config_type']))  # noqa: E501
        if 'environment_ref' in params:
            query_params.append(('environmentRef', params['environment_ref']))  # noqa: E501
        if 'service_ref' in params:
            query_params.append(('serviceRef', params['service_ref']))  # noqa: E501
        if 'infra_identifier' in params:
            query_params.append(('infraIdentifier', params['infra_identifier']))  # noqa: E501
        if 'service_overrides_type' in params:
            query_params.append(('serviceOverridesType', params['service_overrides_type']))  # noqa: E501
        if 'identifier' in params:
            query_params.append(('identifier', params['identifier']))  # noqa: E501

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
            '/ng/api/serviceOverrides/move-config', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ResponseDTOServiceOverrideMoveConfigResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_service_override(self, body, account_identifier, **kwargs):  # noqa: E501
        """Update an ServiceOverride Entity  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_service_override(body, account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ServiceOverrideRequestV2 body: Details of the Service Override to be updated (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :return: ResponseDTOServiceOverrideResponseV2
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_service_override_with_http_info(body, account_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.update_service_override_with_http_info(body, account_identifier, **kwargs)  # noqa: E501
            return data

    def update_service_override_with_http_info(self, body, account_identifier, **kwargs):  # noqa: E501
        """Update an ServiceOverride Entity  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_service_override_with_http_info(body, account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ServiceOverrideRequestV2 body: Details of the Service Override to be updated (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :return: ResponseDTOServiceOverrideResponseV2
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
                    " to method update_service_override" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update_service_override`")  # noqa: E501
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `update_service_override`")  # noqa: E501

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
            '/ng/api/serviceOverrides', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ResponseDTOServiceOverrideResponseV2',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_service_override_git_details(self, account_identifier, **kwargs):  # noqa: E501
        """Update git-metadata in remote ServiceOverride Entity  # noqa: E501

        Update git-metadata in remote ServiceOverride and returns the identifier of updated ServiceOverride  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_service_override_git_details(account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str identifier: Service Overrides Identifier for Entity.
        :param str environment_ref: Environment Reference for the Entity.
        :param str service_ref: Service Reference for Entity
        :param str infra_identifier: infraIdentifier
        :param str service_overrides_type: Type of the override which is based on source of overrides
        :param GitMetadataUpdateRequestInfo connector_ref: Identifier of Connector needed for CRUD operations on the respective Entity
        :param GitMetadataUpdateRequestInfo repo_name: Name of the repository.
        :param GitMetadataUpdateRequestInfo file_path: File Path of the Entity.
        :return: ResponseDTOServiceOverrideGitUpdateResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_service_override_git_details_with_http_info(account_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.update_service_override_git_details_with_http_info(account_identifier, **kwargs)  # noqa: E501
            return data

    def update_service_override_git_details_with_http_info(self, account_identifier, **kwargs):  # noqa: E501
        """Update git-metadata in remote ServiceOverride Entity  # noqa: E501

        Update git-metadata in remote ServiceOverride and returns the identifier of updated ServiceOverride  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_service_override_git_details_with_http_info(account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str identifier: Service Overrides Identifier for Entity.
        :param str environment_ref: Environment Reference for the Entity.
        :param str service_ref: Service Reference for Entity
        :param str infra_identifier: infraIdentifier
        :param str service_overrides_type: Type of the override which is based on source of overrides
        :param GitMetadataUpdateRequestInfo connector_ref: Identifier of Connector needed for CRUD operations on the respective Entity
        :param GitMetadataUpdateRequestInfo repo_name: Name of the repository.
        :param GitMetadataUpdateRequestInfo file_path: File Path of the Entity.
        :return: ResponseDTOServiceOverrideGitUpdateResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'org_identifier', 'project_identifier', 'identifier', 'environment_ref', 'service_ref', 'infra_identifier', 'service_overrides_type', 'connector_ref', 'repo_name', 'file_path']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_service_override_git_details" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `update_service_override_git_details`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'identifier' in params:
            query_params.append(('identifier', params['identifier']))  # noqa: E501
        if 'environment_ref' in params:
            query_params.append(('environmentRef', params['environment_ref']))  # noqa: E501
        if 'service_ref' in params:
            query_params.append(('serviceRef', params['service_ref']))  # noqa: E501
        if 'infra_identifier' in params:
            query_params.append(('infraIdentifier', params['infra_identifier']))  # noqa: E501
        if 'service_overrides_type' in params:
            query_params.append(('serviceOverridesType', params['service_overrides_type']))  # noqa: E501
        if 'connector_ref' in params:
            query_params.append(('connectorRef', params['connector_ref']))  # noqa: E501
        if 'repo_name' in params:
            query_params.append(('repoName', params['repo_name']))  # noqa: E501
        if 'file_path' in params:
            query_params.append(('filePath', params['file_path']))  # noqa: E501

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
            '/ng/api/serviceOverrides/update-git-metadata', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ResponseDTOServiceOverrideGitUpdateResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
