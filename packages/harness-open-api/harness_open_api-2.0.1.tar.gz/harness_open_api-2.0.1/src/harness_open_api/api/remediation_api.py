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


class RemediationApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def check_artifact_and_deployments(self, harness_account, org, project, **kwargs):  # noqa: E501
        """Check Artifacts And Deployments  # noqa: E501

        Check Artifacts And Deployments.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.check_artifact_and_deployments(harness_account, org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :param str org: Harness organization ID (required)
        :param str project: Harness project ID (required)
        :param RemediationTrackerCreateRequestBody body:
        :return: ArtifactAndDeploymentsResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.check_artifact_and_deployments_with_http_info(harness_account, org, project, **kwargs)  # noqa: E501
        else:
            (data) = self.check_artifact_and_deployments_with_http_info(harness_account, org, project, **kwargs)  # noqa: E501
            return data

    def check_artifact_and_deployments_with_http_info(self, harness_account, org, project, **kwargs):  # noqa: E501
        """Check Artifacts And Deployments  # noqa: E501

        Check Artifacts And Deployments.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.check_artifact_and_deployments_with_http_info(harness_account, org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :param str org: Harness organization ID (required)
        :param str project: Harness project ID (required)
        :param RemediationTrackerCreateRequestBody body:
        :return: ArtifactAndDeploymentsResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['harness_account', 'org', 'project', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method check_artifact_and_deployments" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `check_artifact_and_deployments`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `check_artifact_and_deployments`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `check_artifact_and_deployments`")  # noqa: E501

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
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/orgs/{org}/projects/{project}/remediations/check-artifacts', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ArtifactAndDeploymentsResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def close_remediation_tracker(self, org, project, remediation, harness_account, **kwargs):  # noqa: E501
        """Close Remediation Tracker  # noqa: E501

        Close Remediation Tracker.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.close_remediation_tracker(org, project, remediation, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Harness organization ID (required)
        :param str project: Harness project ID (required)
        :param str remediation: Remediation Tracker Id (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :return: SaveResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.close_remediation_tracker_with_http_info(org, project, remediation, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.close_remediation_tracker_with_http_info(org, project, remediation, harness_account, **kwargs)  # noqa: E501
            return data

    def close_remediation_tracker_with_http_info(self, org, project, remediation, harness_account, **kwargs):  # noqa: E501
        """Close Remediation Tracker  # noqa: E501

        Close Remediation Tracker.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.close_remediation_tracker_with_http_info(org, project, remediation, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Harness organization ID (required)
        :param str project: Harness project ID (required)
        :param str remediation: Remediation Tracker Id (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :return: SaveResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'remediation', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method close_remediation_tracker" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `close_remediation_tracker`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `close_remediation_tracker`")  # noqa: E501
        # verify the required parameter 'remediation' is set
        if ('remediation' not in params or
                params['remediation'] is None):
            raise ValueError("Missing the required parameter `remediation` when calling `close_remediation_tracker`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `close_remediation_tracker`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'remediation' in params:
            path_params['remediation'] = params['remediation']  # noqa: E501

        query_params = []

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/orgs/{org}/projects/{project}/remediations/{remediation}/close', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SaveResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_remediation_tracker(self, harness_account, org, project, **kwargs):  # noqa: E501
        """Create Remediation Tracker  # noqa: E501

        Create Remediation Tracker.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_remediation_tracker(harness_account, org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :param str org: Harness organization ID (required)
        :param str project: Harness project ID (required)
        :param RemediationTrackerCreateRequestBody body:
        :return: RemediationTrackerCreateResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_remediation_tracker_with_http_info(harness_account, org, project, **kwargs)  # noqa: E501
        else:
            (data) = self.create_remediation_tracker_with_http_info(harness_account, org, project, **kwargs)  # noqa: E501
            return data

    def create_remediation_tracker_with_http_info(self, harness_account, org, project, **kwargs):  # noqa: E501
        """Create Remediation Tracker  # noqa: E501

        Create Remediation Tracker.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_remediation_tracker_with_http_info(harness_account, org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :param str org: Harness organization ID (required)
        :param str project: Harness project ID (required)
        :param RemediationTrackerCreateRequestBody body:
        :return: RemediationTrackerCreateResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['harness_account', 'org', 'project', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_remediation_tracker" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `create_remediation_tracker`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `create_remediation_tracker`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `create_remediation_tracker`")  # noqa: E501

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
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/orgs/{org}/projects/{project}/remediations', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RemediationTrackerCreateResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_ticket(self, harness_account, project, remediation, org, **kwargs):  # noqa: E501
        """Create Ticket  # noqa: E501

        Create Ticket  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_ticket(harness_account, project, remediation, org, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :param str project: Harness project ID (required)
        :param str remediation: Remediation Tracker ID (required)
        :param str org: Harness organization ID (required)
        :param CreateTicketRequest body:
        :return: CreateTicketResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_ticket_with_http_info(harness_account, project, remediation, org, **kwargs)  # noqa: E501
        else:
            (data) = self.create_ticket_with_http_info(harness_account, project, remediation, org, **kwargs)  # noqa: E501
            return data

    def create_ticket_with_http_info(self, harness_account, project, remediation, org, **kwargs):  # noqa: E501
        """Create Ticket  # noqa: E501

        Create Ticket  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_ticket_with_http_info(harness_account, project, remediation, org, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :param str project: Harness project ID (required)
        :param str remediation: Remediation Tracker ID (required)
        :param str org: Harness organization ID (required)
        :param CreateTicketRequest body:
        :return: CreateTicketResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['harness_account', 'project', 'remediation', 'org', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_ticket" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `create_ticket`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `create_ticket`")  # noqa: E501
        # verify the required parameter 'remediation' is set
        if ('remediation' not in params or
                params['remediation'] is None):
            raise ValueError("Missing the required parameter `remediation` when calling `create_ticket`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `create_ticket`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'remediation' in params:
            path_params['remediation'] = params['remediation']  # noqa: E501
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501

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
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/orgs/{org}/projects/{project}/remediations/{remediation}/create-ticket', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CreateTicketResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def exclude_artifact(self, harness_account, org, project, remediation, **kwargs):  # noqa: E501
        """Exclude Artifact from Remediation Tracker  # noqa: E501

        Exclude Artifact From Remediation Tracker.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.exclude_artifact(harness_account, org, project, remediation, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :param str org: Harness organization ID (required)
        :param str project: Harness project ID (required)
        :param str remediation: Remediation Tracker Id (required)
        :param ExcludeArtifactRequest body:
        :return: SaveResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.exclude_artifact_with_http_info(harness_account, org, project, remediation, **kwargs)  # noqa: E501
        else:
            (data) = self.exclude_artifact_with_http_info(harness_account, org, project, remediation, **kwargs)  # noqa: E501
            return data

    def exclude_artifact_with_http_info(self, harness_account, org, project, remediation, **kwargs):  # noqa: E501
        """Exclude Artifact from Remediation Tracker  # noqa: E501

        Exclude Artifact From Remediation Tracker.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.exclude_artifact_with_http_info(harness_account, org, project, remediation, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :param str org: Harness organization ID (required)
        :param str project: Harness project ID (required)
        :param str remediation: Remediation Tracker Id (required)
        :param ExcludeArtifactRequest body:
        :return: SaveResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['harness_account', 'org', 'project', 'remediation', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method exclude_artifact" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `exclude_artifact`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `exclude_artifact`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `exclude_artifact`")  # noqa: E501
        # verify the required parameter 'remediation' is set
        if ('remediation' not in params or
                params['remediation'] is None):
            raise ValueError("Missing the required parameter `remediation` when calling `exclude_artifact`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'remediation' in params:
            path_params['remediation'] = params['remediation']  # noqa: E501

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
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/orgs/{org}/projects/{project}/remediations/{remediation}/exclude-artifact', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SaveResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_artifact_in_remediation_details(self, org, project, remediation, artifact, harness_account, **kwargs):  # noqa: E501
        """Get Details of a Artifact in a Remediation Tracker.  # noqa: E501

        Get Details of a Artifact in a Remediation Tracker.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_artifact_in_remediation_details(org, project, remediation, artifact, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Harness organization ID (required)
        :param str project: Harness project ID (required)
        :param str remediation: Remediation Tracker Id (required)
        :param str artifact: Artifact Id (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :return: RemediationArtifactDetailsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_artifact_in_remediation_details_with_http_info(org, project, remediation, artifact, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.get_artifact_in_remediation_details_with_http_info(org, project, remediation, artifact, harness_account, **kwargs)  # noqa: E501
            return data

    def get_artifact_in_remediation_details_with_http_info(self, org, project, remediation, artifact, harness_account, **kwargs):  # noqa: E501
        """Get Details of a Artifact in a Remediation Tracker.  # noqa: E501

        Get Details of a Artifact in a Remediation Tracker.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_artifact_in_remediation_details_with_http_info(org, project, remediation, artifact, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Harness organization ID (required)
        :param str project: Harness project ID (required)
        :param str remediation: Remediation Tracker Id (required)
        :param str artifact: Artifact Id (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :return: RemediationArtifactDetailsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'remediation', 'artifact', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_artifact_in_remediation_details" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `get_artifact_in_remediation_details`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `get_artifact_in_remediation_details`")  # noqa: E501
        # verify the required parameter 'remediation' is set
        if ('remediation' not in params or
                params['remediation'] is None):
            raise ValueError("Missing the required parameter `remediation` when calling `get_artifact_in_remediation_details`")  # noqa: E501
        # verify the required parameter 'artifact' is set
        if ('artifact' not in params or
                params['artifact'] is None):
            raise ValueError("Missing the required parameter `artifact` when calling `get_artifact_in_remediation_details`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `get_artifact_in_remediation_details`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'remediation' in params:
            path_params['remediation'] = params['remediation']  # noqa: E501
        if 'artifact' in params:
            path_params['artifact'] = params['artifact']  # noqa: E501

        query_params = []

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/orgs/{org}/projects/{project}/remediations/{remediation}/artifacts/{artifact}/details', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RemediationArtifactDetailsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_artifact_list_for_remediation(self, harness_account, org, project, remediation, **kwargs):  # noqa: E501
        """Get Artifact List for Remediations.  # noqa: E501

        Get Remediation Details.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_artifact_list_for_remediation(harness_account, org, project, remediation, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :param str org: Harness organization ID (required)
        :param str project: Harness project ID (required)
        :param str remediation: Remediation Tracker Id (required)
        :param RemediationArtifactListingRequestBody body:
        :param int limit: Number of items to return per page.
        :param int page: Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page 
        :return: list[RemediationArtifactListingResponse]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_artifact_list_for_remediation_with_http_info(harness_account, org, project, remediation, **kwargs)  # noqa: E501
        else:
            (data) = self.get_artifact_list_for_remediation_with_http_info(harness_account, org, project, remediation, **kwargs)  # noqa: E501
            return data

    def get_artifact_list_for_remediation_with_http_info(self, harness_account, org, project, remediation, **kwargs):  # noqa: E501
        """Get Artifact List for Remediations.  # noqa: E501

        Get Remediation Details.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_artifact_list_for_remediation_with_http_info(harness_account, org, project, remediation, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :param str org: Harness organization ID (required)
        :param str project: Harness project ID (required)
        :param str remediation: Remediation Tracker Id (required)
        :param RemediationArtifactListingRequestBody body:
        :param int limit: Number of items to return per page.
        :param int page: Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page 
        :return: list[RemediationArtifactListingResponse]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['harness_account', 'org', 'project', 'remediation', 'body', 'limit', 'page']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_artifact_list_for_remediation" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `get_artifact_list_for_remediation`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `get_artifact_list_for_remediation`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `get_artifact_list_for_remediation`")  # noqa: E501
        # verify the required parameter 'remediation' is set
        if ('remediation' not in params or
                params['remediation'] is None):
            raise ValueError("Missing the required parameter `remediation` when calling `get_artifact_list_for_remediation`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'remediation' in params:
            path_params['remediation'] = params['remediation']  # noqa: E501

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
            '/v1/orgs/{org}/projects/{project}/remediations/{remediation}/artifacts', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[RemediationArtifactListingResponse]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_deployments_list_for_artifact_in_remediation(self, harness_account, org, project, remediation, artifact, **kwargs):  # noqa: E501
        """Get Deployments List for Artifact In Remediation.  # noqa: E501

        Get Deployments List for Artifact In Remediation.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_deployments_list_for_artifact_in_remediation(harness_account, org, project, remediation, artifact, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :param str org: Harness organization ID (required)
        :param str project: Harness project ID (required)
        :param str remediation: Remediation Tracker Id (required)
        :param str artifact: Artifact Id (required)
        :param RemediationArtifactDeploymentsListingRequestBody body:
        :param int limit: Number of items to return per page.
        :param int page: Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page 
        :return: list[RemediationArtifactDeploymentsListingResponse]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_deployments_list_for_artifact_in_remediation_with_http_info(harness_account, org, project, remediation, artifact, **kwargs)  # noqa: E501
        else:
            (data) = self.get_deployments_list_for_artifact_in_remediation_with_http_info(harness_account, org, project, remediation, artifact, **kwargs)  # noqa: E501
            return data

    def get_deployments_list_for_artifact_in_remediation_with_http_info(self, harness_account, org, project, remediation, artifact, **kwargs):  # noqa: E501
        """Get Deployments List for Artifact In Remediation.  # noqa: E501

        Get Deployments List for Artifact In Remediation.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_deployments_list_for_artifact_in_remediation_with_http_info(harness_account, org, project, remediation, artifact, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :param str org: Harness organization ID (required)
        :param str project: Harness project ID (required)
        :param str remediation: Remediation Tracker Id (required)
        :param str artifact: Artifact Id (required)
        :param RemediationArtifactDeploymentsListingRequestBody body:
        :param int limit: Number of items to return per page.
        :param int page: Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page 
        :return: list[RemediationArtifactDeploymentsListingResponse]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['harness_account', 'org', 'project', 'remediation', 'artifact', 'body', 'limit', 'page']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_deployments_list_for_artifact_in_remediation" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `get_deployments_list_for_artifact_in_remediation`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `get_deployments_list_for_artifact_in_remediation`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `get_deployments_list_for_artifact_in_remediation`")  # noqa: E501
        # verify the required parameter 'remediation' is set
        if ('remediation' not in params or
                params['remediation'] is None):
            raise ValueError("Missing the required parameter `remediation` when calling `get_deployments_list_for_artifact_in_remediation`")  # noqa: E501
        # verify the required parameter 'artifact' is set
        if ('artifact' not in params or
                params['artifact'] is None):
            raise ValueError("Missing the required parameter `artifact` when calling `get_deployments_list_for_artifact_in_remediation`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'remediation' in params:
            path_params['remediation'] = params['remediation']  # noqa: E501
        if 'artifact' in params:
            path_params['artifact'] = params['artifact']  # noqa: E501

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
            '/v1/orgs/{org}/projects/{project}/remediations/{remediation}/artifacts/{artifact}/deployments', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[RemediationArtifactDeploymentsListingResponse]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_environment_list_for_remediation(self, org, project, remediation, artifact, harness_account, **kwargs):  # noqa: E501
        """Get Environment List for Artifact In Remediation.  # noqa: E501

        Get All Environments impacted with Remediation.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_environment_list_for_remediation(org, project, remediation, artifact, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Harness organization ID (required)
        :param str project: Harness project ID (required)
        :param str remediation: Remediation Tracker Id (required)
        :param str artifact: Artifact Id (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :param str env_type: Environment Type
        :return: list[EnvironmentInfo]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_environment_list_for_remediation_with_http_info(org, project, remediation, artifact, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.get_environment_list_for_remediation_with_http_info(org, project, remediation, artifact, harness_account, **kwargs)  # noqa: E501
            return data

    def get_environment_list_for_remediation_with_http_info(self, org, project, remediation, artifact, harness_account, **kwargs):  # noqa: E501
        """Get Environment List for Artifact In Remediation.  # noqa: E501

        Get All Environments impacted with Remediation.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_environment_list_for_remediation_with_http_info(org, project, remediation, artifact, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Harness organization ID (required)
        :param str project: Harness project ID (required)
        :param str remediation: Remediation Tracker Id (required)
        :param str artifact: Artifact Id (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :param str env_type: Environment Type
        :return: list[EnvironmentInfo]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'remediation', 'artifact', 'harness_account', 'env_type']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_environment_list_for_remediation" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `get_environment_list_for_remediation`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `get_environment_list_for_remediation`")  # noqa: E501
        # verify the required parameter 'remediation' is set
        if ('remediation' not in params or
                params['remediation'] is None):
            raise ValueError("Missing the required parameter `remediation` when calling `get_environment_list_for_remediation`")  # noqa: E501
        # verify the required parameter 'artifact' is set
        if ('artifact' not in params or
                params['artifact'] is None):
            raise ValueError("Missing the required parameter `artifact` when calling `get_environment_list_for_remediation`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `get_environment_list_for_remediation`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'remediation' in params:
            path_params['remediation'] = params['remediation']  # noqa: E501
        if 'artifact' in params:
            path_params['artifact'] = params['artifact']  # noqa: E501

        query_params = []
        if 'env_type' in params:
            query_params.append(('EnvType', params['env_type']))  # noqa: E501

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/orgs/{org}/projects/{project}/remediations/{remediation}/artifacts/{artifact}/environments', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[EnvironmentInfo]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_overall_summary(self, org, project, harness_account, **kwargs):  # noqa: E501
        """Get Remediation Tracker Overall summary  # noqa: E501

        Get Overall summary of Remediation Trackers.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_overall_summary(org, project, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Harness organization ID (required)
        :param str project: Harness project ID (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :return: RemediationTrackersOverallSummaryResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_overall_summary_with_http_info(org, project, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.get_overall_summary_with_http_info(org, project, harness_account, **kwargs)  # noqa: E501
            return data

    def get_overall_summary_with_http_info(self, org, project, harness_account, **kwargs):  # noqa: E501
        """Get Remediation Tracker Overall summary  # noqa: E501

        Get Overall summary of Remediation Trackers.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_overall_summary_with_http_info(org, project, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Harness organization ID (required)
        :param str project: Harness project ID (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :return: RemediationTrackersOverallSummaryResponseBody
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
                    " to method get_overall_summary" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `get_overall_summary`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `get_overall_summary`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `get_overall_summary`")  # noqa: E501

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
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/orgs/{org}/projects/{project}/remediations/overall-summary', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RemediationTrackersOverallSummaryResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_remediation_details(self, org, project, remediation, harness_account, **kwargs):  # noqa: E501
        """Get Remediation Details.  # noqa: E501

        Get Remediation Details.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_remediation_details(org, project, remediation, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Harness organization ID (required)
        :param str project: Harness project ID (required)
        :param str remediation: Remediation Tracker Id (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :return: RemediationDetailsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_remediation_details_with_http_info(org, project, remediation, harness_account, **kwargs)  # noqa: E501
        else:
            (data) = self.get_remediation_details_with_http_info(org, project, remediation, harness_account, **kwargs)  # noqa: E501
            return data

    def get_remediation_details_with_http_info(self, org, project, remediation, harness_account, **kwargs):  # noqa: E501
        """Get Remediation Details.  # noqa: E501

        Get Remediation Details.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_remediation_details_with_http_info(org, project, remediation, harness_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Harness organization ID (required)
        :param str project: Harness project ID (required)
        :param str remediation: Remediation Tracker Id (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :return: RemediationDetailsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'remediation', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_remediation_details" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `get_remediation_details`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `get_remediation_details`")  # noqa: E501
        # verify the required parameter 'remediation' is set
        if ('remediation' not in params or
                params['remediation'] is None):
            raise ValueError("Missing the required parameter `remediation` when calling `get_remediation_details`")  # noqa: E501
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `get_remediation_details`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'remediation' in params:
            path_params['remediation'] = params['remediation']  # noqa: E501

        query_params = []

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/orgs/{org}/projects/{project}/remediations/{remediation}/details', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RemediationDetailsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_remediations(self, harness_account, org, project, **kwargs):  # noqa: E501
        """List All Remediation Trackers  # noqa: E501

        List all Remediation Trackers.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_remediations(harness_account, org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :param str org: Harness organization ID (required)
        :param str project: Harness project ID (required)
        :param RemediationListingRequestBody body:
        :param int limit: Number of items to return per page.
        :param int page: Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page 
        :param str sort: Parameter on the basis of which sorting is done.
        :param str order: Parameter on the basis of which sorting is done.
        :return: list[RemediationListingResponse]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_remediations_with_http_info(harness_account, org, project, **kwargs)  # noqa: E501
        else:
            (data) = self.list_remediations_with_http_info(harness_account, org, project, **kwargs)  # noqa: E501
            return data

    def list_remediations_with_http_info(self, harness_account, org, project, **kwargs):  # noqa: E501
        """List All Remediation Trackers  # noqa: E501

        List all Remediation Trackers.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_remediations_with_http_info(harness_account, org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :param str org: Harness organization ID (required)
        :param str project: Harness project ID (required)
        :param RemediationListingRequestBody body:
        :param int limit: Number of items to return per page.
        :param int page: Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page 
        :param str sort: Parameter on the basis of which sorting is done.
        :param str order: Parameter on the basis of which sorting is done.
        :return: list[RemediationListingResponse]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['harness_account', 'org', 'project', 'body', 'limit', 'page', 'sort', 'order']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_remediations" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `list_remediations`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `list_remediations`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `list_remediations`")  # noqa: E501

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
        if 'order' in params:
            query_params.append(('order', params['order']))  # noqa: E501

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
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/orgs/{org}/projects/{project}/remediations/list', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[RemediationListingResponse]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_remediation_tracker(self, harness_account, org, project, remediation, **kwargs):  # noqa: E501
        """Update Remediation Tracker  # noqa: E501

        Update Remediation Tracker.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_remediation_tracker(harness_account, org, project, remediation, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :param str org: Harness organization ID (required)
        :param str project: Harness project ID (required)
        :param str remediation: Remediation Tracker ID (required)
        :param RemediationTrackerUpdateRequestBody body:
        :return: RemediationTrackerUpdateResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_remediation_tracker_with_http_info(harness_account, org, project, remediation, **kwargs)  # noqa: E501
        else:
            (data) = self.update_remediation_tracker_with_http_info(harness_account, org, project, remediation, **kwargs)  # noqa: E501
            return data

    def update_remediation_tracker_with_http_info(self, harness_account, org, project, remediation, **kwargs):  # noqa: E501
        """Update Remediation Tracker  # noqa: E501

        Update Remediation Tracker.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_remediation_tracker_with_http_info(harness_account, org, project, remediation, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped. (required)
        :param str org: Harness organization ID (required)
        :param str project: Harness project ID (required)
        :param str remediation: Remediation Tracker ID (required)
        :param RemediationTrackerUpdateRequestBody body:
        :return: RemediationTrackerUpdateResponseBody
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['harness_account', 'org', 'project', 'remediation', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_remediation_tracker" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'harness_account' is set
        if ('harness_account' not in params or
                params['harness_account'] is None):
            raise ValueError("Missing the required parameter `harness_account` when calling `update_remediation_tracker`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `update_remediation_tracker`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `update_remediation_tracker`")  # noqa: E501
        # verify the required parameter 'remediation' is set
        if ('remediation' not in params or
                params['remediation'] is None):
            raise ValueError("Missing the required parameter `remediation` when calling `update_remediation_tracker`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'remediation' in params:
            path_params['remediation'] = params['remediation']  # noqa: E501

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
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/orgs/{org}/projects/{project}/remediations/{remediation}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RemediationTrackerUpdateResponseBody',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
