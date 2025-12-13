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


class EntitiesApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def convert_entity(self, body, option, **kwargs):  # noqa: E501
        """Convert Entity Format  # noqa: E501

        Converts entity YAML between Backstage and Harness formats. This is useful when  migrating entities between systems or when standardizing entity definitions across different platforms. The conversion preserves all semantic information while adapting to the target format conventions.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.convert_entity(body, option, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param EntityRequest body: Entity YAML definition provided as a string. The YAML should conform to either the  Harness entity format or the Backstage entity format, depending on the operation. (required)
        :param str option: Conversion direction - either convert from Backstage to Harness format or vice versa (required)
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :return: EntityConvertResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.convert_entity_with_http_info(body, option, **kwargs)  # noqa: E501
        else:
            (data) = self.convert_entity_with_http_info(body, option, **kwargs)  # noqa: E501
            return data

    def convert_entity_with_http_info(self, body, option, **kwargs):  # noqa: E501
        """Convert Entity Format  # noqa: E501

        Converts entity YAML between Backstage and Harness formats. This is useful when  migrating entities between systems or when standardizing entity definitions across different platforms. The conversion preserves all semantic information while adapting to the target format conventions.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.convert_entity_with_http_info(body, option, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param EntityRequest body: Entity YAML definition provided as a string. The YAML should conform to either the  Harness entity format or the Backstage entity format, depending on the operation. (required)
        :param str option: Conversion direction - either convert from Backstage to Harness format or vice versa (required)
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :return: EntityConvertResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'option', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method convert_entity" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `convert_entity`")  # noqa: E501
        # verify the required parameter 'option' is set
        if ('option' not in params or
                params['option'] is None):
            raise ValueError("Missing the required parameter `option` when calling `convert_entity`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'option' in params:
            path_params['option'] = params['option']  # noqa: E501

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
            ['application/json', 'application/yaml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/entities/convert/{option}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='EntityConvertResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_entity(self, body, **kwargs):  # noqa: E501
        """Create an Entity  # noqa: E501

        Creates a new Entity in the specified scope (Account, Organization, or Project).  Entities are the core components of the catalog system and can represent various  resources such as services, APIs, user groups, and more. Each entity has a specific  kind and type that defines its purpose in the system.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_entity(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param EntityCreateRequest body: Entity Create Request Body (required)
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :param str org_identifier: Unique identifier of the organization within the account
        :param str project_identifier: Unique identifier of the project within the organization
        :param bool convert: When set to true, converts Backstage style YAML to Harness entity YAML format
        :param bool dry_run: When set to true, validates the entity creation without actually creating it
        :return: EntityResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_entity_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.create_entity_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def create_entity_with_http_info(self, body, **kwargs):  # noqa: E501
        """Create an Entity  # noqa: E501

        Creates a new Entity in the specified scope (Account, Organization, or Project).  Entities are the core components of the catalog system and can represent various  resources such as services, APIs, user groups, and more. Each entity has a specific  kind and type that defines its purpose in the system.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_entity_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param EntityCreateRequest body: Entity Create Request Body (required)
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :param str org_identifier: Unique identifier of the organization within the account
        :param str project_identifier: Unique identifier of the project within the organization
        :param bool convert: When set to true, converts Backstage style YAML to Harness entity YAML format
        :param bool dry_run: When set to true, validates the entity creation without actually creating it
        :return: EntityResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account', 'org_identifier', 'project_identifier', 'convert', 'dry_run']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_entity" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_entity`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'harness_account' in params:
            query_params.append(('accountIdentifier', params['harness_account']))  # noqa: E501
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'convert' in params:
            query_params.append(('convert', params['convert']))  # noqa: E501
        if 'dry_run' in params:
            query_params.append(('dry_run', params['dry_run']))  # noqa: E501

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
            ['application/json', 'application/yaml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/entities', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='EntityResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_entity(self, scope, kind, identifier, **kwargs):  # noqa: E501
        """Delete an Entity  # noqa: E501

        Permanently removes an Entity identified by its scope, kind, and identifier from the system. This operation cannot be undone, so use it with caution. Any references to the deleted entity from other entities will become invalid.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_entity(scope, kind, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str scope: Scope of the entity (account, account.orgId, account.orgId.projectId) (required)
        :param str kind: Kind of the entity (e.g., component, api, resource, user, workflow) (required)
        :param str identifier: Unique identifier of the entity within its scope and kind (required)
        :param str org_identifier: Unique identifier of the organization within the account
        :param str project_identifier: Unique identifier of the project within the organization
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_entity_with_http_info(scope, kind, identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_entity_with_http_info(scope, kind, identifier, **kwargs)  # noqa: E501
            return data

    def delete_entity_with_http_info(self, scope, kind, identifier, **kwargs):  # noqa: E501
        """Delete an Entity  # noqa: E501

        Permanently removes an Entity identified by its scope, kind, and identifier from the system. This operation cannot be undone, so use it with caution. Any references to the deleted entity from other entities will become invalid.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_entity_with_http_info(scope, kind, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str scope: Scope of the entity (account, account.orgId, account.orgId.projectId) (required)
        :param str kind: Kind of the entity (e.g., component, api, resource, user, workflow) (required)
        :param str identifier: Unique identifier of the entity within its scope and kind (required)
        :param str org_identifier: Unique identifier of the organization within the account
        :param str project_identifier: Unique identifier of the project within the organization
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['scope', 'kind', 'identifier', 'org_identifier', 'project_identifier', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_entity" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'scope' is set
        if ('scope' not in params or
                params['scope'] is None):
            raise ValueError("Missing the required parameter `scope` when calling `delete_entity`")  # noqa: E501
        # verify the required parameter 'kind' is set
        if ('kind' not in params or
                params['kind'] is None):
            raise ValueError("Missing the required parameter `kind` when calling `delete_entity`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `delete_entity`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'scope' in params:
            path_params['scope'] = params['scope']  # noqa: E501
        if 'kind' in params:
            path_params['kind'] = params['kind']  # noqa: E501
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

        query_params = []
        # 2025-07-02
        # WARNING
        # Inconsistency in this API which will be addressed in later versions, will
        # require that the account be passed as part of the Querystring
        if 'harness_account' in params:
            query_params.append(('accountIdentifier', params['harness_account']))  # noqa: E501
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/entities/{scope}/{kind}/{identifier}', 'DELETE',
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

    def get_entities(self, **kwargs):  # noqa: E501
        """Get Entities  # noqa: E501

        Retrieves a paginated list of Entities based on the provided filters.  This endpoint supports comprehensive filtering options to help you find  specific entities across different scopes, kinds, and other properties. The response includes pagination metadata and counts for owned and favorite entities. When a search returns no matching entities, the API returns a 200 status code with an empty data array. This is the expected behavior for this list API. Note that 400 status codes are only returned when a specific entity is requested and not found (e.g., in the Get Entity Details endpoint).  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_entities(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :param int page: Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page
        :param int limit: Maximum number of items to return per page (1-100, default: 10)
        :param str sort: Parameter on the basis of which sorting is done.
        :param str search_term: This would be used to filter resources having attributes matching the search term.
        :param str scopes: Filter entities by specific scopes (account.\\*, account, account.org, account.org.project, account.orgId, account.orgId.projectId, account.orgId.\\*)
        :param str entity_refs: Filter entities by their entity references (comma-separated list in the format of kind:scope/identifier)
        :param bool owned_by_me: When true, returns only entities owned by the current user or their groups
        :param bool favorites: When true, returns only entities marked as favorites by the current user
        :param str kind: Filter entities by their kind (e.g., component, api, resource, user, workflow)
        :param str type: Filter entities by their type (e.g., Service, Website)
        :param str owner: Filter entities by their owner references
        :param str lifecycle: Filter entities by their lifecycle stage (e.g., experimental, production)
        :param str tags: Filter entities by their associated tags (comma-separated list)
        :return: list[EntityResponse]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_entities_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_entities_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_entities_with_http_info(self, **kwargs):  # noqa: E501
        """Get Entities  # noqa: E501

        Retrieves a paginated list of Entities based on the provided filters.  This endpoint supports comprehensive filtering options to help you find  specific entities across different scopes, kinds, and other properties. The response includes pagination metadata and counts for owned and favorite entities. When a search returns no matching entities, the API returns a 200 status code with an empty data array. This is the expected behavior for this list API. Note that 400 status codes are only returned when a specific entity is requested and not found (e.g., in the Get Entity Details endpoint).  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_entities_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :param int page: Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page
        :param int limit: Maximum number of items to return per page (1-100, default: 10)
        :param str sort: Parameter on the basis of which sorting is done.
        :param str search_term: This would be used to filter resources having attributes matching the search term.
        :param str scopes: Filter entities by specific scopes (account.\\*, account, account.org, account.org.project, account.orgId, account.orgId.projectId, account.orgId.\\*)
        :param str entity_refs: Filter entities by their entity references (comma-separated list in the format of kind:scope/identifier)
        :param bool owned_by_me: When true, returns only entities owned by the current user or their groups
        :param bool favorites: When true, returns only entities marked as favorites by the current user
        :param str kind: Filter entities by their kind (e.g., component, api, resource, user, workflow)
        :param str type: Filter entities by their type (e.g., Service, Website)
        :param str owner: Filter entities by their owner references
        :param str lifecycle: Filter entities by their lifecycle stage (e.g., experimental, production)
        :param str tags: Filter entities by their associated tags (comma-separated list)
        :return: list[EntityResponse]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['harness_account', 'page', 'limit', 'sort', 'search_term', 'scopes', 'entity_refs', 'owned_by_me', 'favorites', 'kind', 'type', 'owner', 'lifecycle', 'tags']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_entities" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501
        if 'search_term' in params:
            query_params.append(('search_term', params['search_term']))  # noqa: E501
        if 'scopes' in params:
            query_params.append(('scopes', params['scopes']))  # noqa: E501
        if 'entity_refs' in params:
            query_params.append(('entity_refs', params['entity_refs']))  # noqa: E501
        if 'owned_by_me' in params:
            query_params.append(('owned_by_me', params['owned_by_me']))  # noqa: E501
        if 'favorites' in params:
            query_params.append(('favorites', params['favorites']))  # noqa: E501
        if 'kind' in params:
            query_params.append(('kind', params['kind']))  # noqa: E501
        if 'type' in params:
            query_params.append(('type', params['type']))  # noqa: E501
        if 'owner' in params:
            query_params.append(('owner', params['owner']))  # noqa: E501
        if 'lifecycle' in params:
            query_params.append(('lifecycle', params['lifecycle']))  # noqa: E501
        if 'tags' in params:
            query_params.append(('tags', params['tags']))  # noqa: E501

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/yaml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/entities', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[EntityResponse]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_entities_by_refs(self, **kwargs):  # noqa: E501
        """Get entities by refs  # noqa: E501

        Fetches entities matching the entity references specified in the request body, in conjunction with other provided filters.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_entities_by_refs(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param EntitiesByRefsRequest body: Entity Refs for which entities need to be fetched
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :param int page: Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page
        :param int limit: Maximum number of items to return per page (1-100, default: 10)
        :param str sort: Parameter on the basis of which sorting is done.
        :param str search_term: This would be used to filter resources having attributes matching the search term.
        :param str scopes: Filter entities on the scopes
        :param bool owned_by_me: Filter entities owned by the user and the groups that the user is part of.
        :param bool favorites: Filter entities that are marked as favorites for the user.
        :param str kind: Filter entities by their kind (e.g., component, api, resource, user, workflow)
        :param str type: Types on which the Entities are filtered.
        :param str owner: Owners on which the Entities are filtered.
        :param str lifecycle: Lifecycles on which the Entities are filtered.
        :param str tags: Tags on which the Entities are filtered.
        :return: list[EntityResponse]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_entities_by_refs_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_entities_by_refs_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_entities_by_refs_with_http_info(self, **kwargs):  # noqa: E501
        """Get entities by refs  # noqa: E501

        Fetches entities matching the entity references specified in the request body, in conjunction with other provided filters.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_entities_by_refs_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param EntitiesByRefsRequest body: Entity Refs for which entities need to be fetched
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :param int page: Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page
        :param int limit: Maximum number of items to return per page (1-100, default: 10)
        :param str sort: Parameter on the basis of which sorting is done.
        :param str search_term: This would be used to filter resources having attributes matching the search term.
        :param str scopes: Filter entities on the scopes
        :param bool owned_by_me: Filter entities owned by the user and the groups that the user is part of.
        :param bool favorites: Filter entities that are marked as favorites for the user.
        :param str kind: Filter entities by their kind (e.g., component, api, resource, user, workflow)
        :param str type: Types on which the Entities are filtered.
        :param str owner: Owners on which the Entities are filtered.
        :param str lifecycle: Lifecycles on which the Entities are filtered.
        :param str tags: Tags on which the Entities are filtered.
        :return: list[EntityResponse]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account', 'page', 'limit', 'sort', 'search_term', 'scopes', 'owned_by_me', 'favorites', 'kind', 'type', 'owner', 'lifecycle', 'tags']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_entities_by_refs" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501
        if 'search_term' in params:
            query_params.append(('search_term', params['search_term']))  # noqa: E501
        if 'scopes' in params:
            query_params.append(('scopes', params['scopes']))  # noqa: E501
        if 'owned_by_me' in params:
            query_params.append(('owned_by_me', params['owned_by_me']))  # noqa: E501
        if 'favorites' in params:
            query_params.append(('favorites', params['favorites']))  # noqa: E501
        if 'kind' in params:
            query_params.append(('kind', params['kind']))  # noqa: E501
        if 'type' in params:
            query_params.append(('type', params['type']))  # noqa: E501
        if 'owner' in params:
            query_params.append(('owner', params['owner']))  # noqa: E501
        if 'lifecycle' in params:
            query_params.append(('lifecycle', params['lifecycle']))  # noqa: E501
        if 'tags' in params:
            query_params.append(('tags', params['tags']))  # noqa: E501

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
            ['application/json', 'application/yaml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/entities/by-refs', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[EntityResponse]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_entities_filters(self, account_identifier, **kwargs):  # noqa: E501
        """Get Entity Filter Options  # noqa: E501

        Returns the available filter options that can be used when querying entities. This helps in building dynamic filter UIs for entity exploration and discovery. The response includes filter names and their possible values based on the current entities in the system.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_entities_filters(account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Unique identifier of the account to operate on (required)
        :param str kind: Filter entities by their kind (e.g., component, api, resource, user, workflow)
        :param str scopes: Filter entities by specific scopes (account.\\*, account, account.org, account.org.project, account.orgId, account.orgId.projectId, account.orgId.\\*)
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :return: list[EntityFiltersResponse]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_entities_filters_with_http_info(account_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.get_entities_filters_with_http_info(account_identifier, **kwargs)  # noqa: E501
            return data

    def get_entities_filters_with_http_info(self, account_identifier, **kwargs):  # noqa: E501
        """Get Entity Filter Options  # noqa: E501

        Returns the available filter options that can be used when querying entities. This helps in building dynamic filter UIs for entity exploration and discovery. The response includes filter names and their possible values based on the current entities in the system.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_entities_filters_with_http_info(account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Unique identifier of the account to operate on (required)
        :param str kind: Filter entities by their kind (e.g., component, api, resource, user, workflow)
        :param str scopes: Filter entities by specific scopes (account.\\*, account, account.org, account.org.project, account.orgId, account.orgId.projectId, account.orgId.\\*)
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :return: list[EntityFiltersResponse]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'kind', 'scopes', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_entities_filters" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `get_entities_filters`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        # 2025-08-27
        # WARNING
        # Inconsistency in this API which will be addressed in later versions, will
        # require that the account be passed as part of the Querystring
        if 'harness_account' in params:
            query_params.append(('accountIdentifier', params['harness_account']))  # noqa: E501
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'kind' in params:
            query_params.append(('kind', params['kind']))  # noqa: E501
        if 'scopes' in params:
            query_params.append(('scopes', params['scopes']))  # noqa: E501

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/yaml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/entities/filters', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[EntityFiltersResponse]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_entities_filters_by_query(self, account_identifier, **kwargs):  # noqa: E501
        """Get Entities Filters By Query  # noqa: E501

        Returns the available filter options that can be used when querying entities  based on the provided query.This helps in building dynamic filter UIs for entity  exploration and discovery.The response includes filter names and their possible  values based on the current entities in the system.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_entities_filters_by_query(account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Unique identifier of the account to operate on (required)
        :param EntityFilterQueryRequest body: Query for getting the filters for entities
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :param str kind: Filter entities by their kind (e.g., component, api, resource, user, workflow)
        :param str scopes: Filter entities by specific scopes (account.\\*, account, account.org, account.org.project, account.orgId, account.orgId.projectId, account.orgId.\\*)
        :return: list[EntityFiltersResponse]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_entities_filters_by_query_with_http_info(account_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.get_entities_filters_by_query_with_http_info(account_identifier, **kwargs)  # noqa: E501
            return data

    def get_entities_filters_by_query_with_http_info(self, account_identifier, **kwargs):  # noqa: E501
        """Get Entities Filters By Query  # noqa: E501

        Returns the available filter options that can be used when querying entities  based on the provided query.This helps in building dynamic filter UIs for entity  exploration and discovery.The response includes filter names and their possible  values based on the current entities in the system.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_entities_filters_by_query_with_http_info(account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Unique identifier of the account to operate on (required)
        :param EntityFilterQueryRequest body: Query for getting the filters for entities
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :param str kind: Filter entities by their kind (e.g., component, api, resource, user, workflow)
        :param str scopes: Filter entities by specific scopes (account.\\*, account, account.org, account.org.project, account.orgId, account.orgId.projectId, account.orgId.\\*)
        :return: list[EntityFiltersResponse]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'body', 'harness_account', 'kind', 'scopes']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_entities_filters_by_query" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `get_entities_filters_by_query`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        # 2025-08-27
        # WARNING
        # Inconsistency in this API which will be addressed in later versions, will
        # require that the account be passed as part of the Querystring
        if 'harness_account' in params:
            query_params.append(('accountIdentifier', params['harness_account']))  # noqa: E501
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'kind' in params:
            query_params.append(('kind', params['kind']))  # noqa: E501
        if 'scopes' in params:
            query_params.append(('scopes', params['scopes']))  # noqa: E501

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
            ['application/json', 'application/yaml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/entities/filters', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[EntityFiltersResponse]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_entities_groups(self, **kwargs):  # noqa: E501
        """Get Entities Groups  # noqa: E501

        Retrieves entities organized in hierarchical groups based on account, organization,  and project. This endpoint is useful for displaying entities in a structured UI view where entities need to be presented in their organizational context. The response contains both grouped and ungrouped entities at each level.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_entities_groups(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :param str search_on_entities: Filter entities by a search term across entity attributes
        :param str search_on_groups: Filter groups by a search term across group attributes
        :param str scopes: Filter entities by specific scopes (account.\\*, account, account.org, account.org.project, account.orgId, account.orgId.projectId, account.orgId.\\*)
        :param str kind: Filter entities by their kind (e.g., component, api, resource, user, workflow)
        :param bool owned_by_me: When true, returns only entities owned by the current user and their groups
        :param bool favorites: When true, returns only entities marked as favorites by the current user
        :param str type: Filter entities by their type
        :param str owner: Filter entities by their owner references
        :param str lifecycle: Filter entities by their lifecycle stage
        :param str tags: Filter entities by their associated tags
        :return: EntitiesGroupsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_entities_groups_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_entities_groups_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_entities_groups_with_http_info(self, **kwargs):  # noqa: E501
        """Get Entities Groups  # noqa: E501

        Retrieves entities organized in hierarchical groups based on account, organization,  and project. This endpoint is useful for displaying entities in a structured UI view where entities need to be presented in their organizational context. The response contains both grouped and ungrouped entities at each level.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_entities_groups_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :param str search_on_entities: Filter entities by a search term across entity attributes
        :param str search_on_groups: Filter groups by a search term across group attributes
        :param str scopes: Filter entities by specific scopes (account.\\*, account, account.org, account.org.project, account.orgId, account.orgId.projectId, account.orgId.\\*)
        :param str kind: Filter entities by their kind (e.g., component, api, resource, user, workflow)
        :param bool owned_by_me: When true, returns only entities owned by the current user and their groups
        :param bool favorites: When true, returns only entities marked as favorites by the current user
        :param str type: Filter entities by their type
        :param str owner: Filter entities by their owner references
        :param str lifecycle: Filter entities by their lifecycle stage
        :param str tags: Filter entities by their associated tags
        :return: EntitiesGroupsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['harness_account', 'search_on_entities', 'search_on_groups', 'scopes', 'kind', 'owned_by_me', 'favorites', 'type', 'owner', 'lifecycle', 'tags']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_entities_groups" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'search_on_entities' in params:
            query_params.append(('search_on_entities', params['search_on_entities']))  # noqa: E501
        if 'search_on_groups' in params:
            query_params.append(('search_on_groups', params['search_on_groups']))  # noqa: E501
        if 'scopes' in params:
            query_params.append(('scopes', params['scopes']))  # noqa: E501
        if 'kind' in params:
            query_params.append(('kind', params['kind']))  # noqa: E501
        if 'owned_by_me' in params:
            query_params.append(('owned_by_me', params['owned_by_me']))  # noqa: E501
        if 'favorites' in params:
            query_params.append(('favorites', params['favorites']))  # noqa: E501
        if 'type' in params:
            query_params.append(('type', params['type']))  # noqa: E501
        if 'owner' in params:
            query_params.append(('owner', params['owner']))  # noqa: E501
        if 'lifecycle' in params:
            query_params.append(('lifecycle', params['lifecycle']))  # noqa: E501
        if 'tags' in params:
            query_params.append(('tags', params['tags']))  # noqa: E501

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/yaml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/entities/groups', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='EntitiesGroupsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_entities_kinds(self, account_identifier, **kwargs):  # noqa: E501
        """Get Entity Kinds  # noqa: E501

        Returns a list of all supported Entity Kinds along with their display names,  descriptions, and counts. This is useful for populating filter dropdowns in UIs and for understanding what kinds of entities are available in the system.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_entities_kinds(account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Unique identifier of the account to operate on (required)
        :param str org_identifier: Unique identifier of the organization within the account
        :param str project_identifier: Unique identifier of the project within the organization
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :return: list[EntityKindsResponse]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_entities_kinds_with_http_info(account_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.get_entities_kinds_with_http_info(account_identifier, **kwargs)  # noqa: E501
            return data

    def get_entities_kinds_with_http_info(self, account_identifier, **kwargs):  # noqa: E501
        """Get Entity Kinds  # noqa: E501

        Returns a list of all supported Entity Kinds along with their display names,  descriptions, and counts. This is useful for populating filter dropdowns in UIs and for understanding what kinds of entities are available in the system.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_entities_kinds_with_http_info(account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Unique identifier of the account to operate on (required)
        :param str org_identifier: Unique identifier of the organization within the account
        :param str project_identifier: Unique identifier of the project within the organization
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :return: list[EntityKindsResponse]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'org_identifier', 'project_identifier', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_entities_kinds" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `get_entities_kinds`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        # 2025-08-27
        # WARNING
        # Inconsistency in this API which will be addressed in later versions, will
        # require that the account be passed as part of the Querystring
        if 'harness_account' in params:
            query_params.append(('accountIdentifier', params['harness_account']))  # noqa: E501
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/yaml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/entities/kinds', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[EntityKindsResponse]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_entity(self, scope, kind, identifier, **kwargs):  # noqa: E501
        """Get Entity Details  # noqa: E501

        Retrieves the complete details of an Entity identified by its scope, kind, and identifier, including its YAML definition, metadata, and relationships with other entities. This endpoint provides the most comprehensive view of a specific entity.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_entity(scope, kind, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str scope: Scope of the entity (account, account.orgId, account.orgId.projectId) (required)
        :param str kind: Kind of the entity (e.g., component, api, resource, user, workflow) (required)
        :param str identifier: Unique identifier of the entity within its scope and kind (required)
        :param str org_identifier: Unique identifier of the organization within the account
        :param str project_identifier: Unique identifier of the project within the organization
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :param str branch_name: Name of the branch (for Git Experience).
        :param str connector_ref: Identifier of the Harness Connector used for CRUD operations on the Entity (for Git Experience).
        :param str repo_name: Name of the repository (for Git Experience).
        :param str load_from_cache: Flag to enable loading the remote entity from git or git cache
        :param bool load_from_fallback_branch: Flag to load the entity from the created non default branch
        :return: EntityResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_entity_with_http_info(scope, kind, identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.get_entity_with_http_info(scope, kind, identifier, **kwargs)  # noqa: E501
            return data

    def get_entity_with_http_info(self, scope, kind, identifier, **kwargs):  # noqa: E501
        """Get Entity Details  # noqa: E501

        Retrieves the complete details of an Entity identified by its scope, kind, and identifier, including its YAML definition, metadata, and relationships with other entities. This endpoint provides the most comprehensive view of a specific entity.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_entity_with_http_info(scope, kind, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str scope: Scope of the entity (account, account.orgId, account.orgId.projectId) (required)
        :param str kind: Kind of the entity (e.g., component, api, resource, user, workflow) (required)
        :param str identifier: Unique identifier of the entity within its scope and kind (required)
        :param str org_identifier: Unique identifier of the organization within the account
        :param str project_identifier: Unique identifier of the project within the organization
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :param str branch_name: Name of the branch (for Git Experience).
        :param str connector_ref: Identifier of the Harness Connector used for CRUD operations on the Entity (for Git Experience).
        :param str repo_name: Name of the repository (for Git Experience).
        :param str load_from_cache: Flag to enable loading the remote entity from git or git cache
        :param bool load_from_fallback_branch: Flag to load the entity from the created non default branch
        :return: EntityResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['scope', 'kind', 'identifier', 'org_identifier', 'project_identifier', 'harness_account', 'branch_name', 'connector_ref', 'repo_name', 'load_from_cache', 'load_from_fallback_branch']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_entity" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'scope' is set
        if ('scope' not in params or
                params['scope'] is None):
            raise ValueError("Missing the required parameter `scope` when calling `get_entity`")  # noqa: E501
        # verify the required parameter 'kind' is set
        if ('kind' not in params or
                params['kind'] is None):
            raise ValueError("Missing the required parameter `kind` when calling `get_entity`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `get_entity`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'scope' in params:
            path_params['scope'] = params['scope']  # noqa: E501
        if 'kind' in params:
            path_params['kind'] = params['kind']  # noqa: E501
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

        query_params = []
        # 2025-08-27
        # WARNING
        # Inconsistency in this API which will be addressed in later versions, will
        # require that the account be passed as part of the Querystring
        if 'harness_account' in params:
            query_params.append(('accountIdentifier', params['harness_account']))  # noqa: E501
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'branch_name' in params:
            query_params.append(('branch_name', params['branch_name']))  # noqa: E501
        if 'connector_ref' in params:
            query_params.append(('connector_ref', params['connector_ref']))  # noqa: E501
        if 'repo_name' in params:
            query_params.append(('repo_name', params['repo_name']))  # noqa: E501
        if 'load_from_fallback_branch' in params:
            query_params.append(('load_from_fallback_branch', params['load_from_fallback_branch']))  # noqa: E501

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501
        if 'load_from_cache' in params:
            header_params['Load-From-Cache'] = params['load_from_cache']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/yaml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/entities/{scope}/{kind}/{identifier}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='EntityResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_json_schema(self, **kwargs):  # noqa: E501
        """Get Entity JSON Schema  # noqa: E501

        Returns the JSON Schema for validating Entity definitions. This is useful for client-side validation before submitting entity creation or update requests. The schema can be filtered by entity kind to get specific validation rules.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_json_schema(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str kind: Filter entities by their kind (e.g., component, api, resource, user, workflow)
        :return: EntityJsonSchemaResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_json_schema_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_json_schema_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_json_schema_with_http_info(self, **kwargs):  # noqa: E501
        """Get Entity JSON Schema  # noqa: E501

        Returns the JSON Schema for validating Entity definitions. This is useful for client-side validation before submitting entity creation or update requests. The schema can be filtered by entity kind to get specific validation rules.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_json_schema_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str kind: Filter entities by their kind (e.g., component, api, resource, user, workflow)
        :return: EntityJsonSchemaResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['kind']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_json_schema" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'kind' in params:
            query_params.append(('kind', params['kind']))  # noqa: E501

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
            '/v1/entities/json-schema', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='EntityJsonSchemaResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def import_entity(self, body, **kwargs):  # noqa: E501
        """Import an Entity from Git  # noqa: E501

        Imports a new Entity from Git in the specified scope (Account, Organization, or Project).  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.import_entity(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param GitImportDetails1 body: Git Import Request Body (required)
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :param str org_identifier: Unique identifier of the organization within the account
        :param str project_identifier: Unique identifier of the project within the organization
        :return: EntityResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.import_entity_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.import_entity_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def import_entity_with_http_info(self, body, **kwargs):  # noqa: E501
        """Import an Entity from Git  # noqa: E501

        Imports a new Entity from Git in the specified scope (Account, Organization, or Project).  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.import_entity_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param GitImportDetails1 body: Git Import Request Body (required)
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :param str org_identifier: Unique identifier of the organization within the account
        :param str project_identifier: Unique identifier of the project within the organization
        :return: EntityResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method import_entity" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `import_entity`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        # 2025-08-27
        # WARNING
        # Inconsistency in this API which will be addressed in later versions, will
        # require that the account be passed as part of the Querystring
        if 'harness_account' in params:
            query_params.append(('accountIdentifier', params['harness_account']))  # noqa: E501
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501

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
            ['application/json', 'application/yaml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/entities/import', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='EntityResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def move_entity(self, body, scope, kind, identifier, **kwargs):  # noqa: E501
        """Move an Entity  # noqa: E501

        Move an existing Inline entity to Remote.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.move_entity(body, scope, kind, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param EntityMoveRequest body: Entity Move Request Body (required)
        :param str scope: Scope of the entity (account, account.orgId, account.orgId.projectId) (required)
        :param str kind: Kind of the entity (e.g., component, api, resource, user, workflow) (required)
        :param str identifier: Unique identifier of the entity within its scope and kind (required)
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :param str org_identifier: Unique identifier of the organization within the account
        :param str project_identifier: Unique identifier of the project within the organization
        :return: DefaultSaveResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.move_entity_with_http_info(body, scope, kind, identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.move_entity_with_http_info(body, scope, kind, identifier, **kwargs)  # noqa: E501
            return data

    def move_entity_with_http_info(self, body, scope, kind, identifier, **kwargs):  # noqa: E501
        """Move an Entity  # noqa: E501

        Move an existing Inline entity to Remote.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.move_entity_with_http_info(body, scope, kind, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param EntityMoveRequest body: Entity Move Request Body (required)
        :param str scope: Scope of the entity (account, account.orgId, account.orgId.projectId) (required)
        :param str kind: Kind of the entity (e.g., component, api, resource, user, workflow) (required)
        :param str identifier: Unique identifier of the entity within its scope and kind (required)
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :param str org_identifier: Unique identifier of the organization within the account
        :param str project_identifier: Unique identifier of the project within the organization
        :return: DefaultSaveResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'scope', 'kind', 'identifier', 'harness_account', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method move_entity" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `move_entity`")  # noqa: E501
        # verify the required parameter 'scope' is set
        if ('scope' not in params or
                params['scope'] is None):
            raise ValueError("Missing the required parameter `scope` when calling `move_entity`")  # noqa: E501
        # verify the required parameter 'kind' is set
        if ('kind' not in params or
                params['kind'] is None):
            raise ValueError("Missing the required parameter `kind` when calling `move_entity`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `move_entity`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'scope' in params:
            path_params['scope'] = params['scope']  # noqa: E501
        if 'kind' in params:
            path_params['kind'] = params['kind']  # noqa: E501
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

        query_params = []
        # 2025-08-27
        # WARNING
        # Inconsistency in this API which will be addressed in later versions, will
        # require that the account be passed as part of the Querystring
        if 'harness_account' in params:
            query_params.append(('accountIdentifier', params['harness_account']))  # noqa: E501
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501

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
            ['application/json', 'application/yaml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/entities/move/{scope}/{kind}/{identifier}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DefaultSaveResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_entity(self, body, scope, kind, identifier, **kwargs):  # noqa: E501
        """Update an Entity  # noqa: E501

        Updates an existing Entity identified by its scope, kind, and identifier. All fields in the entity definition will be replaced with the new values provided in the request. This operation is idempotent and will create the entity if it doesn't already exist.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_entity(body, scope, kind, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param EntityUpdateRequest body: Entity Update Request Body (required)
        :param str scope: Scope of the entity (account, account.orgId, account.orgId.projectId) (required)
        :param str kind: Kind of the entity (e.g., component, api, resource, user, workflow) (required)
        :param str identifier: Unique identifier of the entity within its scope and kind (required)
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :param str org_identifier: Unique identifier of the organization within the account
        :param str project_identifier: Unique identifier of the project within the organization
        :return: EntityResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_entity_with_http_info(body, scope, kind, identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.update_entity_with_http_info(body, scope, kind, identifier, **kwargs)  # noqa: E501
            return data

    def update_entity_with_http_info(self, body, scope, kind, identifier, **kwargs):  # noqa: E501
        """Update an Entity  # noqa: E501

        Updates an existing Entity identified by its scope, kind, and identifier. All fields in the entity definition will be replaced with the new values provided in the request. This operation is idempotent and will create the entity if it doesn't already exist.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_entity_with_http_info(body, scope, kind, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param EntityUpdateRequest body: Entity Update Request Body (required)
        :param str scope: Scope of the entity (account, account.orgId, account.orgId.projectId) (required)
        :param str kind: Kind of the entity (e.g., component, api, resource, user, workflow) (required)
        :param str identifier: Unique identifier of the entity within its scope and kind (required)
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :param str org_identifier: Unique identifier of the organization within the account
        :param str project_identifier: Unique identifier of the project within the organization
        :return: EntityResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'scope', 'kind', 'identifier', 'harness_account', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_entity" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update_entity`")  # noqa: E501
        # verify the required parameter 'scope' is set
        if ('scope' not in params or
                params['scope'] is None):
            raise ValueError("Missing the required parameter `scope` when calling `update_entity`")  # noqa: E501
        # verify the required parameter 'kind' is set
        if ('kind' not in params or
                params['kind'] is None):
            raise ValueError("Missing the required parameter `kind` when calling `update_entity`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `update_entity`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'scope' in params:
            path_params['scope'] = params['scope']  # noqa: E501
        if 'kind' in params:
            path_params['kind'] = params['kind']  # noqa: E501
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

        query_params = []
        # 2025-08-27
        # WARNING
        # Inconsistency in this API which will be addressed in later versions, will
        # require that the account be passed as part of the Querystring
        if 'harness_account' in params:
            query_params.append(('accountIdentifier', params['harness_account']))  # noqa: E501
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501

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
            ['application/json', 'application/yaml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/entities/{scope}/{kind}/{identifier}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='EntityResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_git_metadata(self, body, scope, kind, identifier, **kwargs):  # noqa: E501
        """Update GitMetadata for Remote Entities  # noqa: E501

        Update GitMetadata for Remote Entities  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_git_metadata(body, scope, kind, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param GitMetadataUpdateRequest body: (required)
        :param str scope: Scope of the entity (account, account.orgId, account.orgId.projectId) (required)
        :param str kind: Kind of the entity (e.g., component, api, resource, user, workflow) (required)
        :param str identifier: Unique identifier of the entity within its scope and kind (required)
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :param str org_identifier: Unique identifier of the organization within the account
        :param str project_identifier: Unique identifier of the project within the organization
        :return: DefaultSaveResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_git_metadata_with_http_info(body, scope, kind, identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.update_git_metadata_with_http_info(body, scope, kind, identifier, **kwargs)  # noqa: E501
            return data

    def update_git_metadata_with_http_info(self, body, scope, kind, identifier, **kwargs):  # noqa: E501
        """Update GitMetadata for Remote Entities  # noqa: E501

        Update GitMetadata for Remote Entities  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_git_metadata_with_http_info(body, scope, kind, identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param GitMetadataUpdateRequest body: (required)
        :param str scope: Scope of the entity (account, account.orgId, account.orgId.projectId) (required)
        :param str kind: Kind of the entity (e.g., component, api, resource, user, workflow) (required)
        :param str identifier: Unique identifier of the entity within its scope and kind (required)
        :param str harness_account: Identifier field of the account the resource is scoped to.
        :param str org_identifier: Unique identifier of the organization within the account
        :param str project_identifier: Unique identifier of the project within the organization
        :return: DefaultSaveResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'scope', 'kind', 'identifier', 'harness_account', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_git_metadata" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update_git_metadata`")  # noqa: E501
        # verify the required parameter 'scope' is set
        if ('scope' not in params or
                params['scope'] is None):
            raise ValueError("Missing the required parameter `scope` when calling `update_git_metadata`")  # noqa: E501
        # verify the required parameter 'kind' is set
        if ('kind' not in params or
                params['kind'] is None):
            raise ValueError("Missing the required parameter `kind` when calling `update_git_metadata`")  # noqa: E501
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `update_git_metadata`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'scope' in params:
            path_params['scope'] = params['scope']  # noqa: E501
        if 'kind' in params:
            path_params['kind'] = params['kind']  # noqa: E501
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

        query_params = []
        # 2025-08-27
        # WARNING
        # Inconsistency in this API which will be addressed in later versions, will
        # require that the account be passed as part of the Querystring
        if 'harness_account' in params:
            query_params.append(('accountIdentifier', params['harness_account']))  # noqa: E501
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501

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
            ['application/json', 'application/yaml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/entities/git-metadata/{scope}/{kind}/{identifier}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DefaultSaveResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
