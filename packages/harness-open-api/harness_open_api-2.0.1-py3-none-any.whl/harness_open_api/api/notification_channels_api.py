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


class NotificationChannelsApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_notification_channel(self, org, project, **kwargs):  # noqa: E501
        """Create Notification channel  # noqa: E501

        Create Notification Channel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_notification_channel(org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Identifier field of the organization the resource is scoped to (required)
        :param str project: Identifier field of the project the resource is scoped to (required)
        :param NotificationChannelDTO body: Notification channel request
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: NotificationChannelDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_notification_channel_with_http_info(org, project, **kwargs)  # noqa: E501
        else:
            (data) = self.create_notification_channel_with_http_info(org, project, **kwargs)  # noqa: E501
            return data

    def create_notification_channel_with_http_info(self, org, project, **kwargs):  # noqa: E501
        """Create Notification channel  # noqa: E501

        Create Notification Channel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_notification_channel_with_http_info(org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Identifier field of the organization the resource is scoped to (required)
        :param str project: Identifier field of the project the resource is scoped to (required)
        :param NotificationChannelDTO body: Notification channel request
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: NotificationChannelDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'body', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_notification_channel" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `create_notification_channel`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `create_notification_channel`")  # noqa: E501

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
            ['application/json', 'application/xml', 'multipart/form-data'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/orgs/{org}/projects/{project}/notification-channels', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='NotificationChannelDTO',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_notification_channel_account(self, **kwargs):  # noqa: E501
        """Create Notification channel  # noqa: E501

        Create Notification Channel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_notification_channel_account(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param NotificationChannelDTO body: Notification channel request
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: NotificationChannelDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_notification_channel_account_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.create_notification_channel_account_with_http_info(**kwargs)  # noqa: E501
            return data

    def create_notification_channel_account_with_http_info(self, **kwargs):  # noqa: E501
        """Create Notification channel  # noqa: E501

        Create Notification Channel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_notification_channel_account_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param NotificationChannelDTO body: Notification channel request
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: NotificationChannelDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_notification_channel_account" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

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
            ['application/json', 'application/xml', 'multipart/form-data'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/notification-channels', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='NotificationChannelDTO',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_notification_channel_org(self, org, **kwargs):  # noqa: E501
        """Create Notification channel  # noqa: E501

        Create Notification Channel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_notification_channel_org(org, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Identifier field of the organization the resource is scoped to (required)
        :param NotificationChannelDTO body: Notification channel request
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: NotificationChannelDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_notification_channel_org_with_http_info(org, **kwargs)  # noqa: E501
        else:
            (data) = self.create_notification_channel_org_with_http_info(org, **kwargs)  # noqa: E501
            return data

    def create_notification_channel_org_with_http_info(self, org, **kwargs):  # noqa: E501
        """Create Notification channel  # noqa: E501

        Create Notification Channel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_notification_channel_org_with_http_info(org, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Identifier field of the organization the resource is scoped to (required)
        :param NotificationChannelDTO body: Notification channel request
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: NotificationChannelDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'body', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_notification_channel_org" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `create_notification_channel_org`")  # noqa: E501

        collection_formats = {}

        path_params = {}
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
            ['application/json', 'application/xml', 'multipart/form-data'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/orgs/{org}/notification-channels', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='NotificationChannelDTO',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_notification_channel(self, notification_channel, org, project, **kwargs):  # noqa: E501
        """Delete Notification Channel  # noqa: E501

        Delete notification channel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_notification_channel(notification_channel, org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str notification_channel: identifier (required)
        :param str org: Identifier field of the organization the resource is scoped to (required)
        :param str project: Identifier field of the project the resource is scoped to (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_notification_channel_with_http_info(notification_channel, org, project, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_notification_channel_with_http_info(notification_channel, org, project, **kwargs)  # noqa: E501
            return data

    def delete_notification_channel_with_http_info(self, notification_channel, org, project, **kwargs):  # noqa: E501
        """Delete Notification Channel  # noqa: E501

        Delete notification channel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_notification_channel_with_http_info(notification_channel, org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str notification_channel: identifier (required)
        :param str org: Identifier field of the organization the resource is scoped to (required)
        :param str project: Identifier field of the project the resource is scoped to (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['notification_channel', 'org', 'project', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_notification_channel" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'notification_channel' is set
        if ('notification_channel' not in params or
                params['notification_channel'] is None):
            raise ValueError("Missing the required parameter `notification_channel` when calling `delete_notification_channel`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `delete_notification_channel`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `delete_notification_channel`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'notification_channel' in params:
            path_params['notification-channel'] = params['notification_channel']  # noqa: E501
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
            '/v1/orgs/{org}/projects/{project}/notification-channels/{notification-channel}', 'DELETE',
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

    def delete_notification_channel_account(self, notification_channel, **kwargs):  # noqa: E501
        """Delete Notification Channel  # noqa: E501

        Delete notification channel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_notification_channel_account(notification_channel, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str notification_channel: identifier (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_notification_channel_account_with_http_info(notification_channel, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_notification_channel_account_with_http_info(notification_channel, **kwargs)  # noqa: E501
            return data

    def delete_notification_channel_account_with_http_info(self, notification_channel, **kwargs):  # noqa: E501
        """Delete Notification Channel  # noqa: E501

        Delete notification channel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_notification_channel_account_with_http_info(notification_channel, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str notification_channel: identifier (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['notification_channel', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_notification_channel_account" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'notification_channel' is set
        if ('notification_channel' not in params or
                params['notification_channel'] is None):
            raise ValueError("Missing the required parameter `notification_channel` when calling `delete_notification_channel_account`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'notification_channel' in params:
            path_params['notification-channel'] = params['notification_channel']  # noqa: E501

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
            '/v1/notification-channels/{notification-channel}', 'DELETE',
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

    def delete_notification_channel_org(self, notification_channel, org, **kwargs):  # noqa: E501
        """Delete Notification Channel  # noqa: E501

        Delete notification channel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_notification_channel_org(notification_channel, org, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str notification_channel: identifier (required)
        :param str org: Identifier field of the organization the resource is scoped to (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_notification_channel_org_with_http_info(notification_channel, org, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_notification_channel_org_with_http_info(notification_channel, org, **kwargs)  # noqa: E501
            return data

    def delete_notification_channel_org_with_http_info(self, notification_channel, org, **kwargs):  # noqa: E501
        """Delete Notification Channel  # noqa: E501

        Delete notification channel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_notification_channel_org_with_http_info(notification_channel, org, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str notification_channel: identifier (required)
        :param str org: Identifier field of the organization the resource is scoped to (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['notification_channel', 'org', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_notification_channel_org" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'notification_channel' is set
        if ('notification_channel' not in params or
                params['notification_channel'] is None):
            raise ValueError("Missing the required parameter `notification_channel` when calling `delete_notification_channel_org`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `delete_notification_channel_org`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'notification_channel' in params:
            path_params['notification-channel'] = params['notification_channel']  # noqa: E501
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501

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
            '/v1/orgs/{org}/notification-channels/{notification-channel}', 'DELETE',
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

    def get_notification_channel(self, notification_channel, org, project, **kwargs):  # noqa: E501
        """Get Notification channel  # noqa: E501

        Get Notification Channel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_notification_channel(notification_channel, org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str notification_channel: identifier (required)
        :param str org: Identifier field of the organization the resource is scoped to (required)
        :param str project: Identifier field of the project the resource is scoped to (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: NotificationChannelDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_notification_channel_with_http_info(notification_channel, org, project, **kwargs)  # noqa: E501
        else:
            (data) = self.get_notification_channel_with_http_info(notification_channel, org, project, **kwargs)  # noqa: E501
            return data

    def get_notification_channel_with_http_info(self, notification_channel, org, project, **kwargs):  # noqa: E501
        """Get Notification channel  # noqa: E501

        Get Notification Channel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_notification_channel_with_http_info(notification_channel, org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str notification_channel: identifier (required)
        :param str org: Identifier field of the organization the resource is scoped to (required)
        :param str project: Identifier field of the project the resource is scoped to (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: NotificationChannelDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['notification_channel', 'org', 'project', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_notification_channel" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'notification_channel' is set
        if ('notification_channel' not in params or
                params['notification_channel'] is None):
            raise ValueError("Missing the required parameter `notification_channel` when calling `get_notification_channel`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `get_notification_channel`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `get_notification_channel`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'notification_channel' in params:
            path_params['notification-channel'] = params['notification_channel']  # noqa: E501
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
            ['application/json', 'application/xml', 'multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/orgs/{org}/projects/{project}/notification-channels/{notification-channel}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='NotificationChannelDTO',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_notification_channel_account(self, notification_channel, **kwargs):  # noqa: E501
        """Get Notification channel  # noqa: E501

        Get Notification Channel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_notification_channel_account(notification_channel, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str notification_channel: identifier (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: NotificationChannelDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_notification_channel_account_with_http_info(notification_channel, **kwargs)  # noqa: E501
        else:
            (data) = self.get_notification_channel_account_with_http_info(notification_channel, **kwargs)  # noqa: E501
            return data

    def get_notification_channel_account_with_http_info(self, notification_channel, **kwargs):  # noqa: E501
        """Get Notification channel  # noqa: E501

        Get Notification Channel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_notification_channel_account_with_http_info(notification_channel, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str notification_channel: identifier (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: NotificationChannelDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['notification_channel', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_notification_channel_account" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'notification_channel' is set
        if ('notification_channel' not in params or
                params['notification_channel'] is None):
            raise ValueError("Missing the required parameter `notification_channel` when calling `get_notification_channel_account`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'notification_channel' in params:
            path_params['notification-channel'] = params['notification_channel']  # noqa: E501

        query_params = []

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml', 'multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/notification-channels/{notification-channel}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='NotificationChannelDTO',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_notification_channel_org(self, notification_channel, org, **kwargs):  # noqa: E501
        """Get Notification channel  # noqa: E501

        Get Notification Channel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_notification_channel_org(notification_channel, org, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str notification_channel: identifier (required)
        :param str org: Identifier field of the organization the resource is scoped to (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: NotificationChannelDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_notification_channel_org_with_http_info(notification_channel, org, **kwargs)  # noqa: E501
        else:
            (data) = self.get_notification_channel_org_with_http_info(notification_channel, org, **kwargs)  # noqa: E501
            return data

    def get_notification_channel_org_with_http_info(self, notification_channel, org, **kwargs):  # noqa: E501
        """Get Notification channel  # noqa: E501

        Get Notification Channel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_notification_channel_org_with_http_info(notification_channel, org, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str notification_channel: identifier (required)
        :param str org: Identifier field of the organization the resource is scoped to (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: NotificationChannelDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['notification_channel', 'org', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_notification_channel_org" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'notification_channel' is set
        if ('notification_channel' not in params or
                params['notification_channel'] is None):
            raise ValueError("Missing the required parameter `notification_channel` when calling `get_notification_channel_org`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `get_notification_channel_org`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'notification_channel' in params:
            path_params['notification-channel'] = params['notification_channel']  # noqa: E501
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501

        query_params = []

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml', 'multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/orgs/{org}/notification-channels/{notification-channel}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='NotificationChannelDTO',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_notification_channels(self, org, project, **kwargs):  # noqa: E501
        """List Notification channels  # noqa: E501

        Returns a list of notification channels for the scope.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_notification_channels(org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Identifier field of the organization the resource is scoped to (required)
        :param str project: Identifier field of the project the resource is scoped to (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :param int limit: Number of items to return per page.
        :param str search_term: This would be used to filter resources having attributes matching with search term.
        :param str sort: Parameter on the basis of which sorting is done.
        :param str order: Order on the basis of which sorting is done.
        :param str notification_channel_type: Notification Channel Type
        :param int page: Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page 
        :param bool include_parent_scope: Include entities from current and parent scopes.
        :return: list[NotificationChannelDTO]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_notification_channels_with_http_info(org, project, **kwargs)  # noqa: E501
        else:
            (data) = self.list_notification_channels_with_http_info(org, project, **kwargs)  # noqa: E501
            return data

    def list_notification_channels_with_http_info(self, org, project, **kwargs):  # noqa: E501
        """List Notification channels  # noqa: E501

        Returns a list of notification channels for the scope.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_notification_channels_with_http_info(org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Identifier field of the organization the resource is scoped to (required)
        :param str project: Identifier field of the project the resource is scoped to (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :param int limit: Number of items to return per page.
        :param str search_term: This would be used to filter resources having attributes matching with search term.
        :param str sort: Parameter on the basis of which sorting is done.
        :param str order: Order on the basis of which sorting is done.
        :param str notification_channel_type: Notification Channel Type
        :param int page: Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page 
        :param bool include_parent_scope: Include entities from current and parent scopes.
        :return: list[NotificationChannelDTO]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'harness_account', 'limit', 'search_term', 'sort', 'order', 'notification_channel_type', 'page', 'include_parent_scope']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_notification_channels" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `list_notification_channels`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `list_notification_channels`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501

        query_params = []
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'search_term' in params:
            query_params.append(('search_term', params['search_term']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501
        if 'order' in params:
            query_params.append(('order', params['order']))  # noqa: E501
        if 'notification_channel_type' in params:
            query_params.append(('notification_channel_type', params['notification_channel_type']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'include_parent_scope' in params:
            query_params.append(('include_parent_scope', params['include_parent_scope']))  # noqa: E501

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml', 'multipart/form-data', 'text/html', 'text/plain'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/orgs/{org}/projects/{project}/notification-channels', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[NotificationChannelDTO]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_notification_channels_account(self, **kwargs):  # noqa: E501
        """List Notification channels at account level  # noqa: E501

        Returns a list of notification channels for the scope.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_notification_channels_account(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :param int limit: Number of items to return per page.
        :param str search_term: This would be used to filter resources having attributes matching with search term.
        :param str sort: Parameter on the basis of which sorting is done.
        :param str order: Order on the basis of which sorting is done.
        :param str notification_channel_type: Notification Channel Type
        :param int page: Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page 
        :param bool include_parent_scope: Include entities from current and parent scopes.
        :return: list[NotificationChannelDTO]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_notification_channels_account_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.list_notification_channels_account_with_http_info(**kwargs)  # noqa: E501
            return data

    def list_notification_channels_account_with_http_info(self, **kwargs):  # noqa: E501
        """List Notification channels at account level  # noqa: E501

        Returns a list of notification channels for the scope.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_notification_channels_account_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :param int limit: Number of items to return per page.
        :param str search_term: This would be used to filter resources having attributes matching with search term.
        :param str sort: Parameter on the basis of which sorting is done.
        :param str order: Order on the basis of which sorting is done.
        :param str notification_channel_type: Notification Channel Type
        :param int page: Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page 
        :param bool include_parent_scope: Include entities from current and parent scopes.
        :return: list[NotificationChannelDTO]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['harness_account', 'limit', 'search_term', 'sort', 'order', 'notification_channel_type', 'page', 'include_parent_scope']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_notification_channels_account" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'search_term' in params:
            query_params.append(('search_term', params['search_term']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501
        if 'order' in params:
            query_params.append(('order', params['order']))  # noqa: E501
        if 'notification_channel_type' in params:
            query_params.append(('notification_channel_type', params['notification_channel_type']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'include_parent_scope' in params:
            query_params.append(('include_parent_scope', params['include_parent_scope']))  # noqa: E501

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml', 'multipart/form-data', 'text/html', 'text/plain'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/notification-channels', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[NotificationChannelDTO]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_notification_channels_org(self, org, **kwargs):  # noqa: E501
        """List Notification channels at org level  # noqa: E501

        Returns a list of notification channels for the scope.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_notification_channels_org(org, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Identifier field of the organization the resource is scoped to (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :param int limit: Number of items to return per page.
        :param str search_term: This would be used to filter resources having attributes matching with search term.
        :param str sort: Parameter on the basis of which sorting is done.
        :param str order: Order on the basis of which sorting is done.
        :param str notification_channel_type: Notification Channel Type
        :param int page: Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page 
        :param bool include_parent_scope: Include entities from current and parent scopes.
        :return: list[NotificationChannelDTO]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_notification_channels_org_with_http_info(org, **kwargs)  # noqa: E501
        else:
            (data) = self.list_notification_channels_org_with_http_info(org, **kwargs)  # noqa: E501
            return data

    def list_notification_channels_org_with_http_info(self, org, **kwargs):  # noqa: E501
        """List Notification channels at org level  # noqa: E501

        Returns a list of notification channels for the scope.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_notification_channels_org_with_http_info(org, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Identifier field of the organization the resource is scoped to (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :param int limit: Number of items to return per page.
        :param str search_term: This would be used to filter resources having attributes matching with search term.
        :param str sort: Parameter on the basis of which sorting is done.
        :param str order: Order on the basis of which sorting is done.
        :param str notification_channel_type: Notification Channel Type
        :param int page: Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page 
        :param bool include_parent_scope: Include entities from current and parent scopes.
        :return: list[NotificationChannelDTO]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'harness_account', 'limit', 'search_term', 'sort', 'order', 'notification_channel_type', 'page', 'include_parent_scope']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_notification_channels_org" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `list_notification_channels_org`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501

        query_params = []
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'search_term' in params:
            query_params.append(('search_term', params['search_term']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501
        if 'order' in params:
            query_params.append(('order', params['order']))  # noqa: E501
        if 'notification_channel_type' in params:
            query_params.append(('notification_channel_type', params['notification_channel_type']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'include_parent_scope' in params:
            query_params.append(('include_parent_scope', params['include_parent_scope']))  # noqa: E501

        header_params = {}
        if 'harness_account' in params:
            header_params['Harness-Account'] = params['harness_account']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml', 'multipart/form-data', 'text/html', 'text/plain'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/orgs/{org}/notification-channels', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[NotificationChannelDTO]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_notification_channel(self, notification_channel, org, project, **kwargs):  # noqa: E501
        """Update Notification Channel  # noqa: E501

        Update Notification Channel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_notification_channel(notification_channel, org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str notification_channel: identifier (required)
        :param str org: Identifier field of the organization the resource is scoped to (required)
        :param str project: Identifier field of the project the resource is scoped to (required)
        :param NotificationChannelDTO body: Notification channel request
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: NotificationChannelDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_notification_channel_with_http_info(notification_channel, org, project, **kwargs)  # noqa: E501
        else:
            (data) = self.update_notification_channel_with_http_info(notification_channel, org, project, **kwargs)  # noqa: E501
            return data

    def update_notification_channel_with_http_info(self, notification_channel, org, project, **kwargs):  # noqa: E501
        """Update Notification Channel  # noqa: E501

        Update Notification Channel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_notification_channel_with_http_info(notification_channel, org, project, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str notification_channel: identifier (required)
        :param str org: Identifier field of the organization the resource is scoped to (required)
        :param str project: Identifier field of the project the resource is scoped to (required)
        :param NotificationChannelDTO body: Notification channel request
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: NotificationChannelDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['notification_channel', 'org', 'project', 'body', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_notification_channel" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'notification_channel' is set
        if ('notification_channel' not in params or
                params['notification_channel'] is None):
            raise ValueError("Missing the required parameter `notification_channel` when calling `update_notification_channel`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `update_notification_channel`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `update_notification_channel`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'notification_channel' in params:
            path_params['notification-channel'] = params['notification_channel']  # noqa: E501
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
            ['application/json', 'application/xml', 'multipart/form-data'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/orgs/{org}/projects/{project}/notification-channels/{notification-channel}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='NotificationChannelDTO',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_notification_channel_account(self, notification_channel, **kwargs):  # noqa: E501
        """Update Notification Channel  # noqa: E501

        Update Notification Channel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_notification_channel_account(notification_channel, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str notification_channel: identifier (required)
        :param NotificationChannelDTO body: Notification channel request
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: NotificationChannelDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_notification_channel_account_with_http_info(notification_channel, **kwargs)  # noqa: E501
        else:
            (data) = self.update_notification_channel_account_with_http_info(notification_channel, **kwargs)  # noqa: E501
            return data

    def update_notification_channel_account_with_http_info(self, notification_channel, **kwargs):  # noqa: E501
        """Update Notification Channel  # noqa: E501

        Update Notification Channel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_notification_channel_account_with_http_info(notification_channel, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str notification_channel: identifier (required)
        :param NotificationChannelDTO body: Notification channel request
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: NotificationChannelDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['notification_channel', 'body', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_notification_channel_account" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'notification_channel' is set
        if ('notification_channel' not in params or
                params['notification_channel'] is None):
            raise ValueError("Missing the required parameter `notification_channel` when calling `update_notification_channel_account`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'notification_channel' in params:
            path_params['notification-channel'] = params['notification_channel']  # noqa: E501

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
            ['application/json', 'application/xml', 'multipart/form-data'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/notification-channels/{notification-channel}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='NotificationChannelDTO',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_notification_channel_org(self, notification_channel, org, **kwargs):  # noqa: E501
        """Update Notification Channel  # noqa: E501

        Update Notification Channel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_notification_channel_org(notification_channel, org, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str notification_channel: identifier (required)
        :param str org: Identifier field of the organization the resource is scoped to (required)
        :param NotificationChannelDTO body: Notification channel request
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: NotificationChannelDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_notification_channel_org_with_http_info(notification_channel, org, **kwargs)  # noqa: E501
        else:
            (data) = self.update_notification_channel_org_with_http_info(notification_channel, org, **kwargs)  # noqa: E501
            return data

    def update_notification_channel_org_with_http_info(self, notification_channel, org, **kwargs):  # noqa: E501
        """Update Notification Channel  # noqa: E501

        Update Notification Channel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_notification_channel_org_with_http_info(notification_channel, org, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str notification_channel: identifier (required)
        :param str org: Identifier field of the organization the resource is scoped to (required)
        :param NotificationChannelDTO body: Notification channel request
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: NotificationChannelDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['notification_channel', 'org', 'body', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_notification_channel_org" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'notification_channel' is set
        if ('notification_channel' not in params or
                params['notification_channel'] is None):
            raise ValueError("Missing the required parameter `notification_channel` when calling `update_notification_channel_org`")  # noqa: E501
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `update_notification_channel_org`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'notification_channel' in params:
            path_params['notification-channel'] = params['notification_channel']  # noqa: E501
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
            ['application/json', 'application/xml', 'multipart/form-data'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['x-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/orgs/{org}/notification-channels/{notification-channel}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='NotificationChannelDTO',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def validate_notification_channel_identifier(self, org, project, notification_channel, **kwargs):  # noqa: E501
        """Validate Notification Channel Identifier  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.validate_notification_channel_identifier(org, project, notification_channel, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Identifier field of the organization the resource is scoped to (required)
        :param str project: Identifier field of the project the resource is scoped to (required)
        :param str notification_channel: identifier (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: ValidateIdentifierDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.validate_notification_channel_identifier_with_http_info(org, project, notification_channel, **kwargs)  # noqa: E501
        else:
            (data) = self.validate_notification_channel_identifier_with_http_info(org, project, notification_channel, **kwargs)  # noqa: E501
            return data

    def validate_notification_channel_identifier_with_http_info(self, org, project, notification_channel, **kwargs):  # noqa: E501
        """Validate Notification Channel Identifier  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.validate_notification_channel_identifier_with_http_info(org, project, notification_channel, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Identifier field of the organization the resource is scoped to (required)
        :param str project: Identifier field of the project the resource is scoped to (required)
        :param str notification_channel: identifier (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: ValidateIdentifierDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'project', 'notification_channel', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method validate_notification_channel_identifier" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `validate_notification_channel_identifier`")  # noqa: E501
        # verify the required parameter 'project' is set
        if ('project' not in params or
                params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `validate_notification_channel_identifier`")  # noqa: E501
        # verify the required parameter 'notification_channel' is set
        if ('notification_channel' not in params or
                params['notification_channel'] is None):
            raise ValueError("Missing the required parameter `notification_channel` when calling `validate_notification_channel_identifier`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'project' in params:
            path_params['project'] = params['project']  # noqa: E501
        if 'notification_channel' in params:
            path_params['notification-channel'] = params['notification_channel']  # noqa: E501

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
            '/v1/orgs/{org}/projects/{project}/validate-channels/{notification-channel}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ValidateIdentifierDTO',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def validate_notification_channel_identifier_account(self, notification_channel, **kwargs):  # noqa: E501
        """Validate Notification channel identifier  # noqa: E501

        Validate Notification Channel Indetifier  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.validate_notification_channel_identifier_account(notification_channel, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str notification_channel: identifier (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: ValidateIdentifierDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.validate_notification_channel_identifier_account_with_http_info(notification_channel, **kwargs)  # noqa: E501
        else:
            (data) = self.validate_notification_channel_identifier_account_with_http_info(notification_channel, **kwargs)  # noqa: E501
            return data

    def validate_notification_channel_identifier_account_with_http_info(self, notification_channel, **kwargs):  # noqa: E501
        """Validate Notification channel identifier  # noqa: E501

        Validate Notification Channel Indetifier  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.validate_notification_channel_identifier_account_with_http_info(notification_channel, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str notification_channel: identifier (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: ValidateIdentifierDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['notification_channel', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method validate_notification_channel_identifier_account" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'notification_channel' is set
        if ('notification_channel' not in params or
                params['notification_channel'] is None):
            raise ValueError("Missing the required parameter `notification_channel` when calling `validate_notification_channel_identifier_account`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'notification_channel' in params:
            path_params['notification-channel'] = params['notification_channel']  # noqa: E501

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
            '/v1/validate-channels/{notification-channel}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ValidateIdentifierDTO',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def validate_notification_channel_identifier_org(self, org, notification_channel, **kwargs):  # noqa: E501
        """Validate unique identifier for notification channel  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.validate_notification_channel_identifier_org(org, notification_channel, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Identifier field of the organization the resource is scoped to (required)
        :param str notification_channel: identifier (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: ValidateIdentifierDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.validate_notification_channel_identifier_org_with_http_info(org, notification_channel, **kwargs)  # noqa: E501
        else:
            (data) = self.validate_notification_channel_identifier_org_with_http_info(org, notification_channel, **kwargs)  # noqa: E501
            return data

    def validate_notification_channel_identifier_org_with_http_info(self, org, notification_channel, **kwargs):  # noqa: E501
        """Validate unique identifier for notification channel  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.validate_notification_channel_identifier_org_with_http_info(org, notification_channel, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str org: Identifier field of the organization the resource is scoped to (required)
        :param str notification_channel: identifier (required)
        :param str harness_account: Identifier field of the account the resource is scoped to. This is required for Authorization methods other than the x-api-key header. If you are using the x-api-key header, this can be skipped.
        :return: ValidateIdentifierDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['org', 'notification_channel', 'harness_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method validate_notification_channel_identifier_org" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'org' is set
        if ('org' not in params or
                params['org'] is None):
            raise ValueError("Missing the required parameter `org` when calling `validate_notification_channel_identifier_org`")  # noqa: E501
        # verify the required parameter 'notification_channel' is set
        if ('notification_channel' not in params or
                params['notification_channel'] is None):
            raise ValueError("Missing the required parameter `notification_channel` when calling `validate_notification_channel_identifier_org`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'org' in params:
            path_params['org'] = params['org']  # noqa: E501
        if 'notification_channel' in params:
            path_params['notification-channel'] = params['notification_channel']  # noqa: E501

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
            '/v1/orgs/{org}/validate-channels/{notification-channel}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ValidateIdentifierDTO',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
