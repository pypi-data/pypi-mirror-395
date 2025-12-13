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

class BudgetSummary(object):
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
        'actual_cost': 'float',
        'actual_cost_alerts': 'list[float]',
        'alert_thresholds': 'list[AlertThreshold]',
        'budget_amount': 'float',
        'budget_group': 'bool',
        'budget_monthly_breakdown': 'BudgetMonthlyBreakdown',
        'cascade_type': 'str',
        'child_entity_proportions': 'list[BudgetGroupChildEntityDTO]',
        'created_at': 'int',
        'created_by': 'EmbeddedUser',
        'disable_currency_warning': 'bool',
        'folder_id': 'str',
        'forecast_cost': 'float',
        'forecast_cost_alerts': 'list[float]',
        'growth_rate': 'float',
        'id': 'str',
        'is_budget_group': 'bool',
        'last_updated_at': 'int',
        'last_updated_by': 'EmbeddedUser',
        'name': 'str',
        'parent_id': 'str',
        'period': 'str',
        'perspective_id': 'str',
        'perspective_name': 'str',
        'start_time': 'int',
        'time_left': 'int',
        'time_scope': 'str',
        'time_unit': 'str',
        'type': 'str'
    }

    attribute_map = {
        'actual_cost': 'actualCost',
        'actual_cost_alerts': 'actualCostAlerts',
        'alert_thresholds': 'alertThresholds',
        'budget_amount': 'budgetAmount',
        'budget_group': 'budgetGroup',
        'budget_monthly_breakdown': 'budgetMonthlyBreakdown',
        'cascade_type': 'cascadeType',
        'child_entity_proportions': 'childEntityProportions',
        'created_at': 'createdAt',
        'created_by': 'createdBy',
        'disable_currency_warning': 'disableCurrencyWarning',
        'folder_id': 'folderId',
        'forecast_cost': 'forecastCost',
        'forecast_cost_alerts': 'forecastCostAlerts',
        'growth_rate': 'growthRate',
        'id': 'id',
        'is_budget_group': 'isBudgetGroup',
        'last_updated_at': 'lastUpdatedAt',
        'last_updated_by': 'lastUpdatedBy',
        'name': 'name',
        'parent_id': 'parentId',
        'period': 'period',
        'perspective_id': 'perspectiveId',
        'perspective_name': 'perspectiveName',
        'start_time': 'startTime',
        'time_left': 'timeLeft',
        'time_scope': 'timeScope',
        'time_unit': 'timeUnit',
        'type': 'type'
    }

    def __init__(self, actual_cost=None, actual_cost_alerts=None, alert_thresholds=None, budget_amount=None, budget_group=None, budget_monthly_breakdown=None, cascade_type=None, child_entity_proportions=None, created_at=None, created_by=None, disable_currency_warning=None, folder_id=None, forecast_cost=None, forecast_cost_alerts=None, growth_rate=None, id=None, is_budget_group=None, last_updated_at=None, last_updated_by=None, name=None, parent_id=None, period=None, perspective_id=None, perspective_name=None, start_time=None, time_left=None, time_scope=None, time_unit=None, type=None):  # noqa: E501
        """BudgetSummary - a model defined in Swagger"""  # noqa: E501
        self._actual_cost = None
        self._actual_cost_alerts = None
        self._alert_thresholds = None
        self._budget_amount = None
        self._budget_group = None
        self._budget_monthly_breakdown = None
        self._cascade_type = None
        self._child_entity_proportions = None
        self._created_at = None
        self._created_by = None
        self._disable_currency_warning = None
        self._folder_id = None
        self._forecast_cost = None
        self._forecast_cost_alerts = None
        self._growth_rate = None
        self._id = None
        self._is_budget_group = None
        self._last_updated_at = None
        self._last_updated_by = None
        self._name = None
        self._parent_id = None
        self._period = None
        self._perspective_id = None
        self._perspective_name = None
        self._start_time = None
        self._time_left = None
        self._time_scope = None
        self._time_unit = None
        self._type = None
        self.discriminator = None
        if actual_cost is not None:
            self.actual_cost = actual_cost
        if actual_cost_alerts is not None:
            self.actual_cost_alerts = actual_cost_alerts
        if alert_thresholds is not None:
            self.alert_thresholds = alert_thresholds
        if budget_amount is not None:
            self.budget_amount = budget_amount
        if budget_group is not None:
            self.budget_group = budget_group
        if budget_monthly_breakdown is not None:
            self.budget_monthly_breakdown = budget_monthly_breakdown
        if cascade_type is not None:
            self.cascade_type = cascade_type
        if child_entity_proportions is not None:
            self.child_entity_proportions = child_entity_proportions
        if created_at is not None:
            self.created_at = created_at
        if created_by is not None:
            self.created_by = created_by
        if disable_currency_warning is not None:
            self.disable_currency_warning = disable_currency_warning
        if folder_id is not None:
            self.folder_id = folder_id
        if forecast_cost is not None:
            self.forecast_cost = forecast_cost
        if forecast_cost_alerts is not None:
            self.forecast_cost_alerts = forecast_cost_alerts
        if growth_rate is not None:
            self.growth_rate = growth_rate
        if id is not None:
            self.id = id
        if is_budget_group is not None:
            self.is_budget_group = is_budget_group
        if last_updated_at is not None:
            self.last_updated_at = last_updated_at
        if last_updated_by is not None:
            self.last_updated_by = last_updated_by
        if name is not None:
            self.name = name
        if parent_id is not None:
            self.parent_id = parent_id
        if period is not None:
            self.period = period
        if perspective_id is not None:
            self.perspective_id = perspective_id
        if perspective_name is not None:
            self.perspective_name = perspective_name
        if start_time is not None:
            self.start_time = start_time
        if time_left is not None:
            self.time_left = time_left
        if time_scope is not None:
            self.time_scope = time_scope
        if time_unit is not None:
            self.time_unit = time_unit
        if type is not None:
            self.type = type

    @property
    def actual_cost(self):
        """Gets the actual_cost of this BudgetSummary.  # noqa: E501


        :return: The actual_cost of this BudgetSummary.  # noqa: E501
        :rtype: float
        """
        return self._actual_cost

    @actual_cost.setter
    def actual_cost(self, actual_cost):
        """Sets the actual_cost of this BudgetSummary.


        :param actual_cost: The actual_cost of this BudgetSummary.  # noqa: E501
        :type: float
        """

        self._actual_cost = actual_cost

    @property
    def actual_cost_alerts(self):
        """Gets the actual_cost_alerts of this BudgetSummary.  # noqa: E501


        :return: The actual_cost_alerts of this BudgetSummary.  # noqa: E501
        :rtype: list[float]
        """
        return self._actual_cost_alerts

    @actual_cost_alerts.setter
    def actual_cost_alerts(self, actual_cost_alerts):
        """Sets the actual_cost_alerts of this BudgetSummary.


        :param actual_cost_alerts: The actual_cost_alerts of this BudgetSummary.  # noqa: E501
        :type: list[float]
        """

        self._actual_cost_alerts = actual_cost_alerts

    @property
    def alert_thresholds(self):
        """Gets the alert_thresholds of this BudgetSummary.  # noqa: E501


        :return: The alert_thresholds of this BudgetSummary.  # noqa: E501
        :rtype: list[AlertThreshold]
        """
        return self._alert_thresholds

    @alert_thresholds.setter
    def alert_thresholds(self, alert_thresholds):
        """Sets the alert_thresholds of this BudgetSummary.


        :param alert_thresholds: The alert_thresholds of this BudgetSummary.  # noqa: E501
        :type: list[AlertThreshold]
        """

        self._alert_thresholds = alert_thresholds

    @property
    def budget_amount(self):
        """Gets the budget_amount of this BudgetSummary.  # noqa: E501


        :return: The budget_amount of this BudgetSummary.  # noqa: E501
        :rtype: float
        """
        return self._budget_amount

    @budget_amount.setter
    def budget_amount(self, budget_amount):
        """Sets the budget_amount of this BudgetSummary.


        :param budget_amount: The budget_amount of this BudgetSummary.  # noqa: E501
        :type: float
        """

        self._budget_amount = budget_amount

    @property
    def budget_group(self):
        """Gets the budget_group of this BudgetSummary.  # noqa: E501


        :return: The budget_group of this BudgetSummary.  # noqa: E501
        :rtype: bool
        """
        return self._budget_group

    @budget_group.setter
    def budget_group(self, budget_group):
        """Sets the budget_group of this BudgetSummary.


        :param budget_group: The budget_group of this BudgetSummary.  # noqa: E501
        :type: bool
        """

        self._budget_group = budget_group

    @property
    def budget_monthly_breakdown(self):
        """Gets the budget_monthly_breakdown of this BudgetSummary.  # noqa: E501


        :return: The budget_monthly_breakdown of this BudgetSummary.  # noqa: E501
        :rtype: BudgetMonthlyBreakdown
        """
        return self._budget_monthly_breakdown

    @budget_monthly_breakdown.setter
    def budget_monthly_breakdown(self, budget_monthly_breakdown):
        """Sets the budget_monthly_breakdown of this BudgetSummary.


        :param budget_monthly_breakdown: The budget_monthly_breakdown of this BudgetSummary.  # noqa: E501
        :type: BudgetMonthlyBreakdown
        """

        self._budget_monthly_breakdown = budget_monthly_breakdown

    @property
    def cascade_type(self):
        """Gets the cascade_type of this BudgetSummary.  # noqa: E501


        :return: The cascade_type of this BudgetSummary.  # noqa: E501
        :rtype: str
        """
        return self._cascade_type

    @cascade_type.setter
    def cascade_type(self, cascade_type):
        """Sets the cascade_type of this BudgetSummary.


        :param cascade_type: The cascade_type of this BudgetSummary.  # noqa: E501
        :type: str
        """
        allowed_values = ["EQUAL", "PROPORTIONAL", "NO_CASCADE"]  # noqa: E501
        if cascade_type not in allowed_values:
            raise ValueError(
                "Invalid value for `cascade_type` ({0}), must be one of {1}"  # noqa: E501
                .format(cascade_type, allowed_values)
            )

        self._cascade_type = cascade_type

    @property
    def child_entity_proportions(self):
        """Gets the child_entity_proportions of this BudgetSummary.  # noqa: E501


        :return: The child_entity_proportions of this BudgetSummary.  # noqa: E501
        :rtype: list[BudgetGroupChildEntityDTO]
        """
        return self._child_entity_proportions

    @child_entity_proportions.setter
    def child_entity_proportions(self, child_entity_proportions):
        """Sets the child_entity_proportions of this BudgetSummary.


        :param child_entity_proportions: The child_entity_proportions of this BudgetSummary.  # noqa: E501
        :type: list[BudgetGroupChildEntityDTO]
        """

        self._child_entity_proportions = child_entity_proportions

    @property
    def created_at(self):
        """Gets the created_at of this BudgetSummary.  # noqa: E501


        :return: The created_at of this BudgetSummary.  # noqa: E501
        :rtype: int
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this BudgetSummary.


        :param created_at: The created_at of this BudgetSummary.  # noqa: E501
        :type: int
        """

        self._created_at = created_at

    @property
    def created_by(self):
        """Gets the created_by of this BudgetSummary.  # noqa: E501


        :return: The created_by of this BudgetSummary.  # noqa: E501
        :rtype: EmbeddedUser
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this BudgetSummary.


        :param created_by: The created_by of this BudgetSummary.  # noqa: E501
        :type: EmbeddedUser
        """

        self._created_by = created_by

    @property
    def disable_currency_warning(self):
        """Gets the disable_currency_warning of this BudgetSummary.  # noqa: E501


        :return: The disable_currency_warning of this BudgetSummary.  # noqa: E501
        :rtype: bool
        """
        return self._disable_currency_warning

    @disable_currency_warning.setter
    def disable_currency_warning(self, disable_currency_warning):
        """Sets the disable_currency_warning of this BudgetSummary.


        :param disable_currency_warning: The disable_currency_warning of this BudgetSummary.  # noqa: E501
        :type: bool
        """

        self._disable_currency_warning = disable_currency_warning

    @property
    def folder_id(self):
        """Gets the folder_id of this BudgetSummary.  # noqa: E501


        :return: The folder_id of this BudgetSummary.  # noqa: E501
        :rtype: str
        """
        return self._folder_id

    @folder_id.setter
    def folder_id(self, folder_id):
        """Sets the folder_id of this BudgetSummary.


        :param folder_id: The folder_id of this BudgetSummary.  # noqa: E501
        :type: str
        """

        self._folder_id = folder_id

    @property
    def forecast_cost(self):
        """Gets the forecast_cost of this BudgetSummary.  # noqa: E501


        :return: The forecast_cost of this BudgetSummary.  # noqa: E501
        :rtype: float
        """
        return self._forecast_cost

    @forecast_cost.setter
    def forecast_cost(self, forecast_cost):
        """Sets the forecast_cost of this BudgetSummary.


        :param forecast_cost: The forecast_cost of this BudgetSummary.  # noqa: E501
        :type: float
        """

        self._forecast_cost = forecast_cost

    @property
    def forecast_cost_alerts(self):
        """Gets the forecast_cost_alerts of this BudgetSummary.  # noqa: E501


        :return: The forecast_cost_alerts of this BudgetSummary.  # noqa: E501
        :rtype: list[float]
        """
        return self._forecast_cost_alerts

    @forecast_cost_alerts.setter
    def forecast_cost_alerts(self, forecast_cost_alerts):
        """Sets the forecast_cost_alerts of this BudgetSummary.


        :param forecast_cost_alerts: The forecast_cost_alerts of this BudgetSummary.  # noqa: E501
        :type: list[float]
        """

        self._forecast_cost_alerts = forecast_cost_alerts

    @property
    def growth_rate(self):
        """Gets the growth_rate of this BudgetSummary.  # noqa: E501


        :return: The growth_rate of this BudgetSummary.  # noqa: E501
        :rtype: float
        """
        return self._growth_rate

    @growth_rate.setter
    def growth_rate(self, growth_rate):
        """Sets the growth_rate of this BudgetSummary.


        :param growth_rate: The growth_rate of this BudgetSummary.  # noqa: E501
        :type: float
        """

        self._growth_rate = growth_rate

    @property
    def id(self):
        """Gets the id of this BudgetSummary.  # noqa: E501


        :return: The id of this BudgetSummary.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this BudgetSummary.


        :param id: The id of this BudgetSummary.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def is_budget_group(self):
        """Gets the is_budget_group of this BudgetSummary.  # noqa: E501


        :return: The is_budget_group of this BudgetSummary.  # noqa: E501
        :rtype: bool
        """
        return self._is_budget_group

    @is_budget_group.setter
    def is_budget_group(self, is_budget_group):
        """Sets the is_budget_group of this BudgetSummary.


        :param is_budget_group: The is_budget_group of this BudgetSummary.  # noqa: E501
        :type: bool
        """

        self._is_budget_group = is_budget_group

    @property
    def last_updated_at(self):
        """Gets the last_updated_at of this BudgetSummary.  # noqa: E501


        :return: The last_updated_at of this BudgetSummary.  # noqa: E501
        :rtype: int
        """
        return self._last_updated_at

    @last_updated_at.setter
    def last_updated_at(self, last_updated_at):
        """Sets the last_updated_at of this BudgetSummary.


        :param last_updated_at: The last_updated_at of this BudgetSummary.  # noqa: E501
        :type: int
        """

        self._last_updated_at = last_updated_at

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this BudgetSummary.  # noqa: E501


        :return: The last_updated_by of this BudgetSummary.  # noqa: E501
        :rtype: EmbeddedUser
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this BudgetSummary.


        :param last_updated_by: The last_updated_by of this BudgetSummary.  # noqa: E501
        :type: EmbeddedUser
        """

        self._last_updated_by = last_updated_by

    @property
    def name(self):
        """Gets the name of this BudgetSummary.  # noqa: E501


        :return: The name of this BudgetSummary.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this BudgetSummary.


        :param name: The name of this BudgetSummary.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def parent_id(self):
        """Gets the parent_id of this BudgetSummary.  # noqa: E501


        :return: The parent_id of this BudgetSummary.  # noqa: E501
        :rtype: str
        """
        return self._parent_id

    @parent_id.setter
    def parent_id(self, parent_id):
        """Sets the parent_id of this BudgetSummary.


        :param parent_id: The parent_id of this BudgetSummary.  # noqa: E501
        :type: str
        """

        self._parent_id = parent_id

    @property
    def period(self):
        """Gets the period of this BudgetSummary.  # noqa: E501


        :return: The period of this BudgetSummary.  # noqa: E501
        :rtype: str
        """
        return self._period

    @period.setter
    def period(self, period):
        """Sets the period of this BudgetSummary.


        :param period: The period of this BudgetSummary.  # noqa: E501
        :type: str
        """
        allowed_values = ["DAILY", "WEEKLY", "MONTHLY", "QUARTERLY", "YEARLY"]  # noqa: E501
        if period not in allowed_values:
            raise ValueError(
                "Invalid value for `period` ({0}), must be one of {1}"  # noqa: E501
                .format(period, allowed_values)
            )

        self._period = period

    @property
    def perspective_id(self):
        """Gets the perspective_id of this BudgetSummary.  # noqa: E501


        :return: The perspective_id of this BudgetSummary.  # noqa: E501
        :rtype: str
        """
        return self._perspective_id

    @perspective_id.setter
    def perspective_id(self, perspective_id):
        """Sets the perspective_id of this BudgetSummary.


        :param perspective_id: The perspective_id of this BudgetSummary.  # noqa: E501
        :type: str
        """

        self._perspective_id = perspective_id

    @property
    def perspective_name(self):
        """Gets the perspective_name of this BudgetSummary.  # noqa: E501


        :return: The perspective_name of this BudgetSummary.  # noqa: E501
        :rtype: str
        """
        return self._perspective_name

    @perspective_name.setter
    def perspective_name(self, perspective_name):
        """Sets the perspective_name of this BudgetSummary.


        :param perspective_name: The perspective_name of this BudgetSummary.  # noqa: E501
        :type: str
        """

        self._perspective_name = perspective_name

    @property
    def start_time(self):
        """Gets the start_time of this BudgetSummary.  # noqa: E501


        :return: The start_time of this BudgetSummary.  # noqa: E501
        :rtype: int
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this BudgetSummary.


        :param start_time: The start_time of this BudgetSummary.  # noqa: E501
        :type: int
        """

        self._start_time = start_time

    @property
    def time_left(self):
        """Gets the time_left of this BudgetSummary.  # noqa: E501


        :return: The time_left of this BudgetSummary.  # noqa: E501
        :rtype: int
        """
        return self._time_left

    @time_left.setter
    def time_left(self, time_left):
        """Sets the time_left of this BudgetSummary.


        :param time_left: The time_left of this BudgetSummary.  # noqa: E501
        :type: int
        """

        self._time_left = time_left

    @property
    def time_scope(self):
        """Gets the time_scope of this BudgetSummary.  # noqa: E501


        :return: The time_scope of this BudgetSummary.  # noqa: E501
        :rtype: str
        """
        return self._time_scope

    @time_scope.setter
    def time_scope(self, time_scope):
        """Sets the time_scope of this BudgetSummary.


        :param time_scope: The time_scope of this BudgetSummary.  # noqa: E501
        :type: str
        """

        self._time_scope = time_scope

    @property
    def time_unit(self):
        """Gets the time_unit of this BudgetSummary.  # noqa: E501


        :return: The time_unit of this BudgetSummary.  # noqa: E501
        :rtype: str
        """
        return self._time_unit

    @time_unit.setter
    def time_unit(self, time_unit):
        """Sets the time_unit of this BudgetSummary.


        :param time_unit: The time_unit of this BudgetSummary.  # noqa: E501
        :type: str
        """

        self._time_unit = time_unit

    @property
    def type(self):
        """Gets the type of this BudgetSummary.  # noqa: E501

        Whether the Budget is based on a specified amount or based on previous month's actual spend  # noqa: E501

        :return: The type of this BudgetSummary.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this BudgetSummary.

        Whether the Budget is based on a specified amount or based on previous month's actual spend  # noqa: E501

        :param type: The type of this BudgetSummary.  # noqa: E501
        :type: str
        """
        allowed_values = ["SPECIFIED_AMOUNT", "PREVIOUS_MONTH_SPEND", "PREVIOUS_PERIOD_SPEND"]  # noqa: E501
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
        if issubclass(BudgetSummary, dict):
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
        if not isinstance(other, BudgetSummary):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
