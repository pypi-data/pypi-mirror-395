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

class InlineResponse2008Response(object):
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
        'account_breakdown': 'dict(str, InlineResponse2008AccountBreakdown)',
        'breakdown_type': 'str',
        'committed_cost': 'float',
        'costs': 'dict(str, float)',
        'coverage': 'float',
        'end_date': 'date',
        'instance_type_breakdown': 'dict(str, InlineResponse2008InstanceTypeBreakdown)',
        'region_breakdown': 'dict(str, InlineResponse2008RegionBreakdown)',
        'start_date': 'date',
        'total_cost': 'float'
    }

    attribute_map = {
        'account_breakdown': 'account_breakdown',
        'breakdown_type': 'breakdown_type',
        'committed_cost': 'committed_cost',
        'costs': 'costs',
        'coverage': 'coverage',
        'end_date': 'end_date',
        'instance_type_breakdown': 'instance_type_breakdown',
        'region_breakdown': 'region_breakdown',
        'start_date': 'start_date',
        'total_cost': 'total_cost'
    }

    def __init__(self, account_breakdown=None, breakdown_type=None, committed_cost=None, costs=None, coverage=None, end_date=None, instance_type_breakdown=None, region_breakdown=None, start_date=None, total_cost=None):  # noqa: E501
        """InlineResponse2008Response - a model defined in Swagger"""  # noqa: E501
        self._account_breakdown = None
        self._breakdown_type = None
        self._committed_cost = None
        self._costs = None
        self._coverage = None
        self._end_date = None
        self._instance_type_breakdown = None
        self._region_breakdown = None
        self._start_date = None
        self._total_cost = None
        self.discriminator = None
        if account_breakdown is not None:
            self.account_breakdown = account_breakdown
        if breakdown_type is not None:
            self.breakdown_type = breakdown_type
        if committed_cost is not None:
            self.committed_cost = committed_cost
        if costs is not None:
            self.costs = costs
        if coverage is not None:
            self.coverage = coverage
        if end_date is not None:
            self.end_date = end_date
        if instance_type_breakdown is not None:
            self.instance_type_breakdown = instance_type_breakdown
        if region_breakdown is not None:
            self.region_breakdown = region_breakdown
        if start_date is not None:
            self.start_date = start_date
        if total_cost is not None:
            self.total_cost = total_cost

    @property
    def account_breakdown(self):
        """Gets the account_breakdown of this InlineResponse2008Response.  # noqa: E501

        Breakdown of costs by account  # noqa: E501

        :return: The account_breakdown of this InlineResponse2008Response.  # noqa: E501
        :rtype: dict(str, InlineResponse2008AccountBreakdown)
        """
        return self._account_breakdown

    @account_breakdown.setter
    def account_breakdown(self, account_breakdown):
        """Sets the account_breakdown of this InlineResponse2008Response.

        Breakdown of costs by account  # noqa: E501

        :param account_breakdown: The account_breakdown of this InlineResponse2008Response.  # noqa: E501
        :type: dict(str, InlineResponse2008AccountBreakdown)
        """

        self._account_breakdown = account_breakdown

    @property
    def breakdown_type(self):
        """Gets the breakdown_type of this InlineResponse2008Response.  # noqa: E501

        Type of breakdown used (instance_type_breakdown, region_breakdown, or account_breakdown)  # noqa: E501

        :return: The breakdown_type of this InlineResponse2008Response.  # noqa: E501
        :rtype: str
        """
        return self._breakdown_type

    @breakdown_type.setter
    def breakdown_type(self, breakdown_type):
        """Sets the breakdown_type of this InlineResponse2008Response.

        Type of breakdown used (instance_type_breakdown, region_breakdown, or account_breakdown)  # noqa: E501

        :param breakdown_type: The breakdown_type of this InlineResponse2008Response.  # noqa: E501
        :type: str
        """

        self._breakdown_type = breakdown_type

    @property
    def committed_cost(self):
        """Gets the committed_cost of this InlineResponse2008Response.  # noqa: E501

        Committed cost for the period  # noqa: E501

        :return: The committed_cost of this InlineResponse2008Response.  # noqa: E501
        :rtype: float
        """
        return self._committed_cost

    @committed_cost.setter
    def committed_cost(self, committed_cost):
        """Sets the committed_cost of this InlineResponse2008Response.

        Committed cost for the period  # noqa: E501

        :param committed_cost: The committed_cost of this InlineResponse2008Response.  # noqa: E501
        :type: float
        """

        self._committed_cost = committed_cost

    @property
    def costs(self):
        """Gets the costs of this InlineResponse2008Response.  # noqa: E501

        Map of purchase types to costs. For instance type breakdown, this contains region as keys.  # noqa: E501

        :return: The costs of this InlineResponse2008Response.  # noqa: E501
        :rtype: dict(str, float)
        """
        return self._costs

    @costs.setter
    def costs(self, costs):
        """Sets the costs of this InlineResponse2008Response.

        Map of purchase types to costs. For instance type breakdown, this contains region as keys.  # noqa: E501

        :param costs: The costs of this InlineResponse2008Response.  # noqa: E501
        :type: dict(str, float)
        """

        self._costs = costs

    @property
    def coverage(self):
        """Gets the coverage of this InlineResponse2008Response.  # noqa: E501

        Coverage percentage (committed_cost/total_cost * 100)  # noqa: E501

        :return: The coverage of this InlineResponse2008Response.  # noqa: E501
        :rtype: float
        """
        return self._coverage

    @coverage.setter
    def coverage(self, coverage):
        """Sets the coverage of this InlineResponse2008Response.

        Coverage percentage (committed_cost/total_cost * 100)  # noqa: E501

        :param coverage: The coverage of this InlineResponse2008Response.  # noqa: E501
        :type: float
        """

        self._coverage = coverage

    @property
    def end_date(self):
        """Gets the end_date of this InlineResponse2008Response.  # noqa: E501

        End date of the cost data period  # noqa: E501

        :return: The end_date of this InlineResponse2008Response.  # noqa: E501
        :rtype: date
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """Sets the end_date of this InlineResponse2008Response.

        End date of the cost data period  # noqa: E501

        :param end_date: The end_date of this InlineResponse2008Response.  # noqa: E501
        :type: date
        """

        self._end_date = end_date

    @property
    def instance_type_breakdown(self):
        """Gets the instance_type_breakdown of this InlineResponse2008Response.  # noqa: E501

        Breakdown of costs by instance type  # noqa: E501

        :return: The instance_type_breakdown of this InlineResponse2008Response.  # noqa: E501
        :rtype: dict(str, InlineResponse2008InstanceTypeBreakdown)
        """
        return self._instance_type_breakdown

    @instance_type_breakdown.setter
    def instance_type_breakdown(self, instance_type_breakdown):
        """Sets the instance_type_breakdown of this InlineResponse2008Response.

        Breakdown of costs by instance type  # noqa: E501

        :param instance_type_breakdown: The instance_type_breakdown of this InlineResponse2008Response.  # noqa: E501
        :type: dict(str, InlineResponse2008InstanceTypeBreakdown)
        """

        self._instance_type_breakdown = instance_type_breakdown

    @property
    def region_breakdown(self):
        """Gets the region_breakdown of this InlineResponse2008Response.  # noqa: E501

        Breakdown of costs by region  # noqa: E501

        :return: The region_breakdown of this InlineResponse2008Response.  # noqa: E501
        :rtype: dict(str, InlineResponse2008RegionBreakdown)
        """
        return self._region_breakdown

    @region_breakdown.setter
    def region_breakdown(self, region_breakdown):
        """Sets the region_breakdown of this InlineResponse2008Response.

        Breakdown of costs by region  # noqa: E501

        :param region_breakdown: The region_breakdown of this InlineResponse2008Response.  # noqa: E501
        :type: dict(str, InlineResponse2008RegionBreakdown)
        """

        self._region_breakdown = region_breakdown

    @property
    def start_date(self):
        """Gets the start_date of this InlineResponse2008Response.  # noqa: E501

        Start date of the cost data period  # noqa: E501

        :return: The start_date of this InlineResponse2008Response.  # noqa: E501
        :rtype: date
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """Sets the start_date of this InlineResponse2008Response.

        Start date of the cost data period  # noqa: E501

        :param start_date: The start_date of this InlineResponse2008Response.  # noqa: E501
        :type: date
        """

        self._start_date = start_date

    @property
    def total_cost(self):
        """Gets the total_cost of this InlineResponse2008Response.  # noqa: E501

        Total cost for the period  # noqa: E501

        :return: The total_cost of this InlineResponse2008Response.  # noqa: E501
        :rtype: float
        """
        return self._total_cost

    @total_cost.setter
    def total_cost(self, total_cost):
        """Sets the total_cost of this InlineResponse2008Response.

        Total cost for the period  # noqa: E501

        :param total_cost: The total_cost of this InlineResponse2008Response.  # noqa: E501
        :type: float
        """

        self._total_cost = total_cost

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
        if issubclass(InlineResponse2008Response, dict):
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
        if not isinstance(other, InlineResponse2008Response):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
