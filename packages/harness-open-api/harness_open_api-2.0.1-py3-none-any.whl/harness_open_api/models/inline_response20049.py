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

class InlineResponse20049(object):
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
        'access_token': 'str',
        'app_id': 'str',
        'authed_user': 'AuthedUser',
        'bot_user_id': 'str',
        'enterprise': 'Enterprise',
        'expires_in': 'int',
        'is_enterprise_install': 'bool',
        'ok': 'bool',
        'refresh_token': 'str',
        'scope': 'str',
        'team': 'Team',
        'token_type': 'str'
    }

    attribute_map = {
        'access_token': 'access_token',
        'app_id': 'app_id',
        'authed_user': 'authed_user',
        'bot_user_id': 'bot_user_id',
        'enterprise': 'enterprise',
        'expires_in': 'expires_in',
        'is_enterprise_install': 'is_enterprise_install',
        'ok': 'ok',
        'refresh_token': 'refresh_token',
        'scope': 'scope',
        'team': 'team',
        'token_type': 'token_type'
    }

    def __init__(self, access_token=None, app_id=None, authed_user=None, bot_user_id=None, enterprise=None, expires_in=None, is_enterprise_install=None, ok=None, refresh_token=None, scope=None, team=None, token_type=None):  # noqa: E501
        """InlineResponse20049 - a model defined in Swagger"""  # noqa: E501
        self._access_token = None
        self._app_id = None
        self._authed_user = None
        self._bot_user_id = None
        self._enterprise = None
        self._expires_in = None
        self._is_enterprise_install = None
        self._ok = None
        self._refresh_token = None
        self._scope = None
        self._team = None
        self._token_type = None
        self.discriminator = None
        if access_token is not None:
            self.access_token = access_token
        if app_id is not None:
            self.app_id = app_id
        if authed_user is not None:
            self.authed_user = authed_user
        if bot_user_id is not None:
            self.bot_user_id = bot_user_id
        if enterprise is not None:
            self.enterprise = enterprise
        if expires_in is not None:
            self.expires_in = expires_in
        if is_enterprise_install is not None:
            self.is_enterprise_install = is_enterprise_install
        if ok is not None:
            self.ok = ok
        if refresh_token is not None:
            self.refresh_token = refresh_token
        if scope is not None:
            self.scope = scope
        if team is not None:
            self.team = team
        if token_type is not None:
            self.token_type = token_type

    @property
    def access_token(self):
        """Gets the access_token of this InlineResponse20049.  # noqa: E501

        The access token for the application.  # noqa: E501

        :return: The access_token of this InlineResponse20049.  # noqa: E501
        :rtype: str
        """
        return self._access_token

    @access_token.setter
    def access_token(self, access_token):
        """Sets the access_token of this InlineResponse20049.

        The access token for the application.  # noqa: E501

        :param access_token: The access_token of this InlineResponse20049.  # noqa: E501
        :type: str
        """

        self._access_token = access_token

    @property
    def app_id(self):
        """Gets the app_id of this InlineResponse20049.  # noqa: E501

        The ID of the Slack application.  # noqa: E501

        :return: The app_id of this InlineResponse20049.  # noqa: E501
        :rtype: str
        """
        return self._app_id

    @app_id.setter
    def app_id(self, app_id):
        """Sets the app_id of this InlineResponse20049.

        The ID of the Slack application.  # noqa: E501

        :param app_id: The app_id of this InlineResponse20049.  # noqa: E501
        :type: str
        """

        self._app_id = app_id

    @property
    def authed_user(self):
        """Gets the authed_user of this InlineResponse20049.  # noqa: E501


        :return: The authed_user of this InlineResponse20049.  # noqa: E501
        :rtype: AuthedUser
        """
        return self._authed_user

    @authed_user.setter
    def authed_user(self, authed_user):
        """Sets the authed_user of this InlineResponse20049.


        :param authed_user: The authed_user of this InlineResponse20049.  # noqa: E501
        :type: AuthedUser
        """

        self._authed_user = authed_user

    @property
    def bot_user_id(self):
        """Gets the bot_user_id of this InlineResponse20049.  # noqa: E501

        The bot user ID associated with the token.  # noqa: E501

        :return: The bot_user_id of this InlineResponse20049.  # noqa: E501
        :rtype: str
        """
        return self._bot_user_id

    @bot_user_id.setter
    def bot_user_id(self, bot_user_id):
        """Sets the bot_user_id of this InlineResponse20049.

        The bot user ID associated with the token.  # noqa: E501

        :param bot_user_id: The bot_user_id of this InlineResponse20049.  # noqa: E501
        :type: str
        """

        self._bot_user_id = bot_user_id

    @property
    def enterprise(self):
        """Gets the enterprise of this InlineResponse20049.  # noqa: E501


        :return: The enterprise of this InlineResponse20049.  # noqa: E501
        :rtype: Enterprise
        """
        return self._enterprise

    @enterprise.setter
    def enterprise(self, enterprise):
        """Sets the enterprise of this InlineResponse20049.


        :param enterprise: The enterprise of this InlineResponse20049.  # noqa: E501
        :type: Enterprise
        """

        self._enterprise = enterprise

    @property
    def expires_in(self):
        """Gets the expires_in of this InlineResponse20049.  # noqa: E501

        The number of seconds until the token expires.  # noqa: E501

        :return: The expires_in of this InlineResponse20049.  # noqa: E501
        :rtype: int
        """
        return self._expires_in

    @expires_in.setter
    def expires_in(self, expires_in):
        """Sets the expires_in of this InlineResponse20049.

        The number of seconds until the token expires.  # noqa: E501

        :param expires_in: The expires_in of this InlineResponse20049.  # noqa: E501
        :type: int
        """

        self._expires_in = expires_in

    @property
    def is_enterprise_install(self):
        """Gets the is_enterprise_install of this InlineResponse20049.  # noqa: E501

        Indicates if the installation is for an enterprise.  # noqa: E501

        :return: The is_enterprise_install of this InlineResponse20049.  # noqa: E501
        :rtype: bool
        """
        return self._is_enterprise_install

    @is_enterprise_install.setter
    def is_enterprise_install(self, is_enterprise_install):
        """Sets the is_enterprise_install of this InlineResponse20049.

        Indicates if the installation is for an enterprise.  # noqa: E501

        :param is_enterprise_install: The is_enterprise_install of this InlineResponse20049.  # noqa: E501
        :type: bool
        """

        self._is_enterprise_install = is_enterprise_install

    @property
    def ok(self):
        """Gets the ok of this InlineResponse20049.  # noqa: E501

        Indicates whether the request was successful.  # noqa: E501

        :return: The ok of this InlineResponse20049.  # noqa: E501
        :rtype: bool
        """
        return self._ok

    @ok.setter
    def ok(self, ok):
        """Sets the ok of this InlineResponse20049.

        Indicates whether the request was successful.  # noqa: E501

        :param ok: The ok of this InlineResponse20049.  # noqa: E501
        :type: bool
        """

        self._ok = ok

    @property
    def refresh_token(self):
        """Gets the refresh_token of this InlineResponse20049.  # noqa: E501

        The refresh token for the application.  # noqa: E501

        :return: The refresh_token of this InlineResponse20049.  # noqa: E501
        :rtype: str
        """
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self, refresh_token):
        """Sets the refresh_token of this InlineResponse20049.

        The refresh token for the application.  # noqa: E501

        :param refresh_token: The refresh_token of this InlineResponse20049.  # noqa: E501
        :type: str
        """

        self._refresh_token = refresh_token

    @property
    def scope(self):
        """Gets the scope of this InlineResponse20049.  # noqa: E501

        The scopes granted to the application.  # noqa: E501

        :return: The scope of this InlineResponse20049.  # noqa: E501
        :rtype: str
        """
        return self._scope

    @scope.setter
    def scope(self, scope):
        """Sets the scope of this InlineResponse20049.

        The scopes granted to the application.  # noqa: E501

        :param scope: The scope of this InlineResponse20049.  # noqa: E501
        :type: str
        """

        self._scope = scope

    @property
    def team(self):
        """Gets the team of this InlineResponse20049.  # noqa: E501


        :return: The team of this InlineResponse20049.  # noqa: E501
        :rtype: Team
        """
        return self._team

    @team.setter
    def team(self, team):
        """Sets the team of this InlineResponse20049.


        :param team: The team of this InlineResponse20049.  # noqa: E501
        :type: Team
        """

        self._team = team

    @property
    def token_type(self):
        """Gets the token_type of this InlineResponse20049.  # noqa: E501

        The type of token issued.  # noqa: E501

        :return: The token_type of this InlineResponse20049.  # noqa: E501
        :rtype: str
        """
        return self._token_type

    @token_type.setter
    def token_type(self, token_type):
        """Sets the token_type of this InlineResponse20049.

        The type of token issued.  # noqa: E501

        :param token_type: The token_type of this InlineResponse20049.  # noqa: E501
        :type: str
        """

        self._token_type = token_type

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
        if issubclass(InlineResponse20049, dict):
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
        if not isinstance(other, InlineResponse20049):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
