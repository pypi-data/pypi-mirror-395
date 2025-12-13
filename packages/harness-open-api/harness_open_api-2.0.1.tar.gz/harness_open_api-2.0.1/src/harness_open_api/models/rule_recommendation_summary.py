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

class RuleRecommendationSummary(object):
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
        'cloud_provider': 'str',
        'executions': 'list[RuleRecommendationExecution]',
        'id': 'RuleRecommendationSummaryId',
        'is_ootb': 'bool',
        'last_evaluated_at': 'int',
        'potential_savings': 'float',
        'rule_name': 'str',
        'status': 'str',
        'targets': 'list[str]',
        'total_executions': 'int',
        'total_failed_executions': 'int',
        'total_recommendations': 'int'
    }

    attribute_map = {
        'cloud_provider': 'cloudProvider',
        'executions': 'executions',
        'id': 'id',
        'is_ootb': 'isOOTB',
        'last_evaluated_at': 'lastEvaluatedAt',
        'potential_savings': 'potentialSavings',
        'rule_name': 'ruleName',
        'status': 'status',
        'targets': 'targets',
        'total_executions': 'totalExecutions',
        'total_failed_executions': 'totalFailedExecutions',
        'total_recommendations': 'totalRecommendations'
    }

    def __init__(self, cloud_provider=None, executions=None, id=None, is_ootb=None, last_evaluated_at=None, potential_savings=None, rule_name=None, status=None, targets=None, total_executions=None, total_failed_executions=None, total_recommendations=None):  # noqa: E501
        """RuleRecommendationSummary - a model defined in Swagger"""  # noqa: E501
        self._cloud_provider = None
        self._executions = None
        self._id = None
        self._is_ootb = None
        self._last_evaluated_at = None
        self._potential_savings = None
        self._rule_name = None
        self._status = None
        self._targets = None
        self._total_executions = None
        self._total_failed_executions = None
        self._total_recommendations = None
        self.discriminator = None
        if cloud_provider is not None:
            self.cloud_provider = cloud_provider
        if executions is not None:
            self.executions = executions
        if id is not None:
            self.id = id
        if is_ootb is not None:
            self.is_ootb = is_ootb
        if last_evaluated_at is not None:
            self.last_evaluated_at = last_evaluated_at
        if potential_savings is not None:
            self.potential_savings = potential_savings
        if rule_name is not None:
            self.rule_name = rule_name
        if status is not None:
            self.status = status
        if targets is not None:
            self.targets = targets
        if total_executions is not None:
            self.total_executions = total_executions
        if total_failed_executions is not None:
            self.total_failed_executions = total_failed_executions
        if total_recommendations is not None:
            self.total_recommendations = total_recommendations

    @property
    def cloud_provider(self):
        """Gets the cloud_provider of this RuleRecommendationSummary.  # noqa: E501


        :return: The cloud_provider of this RuleRecommendationSummary.  # noqa: E501
        :rtype: str
        """
        return self._cloud_provider

    @cloud_provider.setter
    def cloud_provider(self, cloud_provider):
        """Sets the cloud_provider of this RuleRecommendationSummary.


        :param cloud_provider: The cloud_provider of this RuleRecommendationSummary.  # noqa: E501
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
    def executions(self):
        """Gets the executions of this RuleRecommendationSummary.  # noqa: E501


        :return: The executions of this RuleRecommendationSummary.  # noqa: E501
        :rtype: list[RuleRecommendationExecution]
        """
        return self._executions

    @executions.setter
    def executions(self, executions):
        """Sets the executions of this RuleRecommendationSummary.


        :param executions: The executions of this RuleRecommendationSummary.  # noqa: E501
        :type: list[RuleRecommendationExecution]
        """

        self._executions = executions

    @property
    def id(self):
        """Gets the id of this RuleRecommendationSummary.  # noqa: E501


        :return: The id of this RuleRecommendationSummary.  # noqa: E501
        :rtype: RuleRecommendationSummaryId
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this RuleRecommendationSummary.


        :param id: The id of this RuleRecommendationSummary.  # noqa: E501
        :type: RuleRecommendationSummaryId
        """

        self._id = id

    @property
    def is_ootb(self):
        """Gets the is_ootb of this RuleRecommendationSummary.  # noqa: E501


        :return: The is_ootb of this RuleRecommendationSummary.  # noqa: E501
        :rtype: bool
        """
        return self._is_ootb

    @is_ootb.setter
    def is_ootb(self, is_ootb):
        """Sets the is_ootb of this RuleRecommendationSummary.


        :param is_ootb: The is_ootb of this RuleRecommendationSummary.  # noqa: E501
        :type: bool
        """

        self._is_ootb = is_ootb

    @property
    def last_evaluated_at(self):
        """Gets the last_evaluated_at of this RuleRecommendationSummary.  # noqa: E501


        :return: The last_evaluated_at of this RuleRecommendationSummary.  # noqa: E501
        :rtype: int
        """
        return self._last_evaluated_at

    @last_evaluated_at.setter
    def last_evaluated_at(self, last_evaluated_at):
        """Sets the last_evaluated_at of this RuleRecommendationSummary.


        :param last_evaluated_at: The last_evaluated_at of this RuleRecommendationSummary.  # noqa: E501
        :type: int
        """

        self._last_evaluated_at = last_evaluated_at

    @property
    def potential_savings(self):
        """Gets the potential_savings of this RuleRecommendationSummary.  # noqa: E501


        :return: The potential_savings of this RuleRecommendationSummary.  # noqa: E501
        :rtype: float
        """
        return self._potential_savings

    @potential_savings.setter
    def potential_savings(self, potential_savings):
        """Sets the potential_savings of this RuleRecommendationSummary.


        :param potential_savings: The potential_savings of this RuleRecommendationSummary.  # noqa: E501
        :type: float
        """

        self._potential_savings = potential_savings

    @property
    def rule_name(self):
        """Gets the rule_name of this RuleRecommendationSummary.  # noqa: E501


        :return: The rule_name of this RuleRecommendationSummary.  # noqa: E501
        :rtype: str
        """
        return self._rule_name

    @rule_name.setter
    def rule_name(self, rule_name):
        """Sets the rule_name of this RuleRecommendationSummary.


        :param rule_name: The rule_name of this RuleRecommendationSummary.  # noqa: E501
        :type: str
        """

        self._rule_name = rule_name

    @property
    def status(self):
        """Gets the status of this RuleRecommendationSummary.  # noqa: E501


        :return: The status of this RuleRecommendationSummary.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this RuleRecommendationSummary.


        :param status: The status of this RuleRecommendationSummary.  # noqa: E501
        :type: str
        """
        allowed_values = ["FAILED", "IN_PROGRESS", "PARTIAL_SUCCESS", "SUCCESS", "IGNORED"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def targets(self):
        """Gets the targets of this RuleRecommendationSummary.  # noqa: E501


        :return: The targets of this RuleRecommendationSummary.  # noqa: E501
        :rtype: list[str]
        """
        return self._targets

    @targets.setter
    def targets(self, targets):
        """Sets the targets of this RuleRecommendationSummary.


        :param targets: The targets of this RuleRecommendationSummary.  # noqa: E501
        :type: list[str]
        """

        self._targets = targets

    @property
    def total_executions(self):
        """Gets the total_executions of this RuleRecommendationSummary.  # noqa: E501


        :return: The total_executions of this RuleRecommendationSummary.  # noqa: E501
        :rtype: int
        """
        return self._total_executions

    @total_executions.setter
    def total_executions(self, total_executions):
        """Sets the total_executions of this RuleRecommendationSummary.


        :param total_executions: The total_executions of this RuleRecommendationSummary.  # noqa: E501
        :type: int
        """

        self._total_executions = total_executions

    @property
    def total_failed_executions(self):
        """Gets the total_failed_executions of this RuleRecommendationSummary.  # noqa: E501


        :return: The total_failed_executions of this RuleRecommendationSummary.  # noqa: E501
        :rtype: int
        """
        return self._total_failed_executions

    @total_failed_executions.setter
    def total_failed_executions(self, total_failed_executions):
        """Sets the total_failed_executions of this RuleRecommendationSummary.


        :param total_failed_executions: The total_failed_executions of this RuleRecommendationSummary.  # noqa: E501
        :type: int
        """

        self._total_failed_executions = total_failed_executions

    @property
    def total_recommendations(self):
        """Gets the total_recommendations of this RuleRecommendationSummary.  # noqa: E501


        :return: The total_recommendations of this RuleRecommendationSummary.  # noqa: E501
        :rtype: int
        """
        return self._total_recommendations

    @total_recommendations.setter
    def total_recommendations(self, total_recommendations):
        """Sets the total_recommendations of this RuleRecommendationSummary.


        :param total_recommendations: The total_recommendations of this RuleRecommendationSummary.  # noqa: E501
        :type: int
        """

        self._total_recommendations = total_recommendations

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
        if issubclass(RuleRecommendationSummary, dict):
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
        if not isinstance(other, RuleRecommendationSummary):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
