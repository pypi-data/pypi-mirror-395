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


class InfrastructuresApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_infrastructure(self, body, account_identifier, **kwargs):  # noqa: E501
        """Create an Infrastructure in an Environment  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_infrastructure(body, account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param InfrastructureRequest body: Details of the Infrastructure to be created (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :return: ResponseDTOInfrastructureResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_infrastructure_with_http_info(body, account_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.create_infrastructure_with_http_info(body, account_identifier, **kwargs)  # noqa: E501
            return data

    def create_infrastructure_with_http_info(self, body, account_identifier, **kwargs):  # noqa: E501
        """Create an Infrastructure in an Environment  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_infrastructure_with_http_info(body, account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param InfrastructureRequest body: Details of the Infrastructure to be created (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :return: ResponseDTOInfrastructureResponse
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
                    " to method create_infrastructure" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_infrastructure`")  # noqa: E501
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `create_infrastructure`")  # noqa: E501

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
            ['application/json', 'application/yaml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/ng/api/infrastructures', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ResponseDTOInfrastructureResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_infrastructure(self, infra_identifier, account_identifier, environment_identifier, **kwargs):  # noqa: E501
        """Delete an Infrastructure by identifier  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_infrastructure(infra_identifier, account_identifier, environment_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str infra_identifier: Infrastructure Identifier for the entity (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str environment_identifier: Environment Identifier for the Entity. (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param bool force_delete: If true, the Entity will be forced delete, without checking any references/usages
        :return: ResponseDTOBoolean
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_infrastructure_with_http_info(infra_identifier, account_identifier, environment_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_infrastructure_with_http_info(infra_identifier, account_identifier, environment_identifier, **kwargs)  # noqa: E501
            return data

    def delete_infrastructure_with_http_info(self, infra_identifier, account_identifier, environment_identifier, **kwargs):  # noqa: E501
        """Delete an Infrastructure by identifier  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_infrastructure_with_http_info(infra_identifier, account_identifier, environment_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str infra_identifier: Infrastructure Identifier for the entity (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str environment_identifier: Environment Identifier for the Entity. (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param bool force_delete: If true, the Entity will be forced delete, without checking any references/usages
        :return: ResponseDTOBoolean
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['infra_identifier', 'account_identifier', 'environment_identifier', 'org_identifier', 'project_identifier', 'force_delete']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_infrastructure" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'infra_identifier' is set
        if ('infra_identifier' not in params or
                params['infra_identifier'] is None):
            raise ValueError("Missing the required parameter `infra_identifier` when calling `delete_infrastructure`")  # noqa: E501
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `delete_infrastructure`")  # noqa: E501
        # verify the required parameter 'environment_identifier' is set
        if ('environment_identifier' not in params or
                params['environment_identifier'] is None):
            raise ValueError("Missing the required parameter `environment_identifier` when calling `delete_infrastructure`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'infra_identifier' in params:
            path_params['infraIdentifier'] = params['infra_identifier']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'environment_identifier' in params:
            query_params.append(('environmentIdentifier', params['environment_identifier']))  # noqa: E501
        if 'force_delete' in params:
            query_params.append(('forceDelete', params['force_delete']))  # noqa: E501

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
            '/ng/api/infrastructures/{infraIdentifier}', 'DELETE',
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

    def get_infrastructure(self, infra_identifier, account_identifier, environment_identifier, **kwargs):  # noqa: E501
        """Gets an Infrastructure by identifier  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_infrastructure(infra_identifier, account_identifier, environment_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str infra_identifier: Infrastructure Identifier for the entity (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str environment_identifier: envId (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param bool deleted: Specify whether Infrastructure is deleted or not
        :return: ResponseDTOInfrastructureResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_infrastructure_with_http_info(infra_identifier, account_identifier, environment_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.get_infrastructure_with_http_info(infra_identifier, account_identifier, environment_identifier, **kwargs)  # noqa: E501
            return data

    def get_infrastructure_with_http_info(self, infra_identifier, account_identifier, environment_identifier, **kwargs):  # noqa: E501
        """Gets an Infrastructure by identifier  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_infrastructure_with_http_info(infra_identifier, account_identifier, environment_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str infra_identifier: Infrastructure Identifier for the entity (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str environment_identifier: envId (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param bool deleted: Specify whether Infrastructure is deleted or not
        :return: ResponseDTOInfrastructureResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['infra_identifier', 'account_identifier', 'environment_identifier', 'org_identifier', 'project_identifier', 'deleted']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_infrastructure" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'infra_identifier' is set
        if ('infra_identifier' not in params or
                params['infra_identifier'] is None):
            raise ValueError("Missing the required parameter `infra_identifier` when calling `get_infrastructure`")  # noqa: E501
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `get_infrastructure`")  # noqa: E501
        # verify the required parameter 'environment_identifier' is set
        if ('environment_identifier' not in params or
                params['environment_identifier'] is None):
            raise ValueError("Missing the required parameter `environment_identifier` when calling `get_infrastructure`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'infra_identifier' in params:
            path_params['infraIdentifier'] = params['infra_identifier']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'environment_identifier' in params:
            query_params.append(('environmentIdentifier', params['environment_identifier']))  # noqa: E501
        if 'deleted' in params:
            query_params.append(('deleted', params['deleted']))  # noqa: E501

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
            '/ng/api/infrastructures/{infraIdentifier}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ResponseDTOInfrastructureResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_infrastructure_list(self, account_identifier, environment_identifier, **kwargs):  # noqa: E501
        """Gets Infrastructure list  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_infrastructure_list(account_identifier, environment_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str environment_identifier: Environment Identifier for the Entity. (required)
        :param int page: Page Index of the results to fetch.Default Value: 0
        :param int size: Results per page
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str search_term: The word to be searched and included in the list response
        :param list[str] infra_identifiers: List of InfrastructureIds
        :param str deployment_type:
        :param str deployment_template_identifier: The Identifier of deployment template if infrastructure is of type custom deployment
        :param str version_label: The version label of deployment template if infrastructure is of type custom deployment
        :param list[str] sort: Specifies the sorting criteria of the list. Elements in the list should be of the format \"property,order\" or \"property\". Order can take values ASC or DESC for alphabetical ascending and descending orders respectively. If the order is not specified, it takes ASC by default
        :param list[str] service_refs: list of service refs required to fetch infrastructures scoped to these service refs
        :return: ResponseDTOPageResponseInfrastructureResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_infrastructure_list_with_http_info(account_identifier, environment_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.get_infrastructure_list_with_http_info(account_identifier, environment_identifier, **kwargs)  # noqa: E501
            return data

    def get_infrastructure_list_with_http_info(self, account_identifier, environment_identifier, **kwargs):  # noqa: E501
        """Gets Infrastructure list  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_infrastructure_list_with_http_info(account_identifier, environment_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str environment_identifier: Environment Identifier for the Entity. (required)
        :param int page: Page Index of the results to fetch.Default Value: 0
        :param int size: Results per page
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str search_term: The word to be searched and included in the list response
        :param list[str] infra_identifiers: List of InfrastructureIds
        :param str deployment_type:
        :param str deployment_template_identifier: The Identifier of deployment template if infrastructure is of type custom deployment
        :param str version_label: The version label of deployment template if infrastructure is of type custom deployment
        :param list[str] sort: Specifies the sorting criteria of the list. Elements in the list should be of the format \"property,order\" or \"property\". Order can take values ASC or DESC for alphabetical ascending and descending orders respectively. If the order is not specified, it takes ASC by default
        :param list[str] service_refs: list of service refs required to fetch infrastructures scoped to these service refs
        :return: ResponseDTOPageResponseInfrastructureResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'environment_identifier', 'page', 'size', 'org_identifier', 'project_identifier', 'search_term', 'infra_identifiers', 'deployment_type', 'deployment_template_identifier', 'version_label', 'sort', 'service_refs']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_infrastructure_list" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `get_infrastructure_list`")  # noqa: E501
        # verify the required parameter 'environment_identifier' is set
        if ('environment_identifier' not in params or
                params['environment_identifier'] is None):
            raise ValueError("Missing the required parameter `environment_identifier` when calling `get_infrastructure_list`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'size' in params:
            query_params.append(('size', params['size']))  # noqa: E501
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'environment_identifier' in params:
            query_params.append(('environmentIdentifier', params['environment_identifier']))  # noqa: E501
        if 'search_term' in params:
            query_params.append(('searchTerm', params['search_term']))  # noqa: E501
        if 'infra_identifiers' in params:
            query_params.append(('infraIdentifiers', params['infra_identifiers']))  # noqa: E501
            collection_formats['infraIdentifiers'] = 'multi'  # noqa: E501
        if 'deployment_type' in params:
            query_params.append(('deploymentType', params['deployment_type']))  # noqa: E501
        if 'deployment_template_identifier' in params:
            query_params.append(('deploymentTemplateIdentifier', params['deployment_template_identifier']))  # noqa: E501
        if 'version_label' in params:
            query_params.append(('versionLabel', params['version_label']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501
            collection_formats['sort'] = 'multi'  # noqa: E501
        if 'service_refs' in params:
            query_params.append(('serviceRefs', params['service_refs']))  # noqa: E501
            collection_formats['serviceRefs'] = 'multi'  # noqa: E501

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
            '/ng/api/infrastructures', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ResponseDTOPageResponseInfrastructureResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def import_infrastructure(self, account_identifier, environment_identifier, repo_name, branch, file_path, **kwargs):  # noqa: E501
        """Import and Create Infrastructure from Git Repository  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.import_infrastructure(account_identifier, environment_identifier, repo_name, branch, file_path, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str environment_identifier: Environment Identifier for the entity (required)
        :param str repo_name: Name of the repository. (required)
        :param str branch: Name of the branch. (required)
        :param str file_path: File Path of the Entity. (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str infra_identifier: Infrastructure Identifier for the entity
        :param str connector_ref: Identifier of Connector needed for CRUD operations on the respective Entity
        :param bool is_force_import: isForceImport
        :param bool is_harness_code_repo: Is Harness code repo enabled
        :return: ResponseDTOInfrastructureImportResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.import_infrastructure_with_http_info(account_identifier, environment_identifier, repo_name, branch, file_path, **kwargs)  # noqa: E501
        else:
            (data) = self.import_infrastructure_with_http_info(account_identifier, environment_identifier, repo_name, branch, file_path, **kwargs)  # noqa: E501
            return data

    def import_infrastructure_with_http_info(self, account_identifier, environment_identifier, repo_name, branch, file_path, **kwargs):  # noqa: E501
        """Import and Create Infrastructure from Git Repository  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.import_infrastructure_with_http_info(account_identifier, environment_identifier, repo_name, branch, file_path, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str environment_identifier: Environment Identifier for the entity (required)
        :param str repo_name: Name of the repository. (required)
        :param str branch: Name of the branch. (required)
        :param str file_path: File Path of the Entity. (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str infra_identifier: Infrastructure Identifier for the entity
        :param str connector_ref: Identifier of Connector needed for CRUD operations on the respective Entity
        :param bool is_force_import: isForceImport
        :param bool is_harness_code_repo: Is Harness code repo enabled
        :return: ResponseDTOInfrastructureImportResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'environment_identifier', 'repo_name', 'branch', 'file_path', 'org_identifier', 'project_identifier', 'infra_identifier', 'connector_ref', 'is_force_import', 'is_harness_code_repo']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method import_infrastructure" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `import_infrastructure`")  # noqa: E501
        # verify the required parameter 'environment_identifier' is set
        if ('environment_identifier' not in params or
                params['environment_identifier'] is None):
            raise ValueError("Missing the required parameter `environment_identifier` when calling `import_infrastructure`")  # noqa: E501
        # verify the required parameter 'repo_name' is set
        if ('repo_name' not in params or
                params['repo_name'] is None):
            raise ValueError("Missing the required parameter `repo_name` when calling `import_infrastructure`")  # noqa: E501
        # verify the required parameter 'branch' is set
        if ('branch' not in params or
                params['branch'] is None):
            raise ValueError("Missing the required parameter `branch` when calling `import_infrastructure`")  # noqa: E501
        # verify the required parameter 'file_path' is set
        if ('file_path' not in params or
                params['file_path'] is None):
            raise ValueError("Missing the required parameter `file_path` when calling `import_infrastructure`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'environment_identifier' in params:
            query_params.append(('environmentIdentifier', params['environment_identifier']))  # noqa: E501
        if 'infra_identifier' in params:
            query_params.append(('infraIdentifier', params['infra_identifier']))  # noqa: E501
        if 'connector_ref' in params:
            query_params.append(('connectorRef', params['connector_ref']))  # noqa: E501
        if 'repo_name' in params:
            query_params.append(('repoName', params['repo_name']))  # noqa: E501
        if 'branch' in params:
            query_params.append(('branch', params['branch']))  # noqa: E501
        if 'file_path' in params:
            query_params.append(('filePath', params['file_path']))  # noqa: E501
        if 'is_force_import' in params:
            query_params.append(('isForceImport', params['is_force_import']))  # noqa: E501
        if 'is_harness_code_repo' in params:
            query_params.append(('isHarnessCodeRepo', params['is_harness_code_repo']))  # noqa: E501

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
            '/ng/api/infrastructures/import', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ResponseDTOInfrastructureImportResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def move_infra_configs(self, account_identifier, environment_identifier, infra_identifier, move_config_type, **kwargs):  # noqa: E501
        """Move infra YAML from inline to remote  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.move_infra_configs(account_identifier, environment_identifier, infra_identifier, move_config_type, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str environment_identifier: envId (required)
        :param str infra_identifier: Infrastructure Identifier for the entity (required)
        :param str move_config_type: Tells weather the entity has to be moved from inline to remote or remote to inline (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str connector_ref: Identifier of Connector needed for CRUD operations on the respective Entity
        :param str repo_name: Name of the repository.
        :param str branch: Name of the branch.
        :param str file_path: File Path of the Entity.
        :param str commit_msg: Commit Message to use for the merge commit.
        :param bool is_new_branch: Checks the new branch
        :param str base_branch: Name of the default branch.
        :param bool is_harness_code_repo: Is Harness code repo enabled
        :return: ResponseDTOInfraMoveConfigResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.move_infra_configs_with_http_info(account_identifier, environment_identifier, infra_identifier, move_config_type, **kwargs)  # noqa: E501
        else:
            (data) = self.move_infra_configs_with_http_info(account_identifier, environment_identifier, infra_identifier, move_config_type, **kwargs)  # noqa: E501
            return data

    def move_infra_configs_with_http_info(self, account_identifier, environment_identifier, infra_identifier, move_config_type, **kwargs):  # noqa: E501
        """Move infra YAML from inline to remote  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.move_infra_configs_with_http_info(account_identifier, environment_identifier, infra_identifier, move_config_type, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str environment_identifier: envId (required)
        :param str infra_identifier: Infrastructure Identifier for the entity (required)
        :param str move_config_type: Tells weather the entity has to be moved from inline to remote or remote to inline (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str connector_ref: Identifier of Connector needed for CRUD operations on the respective Entity
        :param str repo_name: Name of the repository.
        :param str branch: Name of the branch.
        :param str file_path: File Path of the Entity.
        :param str commit_msg: Commit Message to use for the merge commit.
        :param bool is_new_branch: Checks the new branch
        :param str base_branch: Name of the default branch.
        :param bool is_harness_code_repo: Is Harness code repo enabled
        :return: ResponseDTOInfraMoveConfigResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'environment_identifier', 'infra_identifier', 'move_config_type', 'org_identifier', 'project_identifier', 'connector_ref', 'repo_name', 'branch', 'file_path', 'commit_msg', 'is_new_branch', 'base_branch', 'is_harness_code_repo']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method move_infra_configs" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `move_infra_configs`")  # noqa: E501
        # verify the required parameter 'environment_identifier' is set
        if ('environment_identifier' not in params or
                params['environment_identifier'] is None):
            raise ValueError("Missing the required parameter `environment_identifier` when calling `move_infra_configs`")  # noqa: E501
        # verify the required parameter 'infra_identifier' is set
        if ('infra_identifier' not in params or
                params['infra_identifier'] is None):
            raise ValueError("Missing the required parameter `infra_identifier` when calling `move_infra_configs`")  # noqa: E501
        # verify the required parameter 'move_config_type' is set
        if ('move_config_type' not in params or
                params['move_config_type'] is None):
            raise ValueError("Missing the required parameter `move_config_type` when calling `move_infra_configs`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'infra_identifier' in params:
            path_params['infraIdentifier'] = params['infra_identifier']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'environment_identifier' in params:
            query_params.append(('environmentIdentifier', params['environment_identifier']))  # noqa: E501
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
            '/ng/api/infrastructures/move-config/{infraIdentifier}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ResponseDTOInfraMoveConfigResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_infrastructure(self, body, account_identifier, **kwargs):  # noqa: E501
        """Update an Infrastructure by identifier  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_infrastructure(body, account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param InfrastructureRequest body: Details of the Infrastructure to be updated (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :return: ResponseDTOInfrastructureResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_infrastructure_with_http_info(body, account_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.update_infrastructure_with_http_info(body, account_identifier, **kwargs)  # noqa: E501
            return data

    def update_infrastructure_with_http_info(self, body, account_identifier, **kwargs):  # noqa: E501
        """Update an Infrastructure by identifier  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_infrastructure_with_http_info(body, account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param InfrastructureRequest body: Details of the Infrastructure to be updated (required)
        :param str account_identifier: Account Identifier for the Entity. (required)
        :return: ResponseDTOInfrastructureResponse
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
                    " to method update_infrastructure" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update_infrastructure`")  # noqa: E501
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `update_infrastructure`")  # noqa: E501

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
            ['application/json', 'application/yaml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/ng/api/infrastructures', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ResponseDTOInfrastructureResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_infrastructure_git_details(self, account_identifier, environment_identifier, infra_identifier, **kwargs):  # noqa: E501
        """Update git-metadata in remote infrastructure Entity  # noqa: E501

        Update git-metadata in remote infrastructure and returns the identifier of updated infrastructure  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_infrastructure_git_details(account_identifier, environment_identifier, infra_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str environment_identifier: envId (required)
        :param str infra_identifier: Infrastructure Identifier for the entity (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str connector_ref: Identifier of Connector needed for CRUD operations on the respective Entity
        :param str repo_name: Name of the repository.
        :param str file_path: File Path of the Entity.
        :return: ResponseDTOInfrastructureGitUpdateResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_infrastructure_git_details_with_http_info(account_identifier, environment_identifier, infra_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.update_infrastructure_git_details_with_http_info(account_identifier, environment_identifier, infra_identifier, **kwargs)  # noqa: E501
            return data

    def update_infrastructure_git_details_with_http_info(self, account_identifier, environment_identifier, infra_identifier, **kwargs):  # noqa: E501
        """Update git-metadata in remote infrastructure Entity  # noqa: E501

        Update git-metadata in remote infrastructure and returns the identifier of updated infrastructure  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_infrastructure_git_details_with_http_info(account_identifier, environment_identifier, infra_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str environment_identifier: envId (required)
        :param str infra_identifier: Infrastructure Identifier for the entity (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str connector_ref: Identifier of Connector needed for CRUD operations on the respective Entity
        :param str repo_name: Name of the repository.
        :param str file_path: File Path of the Entity.
        :return: ResponseDTOInfrastructureGitUpdateResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'environment_identifier', 'infra_identifier', 'org_identifier', 'project_identifier', 'connector_ref', 'repo_name', 'file_path']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_infrastructure_git_details" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `update_infrastructure_git_details`")  # noqa: E501
        # verify the required parameter 'environment_identifier' is set
        if ('environment_identifier' not in params or
                params['environment_identifier'] is None):
            raise ValueError("Missing the required parameter `environment_identifier` when calling `update_infrastructure_git_details`")  # noqa: E501
        # verify the required parameter 'infra_identifier' is set
        if ('infra_identifier' not in params or
                params['infra_identifier'] is None):
            raise ValueError("Missing the required parameter `infra_identifier` when calling `update_infrastructure_git_details`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'infra_identifier' in params:
            path_params['infraIdentifier'] = params['infra_identifier']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'environment_identifier' in params:
            query_params.append(('environmentIdentifier', params['environment_identifier']))  # noqa: E501
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
            '/ng/api/infrastructures/{infraIdentifier}/update-git-metadata', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ResponseDTOInfrastructureGitUpdateResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
