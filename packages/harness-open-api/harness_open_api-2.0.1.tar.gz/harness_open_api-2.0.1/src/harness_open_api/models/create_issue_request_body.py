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

class CreateIssueRequestBody(object):
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
        'details': 'dict(str, object)',
        'epss_last_modified': 'str',
        'epss_percentile': 'float',
        'epss_score': 'float',
        'exemption_id': 'str',
        'key': 'str',
        'key_pattern': 'list[str]',
        'num_occurrences': 'int',
        'occurrences': 'list[dict(str, object)]',
        'product_id': 'str',
        'scan_id': 'str',
        'severity': 'float',
        'severity_code': 'str',
        'subproduct': 'str',
        'target_variant_name': 'str',
        'title': 'str',
        'type': 'str'
    }

    attribute_map = {
        'details': 'details',
        'epss_last_modified': 'epssLastModified',
        'epss_percentile': 'epssPercentile',
        'epss_score': 'epssScore',
        'exemption_id': 'exemptionId',
        'key': 'key',
        'key_pattern': 'keyPattern',
        'num_occurrences': 'numOccurrences',
        'occurrences': 'occurrences',
        'product_id': 'productId',
        'scan_id': 'scanId',
        'severity': 'severity',
        'severity_code': 'severityCode',
        'subproduct': 'subproduct',
        'target_variant_name': 'targetVariantName',
        'title': 'title',
        'type': 'type'
    }

    def __init__(self, details=None, epss_last_modified=None, epss_percentile=None, epss_score=None, exemption_id=None, key=None, key_pattern=None, num_occurrences=None, occurrences=None, product_id=None, scan_id=None, severity=None, severity_code=None, subproduct=None, target_variant_name=None, title=None, type=None):  # noqa: E501
        """CreateIssueRequestBody - a model defined in Swagger"""  # noqa: E501
        self._details = None
        self._epss_last_modified = None
        self._epss_percentile = None
        self._epss_score = None
        self._exemption_id = None
        self._key = None
        self._key_pattern = None
        self._num_occurrences = None
        self._occurrences = None
        self._product_id = None
        self._scan_id = None
        self._severity = None
        self._severity_code = None
        self._subproduct = None
        self._target_variant_name = None
        self._title = None
        self._type = None
        self.discriminator = None
        self.details = details
        if epss_last_modified is not None:
            self.epss_last_modified = epss_last_modified
        if epss_percentile is not None:
            self.epss_percentile = epss_percentile
        if epss_score is not None:
            self.epss_score = epss_score
        if exemption_id is not None:
            self.exemption_id = exemption_id
        self.key = key
        self.key_pattern = key_pattern
        if num_occurrences is not None:
            self.num_occurrences = num_occurrences
        if occurrences is not None:
            self.occurrences = occurrences
        self.product_id = product_id
        self.scan_id = scan_id
        self.severity = severity
        self.severity_code = severity_code
        if subproduct is not None:
            self.subproduct = subproduct
        if target_variant_name is not None:
            self.target_variant_name = target_variant_name
        self.title = title
        if type is not None:
            self.type = type

    @property
    def details(self):
        """Gets the details of this CreateIssueRequestBody.  # noqa: E501

        Issue details common to all occurrences  # noqa: E501

        :return: The details of this CreateIssueRequestBody.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._details

    @details.setter
    def details(self, details):
        """Sets the details of this CreateIssueRequestBody.

        Issue details common to all occurrences  # noqa: E501

        :param details: The details of this CreateIssueRequestBody.  # noqa: E501
        :type: dict(str, object)
        """
        if details is None:
            raise ValueError("Invalid value for `details`, must not be `None`")  # noqa: E501

        self._details = details

    @property
    def epss_last_modified(self):
        """Gets the epss_last_modified of this CreateIssueRequestBody.  # noqa: E501

        Last date the issue EPSS data was last modified  # noqa: E501

        :return: The epss_last_modified of this CreateIssueRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._epss_last_modified

    @epss_last_modified.setter
    def epss_last_modified(self, epss_last_modified):
        """Sets the epss_last_modified of this CreateIssueRequestBody.

        Last date the issue EPSS data was last modified  # noqa: E501

        :param epss_last_modified: The epss_last_modified of this CreateIssueRequestBody.  # noqa: E501
        :type: str
        """

        self._epss_last_modified = epss_last_modified

    @property
    def epss_percentile(self):
        """Gets the epss_percentile of this CreateIssueRequestBody.  # noqa: E501

        EPSS percentile of the issue CVE identifier  # noqa: E501

        :return: The epss_percentile of this CreateIssueRequestBody.  # noqa: E501
        :rtype: float
        """
        return self._epss_percentile

    @epss_percentile.setter
    def epss_percentile(self, epss_percentile):
        """Sets the epss_percentile of this CreateIssueRequestBody.

        EPSS percentile of the issue CVE identifier  # noqa: E501

        :param epss_percentile: The epss_percentile of this CreateIssueRequestBody.  # noqa: E501
        :type: float
        """

        self._epss_percentile = epss_percentile

    @property
    def epss_score(self):
        """Gets the epss_score of this CreateIssueRequestBody.  # noqa: E501

        EPSS score of the issue CVE identifier  # noqa: E501

        :return: The epss_score of this CreateIssueRequestBody.  # noqa: E501
        :rtype: float
        """
        return self._epss_score

    @epss_score.setter
    def epss_score(self, epss_score):
        """Sets the epss_score of this CreateIssueRequestBody.

        EPSS score of the issue CVE identifier  # noqa: E501

        :param epss_score: The epss_score of this CreateIssueRequestBody.  # noqa: E501
        :type: float
        """

        self._epss_score = epss_score

    @property
    def exemption_id(self):
        """Gets the exemption_id of this CreateIssueRequestBody.  # noqa: E501

        ID of Security Test Exemption  # noqa: E501

        :return: The exemption_id of this CreateIssueRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._exemption_id

    @exemption_id.setter
    def exemption_id(self, exemption_id):
        """Sets the exemption_id of this CreateIssueRequestBody.

        ID of Security Test Exemption  # noqa: E501

        :param exemption_id: The exemption_id of this CreateIssueRequestBody.  # noqa: E501
        :type: str
        """

        self._exemption_id = exemption_id

    @property
    def key(self):
        """Gets the key of this CreateIssueRequestBody.  # noqa: E501

        Compression/deduplication key  # noqa: E501

        :return: The key of this CreateIssueRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this CreateIssueRequestBody.

        Compression/deduplication key  # noqa: E501

        :param key: The key of this CreateIssueRequestBody.  # noqa: E501
        :type: str
        """
        if key is None:
            raise ValueError("Invalid value for `key`, must not be `None`")  # noqa: E501

        self._key = key

    @property
    def key_pattern(self):
        """Gets the key_pattern of this CreateIssueRequestBody.  # noqa: E501

        The pattern of fields used to generate this Security Issue's Key  # noqa: E501

        :return: The key_pattern of this CreateIssueRequestBody.  # noqa: E501
        :rtype: list[str]
        """
        return self._key_pattern

    @key_pattern.setter
    def key_pattern(self, key_pattern):
        """Sets the key_pattern of this CreateIssueRequestBody.

        The pattern of fields used to generate this Security Issue's Key  # noqa: E501

        :param key_pattern: The key_pattern of this CreateIssueRequestBody.  # noqa: E501
        :type: list[str]
        """
        if key_pattern is None:
            raise ValueError("Invalid value for `key_pattern`, must not be `None`")  # noqa: E501

        self._key_pattern = key_pattern

    @property
    def num_occurrences(self):
        """Gets the num_occurrences of this CreateIssueRequestBody.  # noqa: E501

        Indicates the number of Occurrences on the Issue  # noqa: E501

        :return: The num_occurrences of this CreateIssueRequestBody.  # noqa: E501
        :rtype: int
        """
        return self._num_occurrences

    @num_occurrences.setter
    def num_occurrences(self, num_occurrences):
        """Sets the num_occurrences of this CreateIssueRequestBody.

        Indicates the number of Occurrences on the Issue  # noqa: E501

        :param num_occurrences: The num_occurrences of this CreateIssueRequestBody.  # noqa: E501
        :type: int
        """

        self._num_occurrences = num_occurrences

    @property
    def occurrences(self):
        """Gets the occurrences of this CreateIssueRequestBody.  # noqa: E501

        Array of details unique to each occurrence  # noqa: E501

        :return: The occurrences of this CreateIssueRequestBody.  # noqa: E501
        :rtype: list[dict(str, object)]
        """
        return self._occurrences

    @occurrences.setter
    def occurrences(self, occurrences):
        """Sets the occurrences of this CreateIssueRequestBody.

        Array of details unique to each occurrence  # noqa: E501

        :param occurrences: The occurrences of this CreateIssueRequestBody.  # noqa: E501
        :type: list[dict(str, object)]
        """

        self._occurrences = occurrences

    @property
    def product_id(self):
        """Gets the product_id of this CreateIssueRequestBody.  # noqa: E501

        The scan tool that identified this Security Issue  # noqa: E501

        :return: The product_id of this CreateIssueRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._product_id

    @product_id.setter
    def product_id(self, product_id):
        """Sets the product_id of this CreateIssueRequestBody.

        The scan tool that identified this Security Issue  # noqa: E501

        :param product_id: The product_id of this CreateIssueRequestBody.  # noqa: E501
        :type: str
        """
        if product_id is None:
            raise ValueError("Invalid value for `product_id`, must not be `None`")  # noqa: E501

        self._product_id = product_id

    @property
    def scan_id(self):
        """Gets the scan_id of this CreateIssueRequestBody.  # noqa: E501

        The Security Scan execution that detected this Security Issue  # noqa: E501

        :return: The scan_id of this CreateIssueRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._scan_id

    @scan_id.setter
    def scan_id(self, scan_id):
        """Sets the scan_id of this CreateIssueRequestBody.

        The Security Scan execution that detected this Security Issue  # noqa: E501

        :param scan_id: The scan_id of this CreateIssueRequestBody.  # noqa: E501
        :type: str
        """
        if scan_id is None:
            raise ValueError("Invalid value for `scan_id`, must not be `None`")  # noqa: E501

        self._scan_id = scan_id

    @property
    def severity(self):
        """Gets the severity of this CreateIssueRequestBody.  # noqa: E501

        Numeric severity, from 0 (lowest) to 10 (highest)  # noqa: E501

        :return: The severity of this CreateIssueRequestBody.  # noqa: E501
        :rtype: float
        """
        return self._severity

    @severity.setter
    def severity(self, severity):
        """Sets the severity of this CreateIssueRequestBody.

        Numeric severity, from 0 (lowest) to 10 (highest)  # noqa: E501

        :param severity: The severity of this CreateIssueRequestBody.  # noqa: E501
        :type: float
        """
        if severity is None:
            raise ValueError("Invalid value for `severity`, must not be `None`")  # noqa: E501

        self._severity = severity

    @property
    def severity_code(self):
        """Gets the severity_code of this CreateIssueRequestBody.  # noqa: E501

        Severity code  # noqa: E501

        :return: The severity_code of this CreateIssueRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._severity_code

    @severity_code.setter
    def severity_code(self, severity_code):
        """Sets the severity_code of this CreateIssueRequestBody.

        Severity code  # noqa: E501

        :param severity_code: The severity_code of this CreateIssueRequestBody.  # noqa: E501
        :type: str
        """
        if severity_code is None:
            raise ValueError("Invalid value for `severity_code`, must not be `None`")  # noqa: E501
        allowed_values = ["Critical", "High", "Medium", "Low", "Info", "Unassigned"]  # noqa: E501
        if severity_code not in allowed_values:
            raise ValueError(
                "Invalid value for `severity_code` ({0}), must be one of {1}"  # noqa: E501
                .format(severity_code, allowed_values)
            )

        self._severity_code = severity_code

    @property
    def subproduct(self):
        """Gets the subproduct of this CreateIssueRequestBody.  # noqa: E501

        The subproduct that identified this Security Issue  # noqa: E501

        :return: The subproduct of this CreateIssueRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._subproduct

    @subproduct.setter
    def subproduct(self, subproduct):
        """Sets the subproduct of this CreateIssueRequestBody.

        The subproduct that identified this Security Issue  # noqa: E501

        :param subproduct: The subproduct of this CreateIssueRequestBody.  # noqa: E501
        :type: str
        """

        self._subproduct = subproduct

    @property
    def target_variant_name(self):
        """Gets the target_variant_name of this CreateIssueRequestBody.  # noqa: E501

        Name of the associated Target and Variant  # noqa: E501

        :return: The target_variant_name of this CreateIssueRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._target_variant_name

    @target_variant_name.setter
    def target_variant_name(self, target_variant_name):
        """Sets the target_variant_name of this CreateIssueRequestBody.

        Name of the associated Target and Variant  # noqa: E501

        :param target_variant_name: The target_variant_name of this CreateIssueRequestBody.  # noqa: E501
        :type: str
        """

        self._target_variant_name = target_variant_name

    @property
    def title(self):
        """Gets the title of this CreateIssueRequestBody.  # noqa: E501

        Title of the Security Issue  # noqa: E501

        :return: The title of this CreateIssueRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this CreateIssueRequestBody.

        Title of the Security Issue  # noqa: E501

        :param title: The title of this CreateIssueRequestBody.  # noqa: E501
        :type: str
        """
        if title is None:
            raise ValueError("Invalid value for `title`, must not be `None`")  # noqa: E501

        self._title = title

    @property
    def type(self):
        """Gets the type of this CreateIssueRequestBody.  # noqa: E501

        The type of vulnerability or quality issue for this Issue  # noqa: E501

        :return: The type of this CreateIssueRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this CreateIssueRequestBody.

        The type of vulnerability or quality issue for this Issue  # noqa: E501

        :param type: The type of this CreateIssueRequestBody.  # noqa: E501
        :type: str
        """
        allowed_values = ["SAST", "DAST", "SCA", "IAC", "SECRET", "MISCONFIG", "BUG_SMELLS", "CODE_SMELLS", "CODE_COVERAGE", "EXTERNAL_POLICY"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

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
        if issubclass(CreateIssueRequestBody, dict):
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
        if not isinstance(other, CreateIssueRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
