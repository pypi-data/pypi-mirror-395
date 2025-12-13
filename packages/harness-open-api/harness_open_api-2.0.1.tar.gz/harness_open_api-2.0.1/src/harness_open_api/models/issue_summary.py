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

class IssueSummary(object):
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
        'current_status': 'str',
        'exemption_coverage': 'str',
        'exemption_id': 'str',
        'exemption_status_at_scan': 'str',
        'id': 'str',
        'key': 'str',
        'num_new_occurrences': 'int',
        'num_occurrences': 'int',
        'num_remediated_occurrences': 'int',
        'origin_status': 'str',
        'origins': 'list[str]',
        'override': 'dict(str, object)',
        'scan_id': 'str',
        'severity': 'float',
        'severity_code': 'str',
        'status': 'str',
        'target_variant_name': 'str',
        'title': 'str',
        'type': 'str'
    }

    attribute_map = {
        'current_status': 'currentStatus',
        'exemption_coverage': 'exemptionCoverage',
        'exemption_id': 'exemptionId',
        'exemption_status_at_scan': 'exemptionStatusAtScan',
        'id': 'id',
        'key': 'key',
        'num_new_occurrences': 'numNewOccurrences',
        'num_occurrences': 'numOccurrences',
        'num_remediated_occurrences': 'numRemediatedOccurrences',
        'origin_status': 'originStatus',
        'origins': 'origins',
        'override': 'override',
        'scan_id': 'scanId',
        'severity': 'severity',
        'severity_code': 'severityCode',
        'status': 'status',
        'target_variant_name': 'targetVariantName',
        'title': 'title',
        'type': 'type'
    }

    def __init__(self, current_status=None, exemption_coverage=None, exemption_id=None, exemption_status_at_scan=None, id=None, key=None, num_new_occurrences=None, num_occurrences=None, num_remediated_occurrences=None, origin_status=None, origins=None, override=None, scan_id=None, severity=None, severity_code=None, status=None, target_variant_name=None, title=None, type=None):  # noqa: E501
        """IssueSummary - a model defined in Swagger"""  # noqa: E501
        self._current_status = None
        self._exemption_coverage = None
        self._exemption_id = None
        self._exemption_status_at_scan = None
        self._id = None
        self._key = None
        self._num_new_occurrences = None
        self._num_occurrences = None
        self._num_remediated_occurrences = None
        self._origin_status = None
        self._origins = None
        self._override = None
        self._scan_id = None
        self._severity = None
        self._severity_code = None
        self._status = None
        self._target_variant_name = None
        self._title = None
        self._type = None
        self.discriminator = None
        if current_status is not None:
            self.current_status = current_status
        if exemption_coverage is not None:
            self.exemption_coverage = exemption_coverage
        if exemption_id is not None:
            self.exemption_id = exemption_id
        if exemption_status_at_scan is not None:
            self.exemption_status_at_scan = exemption_status_at_scan
        self.id = id
        self.key = key
        if num_new_occurrences is not None:
            self.num_new_occurrences = num_new_occurrences
        if num_occurrences is not None:
            self.num_occurrences = num_occurrences
        if num_remediated_occurrences is not None:
            self.num_remediated_occurrences = num_remediated_occurrences
        if origin_status is not None:
            self.origin_status = origin_status
        if origins is not None:
            self.origins = origins
        if override is not None:
            self.override = override
        self.scan_id = scan_id
        self.severity = severity
        self.severity_code = severity_code
        if status is not None:
            self.status = status
        if target_variant_name is not None:
            self.target_variant_name = target_variant_name
        self.title = title
        if type is not None:
            self.type = type

    @property
    def current_status(self):
        """Gets the current_status of this IssueSummary.  # noqa: E501

        Current status of the Exemption  # noqa: E501

        :return: The current_status of this IssueSummary.  # noqa: E501
        :rtype: str
        """
        return self._current_status

    @current_status.setter
    def current_status(self, current_status):
        """Sets the current_status of this IssueSummary.

        Current status of the Exemption  # noqa: E501

        :param current_status: The current_status of this IssueSummary.  # noqa: E501
        :type: str
        """
        allowed_values = ["Pending", "Approved", "Rejected", "Expired"]  # noqa: E501
        if current_status not in allowed_values:
            raise ValueError(
                "Invalid value for `current_status` ({0}), must be one of {1}"  # noqa: E501
                .format(current_status, allowed_values)
            )

        self._current_status = current_status

    @property
    def exemption_coverage(self):
        """Gets the exemption_coverage of this IssueSummary.  # noqa: E501

        Indicates if the Security Issue was found to be Exempted, Partially Exempted.  # noqa: E501

        :return: The exemption_coverage of this IssueSummary.  # noqa: E501
        :rtype: str
        """
        return self._exemption_coverage

    @exemption_coverage.setter
    def exemption_coverage(self, exemption_coverage):
        """Sets the exemption_coverage of this IssueSummary.

        Indicates if the Security Issue was found to be Exempted, Partially Exempted.  # noqa: E501

        :param exemption_coverage: The exemption_coverage of this IssueSummary.  # noqa: E501
        :type: str
        """

        self._exemption_coverage = exemption_coverage

    @property
    def exemption_id(self):
        """Gets the exemption_id of this IssueSummary.  # noqa: E501

        ID of Security Test Exemption  # noqa: E501

        :return: The exemption_id of this IssueSummary.  # noqa: E501
        :rtype: str
        """
        return self._exemption_id

    @exemption_id.setter
    def exemption_id(self, exemption_id):
        """Sets the exemption_id of this IssueSummary.

        ID of Security Test Exemption  # noqa: E501

        :param exemption_id: The exemption_id of this IssueSummary.  # noqa: E501
        :type: str
        """

        self._exemption_id = exemption_id

    @property
    def exemption_status_at_scan(self):
        """Gets the exemption_status_at_scan of this IssueSummary.  # noqa: E501

        Exemption's status at the Security Scan created time  # noqa: E501

        :return: The exemption_status_at_scan of this IssueSummary.  # noqa: E501
        :rtype: str
        """
        return self._exemption_status_at_scan

    @exemption_status_at_scan.setter
    def exemption_status_at_scan(self, exemption_status_at_scan):
        """Sets the exemption_status_at_scan of this IssueSummary.

        Exemption's status at the Security Scan created time  # noqa: E501

        :param exemption_status_at_scan: The exemption_status_at_scan of this IssueSummary.  # noqa: E501
        :type: str
        """
        allowed_values = ["Pending", "Approved", "Rejected", "Expired"]  # noqa: E501
        if exemption_status_at_scan not in allowed_values:
            raise ValueError(
                "Invalid value for `exemption_status_at_scan` ({0}), must be one of {1}"  # noqa: E501
                .format(exemption_status_at_scan, allowed_values)
            )

        self._exemption_status_at_scan = exemption_status_at_scan

    @property
    def id(self):
        """Gets the id of this IssueSummary.  # noqa: E501

        Resource identifier  # noqa: E501

        :return: The id of this IssueSummary.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this IssueSummary.

        Resource identifier  # noqa: E501

        :param id: The id of this IssueSummary.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def key(self):
        """Gets the key of this IssueSummary.  # noqa: E501

        Compression/deduplication key  # noqa: E501

        :return: The key of this IssueSummary.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this IssueSummary.

        Compression/deduplication key  # noqa: E501

        :param key: The key of this IssueSummary.  # noqa: E501
        :type: str
        """
        if key is None:
            raise ValueError("Invalid value for `key`, must not be `None`")  # noqa: E501

        self._key = key

    @property
    def num_new_occurrences(self):
        """Gets the num_new_occurrences of this IssueSummary.  # noqa: E501


        :return: The num_new_occurrences of this IssueSummary.  # noqa: E501
        :rtype: int
        """
        return self._num_new_occurrences

    @num_new_occurrences.setter
    def num_new_occurrences(self, num_new_occurrences):
        """Sets the num_new_occurrences of this IssueSummary.


        :param num_new_occurrences: The num_new_occurrences of this IssueSummary.  # noqa: E501
        :type: int
        """

        self._num_new_occurrences = num_new_occurrences

    @property
    def num_occurrences(self):
        """Gets the num_occurrences of this IssueSummary.  # noqa: E501


        :return: The num_occurrences of this IssueSummary.  # noqa: E501
        :rtype: int
        """
        return self._num_occurrences

    @num_occurrences.setter
    def num_occurrences(self, num_occurrences):
        """Sets the num_occurrences of this IssueSummary.


        :param num_occurrences: The num_occurrences of this IssueSummary.  # noqa: E501
        :type: int
        """

        self._num_occurrences = num_occurrences

    @property
    def num_remediated_occurrences(self):
        """Gets the num_remediated_occurrences of this IssueSummary.  # noqa: E501


        :return: The num_remediated_occurrences of this IssueSummary.  # noqa: E501
        :rtype: int
        """
        return self._num_remediated_occurrences

    @num_remediated_occurrences.setter
    def num_remediated_occurrences(self, num_remediated_occurrences):
        """Sets the num_remediated_occurrences of this IssueSummary.


        :param num_remediated_occurrences: The num_remediated_occurrences of this IssueSummary.  # noqa: E501
        :type: int
        """

        self._num_remediated_occurrences = num_remediated_occurrences

    @property
    def origin_status(self):
        """Gets the origin_status of this IssueSummary.  # noqa: E501

        The status of the origin, either 'approved' or 'unapproved'  # noqa: E501

        :return: The origin_status of this IssueSummary.  # noqa: E501
        :rtype: str
        """
        return self._origin_status

    @origin_status.setter
    def origin_status(self, origin_status):
        """Sets the origin_status of this IssueSummary.

        The status of the origin, either 'approved' or 'unapproved'  # noqa: E501

        :param origin_status: The origin_status of this IssueSummary.  # noqa: E501
        :type: str
        """

        self._origin_status = origin_status

    @property
    def origins(self):
        """Gets the origins of this IssueSummary.  # noqa: E501

        The origin of the issue, either 'app' or 'base'  # noqa: E501

        :return: The origins of this IssueSummary.  # noqa: E501
        :rtype: list[str]
        """
        return self._origins

    @origins.setter
    def origins(self, origins):
        """Sets the origins of this IssueSummary.

        The origin of the issue, either 'app' or 'base'  # noqa: E501

        :param origins: The origins of this IssueSummary.  # noqa: E501
        :type: list[str]
        """

        self._origins = origins

    @property
    def override(self):
        """Gets the override of this IssueSummary.  # noqa: E501

        Indicates the issue has been overridden  # noqa: E501

        :return: The override of this IssueSummary.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._override

    @override.setter
    def override(self, override):
        """Sets the override of this IssueSummary.

        Indicates the issue has been overridden  # noqa: E501

        :param override: The override of this IssueSummary.  # noqa: E501
        :type: dict(str, object)
        """

        self._override = override

    @property
    def scan_id(self):
        """Gets the scan_id of this IssueSummary.  # noqa: E501

        The ID of the Scan that detected this Security Issue  # noqa: E501

        :return: The scan_id of this IssueSummary.  # noqa: E501
        :rtype: str
        """
        return self._scan_id

    @scan_id.setter
    def scan_id(self, scan_id):
        """Sets the scan_id of this IssueSummary.

        The ID of the Scan that detected this Security Issue  # noqa: E501

        :param scan_id: The scan_id of this IssueSummary.  # noqa: E501
        :type: str
        """
        if scan_id is None:
            raise ValueError("Invalid value for `scan_id`, must not be `None`")  # noqa: E501

        self._scan_id = scan_id

    @property
    def severity(self):
        """Gets the severity of this IssueSummary.  # noqa: E501

        Numeric severity, from 0 (lowest) to 10 (highest)  # noqa: E501

        :return: The severity of this IssueSummary.  # noqa: E501
        :rtype: float
        """
        return self._severity

    @severity.setter
    def severity(self, severity):
        """Sets the severity of this IssueSummary.

        Numeric severity, from 0 (lowest) to 10 (highest)  # noqa: E501

        :param severity: The severity of this IssueSummary.  # noqa: E501
        :type: float
        """
        if severity is None:
            raise ValueError("Invalid value for `severity`, must not be `None`")  # noqa: E501

        self._severity = severity

    @property
    def severity_code(self):
        """Gets the severity_code of this IssueSummary.  # noqa: E501

        Severity code  # noqa: E501

        :return: The severity_code of this IssueSummary.  # noqa: E501
        :rtype: str
        """
        return self._severity_code

    @severity_code.setter
    def severity_code(self, severity_code):
        """Sets the severity_code of this IssueSummary.

        Severity code  # noqa: E501

        :param severity_code: The severity_code of this IssueSummary.  # noqa: E501
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
    def status(self):
        """Gets the status of this IssueSummary.  # noqa: E501

        Indicates if the Security Issue was found to be remediated, ignored, etc.  # noqa: E501

        :return: The status of this IssueSummary.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this IssueSummary.

        Indicates if the Security Issue was found to be remediated, ignored, etc.  # noqa: E501

        :param status: The status of this IssueSummary.  # noqa: E501
        :type: str
        """
        allowed_values = ["Remediated", "Compensating Controls", "Acceptable Use", "Acceptable Risk", "False Positive", "Fix Unavailable", "Exempted"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def target_variant_name(self):
        """Gets the target_variant_name of this IssueSummary.  # noqa: E501

        Name of the associated Target and Variant  # noqa: E501

        :return: The target_variant_name of this IssueSummary.  # noqa: E501
        :rtype: str
        """
        return self._target_variant_name

    @target_variant_name.setter
    def target_variant_name(self, target_variant_name):
        """Sets the target_variant_name of this IssueSummary.

        Name of the associated Target and Variant  # noqa: E501

        :param target_variant_name: The target_variant_name of this IssueSummary.  # noqa: E501
        :type: str
        """

        self._target_variant_name = target_variant_name

    @property
    def title(self):
        """Gets the title of this IssueSummary.  # noqa: E501

        Title of the Security Issue  # noqa: E501

        :return: The title of this IssueSummary.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this IssueSummary.

        Title of the Security Issue  # noqa: E501

        :param title: The title of this IssueSummary.  # noqa: E501
        :type: str
        """
        if title is None:
            raise ValueError("Invalid value for `title`, must not be `None`")  # noqa: E501

        self._title = title

    @property
    def type(self):
        """Gets the type of this IssueSummary.  # noqa: E501

        The type of vulnerability or quality issue for this Issue  # noqa: E501

        :return: The type of this IssueSummary.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this IssueSummary.

        The type of vulnerability or quality issue for this Issue  # noqa: E501

        :param type: The type of this IssueSummary.  # noqa: E501
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
        if issubclass(IssueSummary, dict):
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
        if not isinstance(other, IssueSummary):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
