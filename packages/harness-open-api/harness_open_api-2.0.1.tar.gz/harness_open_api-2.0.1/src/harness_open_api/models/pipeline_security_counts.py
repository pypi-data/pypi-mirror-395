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

class PipelineSecurityCounts(object):
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
        'active_issue_count': 'int',
        'existing': 'FrontendIssueCounts',
        'new': 'FrontendIssueCounts',
        'remediated': 'FrontendIssueCounts',
        'total_active': 'int',
        'total_app': 'int',
        'total_base': 'int',
        'total_deduplication_rate': 'float',
        'total_exempted': 'int',
        'total_no_layer': 'int',
        'total_num_occurrence': 'int',
        'total_partially_exempted': 'int',
        'total_pending': 'int',
        'total_rejected': 'int',
        'total_remediated': 'int'
    }

    attribute_map = {
        'active_issue_count': 'activeIssueCount',
        'existing': 'existing',
        'new': 'new',
        'remediated': 'remediated',
        'total_active': 'totalActive',
        'total_app': 'totalApp',
        'total_base': 'totalBase',
        'total_deduplication_rate': 'totalDeduplicationRate',
        'total_exempted': 'totalExempted',
        'total_no_layer': 'totalNoLayer',
        'total_num_occurrence': 'totalNumOccurrence',
        'total_partially_exempted': 'totalPartiallyExempted',
        'total_pending': 'totalPending',
        'total_rejected': 'totalRejected',
        'total_remediated': 'totalRemediated'
    }

    def __init__(self, active_issue_count=None, existing=None, new=None, remediated=None, total_active=None, total_app=None, total_base=None, total_deduplication_rate=None, total_exempted=None, total_no_layer=None, total_num_occurrence=None, total_partially_exempted=None, total_pending=None, total_rejected=None, total_remediated=None):  # noqa: E501
        """PipelineSecurityCounts - a model defined in Swagger"""  # noqa: E501
        self._active_issue_count = None
        self._existing = None
        self._new = None
        self._remediated = None
        self._total_active = None
        self._total_app = None
        self._total_base = None
        self._total_deduplication_rate = None
        self._total_exempted = None
        self._total_no_layer = None
        self._total_num_occurrence = None
        self._total_partially_exempted = None
        self._total_pending = None
        self._total_rejected = None
        self._total_remediated = None
        self.discriminator = None
        if active_issue_count is not None:
            self.active_issue_count = active_issue_count
        self.existing = existing
        self.new = new
        self.remediated = remediated
        self.total_active = total_active
        if total_app is not None:
            self.total_app = total_app
        if total_base is not None:
            self.total_base = total_base
        if total_deduplication_rate is not None:
            self.total_deduplication_rate = total_deduplication_rate
        if total_exempted is not None:
            self.total_exempted = total_exempted
        if total_no_layer is not None:
            self.total_no_layer = total_no_layer
        if total_num_occurrence is not None:
            self.total_num_occurrence = total_num_occurrence
        if total_partially_exempted is not None:
            self.total_partially_exempted = total_partially_exempted
        if total_pending is not None:
            self.total_pending = total_pending
        if total_rejected is not None:
            self.total_rejected = total_rejected
        if total_remediated is not None:
            self.total_remediated = total_remediated

    @property
    def active_issue_count(self):
        """Gets the active_issue_count of this PipelineSecurityCounts.  # noqa: E501


        :return: The active_issue_count of this PipelineSecurityCounts.  # noqa: E501
        :rtype: int
        """
        return self._active_issue_count

    @active_issue_count.setter
    def active_issue_count(self, active_issue_count):
        """Sets the active_issue_count of this PipelineSecurityCounts.


        :param active_issue_count: The active_issue_count of this PipelineSecurityCounts.  # noqa: E501
        :type: int
        """

        self._active_issue_count = active_issue_count

    @property
    def existing(self):
        """Gets the existing of this PipelineSecurityCounts.  # noqa: E501


        :return: The existing of this PipelineSecurityCounts.  # noqa: E501
        :rtype: FrontendIssueCounts
        """
        return self._existing

    @existing.setter
    def existing(self, existing):
        """Sets the existing of this PipelineSecurityCounts.


        :param existing: The existing of this PipelineSecurityCounts.  # noqa: E501
        :type: FrontendIssueCounts
        """
        if existing is None:
            raise ValueError("Invalid value for `existing`, must not be `None`")  # noqa: E501

        self._existing = existing

    @property
    def new(self):
        """Gets the new of this PipelineSecurityCounts.  # noqa: E501


        :return: The new of this PipelineSecurityCounts.  # noqa: E501
        :rtype: FrontendIssueCounts
        """
        return self._new

    @new.setter
    def new(self, new):
        """Sets the new of this PipelineSecurityCounts.


        :param new: The new of this PipelineSecurityCounts.  # noqa: E501
        :type: FrontendIssueCounts
        """
        if new is None:
            raise ValueError("Invalid value for `new`, must not be `None`")  # noqa: E501

        self._new = new

    @property
    def remediated(self):
        """Gets the remediated of this PipelineSecurityCounts.  # noqa: E501


        :return: The remediated of this PipelineSecurityCounts.  # noqa: E501
        :rtype: FrontendIssueCounts
        """
        return self._remediated

    @remediated.setter
    def remediated(self, remediated):
        """Sets the remediated of this PipelineSecurityCounts.


        :param remediated: The remediated of this PipelineSecurityCounts.  # noqa: E501
        :type: FrontendIssueCounts
        """
        if remediated is None:
            raise ValueError("Invalid value for `remediated`, must not be `None`")  # noqa: E501

        self._remediated = remediated

    @property
    def total_active(self):
        """Gets the total_active of this PipelineSecurityCounts.  # noqa: E501


        :return: The total_active of this PipelineSecurityCounts.  # noqa: E501
        :rtype: int
        """
        return self._total_active

    @total_active.setter
    def total_active(self, total_active):
        """Sets the total_active of this PipelineSecurityCounts.


        :param total_active: The total_active of this PipelineSecurityCounts.  # noqa: E501
        :type: int
        """
        if total_active is None:
            raise ValueError("Invalid value for `total_active`, must not be `None`")  # noqa: E501

        self._total_active = total_active

    @property
    def total_app(self):
        """Gets the total_app of this PipelineSecurityCounts.  # noqa: E501


        :return: The total_app of this PipelineSecurityCounts.  # noqa: E501
        :rtype: int
        """
        return self._total_app

    @total_app.setter
    def total_app(self, total_app):
        """Sets the total_app of this PipelineSecurityCounts.


        :param total_app: The total_app of this PipelineSecurityCounts.  # noqa: E501
        :type: int
        """

        self._total_app = total_app

    @property
    def total_base(self):
        """Gets the total_base of this PipelineSecurityCounts.  # noqa: E501


        :return: The total_base of this PipelineSecurityCounts.  # noqa: E501
        :rtype: int
        """
        return self._total_base

    @total_base.setter
    def total_base(self, total_base):
        """Sets the total_base of this PipelineSecurityCounts.


        :param total_base: The total_base of this PipelineSecurityCounts.  # noqa: E501
        :type: int
        """

        self._total_base = total_base

    @property
    def total_deduplication_rate(self):
        """Gets the total_deduplication_rate of this PipelineSecurityCounts.  # noqa: E501


        :return: The total_deduplication_rate of this PipelineSecurityCounts.  # noqa: E501
        :rtype: float
        """
        return self._total_deduplication_rate

    @total_deduplication_rate.setter
    def total_deduplication_rate(self, total_deduplication_rate):
        """Sets the total_deduplication_rate of this PipelineSecurityCounts.


        :param total_deduplication_rate: The total_deduplication_rate of this PipelineSecurityCounts.  # noqa: E501
        :type: float
        """

        self._total_deduplication_rate = total_deduplication_rate

    @property
    def total_exempted(self):
        """Gets the total_exempted of this PipelineSecurityCounts.  # noqa: E501


        :return: The total_exempted of this PipelineSecurityCounts.  # noqa: E501
        :rtype: int
        """
        return self._total_exempted

    @total_exempted.setter
    def total_exempted(self, total_exempted):
        """Sets the total_exempted of this PipelineSecurityCounts.


        :param total_exempted: The total_exempted of this PipelineSecurityCounts.  # noqa: E501
        :type: int
        """

        self._total_exempted = total_exempted

    @property
    def total_no_layer(self):
        """Gets the total_no_layer of this PipelineSecurityCounts.  # noqa: E501


        :return: The total_no_layer of this PipelineSecurityCounts.  # noqa: E501
        :rtype: int
        """
        return self._total_no_layer

    @total_no_layer.setter
    def total_no_layer(self, total_no_layer):
        """Sets the total_no_layer of this PipelineSecurityCounts.


        :param total_no_layer: The total_no_layer of this PipelineSecurityCounts.  # noqa: E501
        :type: int
        """

        self._total_no_layer = total_no_layer

    @property
    def total_num_occurrence(self):
        """Gets the total_num_occurrence of this PipelineSecurityCounts.  # noqa: E501


        :return: The total_num_occurrence of this PipelineSecurityCounts.  # noqa: E501
        :rtype: int
        """
        return self._total_num_occurrence

    @total_num_occurrence.setter
    def total_num_occurrence(self, total_num_occurrence):
        """Sets the total_num_occurrence of this PipelineSecurityCounts.


        :param total_num_occurrence: The total_num_occurrence of this PipelineSecurityCounts.  # noqa: E501
        :type: int
        """

        self._total_num_occurrence = total_num_occurrence

    @property
    def total_partially_exempted(self):
        """Gets the total_partially_exempted of this PipelineSecurityCounts.  # noqa: E501


        :return: The total_partially_exempted of this PipelineSecurityCounts.  # noqa: E501
        :rtype: int
        """
        return self._total_partially_exempted

    @total_partially_exempted.setter
    def total_partially_exempted(self, total_partially_exempted):
        """Sets the total_partially_exempted of this PipelineSecurityCounts.


        :param total_partially_exempted: The total_partially_exempted of this PipelineSecurityCounts.  # noqa: E501
        :type: int
        """

        self._total_partially_exempted = total_partially_exempted

    @property
    def total_pending(self):
        """Gets the total_pending of this PipelineSecurityCounts.  # noqa: E501


        :return: The total_pending of this PipelineSecurityCounts.  # noqa: E501
        :rtype: int
        """
        return self._total_pending

    @total_pending.setter
    def total_pending(self, total_pending):
        """Sets the total_pending of this PipelineSecurityCounts.


        :param total_pending: The total_pending of this PipelineSecurityCounts.  # noqa: E501
        :type: int
        """

        self._total_pending = total_pending

    @property
    def total_rejected(self):
        """Gets the total_rejected of this PipelineSecurityCounts.  # noqa: E501


        :return: The total_rejected of this PipelineSecurityCounts.  # noqa: E501
        :rtype: int
        """
        return self._total_rejected

    @total_rejected.setter
    def total_rejected(self, total_rejected):
        """Sets the total_rejected of this PipelineSecurityCounts.


        :param total_rejected: The total_rejected of this PipelineSecurityCounts.  # noqa: E501
        :type: int
        """

        self._total_rejected = total_rejected

    @property
    def total_remediated(self):
        """Gets the total_remediated of this PipelineSecurityCounts.  # noqa: E501


        :return: The total_remediated of this PipelineSecurityCounts.  # noqa: E501
        :rtype: int
        """
        return self._total_remediated

    @total_remediated.setter
    def total_remediated(self, total_remediated):
        """Sets the total_remediated of this PipelineSecurityCounts.


        :param total_remediated: The total_remediated of this PipelineSecurityCounts.  # noqa: E501
        :type: int
        """

        self._total_remediated = total_remediated

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
        if issubclass(PipelineSecurityCounts, dict):
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
        if not isinstance(other, PipelineSecurityCounts):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
