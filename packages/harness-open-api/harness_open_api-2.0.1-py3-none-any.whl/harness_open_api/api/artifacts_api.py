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


class ArtifactsApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def delete_artifact(self, registry_ref, artifact, **kwargs):  # noqa: E501
        """Delete Artifact  # noqa: E501

        Delete Artifact.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_artifact(registry_ref, artifact, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param str artifact_type: artifact type.
        :return: InlineResponse20010
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_artifact_with_http_info(registry_ref, artifact, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_artifact_with_http_info(registry_ref, artifact, **kwargs)  # noqa: E501
            return data

    def delete_artifact_with_http_info(self, registry_ref, artifact, **kwargs):  # noqa: E501
        """Delete Artifact  # noqa: E501

        Delete Artifact.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_artifact_with_http_info(registry_ref, artifact, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param str artifact_type: artifact type.
        :return: InlineResponse20010
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['registry_ref', 'artifact', 'artifact_type']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_artifact" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'registry_ref' is set
        if ('registry_ref' not in params or
                params['registry_ref'] is None):
            raise ValueError("Missing the required parameter `registry_ref` when calling `delete_artifact`")  # noqa: E501
        # verify the required parameter 'artifact' is set
        if ('artifact' not in params or
                params['artifact'] is None):
            raise ValueError("Missing the required parameter `artifact` when calling `delete_artifact`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'registry_ref' in params:
            path_params['registry_ref'] = params['registry_ref']  # noqa: E501
        if 'artifact' in params:
            path_params['artifact'] = params['artifact']  # noqa: E501

        query_params = []
        if 'artifact_type' in params:
            query_params.append(('artifact_type', params['artifact_type']))  # noqa: E501

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
            '/har/api/v1/registry/{registry_ref}/artifact/{artifact}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20010',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_artifact_version(self, registry_ref, artifact, version, **kwargs):  # noqa: E501
        """Delete an Artifact Version  # noqa: E501

        Delete Artifact Version.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_artifact_version(registry_ref, artifact, version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param str version: Name of Artifact Version. (required)
        :param str artifact_type: artifact type.
        :return: InlineResponse20010
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_artifact_version_with_http_info(registry_ref, artifact, version, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_artifact_version_with_http_info(registry_ref, artifact, version, **kwargs)  # noqa: E501
            return data

    def delete_artifact_version_with_http_info(self, registry_ref, artifact, version, **kwargs):  # noqa: E501
        """Delete an Artifact Version  # noqa: E501

        Delete Artifact Version.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_artifact_version_with_http_info(registry_ref, artifact, version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param str version: Name of Artifact Version. (required)
        :param str artifact_type: artifact type.
        :return: InlineResponse20010
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['registry_ref', 'artifact', 'version', 'artifact_type']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_artifact_version" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'registry_ref' is set
        if ('registry_ref' not in params or
                params['registry_ref'] is None):
            raise ValueError("Missing the required parameter `registry_ref` when calling `delete_artifact_version`")  # noqa: E501
        # verify the required parameter 'artifact' is set
        if ('artifact' not in params or
                params['artifact'] is None):
            raise ValueError("Missing the required parameter `artifact` when calling `delete_artifact_version`")  # noqa: E501
        # verify the required parameter 'version' is set
        if ('version' not in params or
                params['version'] is None):
            raise ValueError("Missing the required parameter `version` when calling `delete_artifact_version`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'registry_ref' in params:
            path_params['registry_ref'] = params['registry_ref']  # noqa: E501
        if 'artifact' in params:
            path_params['artifact'] = params['artifact']  # noqa: E501
        if 'version' in params:
            path_params['version'] = params['version']  # noqa: E501

        query_params = []
        if 'artifact_type' in params:
            query_params.append(('artifact_type', params['artifact_type']))  # noqa: E501

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
            '/har/api/v1/registry/{registry_ref}/artifact/{artifact}/version/{version}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20010',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_all_artifact_versions(self, registry_ref, artifact, **kwargs):  # noqa: E501
        """List Artifact Versions  # noqa: E501

        Lists all the Artifact Versions.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_artifact_versions(registry_ref, artifact, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param str artifact_type: artifact type.
        :param int page: Current page number
        :param int size: Number of items per page
        :param str sort_order: sortOrder
        :param str sort_field: sortField
        :param str search_term: search Term.
        :return: InlineResponse20027
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_all_artifact_versions_with_http_info(registry_ref, artifact, **kwargs)  # noqa: E501
        else:
            (data) = self.get_all_artifact_versions_with_http_info(registry_ref, artifact, **kwargs)  # noqa: E501
            return data

    def get_all_artifact_versions_with_http_info(self, registry_ref, artifact, **kwargs):  # noqa: E501
        """List Artifact Versions  # noqa: E501

        Lists all the Artifact Versions.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_artifact_versions_with_http_info(registry_ref, artifact, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param str artifact_type: artifact type.
        :param int page: Current page number
        :param int size: Number of items per page
        :param str sort_order: sortOrder
        :param str sort_field: sortField
        :param str search_term: search Term.
        :return: InlineResponse20027
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['registry_ref', 'artifact', 'artifact_type', 'page', 'size', 'sort_order', 'sort_field', 'search_term']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_all_artifact_versions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'registry_ref' is set
        if ('registry_ref' not in params or
                params['registry_ref'] is None):
            raise ValueError("Missing the required parameter `registry_ref` when calling `get_all_artifact_versions`")  # noqa: E501
        # verify the required parameter 'artifact' is set
        if ('artifact' not in params or
                params['artifact'] is None):
            raise ValueError("Missing the required parameter `artifact` when calling `get_all_artifact_versions`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'registry_ref' in params:
            path_params['registry_ref'] = params['registry_ref']  # noqa: E501
        if 'artifact' in params:
            path_params['artifact'] = params['artifact']  # noqa: E501

        query_params = []
        if 'artifact_type' in params:
            query_params.append(('artifact_type', params['artifact_type']))  # noqa: E501
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
            '/har/api/v1/registry/{registry_ref}/artifact/{artifact}/versions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20027',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_artifact_deployments(self, registry_ref, artifact, version, **kwargs):  # noqa: E501
        """Describe Artifact Deployments  # noqa: E501

        Get Artifact Deployments  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_artifact_deployments(registry_ref, artifact, version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param str version: Name of Artifact Version. (required)
        :param str env_type: env type
        :param int page: Current page number
        :param int size: Number of items per page
        :param str sort_order: sortOrder
        :param str sort_field: sortField
        :param str search_term: search Term.
        :param str version_type: Version Type.
        :return: InlineResponse20015
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_artifact_deployments_with_http_info(registry_ref, artifact, version, **kwargs)  # noqa: E501
        else:
            (data) = self.get_artifact_deployments_with_http_info(registry_ref, artifact, version, **kwargs)  # noqa: E501
            return data

    def get_artifact_deployments_with_http_info(self, registry_ref, artifact, version, **kwargs):  # noqa: E501
        """Describe Artifact Deployments  # noqa: E501

        Get Artifact Deployments  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_artifact_deployments_with_http_info(registry_ref, artifact, version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param str version: Name of Artifact Version. (required)
        :param str env_type: env type
        :param int page: Current page number
        :param int size: Number of items per page
        :param str sort_order: sortOrder
        :param str sort_field: sortField
        :param str search_term: search Term.
        :param str version_type: Version Type.
        :return: InlineResponse20015
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['registry_ref', 'artifact', 'version', 'env_type', 'page', 'size', 'sort_order', 'sort_field', 'search_term', 'version_type']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_artifact_deployments" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'registry_ref' is set
        if ('registry_ref' not in params or
                params['registry_ref'] is None):
            raise ValueError("Missing the required parameter `registry_ref` when calling `get_artifact_deployments`")  # noqa: E501
        # verify the required parameter 'artifact' is set
        if ('artifact' not in params or
                params['artifact'] is None):
            raise ValueError("Missing the required parameter `artifact` when calling `get_artifact_deployments`")  # noqa: E501
        # verify the required parameter 'version' is set
        if ('version' not in params or
                params['version'] is None):
            raise ValueError("Missing the required parameter `version` when calling `get_artifact_deployments`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'registry_ref' in params:
            path_params['registry_ref'] = params['registry_ref']  # noqa: E501
        if 'artifact' in params:
            path_params['artifact'] = params['artifact']  # noqa: E501
        if 'version' in params:
            path_params['version'] = params['version']  # noqa: E501

        query_params = []
        if 'env_type' in params:
            query_params.append(('env_type', params['env_type']))  # noqa: E501
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
        if 'version_type' in params:
            query_params.append(('version_type', params['version_type']))  # noqa: E501

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
            '/har/api/v1/registry/{registry_ref}/artifact/{artifact}/version/{version}/deploymentdetails', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20015',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_artifact_details(self, registry_ref, artifact, version, **kwargs):  # noqa: E501
        """Describe Artifact Details  # noqa: E501

        Get Artifact Details  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_artifact_details(registry_ref, artifact, version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param str version: Name of Artifact Version. (required)
        :param str artifact_type: artifact type.
        :param str child_version: Child version incase of Docker artifacts.
        :return: InlineResponse20016
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_artifact_details_with_http_info(registry_ref, artifact, version, **kwargs)  # noqa: E501
        else:
            (data) = self.get_artifact_details_with_http_info(registry_ref, artifact, version, **kwargs)  # noqa: E501
            return data

    def get_artifact_details_with_http_info(self, registry_ref, artifact, version, **kwargs):  # noqa: E501
        """Describe Artifact Details  # noqa: E501

        Get Artifact Details  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_artifact_details_with_http_info(registry_ref, artifact, version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param str version: Name of Artifact Version. (required)
        :param str artifact_type: artifact type.
        :param str child_version: Child version incase of Docker artifacts.
        :return: InlineResponse20016
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['registry_ref', 'artifact', 'version', 'artifact_type', 'child_version']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_artifact_details" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'registry_ref' is set
        if ('registry_ref' not in params or
                params['registry_ref'] is None):
            raise ValueError("Missing the required parameter `registry_ref` when calling `get_artifact_details`")  # noqa: E501
        # verify the required parameter 'artifact' is set
        if ('artifact' not in params or
                params['artifact'] is None):
            raise ValueError("Missing the required parameter `artifact` when calling `get_artifact_details`")  # noqa: E501
        # verify the required parameter 'version' is set
        if ('version' not in params or
                params['version'] is None):
            raise ValueError("Missing the required parameter `version` when calling `get_artifact_details`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'registry_ref' in params:
            path_params['registry_ref'] = params['registry_ref']  # noqa: E501
        if 'artifact' in params:
            path_params['artifact'] = params['artifact']  # noqa: E501
        if 'version' in params:
            path_params['version'] = params['version']  # noqa: E501

        query_params = []
        if 'artifact_type' in params:
            query_params.append(('artifact_type', params['artifact_type']))  # noqa: E501
        if 'child_version' in params:
            query_params.append(('childVersion', params['child_version']))  # noqa: E501

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
            '/har/api/v1/registry/{registry_ref}/artifact/{artifact}/version/{version}/details', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20016',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_artifact_file(self, registry_ref, artifact, version, file_name, **kwargs):  # noqa: E501
        """Get Artifact file  # noqa: E501

        just validate existence of Artifact file  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_artifact_file(registry_ref, artifact, version, file_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param str version: Name of Artifact Version. (required)
        :param str file_name: Name of Artifact File. (required)
        :param str artifact_type: artifact type.
        :return: InlineResponse20022
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_artifact_file_with_http_info(registry_ref, artifact, version, file_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_artifact_file_with_http_info(registry_ref, artifact, version, file_name, **kwargs)  # noqa: E501
            return data

    def get_artifact_file_with_http_info(self, registry_ref, artifact, version, file_name, **kwargs):  # noqa: E501
        """Get Artifact file  # noqa: E501

        just validate existence of Artifact file  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_artifact_file_with_http_info(registry_ref, artifact, version, file_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param str version: Name of Artifact Version. (required)
        :param str file_name: Name of Artifact File. (required)
        :param str artifact_type: artifact type.
        :return: InlineResponse20022
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['registry_ref', 'artifact', 'version', 'file_name', 'artifact_type']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_artifact_file" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'registry_ref' is set
        if ('registry_ref' not in params or
                params['registry_ref'] is None):
            raise ValueError("Missing the required parameter `registry_ref` when calling `get_artifact_file`")  # noqa: E501
        # verify the required parameter 'artifact' is set
        if ('artifact' not in params or
                params['artifact'] is None):
            raise ValueError("Missing the required parameter `artifact` when calling `get_artifact_file`")  # noqa: E501
        # verify the required parameter 'version' is set
        if ('version' not in params or
                params['version'] is None):
            raise ValueError("Missing the required parameter `version` when calling `get_artifact_file`")  # noqa: E501
        # verify the required parameter 'file_name' is set
        if ('file_name' not in params or
                params['file_name'] is None):
            raise ValueError("Missing the required parameter `file_name` when calling `get_artifact_file`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'registry_ref' in params:
            path_params['registry_ref'] = params['registry_ref']  # noqa: E501
        if 'artifact' in params:
            path_params['artifact'] = params['artifact']  # noqa: E501
        if 'version' in params:
            path_params['version'] = params['version']  # noqa: E501
        if 'file_name' in params:
            path_params['file_name'] = params['file_name']  # noqa: E501

        query_params = []
        if 'artifact_type' in params:
            query_params.append(('artifact_type', params['artifact_type']))  # noqa: E501

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
            '/har/api/v1/registry/{registry_ref}/artifact/{artifact}/version/{version}/file/{file_name}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20022',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_artifact_files(self, registry_ref, artifact, version, **kwargs):  # noqa: E501
        """Describe Artifact files  # noqa: E501

        Get Artifact files  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_artifact_files(registry_ref, artifact, version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param str version: Name of Artifact Version. (required)
        :param str artifact_type: artifact type.
        :param int page: Current page number
        :param int size: Number of items per page
        :param str sort_order: sortOrder
        :param str sort_field: sortField
        :param str search_term: search Term.
        :return: InlineResponse20023
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_artifact_files_with_http_info(registry_ref, artifact, version, **kwargs)  # noqa: E501
        else:
            (data) = self.get_artifact_files_with_http_info(registry_ref, artifact, version, **kwargs)  # noqa: E501
            return data

    def get_artifact_files_with_http_info(self, registry_ref, artifact, version, **kwargs):  # noqa: E501
        """Describe Artifact files  # noqa: E501

        Get Artifact files  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_artifact_files_with_http_info(registry_ref, artifact, version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param str version: Name of Artifact Version. (required)
        :param str artifact_type: artifact type.
        :param int page: Current page number
        :param int size: Number of items per page
        :param str sort_order: sortOrder
        :param str sort_field: sortField
        :param str search_term: search Term.
        :return: InlineResponse20023
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['registry_ref', 'artifact', 'version', 'artifact_type', 'page', 'size', 'sort_order', 'sort_field', 'search_term']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_artifact_files" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'registry_ref' is set
        if ('registry_ref' not in params or
                params['registry_ref'] is None):
            raise ValueError("Missing the required parameter `registry_ref` when calling `get_artifact_files`")  # noqa: E501
        # verify the required parameter 'artifact' is set
        if ('artifact' not in params or
                params['artifact'] is None):
            raise ValueError("Missing the required parameter `artifact` when calling `get_artifact_files`")  # noqa: E501
        # verify the required parameter 'version' is set
        if ('version' not in params or
                params['version'] is None):
            raise ValueError("Missing the required parameter `version` when calling `get_artifact_files`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'registry_ref' in params:
            path_params['registry_ref'] = params['registry_ref']  # noqa: E501
        if 'artifact' in params:
            path_params['artifact'] = params['artifact']  # noqa: E501
        if 'version' in params:
            path_params['version'] = params['version']  # noqa: E501

        query_params = []
        if 'artifact_type' in params:
            query_params.append(('artifact_type', params['artifact_type']))  # noqa: E501
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
            '/har/api/v1/registry/{registry_ref}/artifact/{artifact}/version/{version}/files', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20023',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_artifact_stats(self, registry_ref, artifact, **kwargs):  # noqa: E501
        """Get Artifact Stats  # noqa: E501

        Get Artifact Stats.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_artifact_stats(registry_ref, artifact, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param str _from: Date. Format - MM/DD/YYYY
        :param str to: Date. Format - MM/DD/YYYY
        :return: InlineResponse20012
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_artifact_stats_with_http_info(registry_ref, artifact, **kwargs)  # noqa: E501
        else:
            (data) = self.get_artifact_stats_with_http_info(registry_ref, artifact, **kwargs)  # noqa: E501
            return data

    def get_artifact_stats_with_http_info(self, registry_ref, artifact, **kwargs):  # noqa: E501
        """Get Artifact Stats  # noqa: E501

        Get Artifact Stats.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_artifact_stats_with_http_info(registry_ref, artifact, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param str _from: Date. Format - MM/DD/YYYY
        :param str to: Date. Format - MM/DD/YYYY
        :return: InlineResponse20012
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['registry_ref', 'artifact', '_from', 'to']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_artifact_stats" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'registry_ref' is set
        if ('registry_ref' not in params or
                params['registry_ref'] is None):
            raise ValueError("Missing the required parameter `registry_ref` when calling `get_artifact_stats`")  # noqa: E501
        # verify the required parameter 'artifact' is set
        if ('artifact' not in params or
                params['artifact'] is None):
            raise ValueError("Missing the required parameter `artifact` when calling `get_artifact_stats`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'registry_ref' in params:
            path_params['registry_ref'] = params['registry_ref']  # noqa: E501
        if 'artifact' in params:
            path_params['artifact'] = params['artifact']  # noqa: E501

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
            '/har/api/v1/registry/{registry_ref}/artifact/{artifact}/stats', 'GET',
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

    def get_artifact_stats_for_registry(self, registry_ref, **kwargs):  # noqa: E501
        """Get Artifact Stats  # noqa: E501

        Get Artifact Stats.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_artifact_stats_for_registry(registry_ref, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str _from: Date. Format - MM/DD/YYYY
        :param str to: Date. Format - MM/DD/YYYY
        :return: InlineResponse20012
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_artifact_stats_for_registry_with_http_info(registry_ref, **kwargs)  # noqa: E501
        else:
            (data) = self.get_artifact_stats_for_registry_with_http_info(registry_ref, **kwargs)  # noqa: E501
            return data

    def get_artifact_stats_for_registry_with_http_info(self, registry_ref, **kwargs):  # noqa: E501
        """Get Artifact Stats  # noqa: E501

        Get Artifact Stats.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_artifact_stats_for_registry_with_http_info(registry_ref, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str _from: Date. Format - MM/DD/YYYY
        :param str to: Date. Format - MM/DD/YYYY
        :return: InlineResponse20012
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['registry_ref', '_from', 'to']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_artifact_stats_for_registry" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'registry_ref' is set
        if ('registry_ref' not in params or
                params['registry_ref'] is None):
            raise ValueError("Missing the required parameter `registry_ref` when calling `get_artifact_stats_for_registry`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'registry_ref' in params:
            path_params['registry_ref'] = params['registry_ref']  # noqa: E501

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
            '/har/api/v1/registry/{registry_ref}/artifact/stats', 'GET',
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

    def get_artifact_summary(self, registry_ref, artifact, **kwargs):  # noqa: E501
        """Get Artifact Summary  # noqa: E501

        Get Artifact Summary.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_artifact_summary(registry_ref, artifact, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param str artifact_type: artifact type.
        :return: InlineResponse20013
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_artifact_summary_with_http_info(registry_ref, artifact, **kwargs)  # noqa: E501
        else:
            (data) = self.get_artifact_summary_with_http_info(registry_ref, artifact, **kwargs)  # noqa: E501
            return data

    def get_artifact_summary_with_http_info(self, registry_ref, artifact, **kwargs):  # noqa: E501
        """Get Artifact Summary  # noqa: E501

        Get Artifact Summary.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_artifact_summary_with_http_info(registry_ref, artifact, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param str artifact_type: artifact type.
        :return: InlineResponse20013
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['registry_ref', 'artifact', 'artifact_type']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_artifact_summary" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'registry_ref' is set
        if ('registry_ref' not in params or
                params['registry_ref'] is None):
            raise ValueError("Missing the required parameter `registry_ref` when calling `get_artifact_summary`")  # noqa: E501
        # verify the required parameter 'artifact' is set
        if ('artifact' not in params or
                params['artifact'] is None):
            raise ValueError("Missing the required parameter `artifact` when calling `get_artifact_summary`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'registry_ref' in params:
            path_params['registry_ref'] = params['registry_ref']  # noqa: E501
        if 'artifact' in params:
            path_params['artifact'] = params['artifact']  # noqa: E501

        query_params = []
        if 'artifact_type' in params:
            query_params.append(('artifact_type', params['artifact_type']))  # noqa: E501

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
            '/har/api/v1/registry/{registry_ref}/artifact/{artifact}/summary', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20013',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_artifact_version_summary(self, registry_ref, artifact, version, **kwargs):  # noqa: E501
        """Get Artifact Version Summary  # noqa: E501

        Get Artifact Version Summary.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_artifact_version_summary(registry_ref, artifact, version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param str version: Name of Artifact Version. (required)
        :param str artifact_type: artifact type.
        :param str digest: Digest.
        :return: InlineResponse20026
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_artifact_version_summary_with_http_info(registry_ref, artifact, version, **kwargs)  # noqa: E501
        else:
            (data) = self.get_artifact_version_summary_with_http_info(registry_ref, artifact, version, **kwargs)  # noqa: E501
            return data

    def get_artifact_version_summary_with_http_info(self, registry_ref, artifact, version, **kwargs):  # noqa: E501
        """Get Artifact Version Summary  # noqa: E501

        Get Artifact Version Summary.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_artifact_version_summary_with_http_info(registry_ref, artifact, version, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param str version: Name of Artifact Version. (required)
        :param str artifact_type: artifact type.
        :param str digest: Digest.
        :return: InlineResponse20026
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['registry_ref', 'artifact', 'version', 'artifact_type', 'digest']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_artifact_version_summary" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'registry_ref' is set
        if ('registry_ref' not in params or
                params['registry_ref'] is None):
            raise ValueError("Missing the required parameter `registry_ref` when calling `get_artifact_version_summary`")  # noqa: E501
        # verify the required parameter 'artifact' is set
        if ('artifact' not in params or
                params['artifact'] is None):
            raise ValueError("Missing the required parameter `artifact` when calling `get_artifact_version_summary`")  # noqa: E501
        # verify the required parameter 'version' is set
        if ('version' not in params or
                params['version'] is None):
            raise ValueError("Missing the required parameter `version` when calling `get_artifact_version_summary`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'registry_ref' in params:
            path_params['registry_ref'] = params['registry_ref']  # noqa: E501
        if 'artifact' in params:
            path_params['artifact'] = params['artifact']  # noqa: E501
        if 'version' in params:
            path_params['version'] = params['version']  # noqa: E501

        query_params = []
        if 'artifact_type' in params:
            query_params.append(('artifact_type', params['artifact_type']))  # noqa: E501
        if 'digest' in params:
            query_params.append(('digest', params['digest']))  # noqa: E501

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
            '/har/api/v1/registry/{registry_ref}/artifact/{artifact}/version/{version}/summary', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20026',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_oci_artifact_tags(self, registry_ref, artifact, **kwargs):  # noqa: E501
        """List OCI Artifact tags  # noqa: E501

        Lists OCI Artifact Tags.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_oci_artifact_tags(registry_ref, artifact, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param int page: Current page number
        :param int size: Number of items per page
        :param str search_term: search Term.
        :return: InlineResponse20014
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_oci_artifact_tags_with_http_info(registry_ref, artifact, **kwargs)  # noqa: E501
        else:
            (data) = self.get_oci_artifact_tags_with_http_info(registry_ref, artifact, **kwargs)  # noqa: E501
            return data

    def get_oci_artifact_tags_with_http_info(self, registry_ref, artifact, **kwargs):  # noqa: E501
        """List OCI Artifact tags  # noqa: E501

        Lists OCI Artifact Tags.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_oci_artifact_tags_with_http_info(registry_ref, artifact, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param int page: Current page number
        :param int size: Number of items per page
        :param str search_term: search Term.
        :return: InlineResponse20014
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['registry_ref', 'artifact', 'page', 'size', 'search_term']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_oci_artifact_tags" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'registry_ref' is set
        if ('registry_ref' not in params or
                params['registry_ref'] is None):
            raise ValueError("Missing the required parameter `registry_ref` when calling `get_oci_artifact_tags`")  # noqa: E501
        # verify the required parameter 'artifact' is set
        if ('artifact' not in params or
                params['artifact'] is None):
            raise ValueError("Missing the required parameter `artifact` when calling `get_oci_artifact_tags`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'registry_ref' in params:
            path_params['registry_ref'] = params['registry_ref']  # noqa: E501
        if 'artifact' in params:
            path_params['artifact'] = params['artifact']  # noqa: E501

        query_params = []
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'size' in params:
            query_params.append(('size', params['size']))  # noqa: E501
        if 'search_term' in params:
            query_params.append(('search_term', params['search_term']))  # noqa: E501

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
            '/har/api/v1/registry/{registry_ref}/artifact/{artifact}/tags', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20014',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_artifact_labels(self, registry_ref, **kwargs):  # noqa: E501
        """List Artifact Labels  # noqa: E501

        List Artifact Labels.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_artifact_labels(registry_ref, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param int page: Current page number
        :param int size: Number of items per page
        :param str search_term: search Term.
        :return: InlineResponse20011
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_artifact_labels_with_http_info(registry_ref, **kwargs)  # noqa: E501
        else:
            (data) = self.list_artifact_labels_with_http_info(registry_ref, **kwargs)  # noqa: E501
            return data

    def list_artifact_labels_with_http_info(self, registry_ref, **kwargs):  # noqa: E501
        """List Artifact Labels  # noqa: E501

        List Artifact Labels.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_artifact_labels_with_http_info(registry_ref, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param int page: Current page number
        :param int size: Number of items per page
        :param str search_term: search Term.
        :return: InlineResponse20011
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['registry_ref', 'page', 'size', 'search_term']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_artifact_labels" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'registry_ref' is set
        if ('registry_ref' not in params or
                params['registry_ref'] is None):
            raise ValueError("Missing the required parameter `registry_ref` when calling `list_artifact_labels`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'registry_ref' in params:
            path_params['registry_ref'] = params['registry_ref']  # noqa: E501

        query_params = []
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'size' in params:
            query_params.append(('size', params['size']))  # noqa: E501
        if 'search_term' in params:
            query_params.append(('search_term', params['search_term']))  # noqa: E501

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
            '/har/api/v1/registry/{registry_ref}/artifact/labels', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20011',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def redirect_harness_artifact(self, registry_identifier, artifact, **kwargs):  # noqa: E501
        """Redirect to Harness Artifact Page  # noqa: E501

        Redirect to Harness Artifact Page  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.redirect_harness_artifact(registry_identifier, artifact, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_identifier: Unique registry Identifier in a account. (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param str account_identifier: Account Identifier
        :param str version: Version
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.redirect_harness_artifact_with_http_info(registry_identifier, artifact, **kwargs)  # noqa: E501
        else:
            (data) = self.redirect_harness_artifact_with_http_info(registry_identifier, artifact, **kwargs)  # noqa: E501
            return data

    def redirect_harness_artifact_with_http_info(self, registry_identifier, artifact, **kwargs):  # noqa: E501
        """Redirect to Harness Artifact Page  # noqa: E501

        Redirect to Harness Artifact Page  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.redirect_harness_artifact_with_http_info(registry_identifier, artifact, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_identifier: Unique registry Identifier in a account. (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param str account_identifier: Account Identifier
        :param str version: Version
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['registry_identifier', 'artifact', 'account_identifier', 'version']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method redirect_harness_artifact" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'registry_identifier' is set
        if ('registry_identifier' not in params or
                params['registry_identifier'] is None):
            raise ValueError("Missing the required parameter `registry_identifier` when calling `redirect_harness_artifact`")  # noqa: E501
        # verify the required parameter 'artifact' is set
        if ('artifact' not in params or
                params['artifact'] is None):
            raise ValueError("Missing the required parameter `artifact` when calling `redirect_harness_artifact`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'registry_identifier' in params:
            path_params['registry_identifier'] = params['registry_identifier']  # noqa: E501
        if 'artifact' in params:
            path_params['artifact'] = params['artifact']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'version' in params:
            query_params.append(('version', params['version']))  # noqa: E501

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
            '/har/api/v1/registry/{registry_identifier}/artifact/{artifact}/redirect', 'GET',
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

    def update_artifact_labels(self, registry_ref, artifact, **kwargs):  # noqa: E501
        """Update Artifact Labels  # noqa: E501

        Update Artifact Labels.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_artifact_labels(registry_ref, artifact, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param ArtifactLabelRequest body: request to update artifact labels
        :param str artifact_type: artifact type.
        :return: InlineResponse20013
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_artifact_labels_with_http_info(registry_ref, artifact, **kwargs)  # noqa: E501
        else:
            (data) = self.update_artifact_labels_with_http_info(registry_ref, artifact, **kwargs)  # noqa: E501
            return data

    def update_artifact_labels_with_http_info(self, registry_ref, artifact, **kwargs):  # noqa: E501
        """Update Artifact Labels  # noqa: E501

        Update Artifact Labels.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_artifact_labels_with_http_info(registry_ref, artifact, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str registry_ref: Reference to the scope in which the registry exists.  Format depends on the scope:  - **Account-level**: `account_id/registry_name/+` - **Organization-level**: `account_id/org_id/registry_name/+` - **Project-level**: `account_id/org_id/project_id/registry_name/+`  The `/+` suffix is used internally to route scoped requests. It must be included **exactly as shown** in the URL.  (required)
        :param str artifact: Name of the artifact.  The value depends on whether the name contains a slash (`/`):  - If the artifact name **contains `/`**, append a trailing `/+` at the end.   - Example: `mygroup/myartifact/+` - If the artifact name **does not contain `/`**, use the plain name.   - Example: `myartifact`  This is used internally to distinguish between namespaced and flat artifact names.  (required)
        :param ArtifactLabelRequest body: request to update artifact labels
        :param str artifact_type: artifact type.
        :return: InlineResponse20013
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['registry_ref', 'artifact', 'body', 'artifact_type']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_artifact_labels" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'registry_ref' is set
        if ('registry_ref' not in params or
                params['registry_ref'] is None):
            raise ValueError("Missing the required parameter `registry_ref` when calling `update_artifact_labels`")  # noqa: E501
        # verify the required parameter 'artifact' is set
        if ('artifact' not in params or
                params['artifact'] is None):
            raise ValueError("Missing the required parameter `artifact` when calling `update_artifact_labels`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'registry_ref' in params:
            path_params['registry_ref'] = params['registry_ref']  # noqa: E501
        if 'artifact' in params:
            path_params['artifact'] = params['artifact']  # noqa: E501

        query_params = []
        if 'artifact_type' in params:
            query_params.append(('artifact_type', params['artifact_type']))  # noqa: E501

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
            '/har/api/v1/registry/{registry_ref}/artifact/{artifact}/labels', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20013',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
