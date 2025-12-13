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

class ComputeCoveragesDetailTable(object):
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
        'coverage': 'float',
        'machine_type': 'str',
        'on_demand_cost': 'float',
        'on_demand_hours': 'float',
        'region': 'str',
        'reservation_cost': 'float',
        'ri_coverage_hours': 'float',
        'savings_plan_hours': 'float',
        'spot_cost': 'float',
        'spot_hours': 'float',
        'total_cost': 'float',
        'total_covered_hours': 'float',
        'total_hours': 'float',
        'trend': 'float'
    }

    attribute_map = {
        'coverage': 'coverage',
        'machine_type': 'machine_type',
        'on_demand_cost': 'on_demand_cost',
        'on_demand_hours': 'on_demand_hours',
        'region': 'region',
        'reservation_cost': 'reservation_cost',
        'ri_coverage_hours': 'ri_coverage_hours',
        'savings_plan_hours': 'savings_plan_hours',
        'spot_cost': 'spot_cost',
        'spot_hours': 'spot_hours',
        'total_cost': 'total_cost',
        'total_covered_hours': 'total_covered_hours',
        'total_hours': 'total_hours',
        'trend': 'trend'
    }

    def __init__(self, coverage=None, machine_type=None, on_demand_cost=None, on_demand_hours=None, region=None, reservation_cost=None, ri_coverage_hours=None, savings_plan_hours=None, spot_cost=None, spot_hours=None, total_cost=None, total_covered_hours=None, total_hours=None, trend=None):  # noqa: E501
        """ComputeCoveragesDetailTable - a model defined in Swagger"""  # noqa: E501
        self._coverage = None
        self._machine_type = None
        self._on_demand_cost = None
        self._on_demand_hours = None
        self._region = None
        self._reservation_cost = None
        self._ri_coverage_hours = None
        self._savings_plan_hours = None
        self._spot_cost = None
        self._spot_hours = None
        self._total_cost = None
        self._total_covered_hours = None
        self._total_hours = None
        self._trend = None
        self.discriminator = None
        if coverage is not None:
            self.coverage = coverage
        if machine_type is not None:
            self.machine_type = machine_type
        if on_demand_cost is not None:
            self.on_demand_cost = on_demand_cost
        if on_demand_hours is not None:
            self.on_demand_hours = on_demand_hours
        if region is not None:
            self.region = region
        if reservation_cost is not None:
            self.reservation_cost = reservation_cost
        if ri_coverage_hours is not None:
            self.ri_coverage_hours = ri_coverage_hours
        if savings_plan_hours is not None:
            self.savings_plan_hours = savings_plan_hours
        if spot_cost is not None:
            self.spot_cost = spot_cost
        if spot_hours is not None:
            self.spot_hours = spot_hours
        if total_cost is not None:
            self.total_cost = total_cost
        if total_covered_hours is not None:
            self.total_covered_hours = total_covered_hours
        if total_hours is not None:
            self.total_hours = total_hours
        if trend is not None:
            self.trend = trend

    @property
    def coverage(self):
        """Gets the coverage of this ComputeCoveragesDetailTable.  # noqa: E501

        Coverage percentage  # noqa: E501

        :return: The coverage of this ComputeCoveragesDetailTable.  # noqa: E501
        :rtype: float
        """
        return self._coverage

    @coverage.setter
    def coverage(self, coverage):
        """Sets the coverage of this ComputeCoveragesDetailTable.

        Coverage percentage  # noqa: E501

        :param coverage: The coverage of this ComputeCoveragesDetailTable.  # noqa: E501
        :type: float
        """

        self._coverage = coverage

    @property
    def machine_type(self):
        """Gets the machine_type of this ComputeCoveragesDetailTable.  # noqa: E501

        Machine type information when grouped by machine type  # noqa: E501

        :return: The machine_type of this ComputeCoveragesDetailTable.  # noqa: E501
        :rtype: str
        """
        return self._machine_type

    @machine_type.setter
    def machine_type(self, machine_type):
        """Sets the machine_type of this ComputeCoveragesDetailTable.

        Machine type information when grouped by machine type  # noqa: E501

        :param machine_type: The machine_type of this ComputeCoveragesDetailTable.  # noqa: E501
        :type: str
        """

        self._machine_type = machine_type

    @property
    def on_demand_cost(self):
        """Gets the on_demand_cost of this ComputeCoveragesDetailTable.  # noqa: E501

        Cost for on-demand instances  # noqa: E501

        :return: The on_demand_cost of this ComputeCoveragesDetailTable.  # noqa: E501
        :rtype: float
        """
        return self._on_demand_cost

    @on_demand_cost.setter
    def on_demand_cost(self, on_demand_cost):
        """Sets the on_demand_cost of this ComputeCoveragesDetailTable.

        Cost for on-demand instances  # noqa: E501

        :param on_demand_cost: The on_demand_cost of this ComputeCoveragesDetailTable.  # noqa: E501
        :type: float
        """

        self._on_demand_cost = on_demand_cost

    @property
    def on_demand_hours(self):
        """Gets the on_demand_hours of this ComputeCoveragesDetailTable.  # noqa: E501

        Hours billed at on-demand rates  # noqa: E501

        :return: The on_demand_hours of this ComputeCoveragesDetailTable.  # noqa: E501
        :rtype: float
        """
        return self._on_demand_hours

    @on_demand_hours.setter
    def on_demand_hours(self, on_demand_hours):
        """Sets the on_demand_hours of this ComputeCoveragesDetailTable.

        Hours billed at on-demand rates  # noqa: E501

        :param on_demand_hours: The on_demand_hours of this ComputeCoveragesDetailTable.  # noqa: E501
        :type: float
        """

        self._on_demand_hours = on_demand_hours

    @property
    def region(self):
        """Gets the region of this ComputeCoveragesDetailTable.  # noqa: E501

        Region information when grouped by region  # noqa: E501

        :return: The region of this ComputeCoveragesDetailTable.  # noqa: E501
        :rtype: str
        """
        return self._region

    @region.setter
    def region(self, region):
        """Sets the region of this ComputeCoveragesDetailTable.

        Region information when grouped by region  # noqa: E501

        :param region: The region of this ComputeCoveragesDetailTable.  # noqa: E501
        :type: str
        """

        self._region = region

    @property
    def reservation_cost(self):
        """Gets the reservation_cost of this ComputeCoveragesDetailTable.  # noqa: E501

        Total cost for reserved instances  # noqa: E501

        :return: The reservation_cost of this ComputeCoveragesDetailTable.  # noqa: E501
        :rtype: float
        """
        return self._reservation_cost

    @reservation_cost.setter
    def reservation_cost(self, reservation_cost):
        """Sets the reservation_cost of this ComputeCoveragesDetailTable.

        Total cost for reserved instances  # noqa: E501

        :param reservation_cost: The reservation_cost of this ComputeCoveragesDetailTable.  # noqa: E501
        :type: float
        """

        self._reservation_cost = reservation_cost

    @property
    def ri_coverage_hours(self):
        """Gets the ri_coverage_hours of this ComputeCoveragesDetailTable.  # noqa: E501

        Hours covered by reserved instances  # noqa: E501

        :return: The ri_coverage_hours of this ComputeCoveragesDetailTable.  # noqa: E501
        :rtype: float
        """
        return self._ri_coverage_hours

    @ri_coverage_hours.setter
    def ri_coverage_hours(self, ri_coverage_hours):
        """Sets the ri_coverage_hours of this ComputeCoveragesDetailTable.

        Hours covered by reserved instances  # noqa: E501

        :param ri_coverage_hours: The ri_coverage_hours of this ComputeCoveragesDetailTable.  # noqa: E501
        :type: float
        """

        self._ri_coverage_hours = ri_coverage_hours

    @property
    def savings_plan_hours(self):
        """Gets the savings_plan_hours of this ComputeCoveragesDetailTable.  # noqa: E501

        Hours covered by savings plans  # noqa: E501

        :return: The savings_plan_hours of this ComputeCoveragesDetailTable.  # noqa: E501
        :rtype: float
        """
        return self._savings_plan_hours

    @savings_plan_hours.setter
    def savings_plan_hours(self, savings_plan_hours):
        """Sets the savings_plan_hours of this ComputeCoveragesDetailTable.

        Hours covered by savings plans  # noqa: E501

        :param savings_plan_hours: The savings_plan_hours of this ComputeCoveragesDetailTable.  # noqa: E501
        :type: float
        """

        self._savings_plan_hours = savings_plan_hours

    @property
    def spot_cost(self):
        """Gets the spot_cost of this ComputeCoveragesDetailTable.  # noqa: E501

        Cost for spot instances  # noqa: E501

        :return: The spot_cost of this ComputeCoveragesDetailTable.  # noqa: E501
        :rtype: float
        """
        return self._spot_cost

    @spot_cost.setter
    def spot_cost(self, spot_cost):
        """Sets the spot_cost of this ComputeCoveragesDetailTable.

        Cost for spot instances  # noqa: E501

        :param spot_cost: The spot_cost of this ComputeCoveragesDetailTable.  # noqa: E501
        :type: float
        """

        self._spot_cost = spot_cost

    @property
    def spot_hours(self):
        """Gets the spot_hours of this ComputeCoveragesDetailTable.  # noqa: E501

        Hours covered by spot instances  # noqa: E501

        :return: The spot_hours of this ComputeCoveragesDetailTable.  # noqa: E501
        :rtype: float
        """
        return self._spot_hours

    @spot_hours.setter
    def spot_hours(self, spot_hours):
        """Sets the spot_hours of this ComputeCoveragesDetailTable.

        Hours covered by spot instances  # noqa: E501

        :param spot_hours: The spot_hours of this ComputeCoveragesDetailTable.  # noqa: E501
        :type: float
        """

        self._spot_hours = spot_hours

    @property
    def total_cost(self):
        """Gets the total_cost of this ComputeCoveragesDetailTable.  # noqa: E501

        Total cost including all coverage types  # noqa: E501

        :return: The total_cost of this ComputeCoveragesDetailTable.  # noqa: E501
        :rtype: float
        """
        return self._total_cost

    @total_cost.setter
    def total_cost(self, total_cost):
        """Sets the total_cost of this ComputeCoveragesDetailTable.

        Total cost including all coverage types  # noqa: E501

        :param total_cost: The total_cost of this ComputeCoveragesDetailTable.  # noqa: E501
        :type: float
        """

        self._total_cost = total_cost

    @property
    def total_covered_hours(self):
        """Gets the total_covered_hours of this ComputeCoveragesDetailTable.  # noqa: E501

        Total hours covered by RI or SP  # noqa: E501

        :return: The total_covered_hours of this ComputeCoveragesDetailTable.  # noqa: E501
        :rtype: float
        """
        return self._total_covered_hours

    @total_covered_hours.setter
    def total_covered_hours(self, total_covered_hours):
        """Sets the total_covered_hours of this ComputeCoveragesDetailTable.

        Total hours covered by RI or SP  # noqa: E501

        :param total_covered_hours: The total_covered_hours of this ComputeCoveragesDetailTable.  # noqa: E501
        :type: float
        """

        self._total_covered_hours = total_covered_hours

    @property
    def total_hours(self):
        """Gets the total_hours of this ComputeCoveragesDetailTable.  # noqa: E501

        Total hours of usage  # noqa: E501

        :return: The total_hours of this ComputeCoveragesDetailTable.  # noqa: E501
        :rtype: float
        """
        return self._total_hours

    @total_hours.setter
    def total_hours(self, total_hours):
        """Sets the total_hours of this ComputeCoveragesDetailTable.

        Total hours of usage  # noqa: E501

        :param total_hours: The total_hours of this ComputeCoveragesDetailTable.  # noqa: E501
        :type: float
        """

        self._total_hours = total_hours

    @property
    def trend(self):
        """Gets the trend of this ComputeCoveragesDetailTable.  # noqa: E501

        Trend in coverage percentage compared to previous period  # noqa: E501

        :return: The trend of this ComputeCoveragesDetailTable.  # noqa: E501
        :rtype: float
        """
        return self._trend

    @trend.setter
    def trend(self, trend):
        """Sets the trend of this ComputeCoveragesDetailTable.

        Trend in coverage percentage compared to previous period  # noqa: E501

        :param trend: The trend of this ComputeCoveragesDetailTable.  # noqa: E501
        :type: float
        """

        self._trend = trend

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
        if issubclass(ComputeCoveragesDetailTable, dict):
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
        if not isinstance(other, ComputeCoveragesDetailTable):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
