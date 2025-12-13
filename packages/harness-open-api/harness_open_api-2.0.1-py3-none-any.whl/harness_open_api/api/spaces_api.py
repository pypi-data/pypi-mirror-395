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


class SpacesApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_all_harness_artifacts(self, space_ref, **kwargs):  # noqa: E501
        """List Harness Artifacts  # noqa: E501

        Lists all the Harness Artifacts.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_harness_artifacts(space_ref, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/+` - **Organization-level**: `account_id/org/+` - **Project-level**: `account_id/org/project/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param list[str] reg_identifier: Registry Identifier
        :param int page: Current page number
        :param int size: Number of items per page
        :param str sort_order: sortOrder
        :param str sort_field: sortField
        :param str search_term: search Term.
        :param bool latest_version: Latest Version Filter.
        :param bool deployed_artifact: Deployed Artifact Filter.
        :param list[str] package_type: Registry Package Type
        :return: InlineResponse20037
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_all_harness_artifacts_with_http_info(space_ref, **kwargs)  # noqa: E501
        else:
            (data) = self.get_all_harness_artifacts_with_http_info(space_ref, **kwargs)  # noqa: E501
            return data

    def get_all_harness_artifacts_with_http_info(self, space_ref, **kwargs):  # noqa: E501
        """List Harness Artifacts  # noqa: E501

        Lists all the Harness Artifacts.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_harness_artifacts_with_http_info(space_ref, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/+` - **Organization-level**: `account_id/org/+` - **Project-level**: `account_id/org/project/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param list[str] reg_identifier: Registry Identifier
        :param int page: Current page number
        :param int size: Number of items per page
        :param str sort_order: sortOrder
        :param str sort_field: sortField
        :param str search_term: search Term.
        :param bool latest_version: Latest Version Filter.
        :param bool deployed_artifact: Deployed Artifact Filter.
        :param list[str] package_type: Registry Package Type
        :return: InlineResponse20037
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['space_ref', 'reg_identifier', 'page', 'size', 'sort_order', 'sort_field', 'search_term', 'latest_version', 'deployed_artifact', 'package_type']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_all_harness_artifacts" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'space_ref' is set
        if ('space_ref' not in params or
                params['space_ref'] is None):
            raise ValueError("Missing the required parameter `space_ref` when calling `get_all_harness_artifacts`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'space_ref' in params:
            path_params['space_ref'] = params['space_ref']  # noqa: E501

        query_params = []
        if 'reg_identifier' in params:
            query_params.append(('reg_identifier', params['reg_identifier']))  # noqa: E501
            collection_formats['reg_identifier'] = 'multi'  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'size' in params:
            query_params.append(('size', params['size']))  # noqa: E501
        if 'sort_order' in params:
            query_params.append(('sort_order', params['sort_order']))  # noqa: E501
        if 'sort_field' in params:
            query_params.append(('sort_field', params['sort_field']))  # noqa: E501
        if 'search_term' in params:
            query_params.append(('search_term', params['search_term']))  # noqa: E501
        if 'latest_version' in params:
            query_params.append(('latest_version', params['latest_version']))  # noqa: E501
        if 'deployed_artifact' in params:
            query_params.append(('deployed_artifact', params['deployed_artifact']))  # noqa: E501
        if 'package_type' in params:
            query_params.append(('package_type', params['package_type']))  # noqa: E501
            collection_formats['package_type'] = 'multi'  # noqa: E501

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
            '/har/api/v1/spaces/{space_ref}/artifacts', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20037',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_all_registries(self, space_ref, **kwargs):  # noqa: E501
        """List registries  # noqa: E501

        Lists all the registries.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_registries(space_ref, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/+` - **Organization-level**: `account_id/org/+` - **Project-level**: `account_id/org/project/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param list[str] package_type: Registry Package Type
        :param str type: Registry Type
        :param int page: Current page number
        :param int size: Number of items per page
        :param str sort_order: sortOrder
        :param str sort_field: sortField
        :param str search_term: search Term.
        :param bool recursive: Whether to list registries recursively.  **Deprecated.** Use the new `scope` parameter.  * `recursive=true`  → `scope=ancestors` * `recursive=false` → `scope=none` 
        :param str scope: **Scope of registries to list** * **none** – current space only (default)   * **ancestors** – current space **plus** all parent spaces   * **descendants** – current space **plus** all child spaces   If omitted, `none` is assumed. 
        :return: InlineResponse20039
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_all_registries_with_http_info(space_ref, **kwargs)  # noqa: E501
        else:
            (data) = self.get_all_registries_with_http_info(space_ref, **kwargs)  # noqa: E501
            return data

    def get_all_registries_with_http_info(self, space_ref, **kwargs):  # noqa: E501
        """List registries  # noqa: E501

        Lists all the registries.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_registries_with_http_info(space_ref, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/+` - **Organization-level**: `account_id/org/+` - **Project-level**: `account_id/org/project/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param list[str] package_type: Registry Package Type
        :param str type: Registry Type
        :param int page: Current page number
        :param int size: Number of items per page
        :param str sort_order: sortOrder
        :param str sort_field: sortField
        :param str search_term: search Term.
        :param bool recursive: Whether to list registries recursively.  **Deprecated.** Use the new `scope` parameter.  * `recursive=true`  → `scope=ancestors` * `recursive=false` → `scope=none` 
        :param str scope: **Scope of registries to list** * **none** – current space only (default)   * **ancestors** – current space **plus** all parent spaces   * **descendants** – current space **plus** all child spaces   If omitted, `none` is assumed. 
        :return: InlineResponse20039
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['space_ref', 'package_type', 'type', 'page', 'size', 'sort_order', 'sort_field', 'search_term', 'recursive', 'scope']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_all_registries" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'space_ref' is set
        if ('space_ref' not in params or
                params['space_ref'] is None):
            raise ValueError("Missing the required parameter `space_ref` when calling `get_all_registries`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'space_ref' in params:
            path_params['space_ref'] = params['space_ref']  # noqa: E501

        query_params = []
        if 'package_type' in params:
            query_params.append(('package_type', params['package_type']))  # noqa: E501
            collection_formats['package_type'] = 'multi'  # noqa: E501
        if 'type' in params:
            query_params.append(('type', params['type']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'size' in params:
            query_params.append(('size', params['size']))  # noqa: E501
        if 'sort_order' in params:
            query_params.append(('sort_order', params['sort_order']))  # noqa: E501
        if 'sort_field' in params:
            query_params.append(('sort_field', params['sort_field']))  # noqa: E501
        if 'search_term' in params:
            query_params.append(('search_term', params['search_term']))  # noqa: E501
        if 'recursive' in params:
            query_params.append(('recursive', params['recursive']))  # noqa: E501
        if 'scope' in params:
            query_params.append(('scope', params['scope']))  # noqa: E501

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
            '/har/api/v1/spaces/{space_ref}/registries', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20039',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_artifact_stats_for_space(self, space_ref, **kwargs):  # noqa: E501
        """Get artifact stats  # noqa: E501

        Get artifact stats  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_artifact_stats_for_space(space_ref, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/+` - **Organization-level**: `account_id/org/+` - **Project-level**: `account_id/org/project/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str _from: Date. Format - MM/DD/YYYY
        :param str to: Date. Format - MM/DD/YYYY
        :return: InlineResponse20012
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_artifact_stats_for_space_with_http_info(space_ref, **kwargs)  # noqa: E501
        else:
            (data) = self.get_artifact_stats_for_space_with_http_info(space_ref, **kwargs)  # noqa: E501
            return data

    def get_artifact_stats_for_space_with_http_info(self, space_ref, **kwargs):  # noqa: E501
        """Get artifact stats  # noqa: E501

        Get artifact stats  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_artifact_stats_for_space_with_http_info(space_ref, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/+` - **Organization-level**: `account_id/org/+` - **Project-level**: `account_id/org/project/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str _from: Date. Format - MM/DD/YYYY
        :param str to: Date. Format - MM/DD/YYYY
        :return: InlineResponse20012
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['space_ref', '_from', 'to']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_artifact_stats_for_space" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'space_ref' is set
        if ('space_ref' not in params or
                params['space_ref'] is None):
            raise ValueError("Missing the required parameter `space_ref` when calling `get_artifact_stats_for_space`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'space_ref' in params:
            path_params['space_ref'] = params['space_ref']  # noqa: E501

        query_params = []
        if '_from' in params:
            query_params.append(('from', params['_from']))  # noqa: E501
        if 'to' in params:
            query_params.append(('to', params['to']))  # noqa: E501

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
            '/har/api/v1/spaces/{space_ref}/artifact/stats', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20012',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_storage_details(self, space_ref, **kwargs):  # noqa: E501
        """Get storage details for given space  # noqa: E501

        Get storage details for given space  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_storage_details(space_ref, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/+` - **Organization-level**: `account_id/org/+` - **Project-level**: `account_id/org/project/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :return: InlineResponse20038
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_storage_details_with_http_info(space_ref, **kwargs)  # noqa: E501
        else:
            (data) = self.get_storage_details_with_http_info(space_ref, **kwargs)  # noqa: E501
            return data

    def get_storage_details_with_http_info(self, space_ref, **kwargs):  # noqa: E501
        """Get storage details for given space  # noqa: E501

        Get storage details for given space  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_storage_details_with_http_info(space_ref, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str space_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/+` - **Organization-level**: `account_id/org/+` - **Project-level**: `account_id/org/project/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :return: InlineResponse20038
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['space_ref']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_storage_details" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'space_ref' is set
        if ('space_ref' not in params or
                params['space_ref'] is None):
            raise ValueError("Missing the required parameter `space_ref` when calling `get_storage_details`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'space_ref' in params:
            path_params['space_ref'] = params['space_ref']  # noqa: E501

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
            '/har/api/v1/spaces/{space_ref}/details', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20038',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
