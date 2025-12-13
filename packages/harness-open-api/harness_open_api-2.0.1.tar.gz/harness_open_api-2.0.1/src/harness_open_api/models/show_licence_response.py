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

class ShowLicenceResponse(object):
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
        'account': 'str',
        'is_licenced': 'bool',
        'is_paid': 'bool',
        'reason': 'str',
        'start_time': 'int',
        'total': 'int',
        'used': 'int'
    }

    attribute_map = {
        'account': 'account',
        'is_licenced': 'isLicenced',
        'is_paid': 'isPaid',
        'reason': 'reason',
        'start_time': 'startTime',
        'total': 'total',
        'used': 'used'
    }

    def __init__(self, account=None, is_licenced=None, is_paid=None, reason=None, start_time=None, total=None, used=None):  # noqa: E501
        """ShowLicenceResponse - a model defined in Swagger"""  # noqa: E501
        self._account = None
        self._is_licenced = None
        self._is_paid = None
        self._reason = None
        self._start_time = None
        self._total = None
        self._used = None
        self.discriminator = None
        self.account = account
        self.is_licenced = is_licenced
        self.is_paid = is_paid
        if reason is not None:
            self.reason = reason
        self.start_time = start_time
        self.total = total
        self.used = used

    @property
    def account(self):
        """Gets the account of this ShowLicenceResponse.  # noqa: E501

        Account identifier  # noqa: E501

        :return: The account of this ShowLicenceResponse.  # noqa: E501
        :rtype: str
        """
        return self._account

    @account.setter
    def account(self, account):
        """Sets the account of this ShowLicenceResponse.

        Account identifier  # noqa: E501

        :param account: The account of this ShowLicenceResponse.  # noqa: E501
        :type: str
        """
        if account is None:
            raise ValueError("Invalid value for `account`, must not be `None`")  # noqa: E501

        self._account = account

    @property
    def is_licenced(self):
        """Gets the is_licenced of this ShowLicenceResponse.  # noqa: E501

        True when this account is currently licenced to execute apply operations  # noqa: E501

        :return: The is_licenced of this ShowLicenceResponse.  # noqa: E501
        :rtype: bool
        """
        return self._is_licenced

    @is_licenced.setter
    def is_licenced(self, is_licenced):
        """Sets the is_licenced of this ShowLicenceResponse.

        True when this account is currently licenced to execute apply operations  # noqa: E501

        :param is_licenced: The is_licenced of this ShowLicenceResponse.  # noqa: E501
        :type: bool
        """
        if is_licenced is None:
            raise ValueError("Invalid value for `is_licenced`, must not be `None`")  # noqa: E501

        self._is_licenced = is_licenced

    @property
    def is_paid(self):
        """Gets the is_paid of this ShowLicenceResponse.  # noqa: E501

        True when this account is a paid account  # noqa: E501

        :return: The is_paid of this ShowLicenceResponse.  # noqa: E501
        :rtype: bool
        """
        return self._is_paid

    @is_paid.setter
    def is_paid(self, is_paid):
        """Sets the is_paid of this ShowLicenceResponse.

        True when this account is a paid account  # noqa: E501

        :param is_paid: The is_paid of this ShowLicenceResponse.  # noqa: E501
        :type: bool
        """
        if is_paid is None:
            raise ValueError("Invalid value for `is_paid`, must not be `None`")  # noqa: E501

        self._is_paid = is_paid

    @property
    def reason(self):
        """Gets the reason of this ShowLicenceResponse.  # noqa: E501

        If the account is not licenced, this is the reason why  # noqa: E501

        :return: The reason of this ShowLicenceResponse.  # noqa: E501
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """Sets the reason of this ShowLicenceResponse.

        If the account is not licenced, this is the reason why  # noqa: E501

        :param reason: The reason of this ShowLicenceResponse.  # noqa: E501
        :type: str
        """

        self._reason = reason

    @property
    def start_time(self):
        """Gets the start_time of this ShowLicenceResponse.  # noqa: E501

        The unix timestamp of the current period over which usage was calculated  # noqa: E501

        :return: The start_time of this ShowLicenceResponse.  # noqa: E501
        :rtype: int
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this ShowLicenceResponse.

        The unix timestamp of the current period over which usage was calculated  # noqa: E501

        :param start_time: The start_time of this ShowLicenceResponse.  # noqa: E501
        :type: int
        """
        if start_time is None:
            raise ValueError("Invalid value for `start_time`, must not be `None`")  # noqa: E501

        self._start_time = start_time

    @property
    def total(self):
        """Gets the total of this ShowLicenceResponse.  # noqa: E501

        The total number of successful apply operations this account is licenced to perform  # noqa: E501

        :return: The total of this ShowLicenceResponse.  # noqa: E501
        :rtype: int
        """
        return self._total

    @total.setter
    def total(self, total):
        """Sets the total of this ShowLicenceResponse.

        The total number of successful apply operations this account is licenced to perform  # noqa: E501

        :param total: The total of this ShowLicenceResponse.  # noqa: E501
        :type: int
        """
        if total is None:
            raise ValueError("Invalid value for `total`, must not be `None`")  # noqa: E501

        self._total = total

    @property
    def used(self):
        """Gets the used of this ShowLicenceResponse.  # noqa: E501

        The count of successful apply operations already performed  # noqa: E501

        :return: The used of this ShowLicenceResponse.  # noqa: E501
        :rtype: int
        """
        return self._used

    @used.setter
    def used(self, used):
        """Sets the used of this ShowLicenceResponse.

        The count of successful apply operations already performed  # noqa: E501

        :param used: The used of this ShowLicenceResponse.  # noqa: E501
        :type: int
        """
        if used is None:
            raise ValueError("Invalid value for `used`, must not be `None`")  # noqa: E501

        self._used = used

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
        if issubclass(ShowLicenceResponse, dict):
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
        if not isinstance(other, ShowLicenceResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
