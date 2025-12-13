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

class AllIssueSummary(object):
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
        'exemption_expiration': 'int',
        'exemption_id': 'str',
        'exemption_status': 'str',
        'id': 'str',
        'issue_type': 'str',
        'last_detected': 'int',
        'num_occurrences': 'float',
        'num_targets_impacted': 'float',
        'override': 'dict(str, object)',
        'severity_code': 'str',
        'status': 'str',
        'title': 'str'
    }

    attribute_map = {
        'exemption_expiration': 'exemptionExpiration',
        'exemption_id': 'exemptionId',
        'exemption_status': 'exemptionStatus',
        'id': 'id',
        'issue_type': 'issueType',
        'last_detected': 'lastDetected',
        'num_occurrences': 'numOccurrences',
        'num_targets_impacted': 'numTargetsImpacted',
        'override': 'override',
        'severity_code': 'severityCode',
        'status': 'status',
        'title': 'title'
    }

    def __init__(self, exemption_expiration=None, exemption_id=None, exemption_status=None, id=None, issue_type=None, last_detected=None, num_occurrences=None, num_targets_impacted=None, override=None, severity_code=None, status=None, title=None):  # noqa: E501
        """AllIssueSummary - a model defined in Swagger"""  # noqa: E501
        self._exemption_expiration = None
        self._exemption_id = None
        self._exemption_status = None
        self._id = None
        self._issue_type = None
        self._last_detected = None
        self._num_occurrences = None
        self._num_targets_impacted = None
        self._override = None
        self._severity_code = None
        self._status = None
        self._title = None
        self.discriminator = None
        if exemption_expiration is not None:
            self.exemption_expiration = exemption_expiration
        if exemption_id is not None:
            self.exemption_id = exemption_id
        if exemption_status is not None:
            self.exemption_status = exemption_status
        self.id = id
        if issue_type is not None:
            self.issue_type = issue_type
        self.last_detected = last_detected
        self.num_occurrences = num_occurrences
        self.num_targets_impacted = num_targets_impacted
        if override is not None:
            self.override = override
        self.severity_code = severity_code
        if status is not None:
            self.status = status
        self.title = title

    @property
    def exemption_expiration(self):
        """Gets the exemption_expiration of this AllIssueSummary.  # noqa: E501

        Unix timestamp at which this Exemption will expire  # noqa: E501

        :return: The exemption_expiration of this AllIssueSummary.  # noqa: E501
        :rtype: int
        """
        return self._exemption_expiration

    @exemption_expiration.setter
    def exemption_expiration(self, exemption_expiration):
        """Sets the exemption_expiration of this AllIssueSummary.

        Unix timestamp at which this Exemption will expire  # noqa: E501

        :param exemption_expiration: The exemption_expiration of this AllIssueSummary.  # noqa: E501
        :type: int
        """

        self._exemption_expiration = exemption_expiration

    @property
    def exemption_id(self):
        """Gets the exemption_id of this AllIssueSummary.  # noqa: E501

        ID of Security Test Exemption  # noqa: E501

        :return: The exemption_id of this AllIssueSummary.  # noqa: E501
        :rtype: str
        """
        return self._exemption_id

    @exemption_id.setter
    def exemption_id(self, exemption_id):
        """Sets the exemption_id of this AllIssueSummary.

        ID of Security Test Exemption  # noqa: E501

        :param exemption_id: The exemption_id of this AllIssueSummary.  # noqa: E501
        :type: str
        """

        self._exemption_id = exemption_id

    @property
    def exemption_status(self):
        """Gets the exemption_status of this AllIssueSummary.  # noqa: E501

        Status of project scoped exemption for this issue  # noqa: E501

        :return: The exemption_status of this AllIssueSummary.  # noqa: E501
        :rtype: str
        """
        return self._exemption_status

    @exemption_status.setter
    def exemption_status(self, exemption_status):
        """Sets the exemption_status of this AllIssueSummary.

        Status of project scoped exemption for this issue  # noqa: E501

        :param exemption_status: The exemption_status of this AllIssueSummary.  # noqa: E501
        :type: str
        """

        self._exemption_status = exemption_status

    @property
    def id(self):
        """Gets the id of this AllIssueSummary.  # noqa: E501

        Resource identifier  # noqa: E501

        :return: The id of this AllIssueSummary.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this AllIssueSummary.

        Resource identifier  # noqa: E501

        :param id: The id of this AllIssueSummary.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def issue_type(self):
        """Gets the issue_type of this AllIssueSummary.  # noqa: E501

        Issue Type  # noqa: E501

        :return: The issue_type of this AllIssueSummary.  # noqa: E501
        :rtype: str
        """
        return self._issue_type

    @issue_type.setter
    def issue_type(self, issue_type):
        """Sets the issue_type of this AllIssueSummary.

        Issue Type  # noqa: E501

        :param issue_type: The issue_type of this AllIssueSummary.  # noqa: E501
        :type: str
        """

        self._issue_type = issue_type

    @property
    def last_detected(self):
        """Gets the last_detected of this AllIssueSummary.  # noqa: E501

        Timestamp of the last detection of this issue  # noqa: E501

        :return: The last_detected of this AllIssueSummary.  # noqa: E501
        :rtype: int
        """
        return self._last_detected

    @last_detected.setter
    def last_detected(self, last_detected):
        """Sets the last_detected of this AllIssueSummary.

        Timestamp of the last detection of this issue  # noqa: E501

        :param last_detected: The last_detected of this AllIssueSummary.  # noqa: E501
        :type: int
        """
        if last_detected is None:
            raise ValueError("Invalid value for `last_detected`, must not be `None`")  # noqa: E501

        self._last_detected = last_detected

    @property
    def num_occurrences(self):
        """Gets the num_occurrences of this AllIssueSummary.  # noqa: E501

        Number of occurrences of this issue against the latest baseline scan  # noqa: E501

        :return: The num_occurrences of this AllIssueSummary.  # noqa: E501
        :rtype: float
        """
        return self._num_occurrences

    @num_occurrences.setter
    def num_occurrences(self, num_occurrences):
        """Sets the num_occurrences of this AllIssueSummary.

        Number of occurrences of this issue against the latest baseline scan  # noqa: E501

        :param num_occurrences: The num_occurrences of this AllIssueSummary.  # noqa: E501
        :type: float
        """
        if num_occurrences is None:
            raise ValueError("Invalid value for `num_occurrences`, must not be `None`")  # noqa: E501

        self._num_occurrences = num_occurrences

    @property
    def num_targets_impacted(self):
        """Gets the num_targets_impacted of this AllIssueSummary.  # noqa: E501

        Number of targets impacted where this issue was found against the latest baseline scan  # noqa: E501

        :return: The num_targets_impacted of this AllIssueSummary.  # noqa: E501
        :rtype: float
        """
        return self._num_targets_impacted

    @num_targets_impacted.setter
    def num_targets_impacted(self, num_targets_impacted):
        """Sets the num_targets_impacted of this AllIssueSummary.

        Number of targets impacted where this issue was found against the latest baseline scan  # noqa: E501

        :param num_targets_impacted: The num_targets_impacted of this AllIssueSummary.  # noqa: E501
        :type: float
        """
        if num_targets_impacted is None:
            raise ValueError("Invalid value for `num_targets_impacted`, must not be `None`")  # noqa: E501

        self._num_targets_impacted = num_targets_impacted

    @property
    def override(self):
        """Gets the override of this AllIssueSummary.  # noqa: E501

        Indicates the issue has been overridden  # noqa: E501

        :return: The override of this AllIssueSummary.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._override

    @override.setter
    def override(self, override):
        """Sets the override of this AllIssueSummary.

        Indicates the issue has been overridden  # noqa: E501

        :param override: The override of this AllIssueSummary.  # noqa: E501
        :type: dict(str, object)
        """

        self._override = override

    @property
    def severity_code(self):
        """Gets the severity_code of this AllIssueSummary.  # noqa: E501

        Severity code  # noqa: E501

        :return: The severity_code of this AllIssueSummary.  # noqa: E501
        :rtype: str
        """
        return self._severity_code

    @severity_code.setter
    def severity_code(self, severity_code):
        """Sets the severity_code of this AllIssueSummary.

        Severity code  # noqa: E501

        :param severity_code: The severity_code of this AllIssueSummary.  # noqa: E501
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
        """Gets the status of this AllIssueSummary.  # noqa: E501

        Issue Status  # noqa: E501

        :return: The status of this AllIssueSummary.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this AllIssueSummary.

        Issue Status  # noqa: E501

        :param status: The status of this AllIssueSummary.  # noqa: E501
        :type: str
        """
        allowed_values = ["Active", "Exempted"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def title(self):
        """Gets the title of this AllIssueSummary.  # noqa: E501

        Title of the Security Issue  # noqa: E501

        :return: The title of this AllIssueSummary.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this AllIssueSummary.

        Title of the Security Issue  # noqa: E501

        :param title: The title of this AllIssueSummary.  # noqa: E501
        :type: str
        """
        if title is None:
            raise ValueError("Invalid value for `title`, must not be `None`")  # noqa: E501

        self._title = title

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
        if issubclass(AllIssueSummary, dict):
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
        if not isinstance(other, AllIssueSummary):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
