# coding: utf-8

"""
    Harness NextGen Software Delivery Platform API Reference

    The Harness Software Delivery Platform uses OpenAPI Specification v3.0. Harness constantly improves these APIs. Please be aware that some improvements could cause breaking changes. # Introduction     The Harness API allows you to integrate and use all the services and modules we provide on the Harness Platform. If you use client-side SDKs, Harness functionality can be integrated with your client-side automation, helping you reduce manual efforts and deploy code faster.    For more information about how Harness works, read our [documentation](https://developer.harness.io/docs/getting-started) or visit the [Harness Developer Hub](https://developer.harness.io/).  ## How it works    The Harness API is a RESTful API that uses standard HTTP verbs. You can send requests in JSON, YAML, or form-data format. The format of the response matches the format of your request. You must send a single request at a time and ensure that you include your authentication key. For more information about this, go to [Authentication](#section/Introduction/Authentication).  ## Get started    Before you start integrating, get to know our API better by reading the following topics:    * [Harness key concepts](https://developer.harness.io/docs/getting-started/learn-harness-key-concepts/)   * [Authentication](#section/Introduction/Authentication)   * [Requests and responses](#section/Introduction/Requests-and-Responses)   * [Common Parameters](#section/Introduction/Common-Parameters-Beta)   * [Status Codes](#section/Introduction/Status-Codes)   * [Errors](#tag/Error-Response)   * [Versioning](#section/Introduction/Versioning-Beta)   * [Pagination](/#section/Introduction/Pagination-Beta)    The methods you need to integrate with depend on the functionality you want to use. Work with  your Harness Solutions Engineer to determine which methods you need.  ## Authentication  To authenticate with the Harness API, you need to:   1. Generate an API token on the Harness Platform.   2. Send the API token you generate in the `x-api-key` header in each request.  ### Generate an API token  To generate an API token, complete the following steps:   1. Go to the [Harness Platform](https://app.harness.io/).   2. On the left-hand navigation, click **My Profile**.   3. Click **+API Key**, enter a name for your key and then click **Save**.   4. Within the API Key tile, click **+Token**.   5. Enter a name for your token and click **Generate Token**. **Important**: Make sure to save your token securely. Harness does not store the API token for future reference, so make sure to save your token securely before you leave the page.  ### Send the API token in your requests  Send the token you created in the Harness Platform in the x-api-key header. For example:   `x-api-key: YOUR_API_KEY_HERE`  ## Requests and Responses    The structure for each request and response is outlined in the API documentation. We have examples in JSON and YAML for every request and response. You can use our online editor to test the examples.  ## Common Parameters [Beta]  | Field Name | Type    | Default | Description    | |------------|---------|---------|----------------| | identifier | string  | none    | URL-friendly version of the name, used to identify a resource within it's scope and so needs to be unique within the scope.                                                                                                            | | name       | string  | none    | Human-friendly name for the resource.                                                                                       | | org        | string  | none    | Limit to provided org identifiers.                                                                                                                     | | project    | string  | none    | Limit to provided project identifiers.                                                                                                                 | | description| string  | none    | More information about the specific resource.                                                                                    | | tags       | map[string]string  | none    | List of labels applied to the resource.                                                                                                                         | | order      | string  | desc    | Order to use when sorting the specified fields. Type: enum(asc,desc).                                                                                                                                     | | sort       | string  | none    | Fields on which to sort. Note: Specify the fields that you want to use for sorting. When doing so, consider the operational overhead of sorting fields. | | limit      | int     | 30      | Pagination: Number of items to return.                                                                                                                 | | page       | int     | 1       | Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page.                  | | created    | int64   | none    | Unix timestamp that shows when the resource was created (in milliseconds).                                                               | | updated    | int64   | none    | Unix timestamp that shows when the resource was last edited (in milliseconds).                                                           |   ## Status Codes    Harness uses conventional HTTP status codes to indicate the status of an API request.    Generally, 2xx responses are reserved for success and 4xx status codes are reserved for failures. A 5xx response code indicates an error on the Harness server.    | Error Code  | Description |   |-------------|-------------|   | 200         |     OK      |   | 201         |   Created   |   | 202         |   Accepted  |   | 204         |  No Content |   | 400         | Bad Request |   | 401         | Unauthorized |   | 403         | Forbidden |   | 412         | Precondition Failed |   | 415         | Unsupported Media Type |   | 500         | Server Error |    To view our error response structures, go [here](#tag/Error-Response).  ## Versioning [Beta]  ### Harness Version   The current version of our Beta APIs is yet to be announced. The version number will use the date-header format and will be valid only for our Beta APIs.  ### Generation   All our beta APIs are versioned as a Generation, and this version is included in the path to every API resource. For example, v1 beta APIs begin with `app.harness.io/v1/`, where v1 is the API Generation.    The version number represents the core API and does not change frequently. The version number changes only if there is a significant departure from the basic underpinnings of the existing API. For example, when Harness performs a system-wide refactoring of core concepts or resources.  ## Pagination [Beta]  We use pagination to place limits on the number of responses associated with list endpoints. Pagination is achieved by the use of limit query parameters. The limit defaults to 30. Its maximum value is 100.  Following are the pagination headers supported in the response bodies of paginated APIs:   1. X-Total-Elements : Indicates the total number of entries in a paginated response.   2. X-Page-Number : Indicates the page number currently returned for a paginated response.   3. X-Page-Size : Indicates the number of entries per page for a paginated response.  For example:    ``` X-Total-Elements : 30 X-Page-Number : 0 X-Page-Size : 10   ```   # noqa: E501

    OpenAPI spec version: 1.0
    Contact: contact@harness.io
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class ChannelDTO(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'api_key': 'str',
        'datadog_urls': 'list[str]',
        'delegate_selectors': 'list[str]',
        'email_ids': 'list[str]',
        'execute_on_delegate': 'bool',
        'headers': 'list[WebHookHeaders]',
        'ms_team_keys': 'list[str]',
        'pager_duty_integration_keys': 'list[str]',
        'slack_webhook_urls': 'list[str]',
        'user_groups': 'list[UserGroupDTO1]',
        'webhook_urls': 'list[str]'
    }

    attribute_map = {
        'api_key': 'api_key',
        'datadog_urls': 'datadog_urls',
        'delegate_selectors': 'delegate_selectors',
        'email_ids': 'email_ids',
        'execute_on_delegate': 'execute_on_delegate',
        'headers': 'headers',
        'ms_team_keys': 'ms_team_keys',
        'pager_duty_integration_keys': 'pager_duty_integration_keys',
        'slack_webhook_urls': 'slack_webhook_urls',
        'user_groups': 'user_groups',
        'webhook_urls': 'webhook_urls'
    }

    def __init__(self, api_key=None, datadog_urls=None, delegate_selectors=None, email_ids=None, execute_on_delegate=None, headers=None, ms_team_keys=None, pager_duty_integration_keys=None, slack_webhook_urls=None, user_groups=None, webhook_urls=None):  # noqa: E501
        """ChannelDTO - a model defined in Swagger"""  # noqa: E501
        self._api_key = None
        self._datadog_urls = None
        self._delegate_selectors = None
        self._email_ids = None
        self._execute_on_delegate = None
        self._headers = None
        self._ms_team_keys = None
        self._pager_duty_integration_keys = None
        self._slack_webhook_urls = None
        self._user_groups = None
        self._webhook_urls = None
        self.discriminator = None
        if api_key is not None:
            self.api_key = api_key
        if datadog_urls is not None:
            self.datadog_urls = datadog_urls
        if delegate_selectors is not None:
            self.delegate_selectors = delegate_selectors
        if email_ids is not None:
            self.email_ids = email_ids
        if execute_on_delegate is not None:
            self.execute_on_delegate = execute_on_delegate
        if headers is not None:
            self.headers = headers
        if ms_team_keys is not None:
            self.ms_team_keys = ms_team_keys
        if pager_duty_integration_keys is not None:
            self.pager_duty_integration_keys = pager_duty_integration_keys
        if slack_webhook_urls is not None:
            self.slack_webhook_urls = slack_webhook_urls
        if user_groups is not None:
            self.user_groups = user_groups
        if webhook_urls is not None:
            self.webhook_urls = webhook_urls

    @property
    def api_key(self):
        """Gets the api_key of this ChannelDTO.  # noqa: E501


        :return: The api_key of this ChannelDTO.  # noqa: E501
        :rtype: str
        """
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        """Sets the api_key of this ChannelDTO.


        :param api_key: The api_key of this ChannelDTO.  # noqa: E501
        :type: str
        """

        self._api_key = api_key

    @property
    def datadog_urls(self):
        """Gets the datadog_urls of this ChannelDTO.  # noqa: E501


        :return: The datadog_urls of this ChannelDTO.  # noqa: E501
        :rtype: list[str]
        """
        return self._datadog_urls

    @datadog_urls.setter
    def datadog_urls(self, datadog_urls):
        """Sets the datadog_urls of this ChannelDTO.


        :param datadog_urls: The datadog_urls of this ChannelDTO.  # noqa: E501
        :type: list[str]
        """

        self._datadog_urls = datadog_urls

    @property
    def delegate_selectors(self):
        """Gets the delegate_selectors of this ChannelDTO.  # noqa: E501


        :return: The delegate_selectors of this ChannelDTO.  # noqa: E501
        :rtype: list[str]
        """
        return self._delegate_selectors

    @delegate_selectors.setter
    def delegate_selectors(self, delegate_selectors):
        """Sets the delegate_selectors of this ChannelDTO.


        :param delegate_selectors: The delegate_selectors of this ChannelDTO.  # noqa: E501
        :type: list[str]
        """

        self._delegate_selectors = delegate_selectors

    @property
    def email_ids(self):
        """Gets the email_ids of this ChannelDTO.  # noqa: E501


        :return: The email_ids of this ChannelDTO.  # noqa: E501
        :rtype: list[str]
        """
        return self._email_ids

    @email_ids.setter
    def email_ids(self, email_ids):
        """Sets the email_ids of this ChannelDTO.


        :param email_ids: The email_ids of this ChannelDTO.  # noqa: E501
        :type: list[str]
        """

        self._email_ids = email_ids

    @property
    def execute_on_delegate(self):
        """Gets the execute_on_delegate of this ChannelDTO.  # noqa: E501


        :return: The execute_on_delegate of this ChannelDTO.  # noqa: E501
        :rtype: bool
        """
        return self._execute_on_delegate

    @execute_on_delegate.setter
    def execute_on_delegate(self, execute_on_delegate):
        """Sets the execute_on_delegate of this ChannelDTO.


        :param execute_on_delegate: The execute_on_delegate of this ChannelDTO.  # noqa: E501
        :type: bool
        """

        self._execute_on_delegate = execute_on_delegate

    @property
    def headers(self):
        """Gets the headers of this ChannelDTO.  # noqa: E501


        :return: The headers of this ChannelDTO.  # noqa: E501
        :rtype: list[WebHookHeaders]
        """
        return self._headers

    @headers.setter
    def headers(self, headers):
        """Sets the headers of this ChannelDTO.


        :param headers: The headers of this ChannelDTO.  # noqa: E501
        :type: list[WebHookHeaders]
        """

        self._headers = headers

    @property
    def ms_team_keys(self):
        """Gets the ms_team_keys of this ChannelDTO.  # noqa: E501


        :return: The ms_team_keys of this ChannelDTO.  # noqa: E501
        :rtype: list[str]
        """
        return self._ms_team_keys

    @ms_team_keys.setter
    def ms_team_keys(self, ms_team_keys):
        """Sets the ms_team_keys of this ChannelDTO.


        :param ms_team_keys: The ms_team_keys of this ChannelDTO.  # noqa: E501
        :type: list[str]
        """

        self._ms_team_keys = ms_team_keys

    @property
    def pager_duty_integration_keys(self):
        """Gets the pager_duty_integration_keys of this ChannelDTO.  # noqa: E501


        :return: The pager_duty_integration_keys of this ChannelDTO.  # noqa: E501
        :rtype: list[str]
        """
        return self._pager_duty_integration_keys

    @pager_duty_integration_keys.setter
    def pager_duty_integration_keys(self, pager_duty_integration_keys):
        """Sets the pager_duty_integration_keys of this ChannelDTO.


        :param pager_duty_integration_keys: The pager_duty_integration_keys of this ChannelDTO.  # noqa: E501
        :type: list[str]
        """

        self._pager_duty_integration_keys = pager_duty_integration_keys

    @property
    def slack_webhook_urls(self):
        """Gets the slack_webhook_urls of this ChannelDTO.  # noqa: E501


        :return: The slack_webhook_urls of this ChannelDTO.  # noqa: E501
        :rtype: list[str]
        """
        return self._slack_webhook_urls

    @slack_webhook_urls.setter
    def slack_webhook_urls(self, slack_webhook_urls):
        """Sets the slack_webhook_urls of this ChannelDTO.


        :param slack_webhook_urls: The slack_webhook_urls of this ChannelDTO.  # noqa: E501
        :type: list[str]
        """

        self._slack_webhook_urls = slack_webhook_urls

    @property
    def user_groups(self):
        """Gets the user_groups of this ChannelDTO.  # noqa: E501


        :return: The user_groups of this ChannelDTO.  # noqa: E501
        :rtype: list[UserGroupDTO1]
        """
        return self._user_groups

    @user_groups.setter
    def user_groups(self, user_groups):
        """Sets the user_groups of this ChannelDTO.


        :param user_groups: The user_groups of this ChannelDTO.  # noqa: E501
        :type: list[UserGroupDTO1]
        """

        self._user_groups = user_groups

    @property
    def webhook_urls(self):
        """Gets the webhook_urls of this ChannelDTO.  # noqa: E501


        :return: The webhook_urls of this ChannelDTO.  # noqa: E501
        :rtype: list[str]
        """
        return self._webhook_urls

    @webhook_urls.setter
    def webhook_urls(self, webhook_urls):
        """Sets the webhook_urls of this ChannelDTO.


        :param webhook_urls: The webhook_urls of this ChannelDTO.  # noqa: E501
        :type: list[str]
        """

        self._webhook_urls = webhook_urls

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(ChannelDTO, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ChannelDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
