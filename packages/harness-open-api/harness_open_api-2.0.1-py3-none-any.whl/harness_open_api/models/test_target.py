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

class TestTarget(object):
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
        'approved_variants_count': 'int',
        'baseline': 'TestTargetVariant',
        'baseline_reg_ex': 'str',
        'directory': 'str',
        'id': 'str',
        'last_scanned': 'int',
        'name': 'str',
        'status': 'str',
        'total_variants_count': 'int',
        'type': 'str',
        'url': 'str',
        'variants': 'list[TestTargetVariant]'
    }

    attribute_map = {
        'approved_variants_count': 'approvedVariantsCount',
        'baseline': 'baseline',
        'baseline_reg_ex': 'baselineRegEx',
        'directory': 'directory',
        'id': 'id',
        'last_scanned': 'lastScanned',
        'name': 'name',
        'status': 'status',
        'total_variants_count': 'totalVariantsCount',
        'type': 'type',
        'url': 'url',
        'variants': 'variants'
    }

    def __init__(self, approved_variants_count=None, baseline=None, baseline_reg_ex=None, directory=None, id=None, last_scanned=None, name=None, status=None, total_variants_count=None, type=None, url=None, variants=None):  # noqa: E501
        """TestTarget - a model defined in Swagger"""  # noqa: E501
        self._approved_variants_count = None
        self._baseline = None
        self._baseline_reg_ex = None
        self._directory = None
        self._id = None
        self._last_scanned = None
        self._name = None
        self._status = None
        self._total_variants_count = None
        self._type = None
        self._url = None
        self._variants = None
        self.discriminator = None
        self.approved_variants_count = approved_variants_count
        if baseline is not None:
            self.baseline = baseline
        if baseline_reg_ex is not None:
            self.baseline_reg_ex = baseline_reg_ex
        if directory is not None:
            self.directory = directory
        self.id = id
        self.last_scanned = last_scanned
        self.name = name
        if status is not None:
            self.status = status
        self.total_variants_count = total_variants_count
        self.type = type
        if url is not None:
            self.url = url
        self.variants = variants

    @property
    def approved_variants_count(self):
        """Gets the approved_variants_count of this TestTarget.  # noqa: E501

        Number of approved variants for a test target  # noqa: E501

        :return: The approved_variants_count of this TestTarget.  # noqa: E501
        :rtype: int
        """
        return self._approved_variants_count

    @approved_variants_count.setter
    def approved_variants_count(self, approved_variants_count):
        """Sets the approved_variants_count of this TestTarget.

        Number of approved variants for a test target  # noqa: E501

        :param approved_variants_count: The approved_variants_count of this TestTarget.  # noqa: E501
        :type: int
        """
        if approved_variants_count is None:
            raise ValueError("Invalid value for `approved_variants_count`, must not be `None`")  # noqa: E501

        self._approved_variants_count = approved_variants_count

    @property
    def baseline(self):
        """Gets the baseline of this TestTarget.  # noqa: E501


        :return: The baseline of this TestTarget.  # noqa: E501
        :rtype: TestTargetVariant
        """
        return self._baseline

    @baseline.setter
    def baseline(self, baseline):
        """Sets the baseline of this TestTarget.


        :param baseline: The baseline of this TestTarget.  # noqa: E501
        :type: TestTargetVariant
        """

        self._baseline = baseline

    @property
    def baseline_reg_ex(self):
        """Gets the baseline_reg_ex of this TestTarget.  # noqa: E501

        RegEx to match for dynamically selecting the Baseline for this Scan Target. Must be compatible with the RE2 standard.  # noqa: E501

        :return: The baseline_reg_ex of this TestTarget.  # noqa: E501
        :rtype: str
        """
        return self._baseline_reg_ex

    @baseline_reg_ex.setter
    def baseline_reg_ex(self, baseline_reg_ex):
        """Sets the baseline_reg_ex of this TestTarget.

        RegEx to match for dynamically selecting the Baseline for this Scan Target. Must be compatible with the RE2 standard.  # noqa: E501

        :param baseline_reg_ex: The baseline_reg_ex of this TestTarget.  # noqa: E501
        :type: str
        """

        self._baseline_reg_ex = baseline_reg_ex

    @property
    def directory(self):
        """Gets the directory of this TestTarget.  # noqa: E501

        Directory of target  # noqa: E501

        :return: The directory of this TestTarget.  # noqa: E501
        :rtype: str
        """
        return self._directory

    @directory.setter
    def directory(self, directory):
        """Sets the directory of this TestTarget.

        Directory of target  # noqa: E501

        :param directory: The directory of this TestTarget.  # noqa: E501
        :type: str
        """

        self._directory = directory

    @property
    def id(self):
        """Gets the id of this TestTarget.  # noqa: E501

        ID of target  # noqa: E501

        :return: The id of this TestTarget.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this TestTarget.

        ID of target  # noqa: E501

        :param id: The id of this TestTarget.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def last_scanned(self):
        """Gets the last_scanned of this TestTarget.  # noqa: E501

        Timestamp at which the Baseline was last scanned  # noqa: E501

        :return: The last_scanned of this TestTarget.  # noqa: E501
        :rtype: int
        """
        return self._last_scanned

    @last_scanned.setter
    def last_scanned(self, last_scanned):
        """Sets the last_scanned of this TestTarget.

        Timestamp at which the Baseline was last scanned  # noqa: E501

        :param last_scanned: The last_scanned of this TestTarget.  # noqa: E501
        :type: int
        """
        if last_scanned is None:
            raise ValueError("Invalid value for `last_scanned`, must not be `None`")  # noqa: E501

        self._last_scanned = last_scanned

    @property
    def name(self):
        """Gets the name of this TestTarget.  # noqa: E501

        Name of Target  # noqa: E501

        :return: The name of this TestTarget.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this TestTarget.

        Name of Target  # noqa: E501

        :param name: The name of this TestTarget.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def status(self):
        """Gets the status of this TestTarget.  # noqa: E501

        Status of target as base image  # noqa: E501

        :return: The status of this TestTarget.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this TestTarget.

        Status of target as base image  # noqa: E501

        :param status: The status of this TestTarget.  # noqa: E501
        :type: str
        """
        allowed_values = ["approved", "unapproved"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def total_variants_count(self):
        """Gets the total_variants_count of this TestTarget.  # noqa: E501

        Number of total variants for a test target  # noqa: E501

        :return: The total_variants_count of this TestTarget.  # noqa: E501
        :rtype: int
        """
        return self._total_variants_count

    @total_variants_count.setter
    def total_variants_count(self, total_variants_count):
        """Sets the total_variants_count of this TestTarget.

        Number of total variants for a test target  # noqa: E501

        :param total_variants_count: The total_variants_count of this TestTarget.  # noqa: E501
        :type: int
        """
        if total_variants_count is None:
            raise ValueError("Invalid value for `total_variants_count`, must not be `None`")  # noqa: E501

        self._total_variants_count = total_variants_count

    @property
    def type(self):
        """Gets the type of this TestTarget.  # noqa: E501

        Type of target  # noqa: E501

        :return: The type of this TestTarget.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this TestTarget.

        Type of target  # noqa: E501

        :param type: The type of this TestTarget.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["container", "repository", "instance", "configuration"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def url(self):
        """Gets the url of this TestTarget.  # noqa: E501

        Url of target  # noqa: E501

        :return: The url of this TestTarget.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this TestTarget.

        Url of target  # noqa: E501

        :param url: The url of this TestTarget.  # noqa: E501
        :type: str
        """

        self._url = url

    @property
    def variants(self):
        """Gets the variants of this TestTarget.  # noqa: E501


        :return: The variants of this TestTarget.  # noqa: E501
        :rtype: list[TestTargetVariant]
        """
        return self._variants

    @variants.setter
    def variants(self, variants):
        """Sets the variants of this TestTarget.


        :param variants: The variants of this TestTarget.  # noqa: E501
        :type: list[TestTargetVariant]
        """
        if variants is None:
            raise ValueError("Invalid value for `variants`, must not be `None`")  # noqa: E501

        self._variants = variants

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
        if issubclass(TestTarget, dict):
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
        if not isinstance(other, TestTarget):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
