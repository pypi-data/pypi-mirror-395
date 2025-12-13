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

class LdapConnectionSettingsDTO1(object):
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
        'bind_d_n': 'str',
        'connection_timeout': 'int',
        'delegate_selectors': 'list[str]',
        'host': 'str',
        'max_referral_hops': 'int',
        'port': 'int',
        'referrals_enabled': 'bool',
        'response_timeout': 'int',
        'secret_ref_path': 'str',
        'ssl_enabled': 'bool',
        'use_recursive_group_membership_search': 'bool'
    }

    attribute_map = {
        'bind_d_n': 'bind_d_n',
        'connection_timeout': 'connection_timeout',
        'delegate_selectors': 'delegate_selectors',
        'host': 'host',
        'max_referral_hops': 'max_referral_hops',
        'port': 'port',
        'referrals_enabled': 'referrals_enabled',
        'response_timeout': 'response_timeout',
        'secret_ref_path': 'secret_ref_path',
        'ssl_enabled': 'ssl_enabled',
        'use_recursive_group_membership_search': 'use_recursive_group_membership_search'
    }

    def __init__(self, bind_d_n=None, connection_timeout=None, delegate_selectors=None, host=None, max_referral_hops=None, port=None, referrals_enabled=None, response_timeout=None, secret_ref_path=None, ssl_enabled=None, use_recursive_group_membership_search=None):  # noqa: E501
        """LdapConnectionSettingsDTO1 - a model defined in Swagger"""  # noqa: E501
        self._bind_d_n = None
        self._connection_timeout = None
        self._delegate_selectors = None
        self._host = None
        self._max_referral_hops = None
        self._port = None
        self._referrals_enabled = None
        self._response_timeout = None
        self._secret_ref_path = None
        self._ssl_enabled = None
        self._use_recursive_group_membership_search = None
        self.discriminator = None
        if bind_d_n is not None:
            self.bind_d_n = bind_d_n
        if connection_timeout is not None:
            self.connection_timeout = connection_timeout
        if delegate_selectors is not None:
            self.delegate_selectors = delegate_selectors
        if host is not None:
            self.host = host
        if max_referral_hops is not None:
            self.max_referral_hops = max_referral_hops
        if port is not None:
            self.port = port
        if referrals_enabled is not None:
            self.referrals_enabled = referrals_enabled
        if response_timeout is not None:
            self.response_timeout = response_timeout
        if secret_ref_path is not None:
            self.secret_ref_path = secret_ref_path
        if ssl_enabled is not None:
            self.ssl_enabled = ssl_enabled
        if use_recursive_group_membership_search is not None:
            self.use_recursive_group_membership_search = use_recursive_group_membership_search

    @property
    def bind_d_n(self):
        """Gets the bind_d_n of this LdapConnectionSettingsDTO1.  # noqa: E501


        :return: The bind_d_n of this LdapConnectionSettingsDTO1.  # noqa: E501
        :rtype: str
        """
        return self._bind_d_n

    @bind_d_n.setter
    def bind_d_n(self, bind_d_n):
        """Sets the bind_d_n of this LdapConnectionSettingsDTO1.


        :param bind_d_n: The bind_d_n of this LdapConnectionSettingsDTO1.  # noqa: E501
        :type: str
        """

        self._bind_d_n = bind_d_n

    @property
    def connection_timeout(self):
        """Gets the connection_timeout of this LdapConnectionSettingsDTO1.  # noqa: E501


        :return: The connection_timeout of this LdapConnectionSettingsDTO1.  # noqa: E501
        :rtype: int
        """
        return self._connection_timeout

    @connection_timeout.setter
    def connection_timeout(self, connection_timeout):
        """Sets the connection_timeout of this LdapConnectionSettingsDTO1.


        :param connection_timeout: The connection_timeout of this LdapConnectionSettingsDTO1.  # noqa: E501
        :type: int
        """

        self._connection_timeout = connection_timeout

    @property
    def delegate_selectors(self):
        """Gets the delegate_selectors of this LdapConnectionSettingsDTO1.  # noqa: E501


        :return: The delegate_selectors of this LdapConnectionSettingsDTO1.  # noqa: E501
        :rtype: list[str]
        """
        return self._delegate_selectors

    @delegate_selectors.setter
    def delegate_selectors(self, delegate_selectors):
        """Sets the delegate_selectors of this LdapConnectionSettingsDTO1.


        :param delegate_selectors: The delegate_selectors of this LdapConnectionSettingsDTO1.  # noqa: E501
        :type: list[str]
        """

        self._delegate_selectors = delegate_selectors

    @property
    def host(self):
        """Gets the host of this LdapConnectionSettingsDTO1.  # noqa: E501


        :return: The host of this LdapConnectionSettingsDTO1.  # noqa: E501
        :rtype: str
        """
        return self._host

    @host.setter
    def host(self, host):
        """Sets the host of this LdapConnectionSettingsDTO1.


        :param host: The host of this LdapConnectionSettingsDTO1.  # noqa: E501
        :type: str
        """

        self._host = host

    @property
    def max_referral_hops(self):
        """Gets the max_referral_hops of this LdapConnectionSettingsDTO1.  # noqa: E501


        :return: The max_referral_hops of this LdapConnectionSettingsDTO1.  # noqa: E501
        :rtype: int
        """
        return self._max_referral_hops

    @max_referral_hops.setter
    def max_referral_hops(self, max_referral_hops):
        """Sets the max_referral_hops of this LdapConnectionSettingsDTO1.


        :param max_referral_hops: The max_referral_hops of this LdapConnectionSettingsDTO1.  # noqa: E501
        :type: int
        """

        self._max_referral_hops = max_referral_hops

    @property
    def port(self):
        """Gets the port of this LdapConnectionSettingsDTO1.  # noqa: E501


        :return: The port of this LdapConnectionSettingsDTO1.  # noqa: E501
        :rtype: int
        """
        return self._port

    @port.setter
    def port(self, port):
        """Sets the port of this LdapConnectionSettingsDTO1.


        :param port: The port of this LdapConnectionSettingsDTO1.  # noqa: E501
        :type: int
        """

        self._port = port

    @property
    def referrals_enabled(self):
        """Gets the referrals_enabled of this LdapConnectionSettingsDTO1.  # noqa: E501


        :return: The referrals_enabled of this LdapConnectionSettingsDTO1.  # noqa: E501
        :rtype: bool
        """
        return self._referrals_enabled

    @referrals_enabled.setter
    def referrals_enabled(self, referrals_enabled):
        """Sets the referrals_enabled of this LdapConnectionSettingsDTO1.


        :param referrals_enabled: The referrals_enabled of this LdapConnectionSettingsDTO1.  # noqa: E501
        :type: bool
        """

        self._referrals_enabled = referrals_enabled

    @property
    def response_timeout(self):
        """Gets the response_timeout of this LdapConnectionSettingsDTO1.  # noqa: E501


        :return: The response_timeout of this LdapConnectionSettingsDTO1.  # noqa: E501
        :rtype: int
        """
        return self._response_timeout

    @response_timeout.setter
    def response_timeout(self, response_timeout):
        """Sets the response_timeout of this LdapConnectionSettingsDTO1.


        :param response_timeout: The response_timeout of this LdapConnectionSettingsDTO1.  # noqa: E501
        :type: int
        """

        self._response_timeout = response_timeout

    @property
    def secret_ref_path(self):
        """Gets the secret_ref_path of this LdapConnectionSettingsDTO1.  # noqa: E501


        :return: The secret_ref_path of this LdapConnectionSettingsDTO1.  # noqa: E501
        :rtype: str
        """
        return self._secret_ref_path

    @secret_ref_path.setter
    def secret_ref_path(self, secret_ref_path):
        """Sets the secret_ref_path of this LdapConnectionSettingsDTO1.


        :param secret_ref_path: The secret_ref_path of this LdapConnectionSettingsDTO1.  # noqa: E501
        :type: str
        """

        self._secret_ref_path = secret_ref_path

    @property
    def ssl_enabled(self):
        """Gets the ssl_enabled of this LdapConnectionSettingsDTO1.  # noqa: E501


        :return: The ssl_enabled of this LdapConnectionSettingsDTO1.  # noqa: E501
        :rtype: bool
        """
        return self._ssl_enabled

    @ssl_enabled.setter
    def ssl_enabled(self, ssl_enabled):
        """Sets the ssl_enabled of this LdapConnectionSettingsDTO1.


        :param ssl_enabled: The ssl_enabled of this LdapConnectionSettingsDTO1.  # noqa: E501
        :type: bool
        """

        self._ssl_enabled = ssl_enabled

    @property
    def use_recursive_group_membership_search(self):
        """Gets the use_recursive_group_membership_search of this LdapConnectionSettingsDTO1.  # noqa: E501


        :return: The use_recursive_group_membership_search of this LdapConnectionSettingsDTO1.  # noqa: E501
        :rtype: bool
        """
        return self._use_recursive_group_membership_search

    @use_recursive_group_membership_search.setter
    def use_recursive_group_membership_search(self, use_recursive_group_membership_search):
        """Sets the use_recursive_group_membership_search of this LdapConnectionSettingsDTO1.


        :param use_recursive_group_membership_search: The use_recursive_group_membership_search of this LdapConnectionSettingsDTO1.  # noqa: E501
        :type: bool
        """

        self._use_recursive_group_membership_search = use_recursive_group_membership_search

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
        if issubclass(LdapConnectionSettingsDTO1, dict):
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
        if not isinstance(other, LdapConnectionSettingsDTO1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
