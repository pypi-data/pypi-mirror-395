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


class PullreqApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def checks_pull_req(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Get status checks  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.checks_pull_req(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesPullReqChecks
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.checks_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
        else:
            (data) = self.checks_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
            return data

    def checks_pull_req_with_http_info(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Get status checks  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.checks_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesPullReqChecks
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method checks_pull_req" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `checks_pull_req`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `checks_pull_req`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `checks_pull_req`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/checks', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesPullReqChecks',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def codeowners_pull_req(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Get code owners  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.codeowners_pull_req(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesCodeOwnerEvaluation
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.codeowners_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
        else:
            (data) = self.codeowners_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
            return data

    def codeowners_pull_req_with_http_info(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Get code owners  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.codeowners_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesCodeOwnerEvaluation
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method codeowners_pull_req" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `codeowners_pull_req`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `codeowners_pull_req`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `codeowners_pull_req`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/codeowners', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesCodeOwnerEvaluation',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def comment_apply_suggestions(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Apply pull request code comment suggestions  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.comment_apply_suggestions(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param OpenapiCommentApplySuggestionstRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: PullreqCommentApplySuggestionsOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.comment_apply_suggestions_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
        else:
            (data) = self.comment_apply_suggestions_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
            return data

    def comment_apply_suggestions_with_http_info(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Apply pull request code comment suggestions  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.comment_apply_suggestions_with_http_info(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param OpenapiCommentApplySuggestionstRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: PullreqCommentApplySuggestionsOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method comment_apply_suggestions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `comment_apply_suggestions`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `comment_apply_suggestions`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `comment_apply_suggestions`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/comments/apply-suggestions', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='PullreqCommentApplySuggestionsOutput',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def comment_create_pull_req(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Create new pull request comment  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.comment_create_pull_req(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param OpenapiCommentCreatePullReqRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesPullReqActivity
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.comment_create_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
        else:
            (data) = self.comment_create_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
            return data

    def comment_create_pull_req_with_http_info(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Create new pull request comment  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.comment_create_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param OpenapiCommentCreatePullReqRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesPullReqActivity
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method comment_create_pull_req" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `comment_create_pull_req`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `comment_create_pull_req`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `comment_create_pull_req`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/comments', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesPullReqActivity',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def comment_delete_pull_req(self, account_identifier, repo_identifier, pullreq_number, pullreq_comment_id, **kwargs):  # noqa: E501
        """Delete pull request comment  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.comment_delete_pull_req(account_identifier, repo_identifier, pullreq_number, pullreq_comment_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param int pullreq_comment_id: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.comment_delete_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, pullreq_comment_id, **kwargs)  # noqa: E501
        else:
            (data) = self.comment_delete_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, pullreq_comment_id, **kwargs)  # noqa: E501
            return data

    def comment_delete_pull_req_with_http_info(self, account_identifier, repo_identifier, pullreq_number, pullreq_comment_id, **kwargs):  # noqa: E501
        """Delete pull request comment  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.comment_delete_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, pullreq_comment_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param int pullreq_comment_id: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'pullreq_comment_id', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method comment_delete_pull_req" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `comment_delete_pull_req`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `comment_delete_pull_req`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `comment_delete_pull_req`")  # noqa: E501
        # verify the required parameter 'pullreq_comment_id' is set
        if ('pullreq_comment_id' not in params or
                params['pullreq_comment_id'] is None):
            raise ValueError("Missing the required parameter `pullreq_comment_id` when calling `comment_delete_pull_req`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501
        if 'pullreq_comment_id' in params:
            path_params['pullreq_comment_id'] = params['pullreq_comment_id']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/comments/{pullreq_comment_id}', 'DELETE',
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

    def comment_status_pull_req(self, account_identifier, repo_identifier, pullreq_number, pullreq_comment_id, **kwargs):  # noqa: E501
        """Update status of pull request comment  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.comment_status_pull_req(account_identifier, repo_identifier, pullreq_number, pullreq_comment_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param int pullreq_comment_id: (required)
        :param OpenapiCommentStatusPullReqRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesPullReqActivity
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.comment_status_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, pullreq_comment_id, **kwargs)  # noqa: E501
        else:
            (data) = self.comment_status_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, pullreq_comment_id, **kwargs)  # noqa: E501
            return data

    def comment_status_pull_req_with_http_info(self, account_identifier, repo_identifier, pullreq_number, pullreq_comment_id, **kwargs):  # noqa: E501
        """Update status of pull request comment  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.comment_status_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, pullreq_comment_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param int pullreq_comment_id: (required)
        :param OpenapiCommentStatusPullReqRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesPullReqActivity
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'pullreq_comment_id', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method comment_status_pull_req" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `comment_status_pull_req`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `comment_status_pull_req`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `comment_status_pull_req`")  # noqa: E501
        # verify the required parameter 'pullreq_comment_id' is set
        if ('pullreq_comment_id' not in params or
                params['pullreq_comment_id'] is None):
            raise ValueError("Missing the required parameter `pullreq_comment_id` when calling `comment_status_pull_req`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501
        if 'pullreq_comment_id' in params:
            path_params['pullreq_comment_id'] = params['pullreq_comment_id']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/comments/{pullreq_comment_id}/status', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesPullReqActivity',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def comment_update_pull_req(self, account_identifier, repo_identifier, pullreq_number, pullreq_comment_id, **kwargs):  # noqa: E501
        """Update pull request comment  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.comment_update_pull_req(account_identifier, repo_identifier, pullreq_number, pullreq_comment_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param int pullreq_comment_id: (required)
        :param OpenapiCommentUpdatePullReqRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesPullReqActivity
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.comment_update_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, pullreq_comment_id, **kwargs)  # noqa: E501
        else:
            (data) = self.comment_update_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, pullreq_comment_id, **kwargs)  # noqa: E501
            return data

    def comment_update_pull_req_with_http_info(self, account_identifier, repo_identifier, pullreq_number, pullreq_comment_id, **kwargs):  # noqa: E501
        """Update pull request comment  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.comment_update_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, pullreq_comment_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param int pullreq_comment_id: (required)
        :param OpenapiCommentUpdatePullReqRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesPullReqActivity
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'pullreq_comment_id', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method comment_update_pull_req" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `comment_update_pull_req`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `comment_update_pull_req`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `comment_update_pull_req`")  # noqa: E501
        # verify the required parameter 'pullreq_comment_id' is set
        if ('pullreq_comment_id' not in params or
                params['pullreq_comment_id'] is None):
            raise ValueError("Missing the required parameter `pullreq_comment_id` when calling `comment_update_pull_req`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501
        if 'pullreq_comment_id' in params:
            path_params['pullreq_comment_id'] = params['pullreq_comment_id']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/comments/{pullreq_comment_id}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesPullReqActivity',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def count_pull_req_space(self, account_identifier, **kwargs):  # noqa: E501
        """Count pull requests in account/org/project  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.count_pull_req_space(account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param list[str] state: The state of the pull requests to include in the result.
        :param str source_repo_ref: Source repository ref of the pull requests.
        :param str source_branch: Source branch of the pull requests.
        :param str target_branch: Target branch of the pull requests.
        :param str query: The substring by which the pull requests are filtered.
        :param list[int] created_by: List of principal IDs who created pull requests.
        :param int created_lt: The result should contain only entries created before this timestamp (unix millis).
        :param int created_gt: The result should contain only entries created after this timestamp (unix millis).
        :param int updated_lt: The result should contain only entries updated before this timestamp (unix millis).
        :param bool include_subspaces: The result should contain entries from the desired space and of its subspaces.
        :param list[int] label_id: List of label ids used to filter pull requests.
        :param list[int] value_id: List of label value ids used to filter pull requests.
        :param int author_id: Return only pull requests where this user is the author.
        :param int commenter_id: Return only pull requests where this user has created at least one comment.
        :param int mentioned_id: Return only pull requests where this user has been mentioned.
        :param int reviewer_id: Return only pull requests where this user has been added as a reviewer.
        :param list[str] review_decision: Require only this review decision of the reviewer. Requires reviewer_id parameter.
        :param bool include_rules: If true, a list of rules that apply to this branch would be included in the response.
        :return: int
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.count_pull_req_space_with_http_info(account_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.count_pull_req_space_with_http_info(account_identifier, **kwargs)  # noqa: E501
            return data

    def count_pull_req_space_with_http_info(self, account_identifier, **kwargs):  # noqa: E501
        """Count pull requests in account/org/project  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.count_pull_req_space_with_http_info(account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param list[str] state: The state of the pull requests to include in the result.
        :param str source_repo_ref: Source repository ref of the pull requests.
        :param str source_branch: Source branch of the pull requests.
        :param str target_branch: Target branch of the pull requests.
        :param str query: The substring by which the pull requests are filtered.
        :param list[int] created_by: List of principal IDs who created pull requests.
        :param int created_lt: The result should contain only entries created before this timestamp (unix millis).
        :param int created_gt: The result should contain only entries created after this timestamp (unix millis).
        :param int updated_lt: The result should contain only entries updated before this timestamp (unix millis).
        :param bool include_subspaces: The result should contain entries from the desired space and of its subspaces.
        :param list[int] label_id: List of label ids used to filter pull requests.
        :param list[int] value_id: List of label value ids used to filter pull requests.
        :param int author_id: Return only pull requests where this user is the author.
        :param int commenter_id: Return only pull requests where this user has created at least one comment.
        :param int mentioned_id: Return only pull requests where this user has been mentioned.
        :param int reviewer_id: Return only pull requests where this user has been added as a reviewer.
        :param list[str] review_decision: Require only this review decision of the reviewer. Requires reviewer_id parameter.
        :param bool include_rules: If true, a list of rules that apply to this branch would be included in the response.
        :return: int
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'org_identifier', 'project_identifier', 'state', 'source_repo_ref', 'source_branch', 'target_branch', 'query', 'created_by', 'created_lt', 'created_gt', 'updated_lt', 'include_subspaces', 'label_id', 'value_id', 'author_id', 'commenter_id', 'mentioned_id', 'reviewer_id', 'review_decision', 'include_rules']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method count_pull_req_space" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `count_pull_req_space`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'state' in params:
            query_params.append(('state', params['state']))  # noqa: E501
            collection_formats['state'] = 'multi'  # noqa: E501
        if 'source_repo_ref' in params:
            query_params.append(('source_repo_ref', params['source_repo_ref']))  # noqa: E501
        if 'source_branch' in params:
            query_params.append(('source_branch', params['source_branch']))  # noqa: E501
        if 'target_branch' in params:
            query_params.append(('target_branch', params['target_branch']))  # noqa: E501
        if 'query' in params:
            query_params.append(('query', params['query']))  # noqa: E501
        if 'created_by' in params:
            query_params.append(('created_by', params['created_by']))  # noqa: E501
            collection_formats['created_by'] = 'multi'  # noqa: E501
        if 'created_lt' in params:
            query_params.append(('created_lt', params['created_lt']))  # noqa: E501
        if 'created_gt' in params:
            query_params.append(('created_gt', params['created_gt']))  # noqa: E501
        if 'updated_lt' in params:
            query_params.append(('updated_lt', params['updated_lt']))  # noqa: E501
        if 'include_subspaces' in params:
            query_params.append(('include_subspaces', params['include_subspaces']))  # noqa: E501
        if 'label_id' in params:
            query_params.append(('label_id', params['label_id']))  # noqa: E501
            collection_formats['label_id'] = 'multi'  # noqa: E501
        if 'value_id' in params:
            query_params.append(('value_id', params['value_id']))  # noqa: E501
            collection_formats['value_id'] = 'multi'  # noqa: E501
        if 'author_id' in params:
            query_params.append(('author_id', params['author_id']))  # noqa: E501
        if 'commenter_id' in params:
            query_params.append(('commenter_id', params['commenter_id']))  # noqa: E501
        if 'mentioned_id' in params:
            query_params.append(('mentioned_id', params['mentioned_id']))  # noqa: E501
        if 'reviewer_id' in params:
            query_params.append(('reviewer_id', params['reviewer_id']))  # noqa: E501
        if 'review_decision' in params:
            query_params.append(('review_decision', params['review_decision']))  # noqa: E501
            collection_formats['review_decision'] = 'multi'  # noqa: E501
        if 'include_rules' in params:
            query_params.append(('include_rules', params['include_rules']))  # noqa: E501

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
            '/code/api/v1/pullreq/count', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='int',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_pull_req(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Create pull request  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_pull_req(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param OpenapiCreatePullReqRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesPullReq
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_pull_req_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.create_pull_req_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
            return data

    def create_pull_req_with_http_info(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """Create pull request  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_pull_req_with_http_info(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param OpenapiCreatePullReqRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesPullReq
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
                    " to method create_pull_req" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `create_pull_req`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `create_pull_req`")  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesPullReq',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def diff_pull_req(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Get file changes  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.diff_pull_req(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param list[str] path: provide path for diff operation
        :return: list[GitFileDiff]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.diff_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
        else:
            (data) = self.diff_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
            return data

    def diff_pull_req_with_http_info(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Get file changes  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.diff_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param list[str] path: provide path for diff operation
        :return: list[GitFileDiff]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'org_identifier', 'project_identifier', 'path']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method diff_pull_req" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `diff_pull_req`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `diff_pull_req`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `diff_pull_req`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/diff', 'GET',
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

    def diff_pull_req_post(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Get file changes  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.diff_pull_req_post(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param list[ApiFileDiffRequest] body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: list[GitFileDiff]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.diff_pull_req_post_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
        else:
            (data) = self.diff_pull_req_post_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
            return data

    def diff_pull_req_post_with_http_info(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Get file changes  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.diff_pull_req_post_with_http_info(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param list[ApiFileDiffRequest] body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: list[GitFileDiff]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method diff_pull_req_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `diff_pull_req_post`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `diff_pull_req_post`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `diff_pull_req_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/diff', 'POST',
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

    def file_view_add_pull_req(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Mark file as viewed  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.file_view_add_pull_req(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param OpenapiFileViewAddPullReqRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesPullReqFileView
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.file_view_add_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
        else:
            (data) = self.file_view_add_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
            return data

    def file_view_add_pull_req_with_http_info(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Mark file as viewed  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.file_view_add_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param OpenapiFileViewAddPullReqRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesPullReqFileView
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method file_view_add_pull_req" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `file_view_add_pull_req`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `file_view_add_pull_req`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `file_view_add_pull_req`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/file-views', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesPullReqFileView',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def file_view_delete_pull_req(self, account_identifier, repo_identifier, pullreq_number, file_path, **kwargs):  # noqa: E501
        """Remove file view  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.file_view_delete_pull_req(account_identifier, repo_identifier, pullreq_number, file_path, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param str file_path: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.file_view_delete_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, file_path, **kwargs)  # noqa: E501
        else:
            (data) = self.file_view_delete_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, file_path, **kwargs)  # noqa: E501
            return data

    def file_view_delete_pull_req_with_http_info(self, account_identifier, repo_identifier, pullreq_number, file_path, **kwargs):  # noqa: E501
        """Remove file view  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.file_view_delete_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, file_path, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param str file_path: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'file_path', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method file_view_delete_pull_req" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `file_view_delete_pull_req`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `file_view_delete_pull_req`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `file_view_delete_pull_req`")  # noqa: E501
        # verify the required parameter 'file_path' is set
        if ('file_path' not in params or
                params['file_path'] is None):
            raise ValueError("Missing the required parameter `file_path` when calling `file_view_delete_pull_req`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501
        if 'file_path' in params:
            path_params['file_path'] = params['file_path']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/file-views/{file_path}', 'DELETE',
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

    def file_view_list_pull_req(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """List viewed files  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.file_view_list_pull_req(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: list[TypesPullReqFileView]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.file_view_list_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
        else:
            (data) = self.file_view_list_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
            return data

    def file_view_list_pull_req_with_http_info(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """List viewed files  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.file_view_list_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: list[TypesPullReqFileView]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method file_view_list_pull_req" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `file_view_list_pull_req`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `file_view_list_pull_req`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `file_view_list_pull_req`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/file-views', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[TypesPullReqFileView]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_pull_req(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Get pull request  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_pull_req(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesPullReq
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
        else:
            (data) = self.get_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
            return data

    def get_pull_req_with_http_info(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Get pull request  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesPullReq
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_pull_req" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `get_pull_req`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `get_pull_req`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `get_pull_req`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesPullReq',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_pull_req(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """List pull requests  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_pull_req(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param list[str] state: The state of the pull requests to include in the result.
        :param str source_repo_ref: Source repository ref of the pull requests.
        :param str source_branch: Source branch of the pull requests.
        :param str target_branch: Target branch of the pull requests.
        :param str query: The substring by which the pull requests are filtered.
        :param list[int] created_by: List of principal IDs who created pull requests.
        :param str order: The order of the output.
        :param str sort: The data by which the pull requests are sorted.
        :param int created_lt: The result should contain only entries created before this timestamp (unix millis).
        :param int created_gt: The result should contain only entries created after this timestamp (unix millis).
        :param int updated_lt: The result should contain only entries updated before this timestamp (unix millis).
        :param int updated_gt: The result should contain only entries updated after this timestamp (unix millis).
        :param bool exclude_description: By providing this parameter the description would be excluded from the response.
        :param int page: The page to return.
        :param int limit: The maximum number of results to return.
        :param list[int] label_id: List of label ids used to filter pull requests.
        :param list[int] value_id: List of label value ids used to filter pull requests.
        :param int author_id: Return only pull requests where this user is the author.
        :param int commenter_id: Return only pull requests where this user has created at least one comment.
        :param int mentioned_id: Return only pull requests where this user has been mentioned.
        :param int reviewer_id: Return only pull requests where this user has been added as a reviewer.
        :param list[str] review_decision: Require only this review decision of the reviewer. Requires reviewer_id parameter.
        :param bool include_git_stats: If true, the git diff stats would be included in the response.
        :param bool include_checks: If true, the summary of check for the branch commit SHA would be included in the response.
        :param bool include_rules: If true, a list of rules that apply to this branch would be included in the response.
        :return: list[TypesPullReq]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_pull_req_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.list_pull_req_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
            return data

    def list_pull_req_with_http_info(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """List pull requests  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_pull_req_with_http_info(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param list[str] state: The state of the pull requests to include in the result.
        :param str source_repo_ref: Source repository ref of the pull requests.
        :param str source_branch: Source branch of the pull requests.
        :param str target_branch: Target branch of the pull requests.
        :param str query: The substring by which the pull requests are filtered.
        :param list[int] created_by: List of principal IDs who created pull requests.
        :param str order: The order of the output.
        :param str sort: The data by which the pull requests are sorted.
        :param int created_lt: The result should contain only entries created before this timestamp (unix millis).
        :param int created_gt: The result should contain only entries created after this timestamp (unix millis).
        :param int updated_lt: The result should contain only entries updated before this timestamp (unix millis).
        :param int updated_gt: The result should contain only entries updated after this timestamp (unix millis).
        :param bool exclude_description: By providing this parameter the description would be excluded from the response.
        :param int page: The page to return.
        :param int limit: The maximum number of results to return.
        :param list[int] label_id: List of label ids used to filter pull requests.
        :param list[int] value_id: List of label value ids used to filter pull requests.
        :param int author_id: Return only pull requests where this user is the author.
        :param int commenter_id: Return only pull requests where this user has created at least one comment.
        :param int mentioned_id: Return only pull requests where this user has been mentioned.
        :param int reviewer_id: Return only pull requests where this user has been added as a reviewer.
        :param list[str] review_decision: Require only this review decision of the reviewer. Requires reviewer_id parameter.
        :param bool include_git_stats: If true, the git diff stats would be included in the response.
        :param bool include_checks: If true, the summary of check for the branch commit SHA would be included in the response.
        :param bool include_rules: If true, a list of rules that apply to this branch would be included in the response.
        :return: list[TypesPullReq]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'org_identifier', 'project_identifier', 'state', 'source_repo_ref', 'source_branch', 'target_branch', 'query', 'created_by', 'order', 'sort', 'created_lt', 'created_gt', 'updated_lt', 'updated_gt', 'exclude_description', 'page', 'limit', 'label_id', 'value_id', 'author_id', 'commenter_id', 'mentioned_id', 'reviewer_id', 'review_decision', 'include_git_stats', 'include_checks', 'include_rules']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_pull_req" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `list_pull_req`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `list_pull_req`")  # noqa: E501

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
        if 'state' in params:
            query_params.append(('state', params['state']))  # noqa: E501
            collection_formats['state'] = 'multi'  # noqa: E501
        if 'source_repo_ref' in params:
            query_params.append(('source_repo_ref', params['source_repo_ref']))  # noqa: E501
        if 'source_branch' in params:
            query_params.append(('source_branch', params['source_branch']))  # noqa: E501
        if 'target_branch' in params:
            query_params.append(('target_branch', params['target_branch']))  # noqa: E501
        if 'query' in params:
            query_params.append(('query', params['query']))  # noqa: E501
        if 'created_by' in params:
            query_params.append(('created_by', params['created_by']))  # noqa: E501
            collection_formats['created_by'] = 'multi'  # noqa: E501
        if 'order' in params:
            query_params.append(('order', params['order']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501
        if 'created_lt' in params:
            query_params.append(('created_lt', params['created_lt']))  # noqa: E501
        if 'created_gt' in params:
            query_params.append(('created_gt', params['created_gt']))  # noqa: E501
        if 'updated_lt' in params:
            query_params.append(('updated_lt', params['updated_lt']))  # noqa: E501
        if 'updated_gt' in params:
            query_params.append(('updated_gt', params['updated_gt']))  # noqa: E501
        if 'exclude_description' in params:
            query_params.append(('exclude_description', params['exclude_description']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'label_id' in params:
            query_params.append(('label_id', params['label_id']))  # noqa: E501
            collection_formats['label_id'] = 'multi'  # noqa: E501
        if 'value_id' in params:
            query_params.append(('value_id', params['value_id']))  # noqa: E501
            collection_formats['value_id'] = 'multi'  # noqa: E501
        if 'author_id' in params:
            query_params.append(('author_id', params['author_id']))  # noqa: E501
        if 'commenter_id' in params:
            query_params.append(('commenter_id', params['commenter_id']))  # noqa: E501
        if 'mentioned_id' in params:
            query_params.append(('mentioned_id', params['mentioned_id']))  # noqa: E501
        if 'reviewer_id' in params:
            query_params.append(('reviewer_id', params['reviewer_id']))  # noqa: E501
        if 'review_decision' in params:
            query_params.append(('review_decision', params['review_decision']))  # noqa: E501
            collection_formats['review_decision'] = 'multi'  # noqa: E501
        if 'include_git_stats' in params:
            query_params.append(('include_git_stats', params['include_git_stats']))  # noqa: E501
        if 'include_checks' in params:
            query_params.append(('include_checks', params['include_checks']))  # noqa: E501
        if 'include_rules' in params:
            query_params.append(('include_rules', params['include_rules']))  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[TypesPullReq]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_pull_req_activities(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """List activities  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_pull_req_activities(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param list[str] kind: The kind of the pull request activity to include in the result.
        :param list[str] type: The type of the pull request activity to include in the result.
        :param int after: The result should contain only entries created at and after this timestamp (unix millis).
        :param int before: The result should contain only entries created before this timestamp (unix millis).
        :param int limit: The maximum number of results to return.
        :return: list[TypesPullReqActivity]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_pull_req_activities_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
        else:
            (data) = self.list_pull_req_activities_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
            return data

    def list_pull_req_activities_with_http_info(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """List activities  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_pull_req_activities_with_http_info(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param list[str] kind: The kind of the pull request activity to include in the result.
        :param list[str] type: The type of the pull request activity to include in the result.
        :param int after: The result should contain only entries created at and after this timestamp (unix millis).
        :param int before: The result should contain only entries created before this timestamp (unix millis).
        :param int limit: The maximum number of results to return.
        :return: list[TypesPullReqActivity]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'org_identifier', 'project_identifier', 'kind', 'type', 'after', 'before', 'limit']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_pull_req_activities" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `list_pull_req_activities`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `list_pull_req_activities`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `list_pull_req_activities`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'kind' in params:
            query_params.append(('kind', params['kind']))  # noqa: E501
            collection_formats['kind'] = 'multi'  # noqa: E501
        if 'type' in params:
            query_params.append(('type', params['type']))  # noqa: E501
            collection_formats['type'] = 'multi'  # noqa: E501
        if 'after' in params:
            query_params.append(('after', params['after']))  # noqa: E501
        if 'before' in params:
            query_params.append(('before', params['before']))  # noqa: E501
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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/activities', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[TypesPullReqActivity]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_pull_req_commits(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """List commits  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_pull_req_commits(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param int page: The page to return.
        :param int limit: The maximum number of results to return.
        :return: list[TypesCommit]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_pull_req_commits_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
        else:
            (data) = self.list_pull_req_commits_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
            return data

    def list_pull_req_commits_with_http_info(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """List commits  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_pull_req_commits_with_http_info(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param int page: The page to return.
        :param int limit: The maximum number of results to return.
        :return: list[TypesCommit]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'org_identifier', 'project_identifier', 'page', 'limit']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_pull_req_commits" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `list_pull_req_commits`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `list_pull_req_commits`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `list_pull_req_commits`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/commits', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[TypesCommit]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_pull_req_space(self, account_identifier, **kwargs):  # noqa: E501
        """List pull requests in account/org/project  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_pull_req_space(account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param list[str] state: The state of the pull requests to include in the result.
        :param str source_repo_ref: Source repository ref of the pull requests.
        :param str source_branch: Source branch of the pull requests.
        :param str target_branch: Target branch of the pull requests.
        :param str query: The substring by which the pull requests are filtered.
        :param list[int] created_by: List of principal IDs who created pull requests.
        :param int created_lt: The result should contain only entries created before this timestamp (unix millis).
        :param int created_gt: The result should contain only entries created after this timestamp (unix millis).
        :param int updated_lt: The result should contain only entries updated before this timestamp (unix millis).
        :param bool exclude_description: By providing this parameter the description would be excluded from the response.
        :param bool include_subspaces: The result should contain entries from the desired space and of its subspaces.
        :param int limit: The maximum number of results to return.
        :param list[int] label_id: List of label ids used to filter pull requests.
        :param list[int] value_id: List of label value ids used to filter pull requests.
        :param int author_id: Return only pull requests where this user is the author.
        :param int commenter_id: Return only pull requests where this user has created at least one comment.
        :param int mentioned_id: Return only pull requests where this user has been mentioned.
        :param int reviewer_id: Return only pull requests where this user has been added as a reviewer.
        :param list[str] review_decision: Require only this review decision of the reviewer. Requires reviewer_id parameter.
        :param bool include_git_stats: If true, the git diff stats would be included in the response.
        :param bool include_checks: If true, the summary of check for the branch commit SHA would be included in the response.
        :param bool include_rules: If true, a list of rules that apply to this branch would be included in the response.
        :return: list[TypesPullReqRepo]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_pull_req_space_with_http_info(account_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.list_pull_req_space_with_http_info(account_identifier, **kwargs)  # noqa: E501
            return data

    def list_pull_req_space_with_http_info(self, account_identifier, **kwargs):  # noqa: E501
        """List pull requests in account/org/project  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_pull_req_space_with_http_info(account_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param list[str] state: The state of the pull requests to include in the result.
        :param str source_repo_ref: Source repository ref of the pull requests.
        :param str source_branch: Source branch of the pull requests.
        :param str target_branch: Target branch of the pull requests.
        :param str query: The substring by which the pull requests are filtered.
        :param list[int] created_by: List of principal IDs who created pull requests.
        :param int created_lt: The result should contain only entries created before this timestamp (unix millis).
        :param int created_gt: The result should contain only entries created after this timestamp (unix millis).
        :param int updated_lt: The result should contain only entries updated before this timestamp (unix millis).
        :param bool exclude_description: By providing this parameter the description would be excluded from the response.
        :param bool include_subspaces: The result should contain entries from the desired space and of its subspaces.
        :param int limit: The maximum number of results to return.
        :param list[int] label_id: List of label ids used to filter pull requests.
        :param list[int] value_id: List of label value ids used to filter pull requests.
        :param int author_id: Return only pull requests where this user is the author.
        :param int commenter_id: Return only pull requests where this user has created at least one comment.
        :param int mentioned_id: Return only pull requests where this user has been mentioned.
        :param int reviewer_id: Return only pull requests where this user has been added as a reviewer.
        :param list[str] review_decision: Require only this review decision of the reviewer. Requires reviewer_id parameter.
        :param bool include_git_stats: If true, the git diff stats would be included in the response.
        :param bool include_checks: If true, the summary of check for the branch commit SHA would be included in the response.
        :param bool include_rules: If true, a list of rules that apply to this branch would be included in the response.
        :return: list[TypesPullReqRepo]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'org_identifier', 'project_identifier', 'state', 'source_repo_ref', 'source_branch', 'target_branch', 'query', 'created_by', 'created_lt', 'created_gt', 'updated_lt', 'exclude_description', 'include_subspaces', 'limit', 'label_id', 'value_id', 'author_id', 'commenter_id', 'mentioned_id', 'reviewer_id', 'review_decision', 'include_git_stats', 'include_checks', 'include_rules']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_pull_req_space" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `list_pull_req_space`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_identifier' in params:
            query_params.append(('accountIdentifier', params['account_identifier']))  # noqa: E501
        if 'org_identifier' in params:
            query_params.append(('orgIdentifier', params['org_identifier']))  # noqa: E501
        if 'project_identifier' in params:
            query_params.append(('projectIdentifier', params['project_identifier']))  # noqa: E501
        if 'state' in params:
            query_params.append(('state', params['state']))  # noqa: E501
            collection_formats['state'] = 'multi'  # noqa: E501
        if 'source_repo_ref' in params:
            query_params.append(('source_repo_ref', params['source_repo_ref']))  # noqa: E501
        if 'source_branch' in params:
            query_params.append(('source_branch', params['source_branch']))  # noqa: E501
        if 'target_branch' in params:
            query_params.append(('target_branch', params['target_branch']))  # noqa: E501
        if 'query' in params:
            query_params.append(('query', params['query']))  # noqa: E501
        if 'created_by' in params:
            query_params.append(('created_by', params['created_by']))  # noqa: E501
            collection_formats['created_by'] = 'multi'  # noqa: E501
        if 'created_lt' in params:
            query_params.append(('created_lt', params['created_lt']))  # noqa: E501
        if 'created_gt' in params:
            query_params.append(('created_gt', params['created_gt']))  # noqa: E501
        if 'updated_lt' in params:
            query_params.append(('updated_lt', params['updated_lt']))  # noqa: E501
        if 'exclude_description' in params:
            query_params.append(('exclude_description', params['exclude_description']))  # noqa: E501
        if 'include_subspaces' in params:
            query_params.append(('include_subspaces', params['include_subspaces']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'label_id' in params:
            query_params.append(('label_id', params['label_id']))  # noqa: E501
            collection_formats['label_id'] = 'multi'  # noqa: E501
        if 'value_id' in params:
            query_params.append(('value_id', params['value_id']))  # noqa: E501
            collection_formats['value_id'] = 'multi'  # noqa: E501
        if 'author_id' in params:
            query_params.append(('author_id', params['author_id']))  # noqa: E501
        if 'commenter_id' in params:
            query_params.append(('commenter_id', params['commenter_id']))  # noqa: E501
        if 'mentioned_id' in params:
            query_params.append(('mentioned_id', params['mentioned_id']))  # noqa: E501
        if 'reviewer_id' in params:
            query_params.append(('reviewer_id', params['reviewer_id']))  # noqa: E501
        if 'review_decision' in params:
            query_params.append(('review_decision', params['review_decision']))  # noqa: E501
            collection_formats['review_decision'] = 'multi'  # noqa: E501
        if 'include_git_stats' in params:
            query_params.append(('include_git_stats', params['include_git_stats']))  # noqa: E501
        if 'include_checks' in params:
            query_params.append(('include_checks', params['include_checks']))  # noqa: E501
        if 'include_rules' in params:
            query_params.append(('include_rules', params['include_rules']))  # noqa: E501

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
            '/code/api/v1/pullreq', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[TypesPullReqRepo]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def merge_pull_req_op(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Merge  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.merge_pull_req_op(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param OpenapiMergePullReq body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesMergeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.merge_pull_req_op_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
        else:
            (data) = self.merge_pull_req_op_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
            return data

    def merge_pull_req_op_with_http_info(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Merge  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.merge_pull_req_op_with_http_info(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param OpenapiMergePullReq body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesMergeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method merge_pull_req_op" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `merge_pull_req_op`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `merge_pull_req_op`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `merge_pull_req_op`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/merge', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesMergeResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def pr_candidates(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """pr_candidates  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.pr_candidates(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param int limit: The maximum number of results to return.
        :return: TypesBranchTable
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.pr_candidates_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.pr_candidates_with_http_info(account_identifier, repo_identifier, **kwargs)  # noqa: E501
            return data

    def pr_candidates_with_http_info(self, account_identifier, repo_identifier, **kwargs):  # noqa: E501
        """pr_candidates  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.pr_candidates_with_http_info(account_identifier, repo_identifier, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :param int limit: The maximum number of results to return.
        :return: TypesBranchTable
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'org_identifier', 'project_identifier', 'limit']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method pr_candidates" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `pr_candidates`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `pr_candidates`")  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/candidates', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesBranchTable',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def pull_req_meta_data(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Get metadata  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.pull_req_meta_data(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesPullReqStats
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.pull_req_meta_data_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
        else:
            (data) = self.pull_req_meta_data_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
            return data

    def pull_req_meta_data_with_http_info(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Get metadata  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.pull_req_meta_data_with_http_info(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesPullReqStats
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method pull_req_meta_data" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `pull_req_meta_data`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `pull_req_meta_data`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `pull_req_meta_data`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/metadata', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesPullReqStats',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def restore_pull_req_source_branch(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Restore source branch  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.restore_pull_req_source_branch(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param PullreqNumberBranchBody body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesCreateBranchOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.restore_pull_req_source_branch_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
        else:
            (data) = self.restore_pull_req_source_branch_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
            return data

    def restore_pull_req_source_branch_with_http_info(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Restore source branch  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.restore_pull_req_source_branch_with_http_info(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param PullreqNumberBranchBody body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesCreateBranchOutput
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method restore_pull_req_source_branch" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `restore_pull_req_source_branch`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `restore_pull_req_source_branch`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `restore_pull_req_source_branch`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/branch', 'POST',
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

    def revert_pull_req_op(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Revert of a merged pull request  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.revert_pull_req_op(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param PullreqNumberRevertBody body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesRevertResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.revert_pull_req_op_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
        else:
            (data) = self.revert_pull_req_op_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
            return data

    def revert_pull_req_op_with_http_info(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Revert of a merged pull request  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.revert_pull_req_op_with_http_info(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param PullreqNumberRevertBody body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesRevertResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method revert_pull_req_op" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `revert_pull_req_op`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `revert_pull_req_op`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `revert_pull_req_op`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/revert', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesRevertResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def review_submit_pull_req(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Submit review  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.review_submit_pull_req(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param OpenapiReviewSubmitPullReqRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.review_submit_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
        else:
            (data) = self.review_submit_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
            return data

    def review_submit_pull_req_with_http_info(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Submit review  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.review_submit_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param OpenapiReviewSubmitPullReqRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method review_submit_pull_req" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `review_submit_pull_req`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `review_submit_pull_req`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `review_submit_pull_req`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/reviews', 'POST',
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

    def reviewer_add_pull_req(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Add reviewer  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.reviewer_add_pull_req(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param OpenapiReviewerAddPullReqRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesPullReqReviewer
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.reviewer_add_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
        else:
            (data) = self.reviewer_add_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
            return data

    def reviewer_add_pull_req_with_http_info(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Add reviewer  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.reviewer_add_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param OpenapiReviewerAddPullReqRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesPullReqReviewer
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method reviewer_add_pull_req" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `reviewer_add_pull_req`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `reviewer_add_pull_req`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `reviewer_add_pull_req`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/reviewers', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesPullReqReviewer',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def reviewer_combined_list_pull_req(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """reviewer_combined_list_pull_req  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.reviewer_combined_list_pull_req(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: PullreqCombinedListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.reviewer_combined_list_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
        else:
            (data) = self.reviewer_combined_list_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
            return data

    def reviewer_combined_list_pull_req_with_http_info(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """reviewer_combined_list_pull_req  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.reviewer_combined_list_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: PullreqCombinedListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method reviewer_combined_list_pull_req" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `reviewer_combined_list_pull_req`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `reviewer_combined_list_pull_req`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `reviewer_combined_list_pull_req`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/reviewers/combined', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='PullreqCombinedListResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def reviewer_delete_pull_req(self, account_identifier, repo_identifier, pullreq_number, pullreq_reviewer_id, **kwargs):  # noqa: E501
        """Remove reviewer  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.reviewer_delete_pull_req(account_identifier, repo_identifier, pullreq_number, pullreq_reviewer_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param int pullreq_reviewer_id: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.reviewer_delete_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, pullreq_reviewer_id, **kwargs)  # noqa: E501
        else:
            (data) = self.reviewer_delete_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, pullreq_reviewer_id, **kwargs)  # noqa: E501
            return data

    def reviewer_delete_pull_req_with_http_info(self, account_identifier, repo_identifier, pullreq_number, pullreq_reviewer_id, **kwargs):  # noqa: E501
        """Remove reviewer  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.reviewer_delete_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, pullreq_reviewer_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param int pullreq_reviewer_id: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'pullreq_reviewer_id', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method reviewer_delete_pull_req" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `reviewer_delete_pull_req`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `reviewer_delete_pull_req`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `reviewer_delete_pull_req`")  # noqa: E501
        # verify the required parameter 'pullreq_reviewer_id' is set
        if ('pullreq_reviewer_id' not in params or
                params['pullreq_reviewer_id'] is None):
            raise ValueError("Missing the required parameter `pullreq_reviewer_id` when calling `reviewer_delete_pull_req`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501
        if 'pullreq_reviewer_id' in params:
            path_params['pullreq_reviewer_id'] = params['pullreq_reviewer_id']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/reviewers/{pullreq_reviewer_id}', 'DELETE',
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

    def reviewer_list_pull_req(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """List reviewers  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.reviewer_list_pull_req(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: list[TypesPullReqReviewer]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.reviewer_list_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
        else:
            (data) = self.reviewer_list_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
            return data

    def reviewer_list_pull_req_with_http_info(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """List reviewers  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.reviewer_list_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: list[TypesPullReqReviewer]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method reviewer_list_pull_req" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `reviewer_list_pull_req`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `reviewer_list_pull_req`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `reviewer_list_pull_req`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/reviewers', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[TypesPullReqReviewer]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def state_pull_req(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Update state of pull request  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.state_pull_req(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param OpenapiStatePullReqRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesPullReq
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.state_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
        else:
            (data) = self.state_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
            return data

    def state_pull_req_with_http_info(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Update state of pull request  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.state_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param OpenapiStatePullReqRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesPullReq
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method state_pull_req" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `state_pull_req`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `state_pull_req`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `state_pull_req`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/state', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesPullReq',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_pull_req(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Update pull request  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_pull_req(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param OpenapiUpdatePullReqRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesPullReq
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
        else:
            (data) = self.update_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
            return data

    def update_pull_req_with_http_info(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """Update pull request  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param OpenapiUpdatePullReqRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesPullReq
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_pull_req" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `update_pull_req`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `update_pull_req`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `update_pull_req`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesPullReq',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def user_group_reviewer_add_pull_req(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """user_group_reviewer_add_pull_req  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.user_group_reviewer_add_pull_req(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param OpenapiUserGroupReviewerAddRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesUserGroupReviewer
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.user_group_reviewer_add_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
        else:
            (data) = self.user_group_reviewer_add_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, **kwargs)  # noqa: E501
            return data

    def user_group_reviewer_add_pull_req_with_http_info(self, account_identifier, repo_identifier, pullreq_number, **kwargs):  # noqa: E501
        """user_group_reviewer_add_pull_req  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.user_group_reviewer_add_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param OpenapiUserGroupReviewerAddRequest body:
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: TypesUserGroupReviewer
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'body', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method user_group_reviewer_add_pull_req" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `user_group_reviewer_add_pull_req`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `user_group_reviewer_add_pull_req`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `user_group_reviewer_add_pull_req`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/reviewers/usergroups', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TypesUserGroupReviewer',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def user_group_reviewer_delete_pull_req(self, account_identifier, repo_identifier, pullreq_number, user_group_id, **kwargs):  # noqa: E501
        """user_group_reviewer_delete_pull_req  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.user_group_reviewer_delete_pull_req(account_identifier, repo_identifier, pullreq_number, user_group_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param int user_group_id: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.user_group_reviewer_delete_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, user_group_id, **kwargs)  # noqa: E501
        else:
            (data) = self.user_group_reviewer_delete_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, user_group_id, **kwargs)  # noqa: E501
            return data

    def user_group_reviewer_delete_pull_req_with_http_info(self, account_identifier, repo_identifier, pullreq_number, user_group_id, **kwargs):  # noqa: E501
        """user_group_reviewer_delete_pull_req  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.user_group_reviewer_delete_pull_req_with_http_info(account_identifier, repo_identifier, pullreq_number, user_group_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_identifier: Account Identifier for the Entity. (required)
        :param str repo_identifier: (required)
        :param int pullreq_number: (required)
        :param int user_group_id: (required)
        :param str org_identifier: Organization Identifier for the Entity.
        :param str project_identifier: Project Identifier for the Entity.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_identifier', 'repo_identifier', 'pullreq_number', 'user_group_id', 'org_identifier', 'project_identifier']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method user_group_reviewer_delete_pull_req" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_identifier' is set
        if ('account_identifier' not in params or
                params['account_identifier'] is None):
            raise ValueError("Missing the required parameter `account_identifier` when calling `user_group_reviewer_delete_pull_req`")  # noqa: E501
        # verify the required parameter 'repo_identifier' is set
        if ('repo_identifier' not in params or
                params['repo_identifier'] is None):
            raise ValueError("Missing the required parameter `repo_identifier` when calling `user_group_reviewer_delete_pull_req`")  # noqa: E501
        # verify the required parameter 'pullreq_number' is set
        if ('pullreq_number' not in params or
                params['pullreq_number'] is None):
            raise ValueError("Missing the required parameter `pullreq_number` when calling `user_group_reviewer_delete_pull_req`")  # noqa: E501
        # verify the required parameter 'user_group_id' is set
        if ('user_group_id' not in params or
                params['user_group_id'] is None):
            raise ValueError("Missing the required parameter `user_group_id` when calling `user_group_reviewer_delete_pull_req`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repo_identifier' in params:
            path_params['repo_identifier'] = params['repo_identifier']  # noqa: E501
        if 'pullreq_number' in params:
            path_params['pullreq_number'] = params['pullreq_number']  # noqa: E501
        if 'user_group_id' in params:
            path_params['user_group_id'] = params['user_group_id']  # noqa: E501

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
            '/code/api/v1/repos/{repo_identifier}/pullreq/{pullreq_number}/reviewers/usergroups/{user_group_id}', 'DELETE',
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
