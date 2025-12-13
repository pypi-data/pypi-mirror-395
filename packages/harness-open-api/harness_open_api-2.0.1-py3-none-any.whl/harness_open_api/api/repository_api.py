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


class RepositoryApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def archive(self, account_identifier, repo_identifier, git_ref, format, **kwargs):  # noqa: E501
        """Download repo in archived format  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.archive(account_identifier, repo_identifier, git_ref, format, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str git_ref: (required)
        :param str format: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param list[str] path: Without an optional path parameter, all files and subdirectories of the current working directory are included in the archive. If one or more paths are specified, only these are included.
        :param str prefix: Prepend <prefix>/ to paths in the archive.
        :param str attributes: Look for attributes in .gitattributes files in the working tree as well
        :param str time: Set modification time of archive entries. Without this option the committer time is used if <tree-ish> is a commit or tag, and the current time if it is a tree.
        :param int compression: Specify compression level. Larger values allow the command to spend more time to compress to smaller size.
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.archive_with_http_info(account_identifier, repo_identifier, git_ref, format, **kwargs)  # noqa: E501
        else:
            (data) = self.archive_with_http_info(account_identifier, repo_identifier, git_ref, format, **kwargs)  # noqa: E501
            return data

    def archive_with_http_info(self, account_identifier, repo_identifier, git_ref, format, **kwargs):  # noqa: E501
        """Download repo in archived format  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.archive_with_http_info(account_identifier, repo_identifier, git_ref, format, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str git_ref: (required)
        :param str format: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param list[str] path: Without an optional path parameter, all files and subdirectories of the current working directory are included in the archive. If one or more paths are specified, only these are included.
        :param str prefix: Prepend <prefix>/ to paths in the archive.
        :param str attributes: Look for attributes in .gitattributes files in the working tree as well
        :param str time: Set modification time of archive entries. Without this option the committer time is used if <tree-ish> is a commit or tag, and the current time if it is a tree.
        :param int compression: Specify compression level. Larger values allow the command to spend more time to compress to smaller size.
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'git_ref', 'format', 'org_identifier', 'project_identifier', 'path', 'prefix', 'attributes', 'time', 'compression']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method archive" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `archive`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `archive`")  # noqa: E501
        # verify the required parameter 'git_ref' is set
        if ('git_ref' not in params or
                params['git_ref'] is None):
            raise ValueError("Missing the required parameter `git_ref` when calling `archive`")  # noqa: E501
        # verify the required parameter 'format' is set
        if ('format' not in params or
                params['format'] is None):
            raise ValueError("Missing the required parameter `format` when calling `archive`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'git_ref' in params:
            path_params['git_ref'] = params['git_ref']  # noqa: E501
        if 'format' in params:
            path_params['format'] = params['format']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'path' in params:
            query_params.append(('path', params['path']))  # noqa: E501
            collection_formats['path'] = 'multi'  # noqa: E501
        if 'prefix' in params:
            query_params.append(('prefix', params['prefix']))  # noqa: E501
        if 'attributes' in params:
            query_params.append(('attributes', params['attributes']))  # noqa: E501
        if 'time' in params:
            query_params.append(('time', params['time']))  # noqa: E501
        if 'compression' in params:
            query_params.append(('compression', params['compression']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/gzip', 'application/tar', 'application/zip', 'application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/code/api/v1/repos/{repo_identifier}/archive/{git_ref}.{format}', 'GET',
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

    def calculate_commit_divergence(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Get commit divergence  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.calculate_commit_divergence(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param OpenapiCalculateCommitDivergenceRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: list[TypesCommitDivergence]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.calculate_commit_divergence_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.calculate_commit_divergence_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
            return data

    def calculate_commit_divergence_with_http_info(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Get commit divergence  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.calculate_commit_divergence_with_http_info(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param OpenapiCalculateCommitDivergenceRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: list[TypesCommitDivergence]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method calculate_commit_divergence" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `calculate_commit_divergence`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `calculate_commit_divergence`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/commits/calculate-divergence', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[TypesCommitDivergence]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def code_owners_validate(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Validate code owners file  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.code_owners_validate(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str git_ref: The git reference (branch / tag / commitID) that will be used to retrieve the data. If no value is provided the default branch of the repository is used.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.code_owners_validate_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.code_owners_validate_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
            return data

    def code_owners_validate_with_http_info(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Validate code owners file  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.code_owners_validate_with_http_info(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str git_ref: The git reference (branch / tag / commitID) that will be used to retrieve the data. If no value is provided the default branch of the repository is used.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'org_identifier', 'project_identifier', 'git_ref']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method code_owners_validate" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `code_owners_validate`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `code_owners_validate`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'git_ref' in params:
            query_params.append(('git_ref', params['git_ref']))  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/codeowners/validate', 'GET',
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

    def commit_files(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Commit files  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.commit_files(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param OpenapiCommitFilesRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesCommitFilesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.commit_files_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.commit_files_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
            return data

    def commit_files_with_http_info(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Commit files  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.commit_files_with_http_info(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param OpenapiCommitFilesRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesCommitFilesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method commit_files" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `commit_files`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `commit_files`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/commits', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesCommitFilesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_branch(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Create branch  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_branch(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param OpenapiCreateBranchRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesCreateBranchOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_branch_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.create_branch_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
            return data

    def create_branch_with_http_info(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Create branch  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_branch_with_http_info(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param OpenapiCreateBranchRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesCreateBranchOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_branch" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `create_branch`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `create_branch`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/branches', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesCreateBranchOutput',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_repository(self, account_identifier, **kwargs):  # noqa: E501
        """Create repository  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_repository(account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param OpenapiCreateRepositoryRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: RepoRepositoryOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_repository_with_http_info(account_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.create_repository_with_http_info(account_identifier, **kwargs)  # noqa: E501
            return data

    def create_repository_with_http_info(self, account_identifier, **kwargs):  # noqa: E501
        """Create repository  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_repository_with_http_info(account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param OpenapiCreateRepositoryRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: RepoRepositoryOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_repository" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `create_repository`")  # noqa: E501

        collection_formats = {}

        path_params = {}

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
            '/code/api/v1/repos', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RepoRepositoryOutput',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_tag(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Create tag  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_tag(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param OpenapiCreateTagRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesCommitTag
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_tag_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.create_tag_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
            return data

    def create_tag_with_http_info(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Create tag  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_tag_with_http_info(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param OpenapiCreateTagRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesCommitTag
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_tag" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `create_tag`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `create_tag`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/tags', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesCommitTag',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_branch(self, account_identifier, repo_identifier, branch_name, **kwargs):  # noqa: E501
        """Delete branch  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_branch(account_identifier, repo_identifier, branch_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str branch_name: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param bool bypass_rules: Bypass rule violations if possible.
        :param bool dry_run_rules: Dry run rules for operations
        :return: TypesDeleteBranchOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_branch_with_http_info(account_identifier, repo_identifier, branch_name, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_branch_with_http_info(account_identifier, repo_identifier, branch_name, **kwargs)  # noqa: E501
            return data

    def delete_branch_with_http_info(self, account_identifier, repo_identifier, branch_name, **kwargs):  # noqa: E501
        """Delete branch  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_branch_with_http_info(account_identifier, repo_identifier, branch_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str branch_name: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param bool bypass_rules: Bypass rule violations if possible.
        :param bool dry_run_rules: Dry run rules for operations
        :return: TypesDeleteBranchOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'branch_name', 'org_identifier', 'project_identifier', 'bypass_rules', 'dry_run_rules']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_branch" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `delete_branch`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `delete_branch`")  # noqa: E501
        # verify the required parameter 'branch_name' is set
        if ('branch_name' not in params or
                params['branch_name'] is None):
            raise ValueError("Missing the required parameter `branch_name` when calling `delete_branch`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'branch_name' in params:
            path_params['branch_name'] = params['branch_name']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'bypass_rules' in params:
            query_params.append(('bypass_rules', params['bypass_rules']))  # noqa: E501
        if 'dry_run_rules' in params:
            query_params.append(('dry_run_rules', params['dry_run_rules']))  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/branches/{branch_name}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesDeleteBranchOutput',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_repository(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Soft delete repository  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_repository(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: RepoSoftDeleteResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_repository_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_repository_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
            return data

    def delete_repository_with_http_info(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Soft delete repository  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_repository_with_http_info(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: RepoSoftDeleteResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_repository" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `delete_repository`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `delete_repository`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501

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
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/code/api/v1/repos/{repo_identifier}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RepoSoftDeleteResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_tag(self, account_identifier, repo_identifier, tag_name, **kwargs):  # noqa: E501
        """Delete tag  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_tag(account_identifier, repo_identifier, tag_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str tag_name: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param bool bypass_rules: Bypass rule violations if possible.
        :param bool dry_run_rules: Dry run rules for operations
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_tag_with_http_info(account_identifier, repo_identifier, tag_name, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_tag_with_http_info(account_identifier, repo_identifier, tag_name, **kwargs)  # noqa: E501
            return data

    def delete_tag_with_http_info(self, account_identifier, repo_identifier, tag_name, **kwargs):  # noqa: E501
        """Delete tag  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_tag_with_http_info(account_identifier, repo_identifier, tag_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str tag_name: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param bool bypass_rules: Bypass rule violations if possible.
        :param bool dry_run_rules: Dry run rules for operations
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'tag_name', 'org_identifier', 'project_identifier', 'bypass_rules', 'dry_run_rules']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_tag" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `delete_tag`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `delete_tag`")  # noqa: E501
        # verify the required parameter 'tag_name' is set
        if ('tag_name' not in params or
                params['tag_name'] is None):
            raise ValueError("Missing the required parameter `tag_name` when calling `delete_tag`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'tag_name' in params:
            path_params['tag_name'] = params['tag_name']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'bypass_rules' in params:
            query_params.append(('bypass_rules', params['bypass_rules']))  # noqa: E501
        if 'dry_run_rules' in params:
            query_params.append(('dry_run_rules', params['dry_run_rules']))  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/tags/{tag_name}', 'DELETE',
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

    def diff_stats(self, account_identifier, repo_identifier, range, **kwargs):  # noqa: E501
        """Get diff stats  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.diff_stats(account_identifier, repo_identifier, range, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str range: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param list[str] path: provide path for diff operation
        :return: TypesDiffStats
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.diff_stats_with_http_info(account_identifier, repo_identifier, range, **kwargs)  # noqa: E501
        else:
            (data) = self.diff_stats_with_http_info(account_identifier, repo_identifier, range, **kwargs)  # noqa: E501
            return data

    def diff_stats_with_http_info(self, account_identifier, repo_identifier, range, **kwargs):  # noqa: E501
        """Get diff stats  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.diff_stats_with_http_info(account_identifier, repo_identifier, range, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str range: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param list[str] path: provide path for diff operation
        :return: TypesDiffStats
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'range', 'org_identifier', 'project_identifier', 'path']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method diff_stats" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `diff_stats`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `diff_stats`")  # noqa: E501
        # verify the required parameter 'range' is set
        if ('range' not in params or
                params['range'] is None):
            raise ValueError("Missing the required parameter `range` when calling `diff_stats`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'range' in params:
            path_params['range'] = params['range']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'path' in params:
            query_params.append(('path', params['path']))  # noqa: E501
            collection_formats['path'] = 'multi'  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/diff-stats/{range}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesDiffStats',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def find_general_settings(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Get general settings  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_general_settings(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: ReposettingsGeneralSettings
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.find_general_settings_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.find_general_settings_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
            return data

    def find_general_settings_with_http_info(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Get general settings  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_general_settings_with_http_info(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: ReposettingsGeneralSettings
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method find_general_settings" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `find_general_settings`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `find_general_settings`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501

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
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/code/api/v1/repos/{repo_identifier}/settings/general', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ReposettingsGeneralSettings',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def find_security_settings(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Get security settings  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_security_settings(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: ReposettingsSecuritySettings
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.find_security_settings_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.find_security_settings_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
            return data

    def find_security_settings_with_http_info(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Get security settings  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_security_settings_with_http_info(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: ReposettingsSecuritySettings
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method find_security_settings" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `find_security_settings`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `find_security_settings`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501

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
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/code/api/v1/repos/{repo_identifier}/settings/security', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ReposettingsSecuritySettings',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_blame(self, account_identifier, repo_identifier, path, **kwargs):  # noqa: E501
        """Get git blame  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_blame(account_identifier, repo_identifier, path, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str path: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str git_ref: The git reference (branch / tag / commitID) that will be used to retrieve the data. If no value is provided the default branch of the repository is used.
        :param int line_from: Line number from which the file data is considered
        :param int line_to: Line number to which the file data is considered
        :return: list[GitBlamePart]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_blame_with_http_info(account_identifier, repo_identifier, path, **kwargs)  # noqa: E501
        else:
            (data) = self.get_blame_with_http_info(account_identifier, repo_identifier, path, **kwargs)  # noqa: E501
            return data

    def get_blame_with_http_info(self, account_identifier, repo_identifier, path, **kwargs):  # noqa: E501
        """Get git blame  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_blame_with_http_info(account_identifier, repo_identifier, path, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str path: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str git_ref: The git reference (branch / tag / commitID) that will be used to retrieve the data. If no value is provided the default branch of the repository is used.
        :param int line_from: Line number from which the file data is considered
        :param int line_to: Line number to which the file data is considered
        :return: list[GitBlamePart]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'path', 'org_identifier', 'project_identifier', 'git_ref', 'line_from', 'line_to']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_blame" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `get_blame`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `get_blame`")  # noqa: E501
        # verify the required parameter 'path' is set
        if ('path' not in params or
                params['path'] is None):
            raise ValueError("Missing the required parameter `path` when calling `get_blame`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'path' in params:
            path_params['path'] = params['path']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'git_ref' in params:
            query_params.append(('git_ref', params['git_ref']))  # noqa: E501
        if 'line_from' in params:
            query_params.append(('line_from', params['line_from']))  # noqa: E501
        if 'line_to' in params:
            query_params.append(('line_to', params['line_to']))  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/blame/{path}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[GitBlamePart]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_branch(self, account_identifier, repo_identifier, branch_name, **kwargs):  # noqa: E501
        """Get branch  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_branch(account_identifier, repo_identifier, branch_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str branch_name: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param bool include_checks: If true, the summary of check for the branch commit SHA would be included in the response.
        :param bool include_rules: If true, a list of rules that apply to this branch would be included in the response.
        :param bool include_pullreqs: If true, a list of pull requests from the branch would be included in the response.
        :param int max_divergence: If greater than zero, branch divergence from the default branch will be included in the response. The divergence would be calculated up the this many commits.
        :return: TypesBranchExtended
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_branch_with_http_info(account_identifier, repo_identifier, branch_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_branch_with_http_info(account_identifier, repo_identifier, branch_name, **kwargs)  # noqa: E501
            return data

    def get_branch_with_http_info(self, account_identifier, repo_identifier, branch_name, **kwargs):  # noqa: E501
        """Get branch  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_branch_with_http_info(account_identifier, repo_identifier, branch_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str branch_name: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param bool include_checks: If true, the summary of check for the branch commit SHA would be included in the response.
        :param bool include_rules: If true, a list of rules that apply to this branch would be included in the response.
        :param bool include_pullreqs: If true, a list of pull requests from the branch would be included in the response.
        :param int max_divergence: If greater than zero, branch divergence from the default branch will be included in the response. The divergence would be calculated up the this many commits.
        :return: TypesBranchExtended
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'branch_name', 'org_identifier', 'project_identifier', 'include_checks', 'include_rules', 'include_pullreqs', 'max_divergence']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_branch" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `get_branch`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `get_branch`")  # noqa: E501
        # verify the required parameter 'branch_name' is set
        if ('branch_name' not in params or
                params['branch_name'] is None):
            raise ValueError("Missing the required parameter `branch_name` when calling `get_branch`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'branch_name' in params:
            path_params['branch_name'] = params['branch_name']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'include_checks' in params:
            query_params.append(('include_checks', params['include_checks']))  # noqa: E501
        if 'include_rules' in params:
            query_params.append(('include_rules', params['include_rules']))  # noqa: E501
        if 'include_pullreqs' in params:
            query_params.append(('include_pullreqs', params['include_pullreqs']))  # noqa: E501
        if 'max_divergence' in params:
            query_params.append(('max_divergence', params['max_divergence']))  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/branches/{branch_name}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesBranchExtended',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_commit(self, account_identifier, repo_identifier, commit_sha, **kwargs):  # noqa: E501
        """Get commit  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_commit(account_identifier, repo_identifier, commit_sha, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str commit_sha: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesCommit
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_commit_with_http_info(account_identifier, repo_identifier, commit_sha, **kwargs)  # noqa: E501
        else:
            (data) = self.get_commit_with_http_info(account_identifier, repo_identifier, commit_sha, **kwargs)  # noqa: E501
            return data

    def get_commit_with_http_info(self, account_identifier, repo_identifier, commit_sha, **kwargs):  # noqa: E501
        """Get commit  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_commit_with_http_info(account_identifier, repo_identifier, commit_sha, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str commit_sha: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesCommit
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'commit_sha', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_commit" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `get_commit`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `get_commit`")  # noqa: E501
        # verify the required parameter 'commit_sha' is set
        if ('commit_sha' not in params or
                params['commit_sha'] is None):
            raise ValueError("Missing the required parameter `commit_sha` when calling `get_commit`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'commit_sha' in params:
            path_params['commit_sha'] = params['commit_sha']  # noqa: E501

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
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/code/api/v1/repos/{repo_identifier}/commits/{commit_sha}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesCommit',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_commit_diff(self, account_identifier, repo_identifier, commit_sha, **kwargs):  # noqa: E501
        """Get raw git diff of a commit  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_commit_diff(account_identifier, repo_identifier, commit_sha, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str commit_sha: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_commit_diff_with_http_info(account_identifier, repo_identifier, commit_sha, **kwargs)  # noqa: E501
        else:
            (data) = self.get_commit_diff_with_http_info(account_identifier, repo_identifier, commit_sha, **kwargs)  # noqa: E501
            return data

    def get_commit_diff_with_http_info(self, account_identifier, repo_identifier, commit_sha, **kwargs):  # noqa: E501
        """Get raw git diff of a commit  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_commit_diff_with_http_info(account_identifier, repo_identifier, commit_sha, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str commit_sha: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'commit_sha', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_commit_diff" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `get_commit_diff`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `get_commit_diff`")  # noqa: E501
        # verify the required parameter 'commit_sha' is set
        if ('commit_sha' not in params or
                params['commit_sha'] is None):
            raise ValueError("Missing the required parameter `commit_sha` when calling `get_commit_diff`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'commit_sha' in params:
            path_params['commit_sha'] = params['commit_sha']  # noqa: E501

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
            ['text/plain', 'application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/code/api/v1/repos/{repo_identifier}/commits/{commit_sha}/diff', 'GET',
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

    def get_content(self, account_identifier, repo_identifier, path, **kwargs):  # noqa: E501
        """Get content of a file  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_content(account_identifier, repo_identifier, path, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str path: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str git_ref: The git reference (branch / tag / commitID) that will be used to retrieve the data. If no value is provided the default branch of the repository is used.
        :param bool include_commit: Indicates whether optional commit information should be included in the response.
        :param bool flatten_directories: Flatten directories that contain just one subdirectory.
        :return: OpenapiGetContentOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_content_with_http_info(account_identifier, repo_identifier, path, **kwargs)  # noqa: E501
        else:
            (data) = self.get_content_with_http_info(account_identifier, repo_identifier, path, **kwargs)  # noqa: E501
            return data

    def get_content_with_http_info(self, account_identifier, repo_identifier, path, **kwargs):  # noqa: E501
        """Get content of a file  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_content_with_http_info(account_identifier, repo_identifier, path, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str path: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str git_ref: The git reference (branch / tag / commitID) that will be used to retrieve the data. If no value is provided the default branch of the repository is used.
        :param bool include_commit: Indicates whether optional commit information should be included in the response.
        :param bool flatten_directories: Flatten directories that contain just one subdirectory.
        :return: OpenapiGetContentOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'path', 'org_identifier', 'project_identifier', 'git_ref', 'include_commit', 'flatten_directories']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_content" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `get_content`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `get_content`")  # noqa: E501
        # verify the required parameter 'path' is set
        if ('path' not in params or
                params['path'] is None):
            raise ValueError("Missing the required parameter `path` when calling `get_content`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'path' in params:
            path_params['path'] = params['path']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'git_ref' in params:
            query_params.append(('git_ref', params['git_ref']))  # noqa: E501
        if 'include_commit' in params:
            query_params.append(('include_commit', params['include_commit']))  # noqa: E501
        if 'flatten_directories' in params:
            query_params.append(('flatten_directories', params['flatten_directories']))  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/content/{path}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='OpenapiGetContentOutput',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_raw(self, account_identifier, repo_identifier, path, **kwargs):  # noqa: E501
        """Get raw file content  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_raw(account_identifier, repo_identifier, path, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str path: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str git_ref: The git reference (branch / tag / commitID) that will be used to retrieve the data. If no value is provided the default branch of the repository is used.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_raw_with_http_info(account_identifier, repo_identifier, path, **kwargs)  # noqa: E501
        else:
            (data) = self.get_raw_with_http_info(account_identifier, repo_identifier, path, **kwargs)  # noqa: E501
            return data

    def get_raw_with_http_info(self, account_identifier, repo_identifier, path, **kwargs):  # noqa: E501
        """Get raw file content  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_raw_with_http_info(account_identifier, repo_identifier, path, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str path: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str git_ref: The git reference (branch / tag / commitID) that will be used to retrieve the data. If no value is provided the default branch of the repository is used.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'path', 'org_identifier', 'project_identifier', 'git_ref']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_raw" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `get_raw`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `get_raw`")  # noqa: E501
        # verify the required parameter 'path' is set
        if ('path' not in params or
                params['path'] is None):
            raise ValueError("Missing the required parameter `path` when calling `get_raw`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'path' in params:
            path_params['path'] = params['path']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'git_ref' in params:
            query_params.append(('git_ref', params['git_ref']))  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/raw/{path}', 'GET',
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

    def get_repository(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Get repository  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_repository(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: RepoRepositoryOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_repository_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.get_repository_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
            return data

    def get_repository_with_http_info(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Get repository  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_repository_with_http_info(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: RepoRepositoryOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_repository" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `get_repository`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `get_repository`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501

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
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/code/api/v1/repos/{repo_identifier}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RepoRepositoryOutput',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def import_repository(self, account_identifier, **kwargs):  # noqa: E501
        """Import repository  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.import_repository(account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param ReposImportBody body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: RepoRepositoryOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.import_repository_with_http_info(account_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.import_repository_with_http_info(account_identifier, **kwargs)  # noqa: E501
            return data

    def import_repository_with_http_info(self, account_identifier, **kwargs):  # noqa: E501
        """Import repository  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.import_repository_with_http_info(account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param ReposImportBody body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: RepoRepositoryOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method import_repository" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `import_repository`")  # noqa: E501

        collection_formats = {}

        path_params = {}

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
            '/code/api/v1/repos/import', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RepoRepositoryOutput',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_branches(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """List branches  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_branches(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param bool include_commit: Indicates whether optional commit information should be included in the response.
        :param str query: The substring by which the branches are filtered.
        :param str order: The order of the output.
        :param str sort: The data by which the branches are sorted.
        :param int page: The page to return.
        :param int limit: The maximum number of results to return.
        :param bool include_checks: If true, the summary of check for the branch commit SHA would be included in the response.
        :param bool include_rules: If true, a list of rules that apply to this branch would be included in the response.
        :param bool include_pullreqs: If true, a list of pull requests from the branch would be included in the response.
        :param int max_divergence: If greater than zero, branch divergence from the default branch will be included in the response. The divergence would be calculated up the this many commits.
        :return: list[TypesBranchExtended]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_branches_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.list_branches_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
            return data

    def list_branches_with_http_info(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """List branches  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_branches_with_http_info(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param bool include_commit: Indicates whether optional commit information should be included in the response.
        :param str query: The substring by which the branches are filtered.
        :param str order: The order of the output.
        :param str sort: The data by which the branches are sorted.
        :param int page: The page to return.
        :param int limit: The maximum number of results to return.
        :param bool include_checks: If true, the summary of check for the branch commit SHA would be included in the response.
        :param bool include_rules: If true, a list of rules that apply to this branch would be included in the response.
        :param bool include_pullreqs: If true, a list of pull requests from the branch would be included in the response.
        :param int max_divergence: If greater than zero, branch divergence from the default branch will be included in the response. The divergence would be calculated up the this many commits.
        :return: list[TypesBranchExtended]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'org_identifier', 'project_identifier', 'include_commit', 'query', 'order', 'sort', 'page', 'limit', 'include_checks', 'include_rules', 'include_pullreqs', 'max_divergence']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_branches" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `list_branches`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `list_branches`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'include_commit' in params:
            query_params.append(('include_commit', params['include_commit']))  # noqa: E501
        if 'query' in params:
            query_params.append(('query', params['query']))  # noqa: E501
        if 'order' in params:
            query_params.append(('order', params['order']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'include_checks' in params:
            query_params.append(('include_checks', params['include_checks']))  # noqa: E501
        if 'include_rules' in params:
            query_params.append(('include_rules', params['include_rules']))  # noqa: E501
        if 'include_pullreqs' in params:
            query_params.append(('include_pullreqs', params['include_pullreqs']))  # noqa: E501
        if 'max_divergence' in params:
            query_params.append(('max_divergence', params['max_divergence']))  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/branches', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[TypesBranchExtended]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_commits(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """List commits  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_commits(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str git_ref: The git reference (branch / tag / commitID) that will be used to retrieve the data. If no value is provided the default branch of the repository is used.
        :param str after: The result should only contain commits that occurred after the provided reference.
        :param str path: Path for which commit information should be retrieved
        :param int since: Epoch timestamp since when commit information should be retrieved.
        :param int until: Epoch timestamp until when commit information should be retrieved.
        :param str committer: Committer pattern for which commit information should be retrieved.
        :param list[int] committer_id: Committer principal IDs list for which commit information should be retrieved.
        :param str author: Author pattern for which commit information should be retrieved.
        :param list[int] author_id: Author principal IDs for which commit information should be retrieved.
        :param int page: The page to return.
        :param int limit: The maximum number of results to return.
        :param bool include_stats: Indicates whether optional stats should be included in the response.
        :return: TypesListCommitResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_commits_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.list_commits_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
            return data

    def list_commits_with_http_info(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """List commits  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_commits_with_http_info(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str git_ref: The git reference (branch / tag / commitID) that will be used to retrieve the data. If no value is provided the default branch of the repository is used.
        :param str after: The result should only contain commits that occurred after the provided reference.
        :param str path: Path for which commit information should be retrieved
        :param int since: Epoch timestamp since when commit information should be retrieved.
        :param int until: Epoch timestamp until when commit information should be retrieved.
        :param str committer: Committer pattern for which commit information should be retrieved.
        :param list[int] committer_id: Committer principal IDs list for which commit information should be retrieved.
        :param str author: Author pattern for which commit information should be retrieved.
        :param list[int] author_id: Author principal IDs for which commit information should be retrieved.
        :param int page: The page to return.
        :param int limit: The maximum number of results to return.
        :param bool include_stats: Indicates whether optional stats should be included in the response.
        :return: TypesListCommitResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'org_identifier', 'project_identifier', 'git_ref', 'after', 'path', 'since', 'until', 'committer', 'committer_id', 'author', 'author_id', 'page', 'limit', 'include_stats']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_commits" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `list_commits`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `list_commits`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'git_ref' in params:
            query_params.append(('git_ref', params['git_ref']))  # noqa: E501
        if 'after' in params:
            query_params.append(('after', params['after']))  # noqa: E501
        if 'path' in params:
            query_params.append(('path', params['path']))  # noqa: E501
        if 'since' in params:
            query_params.append(('since', params['since']))  # noqa: E501
        if 'until' in params:
            query_params.append(('until', params['until']))  # noqa: E501
        if 'committer' in params:
            query_params.append(('committer', params['committer']))  # noqa: E501
        if 'committer_id' in params:
            query_params.append(('committer_id', params['committer_id']))  # noqa: E501
            collection_formats['committer_id'] = 'multi'  # noqa: E501
        if 'author' in params:
            query_params.append(('author', params['author']))  # noqa: E501
        if 'author_id' in params:
            query_params.append(('author_id', params['author_id']))  # noqa: E501
            collection_formats['author_id'] = 'multi'  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'include_stats' in params:
            query_params.append(('include_stats', params['include_stats']))  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/commits', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesListCommitResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_paths(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """List all paths  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_paths(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str git_ref: The git reference (branch / tag / commitID) that will be used to retrieve the data. If no value is provided the default branch of the repository is used.
        :param bool include_directories: Indicates whether directories should be included in the response.
        :return: RepoListPathsOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_paths_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.list_paths_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
            return data

    def list_paths_with_http_info(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """List all paths  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_paths_with_http_info(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str git_ref: The git reference (branch / tag / commitID) that will be used to retrieve the data. If no value is provided the default branch of the repository is used.
        :param bool include_directories: Indicates whether directories should be included in the response.
        :return: RepoListPathsOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'org_identifier', 'project_identifier', 'git_ref', 'include_directories']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_paths" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `list_paths`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `list_paths`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'git_ref' in params:
            query_params.append(('git_ref', params['git_ref']))  # noqa: E501
        if 'include_directories' in params:
            query_params.append(('include_directories', params['include_directories']))  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/paths', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RepoListPathsOutput',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_repos(self, account_identifier, **kwargs):  # noqa: E501
        """List repositories  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_repos(account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str query: The substring which is used to filter the repositories by their path name.
        :param str sort: The data by which the repositories are sorted.
        :param str order: The order of the output.
        :param int page: The page to return.
        :param int limit: The maximum number of results to return.
        :param bool only_favorites: The result should contain only the favorite entries for the logged in user.
        :param bool recursive: The result should include entities from child spaces.
        :return: list[RepoRepositoryOutput]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_repos_with_http_info(account_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.list_repos_with_http_info(account_identifier, **kwargs)  # noqa: E501
            return data

    def list_repos_with_http_info(self, account_identifier, **kwargs):  # noqa: E501
        """List repositories  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_repos_with_http_info(account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str query: The substring which is used to filter the repositories by their path name.
        :param str sort: The data by which the repositories are sorted.
        :param str order: The order of the output.
        :param int page: The page to return.
        :param int limit: The maximum number of results to return.
        :param bool only_favorites: The result should contain only the favorite entries for the logged in user.
        :param bool recursive: The result should include entities from child spaces.
        :return: list[RepoRepositoryOutput]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'org_identifier', 'project_identifier', 'query', 'sort', 'order', 'page', 'limit', 'only_favorites', 'recursive']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_repos" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `list_repos`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'query' in params:
            query_params.append(('query', params['query']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501
        if 'order' in params:
            query_params.append(('order', params['order']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'only_favorites' in params:
            query_params.append(('only_favorites', params['only_favorites']))  # noqa: E501
        if 'recursive' in params:
            query_params.append(('recursive', params['recursive']))  # noqa: E501

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
            '/code/api/v1/repos', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[RepoRepositoryOutput]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_tags(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """List tags  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_tags(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param bool include_commit: Indicates whether optional commit information should be included in the response.
        :param str query: The substring by which the tags are filtered.
        :param str order: The order of the output.
        :param str sort: The data by which the tags are sorted.
        :param int page: The page to return.
        :param int limit: The maximum number of results to return.
        :return: list[TypesCommitTag]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_tags_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.list_tags_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
            return data

    def list_tags_with_http_info(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """List tags  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_tags_with_http_info(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param bool include_commit: Indicates whether optional commit information should be included in the response.
        :param str query: The substring by which the tags are filtered.
        :param str order: The order of the output.
        :param str sort: The data by which the tags are sorted.
        :param int page: The page to return.
        :param int limit: The maximum number of results to return.
        :return: list[TypesCommitTag]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'org_identifier', 'project_identifier', 'include_commit', 'query', 'order', 'sort', 'page', 'limit']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_tags" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `list_tags`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `list_tags`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'include_commit' in params:
            query_params.append(('include_commit', params['include_commit']))  # noqa: E501
        if 'query' in params:
            query_params.append(('query', params['query']))  # noqa: E501
        if 'order' in params:
            query_params.append(('order', params['order']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/tags', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[TypesCommitTag]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def merge_check(self, account_identifier, repo_identifier, range, **kwargs):  # noqa: E501
        """Check mergeability  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.merge_check(account_identifier, repo_identifier, range, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str range: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param list[str] path: provide path for diff operation
        :return: RepoMergeCheck
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.merge_check_with_http_info(account_identifier, repo_identifier, range, **kwargs)  # noqa: E501
        else:
            (data) = self.merge_check_with_http_info(account_identifier, repo_identifier, range, **kwargs)  # noqa: E501
            return data

    def merge_check_with_http_info(self, account_identifier, repo_identifier, range, **kwargs):  # noqa: E501
        """Check mergeability  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.merge_check_with_http_info(account_identifier, repo_identifier, range, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str range: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param list[str] path: provide path for diff operation
        :return: RepoMergeCheck
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'range', 'org_identifier', 'project_identifier', 'path']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method merge_check" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `merge_check`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `merge_check`")  # noqa: E501
        # verify the required parameter 'range' is set
        if ('range' not in params or
                params['range'] is None):
            raise ValueError("Missing the required parameter `range` when calling `merge_check`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'range' in params:
            path_params['range'] = params['range']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'path' in params:
            query_params.append(('path', params['path']))  # noqa: E501
            collection_formats['path'] = 'multi'  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/merge-check/{range}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RepoMergeCheck',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def path_details(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Get commit details  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.path_details(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param OpenapiPathsDetailsRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str git_ref: The git reference (branch / tag / commitID) that will be used to retrieve the data. If no value is provided the default branch of the repository is used.
        :return: RepoPathsDetailsOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.path_details_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.path_details_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
            return data

    def path_details_with_http_info(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Get commit details  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.path_details_with_http_info(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param OpenapiPathsDetailsRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param str git_ref: The git reference (branch / tag / commitID) that will be used to retrieve the data. If no value is provided the default branch of the repository is used.
        :return: RepoPathsDetailsOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'body', 'org_identifier', 'project_identifier', 'git_ref']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method path_details" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `path_details`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `path_details`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'git_ref' in params:
            query_params.append(('git_ref', params['git_ref']))  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/path-details', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RepoPathsDetailsOutput',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def purge_repository(self, account_identifier, deleted_at, repo_identifier, **kwargs):  # noqa: E501
        """Purge repository  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.purge_repository(account_identifier, deleted_at, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param int deleted_at: The exact time the resource was delete at in epoch format. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.purge_repository_with_http_info(account_identifier, deleted_at, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.purge_repository_with_http_info(account_identifier, deleted_at, repo_identifier, **kwargs)  # noqa: E501
            return data

    def purge_repository_with_http_info(self, account_identifier, deleted_at, repo_identifier, **kwargs):  # noqa: E501
        """Purge repository  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.purge_repository_with_http_info(account_identifier, deleted_at, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param int deleted_at: The exact time the resource was delete at in epoch format. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'deleted_at', 'repo_identifier', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method purge_repository" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `purge_repository`")  # noqa: E501
        # verify the required parameter 'deleted_at' is set
        if ('deleted_at' not in params or
                params['deleted_at'] is None):
            raise ValueError("Missing the required parameter `deleted_at` when calling `purge_repository`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `purge_repository`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'deleted_at' in params:
            query_params.append(('deleted_at', params['deleted_at']))  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/purge', 'POST',
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

    def raw_diff(self, account_identifier, repo_identifier, range, **kwargs):  # noqa: E501
        """Get raw diff  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.raw_diff(account_identifier, repo_identifier, range, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str range: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param list[str] path: provide path for diff operation
        :return: list[GitFileDiff]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.raw_diff_with_http_info(account_identifier, repo_identifier, range, **kwargs)  # noqa: E501
        else:
            (data) = self.raw_diff_with_http_info(account_identifier, repo_identifier, range, **kwargs)  # noqa: E501
            return data

    def raw_diff_with_http_info(self, account_identifier, repo_identifier, range, **kwargs):  # noqa: E501
        """Get raw diff  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.raw_diff_with_http_info(account_identifier, repo_identifier, range, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str range: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param list[str] path: provide path for diff operation
        :return: list[GitFileDiff]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'range', 'org_identifier', 'project_identifier', 'path']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method raw_diff" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `raw_diff`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `raw_diff`")  # noqa: E501
        # verify the required parameter 'range' is set
        if ('range' not in params or
                params['range'] is None):
            raise ValueError("Missing the required parameter `range` when calling `raw_diff`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'range' in params:
            path_params['range'] = params['range']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'path' in params:
            query_params.append(('path', params['path']))  # noqa: E501
            collection_formats['path'] = 'multi'  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/plain'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/code/api/v1/repos/{repo_identifier}/diff/{range}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[GitFileDiff]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def raw_diff_post(self, account_identifier, repo_identifier, range, **kwargs):  # noqa: E501
        """Get raw diff  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.raw_diff_post(account_identifier, repo_identifier, range, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str range: (required)
        :param list[ApiFileDiffRequest] body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: list[GitFileDiff]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.raw_diff_post_with_http_info(account_identifier, repo_identifier, range, **kwargs)  # noqa: E501
        else:
            (data) = self.raw_diff_post_with_http_info(account_identifier, repo_identifier, range, **kwargs)  # noqa: E501
            return data

    def raw_diff_post_with_http_info(self, account_identifier, repo_identifier, range, **kwargs):  # noqa: E501
        """Get raw diff  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.raw_diff_post_with_http_info(account_identifier, repo_identifier, range, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str range: (required)
        :param list[ApiFileDiffRequest] body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: list[GitFileDiff]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'range', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method raw_diff_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `raw_diff_post`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `raw_diff_post`")  # noqa: E501
        # verify the required parameter 'range' is set
        if ('range' not in params or
                params['range'] is None):
            raise ValueError("Missing the required parameter `range` when calling `raw_diff_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'range' in params:
            path_params['range'] = params['range']  # noqa: E501

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
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/plain'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/code/api/v1/repos/{repo_identifier}/diff/{range}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[GitFileDiff]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def rebase_branch(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Rebase a branch relative to another branch or a commit  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.rebase_branch(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param RepoIdentifierRebaseBody body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesRebaseResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.rebase_branch_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.rebase_branch_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
            return data

    def rebase_branch_with_http_info(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Rebase a branch relative to another branch or a commit  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.rebase_branch_with_http_info(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param RepoIdentifierRebaseBody body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesRebaseResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method rebase_branch" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `rebase_branch`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `rebase_branch`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/rebase', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesRebaseResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def restore_repository(self, account_identifier, deleted_at, repo_identifier, **kwargs):  # noqa: E501
        """Restore repository  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.restore_repository(account_identifier, deleted_at, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param int deleted_at: The exact time the resource was delete at in epoch format. (required)
        :param str repo_identifier: (required)
        :param OpenapiRestoreRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: RepoRepositoryOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.restore_repository_with_http_info(account_identifier, deleted_at, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.restore_repository_with_http_info(account_identifier, deleted_at, repo_identifier, **kwargs)  # noqa: E501
            return data

    def restore_repository_with_http_info(self, account_identifier, deleted_at, repo_identifier, **kwargs):  # noqa: E501
        """Restore repository  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.restore_repository_with_http_info(account_identifier, deleted_at, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param int deleted_at: The exact time the resource was delete at in epoch format. (required)
        :param str repo_identifier: (required)
        :param OpenapiRestoreRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: RepoRepositoryOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'deleted_at', 'repo_identifier', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method restore_repository" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `restore_repository`")  # noqa: E501
        # verify the required parameter 'deleted_at' is set
        if ('deleted_at' not in params or
                params['deleted_at'] is None):
            raise ValueError("Missing the required parameter `deleted_at` when calling `restore_repository`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `restore_repository`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'deleted_at' in params:
            query_params.append(('deleted_at', params['deleted_at']))  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/restore', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RepoRepositoryOutput',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def squash_branch(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Squashes commits in a branch relative to another branch or a commit  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.squash_branch(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param RepoIdentifierSquashBody body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesSquashResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.squash_branch_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.squash_branch_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
            return data

    def squash_branch_with_http_info(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Squashes commits in a branch relative to another branch or a commit  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.squash_branch_with_http_info(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param RepoIdentifierSquashBody body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesSquashResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method squash_branch" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `squash_branch`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `squash_branch`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/squash', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesSquashResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def summary(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Get repository summary  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.summary(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesRepositorySummary
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.summary_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.summary_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
            return data

    def summary_with_http_info(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Get repository summary  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.summary_with_http_info(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesRepositorySummary
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method summary" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `summary`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `summary`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501

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
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/code/api/v1/repos/{repo_identifier}/summary', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesRepositorySummary',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_default_branch(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Update default branch  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_default_branch(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param OpenapiUpdateDefaultBranchRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: RepoRepositoryOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_default_branch_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.update_default_branch_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
            return data

    def update_default_branch_with_http_info(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Update default branch  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_default_branch_with_http_info(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param OpenapiUpdateDefaultBranchRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: RepoRepositoryOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_default_branch" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `update_default_branch`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `update_default_branch`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/default-branch', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RepoRepositoryOutput',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_general_settings(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Update general settings  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_general_settings(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param OpenapiGeneralSettingsRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: ReposettingsGeneralSettings
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_general_settings_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.update_general_settings_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
            return data

    def update_general_settings_with_http_info(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Update general settings  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_general_settings_with_http_info(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param OpenapiGeneralSettingsRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: ReposettingsGeneralSettings
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_general_settings" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `update_general_settings`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `update_general_settings`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/settings/general', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ReposettingsGeneralSettings',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_repository(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Update repository  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_repository(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param OpenapiUpdateRepoRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: RepoRepositoryOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_repository_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.update_repository_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
            return data

    def update_repository_with_http_info(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Update repository  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_repository_with_http_info(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param OpenapiUpdateRepoRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: RepoRepositoryOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_repository" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `update_repository`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `update_repository`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RepoRepositoryOutput',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_security_settings(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Update security settings  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_security_settings(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param OpenapiSecuritySettingsRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: ReposettingsSecuritySettings
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_security_settings_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.update_security_settings_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
            return data

    def update_security_settings_with_http_info(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Update security settings  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_security_settings_with_http_info(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param OpenapiSecuritySettingsRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: ReposettingsSecuritySettings
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_security_settings" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `update_security_settings`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `update_security_settings`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/settings/security', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ReposettingsSecuritySettings',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
