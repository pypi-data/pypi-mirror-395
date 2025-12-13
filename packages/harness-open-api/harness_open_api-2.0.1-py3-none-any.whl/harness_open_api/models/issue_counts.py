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

class IssueCounts(object):
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
        'critical': 'int',
        'high': 'int',
        'ignored': 'int',
        'info': 'int',
        'low': 'int',
        'medium': 'int',
        'new_critical': 'int',
        'new_high': 'int',
        'new_info': 'int',
        'new_low': 'int',
        'new_medium': 'int',
        'new_unassigned': 'int',
        'unassigned': 'int'
    }

    attribute_map = {
        'critical': 'critical',
        'high': 'high',
        'ignored': 'ignored',
        'info': 'info',
        'low': 'low',
        'medium': 'medium',
        'new_critical': 'newCritical',
        'new_high': 'newHigh',
        'new_info': 'newInfo',
        'new_low': 'newLow',
        'new_medium': 'newMedium',
        'new_unassigned': 'newUnassigned',
        'unassigned': 'unassigned'
    }

    def __init__(self, critical=None, high=None, ignored=None, info=None, low=None, medium=None, new_critical=None, new_high=None, new_info=None, new_low=None, new_medium=None, new_unassigned=None, unassigned=None):  # noqa: E501
        """IssueCounts - a model defined in Swagger"""  # noqa: E501
        self._critical = None
        self._high = None
        self._ignored = None
        self._info = None
        self._low = None
        self._medium = None
        self._new_critical = None
        self._new_high = None
        self._new_info = None
        self._new_low = None
        self._new_medium = None
        self._new_unassigned = None
        self._unassigned = None
        self.discriminator = None
        self.critical = critical
        self.high = high
        if ignored is not None:
            self.ignored = ignored
        self.info = info
        self.low = low
        self.medium = medium
        if new_critical is not None:
            self.new_critical = new_critical
        if new_high is not None:
            self.new_high = new_high
        if new_info is not None:
            self.new_info = new_info
        if new_low is not None:
            self.new_low = new_low
        if new_medium is not None:
            self.new_medium = new_medium
        if new_unassigned is not None:
            self.new_unassigned = new_unassigned
        if unassigned is not None:
            self.unassigned = unassigned

    @property
    def critical(self):
        """Gets the critical of this IssueCounts.  # noqa: E501

        The number of Critical-severity Issues  # noqa: E501

        :return: The critical of this IssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._critical

    @critical.setter
    def critical(self, critical):
        """Sets the critical of this IssueCounts.

        The number of Critical-severity Issues  # noqa: E501

        :param critical: The critical of this IssueCounts.  # noqa: E501
        :type: int
        """
        if critical is None:
            raise ValueError("Invalid value for `critical`, must not be `None`")  # noqa: E501

        self._critical = critical

    @property
    def high(self):
        """Gets the high of this IssueCounts.  # noqa: E501

        The number of High-severity Issues  # noqa: E501

        :return: The high of this IssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._high

    @high.setter
    def high(self, high):
        """Sets the high of this IssueCounts.

        The number of High-severity Issues  # noqa: E501

        :param high: The high of this IssueCounts.  # noqa: E501
        :type: int
        """
        if high is None:
            raise ValueError("Invalid value for `high`, must not be `None`")  # noqa: E501

        self._high = high

    @property
    def ignored(self):
        """Gets the ignored of this IssueCounts.  # noqa: E501

        The number of Issues ignored due to Exemptions, and therefore not included in other counts  # noqa: E501

        :return: The ignored of this IssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._ignored

    @ignored.setter
    def ignored(self, ignored):
        """Sets the ignored of this IssueCounts.

        The number of Issues ignored due to Exemptions, and therefore not included in other counts  # noqa: E501

        :param ignored: The ignored of this IssueCounts.  # noqa: E501
        :type: int
        """

        self._ignored = ignored

    @property
    def info(self):
        """Gets the info of this IssueCounts.  # noqa: E501

        The number of Informational Issues  # noqa: E501

        :return: The info of this IssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._info

    @info.setter
    def info(self, info):
        """Sets the info of this IssueCounts.

        The number of Informational Issues  # noqa: E501

        :param info: The info of this IssueCounts.  # noqa: E501
        :type: int
        """
        if info is None:
            raise ValueError("Invalid value for `info`, must not be `None`")  # noqa: E501

        self._info = info

    @property
    def low(self):
        """Gets the low of this IssueCounts.  # noqa: E501

        The number of Low-severity Issues  # noqa: E501

        :return: The low of this IssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._low

    @low.setter
    def low(self, low):
        """Sets the low of this IssueCounts.

        The number of Low-severity Issues  # noqa: E501

        :param low: The low of this IssueCounts.  # noqa: E501
        :type: int
        """
        if low is None:
            raise ValueError("Invalid value for `low`, must not be `None`")  # noqa: E501

        self._low = low

    @property
    def medium(self):
        """Gets the medium of this IssueCounts.  # noqa: E501

        The number of Medium-severity Issues  # noqa: E501

        :return: The medium of this IssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._medium

    @medium.setter
    def medium(self, medium):
        """Sets the medium of this IssueCounts.

        The number of Medium-severity Issues  # noqa: E501

        :param medium: The medium of this IssueCounts.  # noqa: E501
        :type: int
        """
        if medium is None:
            raise ValueError("Invalid value for `medium`, must not be `None`")  # noqa: E501

        self._medium = medium

    @property
    def new_critical(self):
        """Gets the new_critical of this IssueCounts.  # noqa: E501

        The number of new Critical-severity Issues  # noqa: E501

        :return: The new_critical of this IssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_critical

    @new_critical.setter
    def new_critical(self, new_critical):
        """Sets the new_critical of this IssueCounts.

        The number of new Critical-severity Issues  # noqa: E501

        :param new_critical: The new_critical of this IssueCounts.  # noqa: E501
        :type: int
        """

        self._new_critical = new_critical

    @property
    def new_high(self):
        """Gets the new_high of this IssueCounts.  # noqa: E501

        The number of new High-severity Issues  # noqa: E501

        :return: The new_high of this IssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_high

    @new_high.setter
    def new_high(self, new_high):
        """Sets the new_high of this IssueCounts.

        The number of new High-severity Issues  # noqa: E501

        :param new_high: The new_high of this IssueCounts.  # noqa: E501
        :type: int
        """

        self._new_high = new_high

    @property
    def new_info(self):
        """Gets the new_info of this IssueCounts.  # noqa: E501

        The number of new Informational Issues  # noqa: E501

        :return: The new_info of this IssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_info

    @new_info.setter
    def new_info(self, new_info):
        """Sets the new_info of this IssueCounts.

        The number of new Informational Issues  # noqa: E501

        :param new_info: The new_info of this IssueCounts.  # noqa: E501
        :type: int
        """

        self._new_info = new_info

    @property
    def new_low(self):
        """Gets the new_low of this IssueCounts.  # noqa: E501

        The number of new Low-severity Issues  # noqa: E501

        :return: The new_low of this IssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_low

    @new_low.setter
    def new_low(self, new_low):
        """Sets the new_low of this IssueCounts.

        The number of new Low-severity Issues  # noqa: E501

        :param new_low: The new_low of this IssueCounts.  # noqa: E501
        :type: int
        """

        self._new_low = new_low

    @property
    def new_medium(self):
        """Gets the new_medium of this IssueCounts.  # noqa: E501

        The number of new Medium-severity Issues  # noqa: E501

        :return: The new_medium of this IssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_medium

    @new_medium.setter
    def new_medium(self, new_medium):
        """Sets the new_medium of this IssueCounts.

        The number of new Medium-severity Issues  # noqa: E501

        :param new_medium: The new_medium of this IssueCounts.  # noqa: E501
        :type: int
        """

        self._new_medium = new_medium

    @property
    def new_unassigned(self):
        """Gets the new_unassigned of this IssueCounts.  # noqa: E501

        The number of new Issues with no associated severity code  # noqa: E501

        :return: The new_unassigned of this IssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_unassigned

    @new_unassigned.setter
    def new_unassigned(self, new_unassigned):
        """Sets the new_unassigned of this IssueCounts.

        The number of new Issues with no associated severity code  # noqa: E501

        :param new_unassigned: The new_unassigned of this IssueCounts.  # noqa: E501
        :type: int
        """

        self._new_unassigned = new_unassigned

    @property
    def unassigned(self):
        """Gets the unassigned of this IssueCounts.  # noqa: E501

        The number of Issues with no associated severity code  # noqa: E501

        :return: The unassigned of this IssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._unassigned

    @unassigned.setter
    def unassigned(self, unassigned):
        """Sets the unassigned of this IssueCounts.

        The number of Issues with no associated severity code  # noqa: E501

        :param unassigned: The unassigned of this IssueCounts.  # noqa: E501
        :type: int
        """

        self._unassigned = unassigned

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
        if issubclass(IssueCounts, dict):
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
        if not isinstance(other, IssueCounts):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
