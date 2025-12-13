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

class RuleExecutionFilter(object):
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
        'account_id': 'str',
        'cloud_provider': 'str',
        'cloud_providers': 'list[str]',
        'cost_type': 'str',
        'execution_ids': 'list[str]',
        'execution_status': 'str',
        'is_dry_run': 'bool',
        'limit': 'int',
        'offset': 'int',
        'region': 'list[str]',
        'resource_count_greater_than_zero': 'bool',
        'rule_enforcement_id': 'list[str]',
        'rule_enforcement_recommendation_id': 'list[str]',
        'rule_execution_sort_type': 'str',
        'rule_ids': 'list[str]',
        'rule_set_ids': 'list[str]',
        'savings': 'float',
        'sort_order': 'str',
        'target_account': 'list[str]',
        'time': 'list[CCMTimeFilter]'
    }

    attribute_map = {
        'account_id': 'accountId',
        'cloud_provider': 'cloudProvider',
        'cloud_providers': 'cloudProviders',
        'cost_type': 'costType',
        'execution_ids': 'executionIds',
        'execution_status': 'executionStatus',
        'is_dry_run': 'isDryRun',
        'limit': 'limit',
        'offset': 'offset',
        'region': 'region',
        'resource_count_greater_than_zero': 'resourceCountGreaterThanZero',
        'rule_enforcement_id': 'ruleEnforcementId',
        'rule_enforcement_recommendation_id': 'ruleEnforcementRecommendationId',
        'rule_execution_sort_type': 'ruleExecutionSortType',
        'rule_ids': 'ruleIds',
        'rule_set_ids': 'ruleSetIds',
        'savings': 'savings',
        'sort_order': 'sortOrder',
        'target_account': 'targetAccount',
        'time': 'time'
    }

    def __init__(self, account_id=None, cloud_provider=None, cloud_providers=None, cost_type=None, execution_ids=None, execution_status=None, is_dry_run=None, limit=None, offset=None, region=None, resource_count_greater_than_zero=None, rule_enforcement_id=None, rule_enforcement_recommendation_id=None, rule_execution_sort_type=None, rule_ids=None, rule_set_ids=None, savings=None, sort_order=None, target_account=None, time=None):  # noqa: E501
        """RuleExecutionFilter - a model defined in Swagger"""  # noqa: E501
        self._account_id = None
        self._cloud_provider = None
        self._cloud_providers = None
        self._cost_type = None
        self._execution_ids = None
        self._execution_status = None
        self._is_dry_run = None
        self._limit = None
        self._offset = None
        self._region = None
        self._resource_count_greater_than_zero = None
        self._rule_enforcement_id = None
        self._rule_enforcement_recommendation_id = None
        self._rule_execution_sort_type = None
        self._rule_ids = None
        self._rule_set_ids = None
        self._savings = None
        self._sort_order = None
        self._target_account = None
        self._time = None
        self.discriminator = None
        if account_id is not None:
            self.account_id = account_id
        if cloud_provider is not None:
            self.cloud_provider = cloud_provider
        if cloud_providers is not None:
            self.cloud_providers = cloud_providers
        if cost_type is not None:
            self.cost_type = cost_type
        if execution_ids is not None:
            self.execution_ids = execution_ids
        if execution_status is not None:
            self.execution_status = execution_status
        if is_dry_run is not None:
            self.is_dry_run = is_dry_run
        if limit is not None:
            self.limit = limit
        if offset is not None:
            self.offset = offset
        if region is not None:
            self.region = region
        if resource_count_greater_than_zero is not None:
            self.resource_count_greater_than_zero = resource_count_greater_than_zero
        if rule_enforcement_id is not None:
            self.rule_enforcement_id = rule_enforcement_id
        if rule_enforcement_recommendation_id is not None:
            self.rule_enforcement_recommendation_id = rule_enforcement_recommendation_id
        if rule_execution_sort_type is not None:
            self.rule_execution_sort_type = rule_execution_sort_type
        if rule_ids is not None:
            self.rule_ids = rule_ids
        if rule_set_ids is not None:
            self.rule_set_ids = rule_set_ids
        if savings is not None:
            self.savings = savings
        if sort_order is not None:
            self.sort_order = sort_order
        if target_account is not None:
            self.target_account = target_account
        if time is not None:
            self.time = time

    @property
    def account_id(self):
        """Gets the account_id of this RuleExecutionFilter.  # noqa: E501

        accountId  # noqa: E501

        :return: The account_id of this RuleExecutionFilter.  # noqa: E501
        :rtype: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """Sets the account_id of this RuleExecutionFilter.

        accountId  # noqa: E501

        :param account_id: The account_id of this RuleExecutionFilter.  # noqa: E501
        :type: str
        """

        self._account_id = account_id

    @property
    def cloud_provider(self):
        """Gets the cloud_provider of this RuleExecutionFilter.  # noqa: E501

        cloudProvider  # noqa: E501

        :return: The cloud_provider of this RuleExecutionFilter.  # noqa: E501
        :rtype: str
        """
        return self._cloud_provider

    @cloud_provider.setter
    def cloud_provider(self, cloud_provider):
        """Sets the cloud_provider of this RuleExecutionFilter.

        cloudProvider  # noqa: E501

        :param cloud_provider: The cloud_provider of this RuleExecutionFilter.  # noqa: E501
        :type: str
        """
        allowed_values = ["AWS", "AZURE", "GCP"]  # noqa: E501
        if cloud_provider not in allowed_values:
            raise ValueError(
                "Invalid value for `cloud_provider` ({0}), must be one of {1}"  # noqa: E501
                .format(cloud_provider, allowed_values)
            )

        self._cloud_provider = cloud_provider

    @property
    def cloud_providers(self):
        """Gets the cloud_providers of this RuleExecutionFilter.  # noqa: E501

        cloudProviders  # noqa: E501

        :return: The cloud_providers of this RuleExecutionFilter.  # noqa: E501
        :rtype: list[str]
        """
        return self._cloud_providers

    @cloud_providers.setter
    def cloud_providers(self, cloud_providers):
        """Sets the cloud_providers of this RuleExecutionFilter.

        cloudProviders  # noqa: E501

        :param cloud_providers: The cloud_providers of this RuleExecutionFilter.  # noqa: E501
        :type: list[str]
        """
        allowed_values = ["AWS", "AZURE", "GCP"]  # noqa: E501
        if not set(cloud_providers).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `cloud_providers` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(cloud_providers) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )

        self._cloud_providers = cloud_providers

    @property
    def cost_type(self):
        """Gets the cost_type of this RuleExecutionFilter.  # noqa: E501

        costType  # noqa: E501

        :return: The cost_type of this RuleExecutionFilter.  # noqa: E501
        :rtype: str
        """
        return self._cost_type

    @cost_type.setter
    def cost_type(self, cost_type):
        """Sets the cost_type of this RuleExecutionFilter.

        costType  # noqa: E501

        :param cost_type: The cost_type of this RuleExecutionFilter.  # noqa: E501
        :type: str
        """
        allowed_values = ["POTENTIAL", "REALIZED"]  # noqa: E501
        if cost_type not in allowed_values:
            raise ValueError(
                "Invalid value for `cost_type` ({0}), must be one of {1}"  # noqa: E501
                .format(cost_type, allowed_values)
            )

        self._cost_type = cost_type

    @property
    def execution_ids(self):
        """Gets the execution_ids of this RuleExecutionFilter.  # noqa: E501

        executionIds  # noqa: E501

        :return: The execution_ids of this RuleExecutionFilter.  # noqa: E501
        :rtype: list[str]
        """
        return self._execution_ids

    @execution_ids.setter
    def execution_ids(self, execution_ids):
        """Sets the execution_ids of this RuleExecutionFilter.

        executionIds  # noqa: E501

        :param execution_ids: The execution_ids of this RuleExecutionFilter.  # noqa: E501
        :type: list[str]
        """

        self._execution_ids = execution_ids

    @property
    def execution_status(self):
        """Gets the execution_status of this RuleExecutionFilter.  # noqa: E501

        Execution Status  # noqa: E501

        :return: The execution_status of this RuleExecutionFilter.  # noqa: E501
        :rtype: str
        """
        return self._execution_status

    @execution_status.setter
    def execution_status(self, execution_status):
        """Sets the execution_status of this RuleExecutionFilter.

        Execution Status  # noqa: E501

        :param execution_status: The execution_status of this RuleExecutionFilter.  # noqa: E501
        :type: str
        """
        allowed_values = ["FAILED", "ENQUEUED", "PARTIAL_SUCCESS", "SUCCESS"]  # noqa: E501
        if execution_status not in allowed_values:
            raise ValueError(
                "Invalid value for `execution_status` ({0}), must be one of {1}"  # noqa: E501
                .format(execution_status, allowed_values)
            )

        self._execution_status = execution_status

    @property
    def is_dry_run(self):
        """Gets the is_dry_run of this RuleExecutionFilter.  # noqa: E501

        isDryRun  # noqa: E501

        :return: The is_dry_run of this RuleExecutionFilter.  # noqa: E501
        :rtype: bool
        """
        return self._is_dry_run

    @is_dry_run.setter
    def is_dry_run(self, is_dry_run):
        """Sets the is_dry_run of this RuleExecutionFilter.

        isDryRun  # noqa: E501

        :param is_dry_run: The is_dry_run of this RuleExecutionFilter.  # noqa: E501
        :type: bool
        """

        self._is_dry_run = is_dry_run

    @property
    def limit(self):
        """Gets the limit of this RuleExecutionFilter.  # noqa: E501

        limit  # noqa: E501

        :return: The limit of this RuleExecutionFilter.  # noqa: E501
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this RuleExecutionFilter.

        limit  # noqa: E501

        :param limit: The limit of this RuleExecutionFilter.  # noqa: E501
        :type: int
        """

        self._limit = limit

    @property
    def offset(self):
        """Gets the offset of this RuleExecutionFilter.  # noqa: E501

        offset  # noqa: E501

        :return: The offset of this RuleExecutionFilter.  # noqa: E501
        :rtype: int
        """
        return self._offset

    @offset.setter
    def offset(self, offset):
        """Sets the offset of this RuleExecutionFilter.

        offset  # noqa: E501

        :param offset: The offset of this RuleExecutionFilter.  # noqa: E501
        :type: int
        """

        self._offset = offset

    @property
    def region(self):
        """Gets the region of this RuleExecutionFilter.  # noqa: E501

        region  # noqa: E501

        :return: The region of this RuleExecutionFilter.  # noqa: E501
        :rtype: list[str]
        """
        return self._region

    @region.setter
    def region(self, region):
        """Sets the region of this RuleExecutionFilter.

        region  # noqa: E501

        :param region: The region of this RuleExecutionFilter.  # noqa: E501
        :type: list[str]
        """

        self._region = region

    @property
    def resource_count_greater_than_zero(self):
        """Gets the resource_count_greater_than_zero of this RuleExecutionFilter.  # noqa: E501

        resourceCountGreaterThanZero  # noqa: E501

        :return: The resource_count_greater_than_zero of this RuleExecutionFilter.  # noqa: E501
        :rtype: bool
        """
        return self._resource_count_greater_than_zero

    @resource_count_greater_than_zero.setter
    def resource_count_greater_than_zero(self, resource_count_greater_than_zero):
        """Sets the resource_count_greater_than_zero of this RuleExecutionFilter.

        resourceCountGreaterThanZero  # noqa: E501

        :param resource_count_greater_than_zero: The resource_count_greater_than_zero of this RuleExecutionFilter.  # noqa: E501
        :type: bool
        """

        self._resource_count_greater_than_zero = resource_count_greater_than_zero

    @property
    def rule_enforcement_id(self):
        """Gets the rule_enforcement_id of this RuleExecutionFilter.  # noqa: E501

        ruleEnforcementId  # noqa: E501

        :return: The rule_enforcement_id of this RuleExecutionFilter.  # noqa: E501
        :rtype: list[str]
        """
        return self._rule_enforcement_id

    @rule_enforcement_id.setter
    def rule_enforcement_id(self, rule_enforcement_id):
        """Sets the rule_enforcement_id of this RuleExecutionFilter.

        ruleEnforcementId  # noqa: E501

        :param rule_enforcement_id: The rule_enforcement_id of this RuleExecutionFilter.  # noqa: E501
        :type: list[str]
        """

        self._rule_enforcement_id = rule_enforcement_id

    @property
    def rule_enforcement_recommendation_id(self):
        """Gets the rule_enforcement_recommendation_id of this RuleExecutionFilter.  # noqa: E501

        ruleEnforcementRecommendationId  # noqa: E501

        :return: The rule_enforcement_recommendation_id of this RuleExecutionFilter.  # noqa: E501
        :rtype: list[str]
        """
        return self._rule_enforcement_recommendation_id

    @rule_enforcement_recommendation_id.setter
    def rule_enforcement_recommendation_id(self, rule_enforcement_recommendation_id):
        """Sets the rule_enforcement_recommendation_id of this RuleExecutionFilter.

        ruleEnforcementRecommendationId  # noqa: E501

        :param rule_enforcement_recommendation_id: The rule_enforcement_recommendation_id of this RuleExecutionFilter.  # noqa: E501
        :type: list[str]
        """

        self._rule_enforcement_recommendation_id = rule_enforcement_recommendation_id

    @property
    def rule_execution_sort_type(self):
        """Gets the rule_execution_sort_type of this RuleExecutionFilter.  # noqa: E501

        ruleExecutionSortType  # noqa: E501

        :return: The rule_execution_sort_type of this RuleExecutionFilter.  # noqa: E501
        :rtype: str
        """
        return self._rule_execution_sort_type

    @rule_execution_sort_type.setter
    def rule_execution_sort_type(self, rule_execution_sort_type):
        """Sets the rule_execution_sort_type of this RuleExecutionFilter.

        ruleExecutionSortType  # noqa: E501

        :param rule_execution_sort_type: The rule_execution_sort_type of this RuleExecutionFilter.  # noqa: E501
        :type: str
        """
        allowed_values = ["COST", "LAST_UPDATED_AT", "RESOURCE_COUNT"]  # noqa: E501
        if rule_execution_sort_type not in allowed_values:
            raise ValueError(
                "Invalid value for `rule_execution_sort_type` ({0}), must be one of {1}"  # noqa: E501
                .format(rule_execution_sort_type, allowed_values)
            )

        self._rule_execution_sort_type = rule_execution_sort_type

    @property
    def rule_ids(self):
        """Gets the rule_ids of this RuleExecutionFilter.  # noqa: E501

        ruleId  # noqa: E501

        :return: The rule_ids of this RuleExecutionFilter.  # noqa: E501
        :rtype: list[str]
        """
        return self._rule_ids

    @rule_ids.setter
    def rule_ids(self, rule_ids):
        """Sets the rule_ids of this RuleExecutionFilter.

        ruleId  # noqa: E501

        :param rule_ids: The rule_ids of this RuleExecutionFilter.  # noqa: E501
        :type: list[str]
        """

        self._rule_ids = rule_ids

    @property
    def rule_set_ids(self):
        """Gets the rule_set_ids of this RuleExecutionFilter.  # noqa: E501

        rulePackId  # noqa: E501

        :return: The rule_set_ids of this RuleExecutionFilter.  # noqa: E501
        :rtype: list[str]
        """
        return self._rule_set_ids

    @rule_set_ids.setter
    def rule_set_ids(self, rule_set_ids):
        """Sets the rule_set_ids of this RuleExecutionFilter.

        rulePackId  # noqa: E501

        :param rule_set_ids: The rule_set_ids of this RuleExecutionFilter.  # noqa: E501
        :type: list[str]
        """

        self._rule_set_ids = rule_set_ids

    @property
    def savings(self):
        """Gets the savings of this RuleExecutionFilter.  # noqa: E501

        savings  # noqa: E501

        :return: The savings of this RuleExecutionFilter.  # noqa: E501
        :rtype: float
        """
        return self._savings

    @savings.setter
    def savings(self, savings):
        """Sets the savings of this RuleExecutionFilter.

        savings  # noqa: E501

        :param savings: The savings of this RuleExecutionFilter.  # noqa: E501
        :type: float
        """

        self._savings = savings

    @property
    def sort_order(self):
        """Gets the sort_order of this RuleExecutionFilter.  # noqa: E501

        sortOrder  # noqa: E501

        :return: The sort_order of this RuleExecutionFilter.  # noqa: E501
        :rtype: str
        """
        return self._sort_order

    @sort_order.setter
    def sort_order(self, sort_order):
        """Sets the sort_order of this RuleExecutionFilter.

        sortOrder  # noqa: E501

        :param sort_order: The sort_order of this RuleExecutionFilter.  # noqa: E501
        :type: str
        """
        allowed_values = ["ASCENDING", "DESCENDING"]  # noqa: E501
        if sort_order not in allowed_values:
            raise ValueError(
                "Invalid value for `sort_order` ({0}), must be one of {1}"  # noqa: E501
                .format(sort_order, allowed_values)
            )

        self._sort_order = sort_order

    @property
    def target_account(self):
        """Gets the target_account of this RuleExecutionFilter.  # noqa: E501

        Account Name  # noqa: E501

        :return: The target_account of this RuleExecutionFilter.  # noqa: E501
        :rtype: list[str]
        """
        return self._target_account

    @target_account.setter
    def target_account(self, target_account):
        """Sets the target_account of this RuleExecutionFilter.

        Account Name  # noqa: E501

        :param target_account: The target_account of this RuleExecutionFilter.  # noqa: E501
        :type: list[str]
        """

        self._target_account = target_account

    @property
    def time(self):
        """Gets the time of this RuleExecutionFilter.  # noqa: E501

        Time  # noqa: E501

        :return: The time of this RuleExecutionFilter.  # noqa: E501
        :rtype: list[CCMTimeFilter]
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this RuleExecutionFilter.

        Time  # noqa: E501

        :param time: The time of this RuleExecutionFilter.  # noqa: E501
        :type: list[CCMTimeFilter]
        """

        self._time = time

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
        if issubclass(RuleExecutionFilter, dict):
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
        if not isinstance(other, RuleExecutionFilter):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
