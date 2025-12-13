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

class SubRuleExecutionDetails(object):
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
        'action_file_present': 'bool',
        'action_type': 'str',
        'actioned_resource_count': 'int',
        'actioned_resource_file_name': 'str',
        'bq_data_ingestion_status': 'str',
        'cost': 'float',
        'cost_computation_message': 'str',
        'cost_computed': 'bool',
        'error_message': 'str',
        'execution_completed_at': 'int',
        'execution_log_bucket_type': 'str',
        'execution_log_path': 'str',
        'execution_status': 'str',
        'execution_type': 'str',
        'is_cost_breakdown_generated': 'bool',
        'policy_name': 'str',
        'resource_breakdown_list': 'list[ResourceBreakdown]',
        'resource_count': 'int',
        'resource_type': 'str',
        'savings': 'float'
    }

    attribute_map = {
        'action_file_present': 'actionFilePresent',
        'action_type': 'actionType',
        'actioned_resource_count': 'actionedResourceCount',
        'actioned_resource_file_name': 'actionedResourceFileName',
        'bq_data_ingestion_status': 'bqDataIngestionStatus',
        'cost': 'cost',
        'cost_computation_message': 'costComputationMessage',
        'cost_computed': 'costComputed',
        'error_message': 'errorMessage',
        'execution_completed_at': 'executionCompletedAt',
        'execution_log_bucket_type': 'executionLogBucketType',
        'execution_log_path': 'executionLogPath',
        'execution_status': 'executionStatus',
        'execution_type': 'executionType',
        'is_cost_breakdown_generated': 'isCostBreakdownGenerated',
        'policy_name': 'policyName',
        'resource_breakdown_list': 'resourceBreakdownList',
        'resource_count': 'resourceCount',
        'resource_type': 'resourceType',
        'savings': 'savings'
    }

    def __init__(self, action_file_present=None, action_type=None, actioned_resource_count=None, actioned_resource_file_name=None, bq_data_ingestion_status=None, cost=None, cost_computation_message=None, cost_computed=None, error_message=None, execution_completed_at=None, execution_log_bucket_type=None, execution_log_path=None, execution_status=None, execution_type=None, is_cost_breakdown_generated=None, policy_name=None, resource_breakdown_list=None, resource_count=None, resource_type=None, savings=None):  # noqa: E501
        """SubRuleExecutionDetails - a model defined in Swagger"""  # noqa: E501
        self._action_file_present = None
        self._action_type = None
        self._actioned_resource_count = None
        self._actioned_resource_file_name = None
        self._bq_data_ingestion_status = None
        self._cost = None
        self._cost_computation_message = None
        self._cost_computed = None
        self._error_message = None
        self._execution_completed_at = None
        self._execution_log_bucket_type = None
        self._execution_log_path = None
        self._execution_status = None
        self._execution_type = None
        self._is_cost_breakdown_generated = None
        self._policy_name = None
        self._resource_breakdown_list = None
        self._resource_count = None
        self._resource_type = None
        self._savings = None
        self.discriminator = None
        if action_file_present is not None:
            self.action_file_present = action_file_present
        if action_type is not None:
            self.action_type = action_type
        if actioned_resource_count is not None:
            self.actioned_resource_count = actioned_resource_count
        if actioned_resource_file_name is not None:
            self.actioned_resource_file_name = actioned_resource_file_name
        if bq_data_ingestion_status is not None:
            self.bq_data_ingestion_status = bq_data_ingestion_status
        if cost is not None:
            self.cost = cost
        if cost_computation_message is not None:
            self.cost_computation_message = cost_computation_message
        if cost_computed is not None:
            self.cost_computed = cost_computed
        if error_message is not None:
            self.error_message = error_message
        if execution_completed_at is not None:
            self.execution_completed_at = execution_completed_at
        if execution_log_bucket_type is not None:
            self.execution_log_bucket_type = execution_log_bucket_type
        if execution_log_path is not None:
            self.execution_log_path = execution_log_path
        if execution_status is not None:
            self.execution_status = execution_status
        if execution_type is not None:
            self.execution_type = execution_type
        if is_cost_breakdown_generated is not None:
            self.is_cost_breakdown_generated = is_cost_breakdown_generated
        if policy_name is not None:
            self.policy_name = policy_name
        if resource_breakdown_list is not None:
            self.resource_breakdown_list = resource_breakdown_list
        if resource_count is not None:
            self.resource_count = resource_count
        if resource_type is not None:
            self.resource_type = resource_type
        if savings is not None:
            self.savings = savings

    @property
    def action_file_present(self):
        """Gets the action_file_present of this SubRuleExecutionDetails.  # noqa: E501


        :return: The action_file_present of this SubRuleExecutionDetails.  # noqa: E501
        :rtype: bool
        """
        return self._action_file_present

    @action_file_present.setter
    def action_file_present(self, action_file_present):
        """Sets the action_file_present of this SubRuleExecutionDetails.


        :param action_file_present: The action_file_present of this SubRuleExecutionDetails.  # noqa: E501
        :type: bool
        """

        self._action_file_present = action_file_present

    @property
    def action_type(self):
        """Gets the action_type of this SubRuleExecutionDetails.  # noqa: E501


        :return: The action_type of this SubRuleExecutionDetails.  # noqa: E501
        :rtype: str
        """
        return self._action_type

    @action_type.setter
    def action_type(self, action_type):
        """Sets the action_type of this SubRuleExecutionDetails.


        :param action_type: The action_type of this SubRuleExecutionDetails.  # noqa: E501
        :type: str
        """

        self._action_type = action_type

    @property
    def actioned_resource_count(self):
        """Gets the actioned_resource_count of this SubRuleExecutionDetails.  # noqa: E501


        :return: The actioned_resource_count of this SubRuleExecutionDetails.  # noqa: E501
        :rtype: int
        """
        return self._actioned_resource_count

    @actioned_resource_count.setter
    def actioned_resource_count(self, actioned_resource_count):
        """Sets the actioned_resource_count of this SubRuleExecutionDetails.


        :param actioned_resource_count: The actioned_resource_count of this SubRuleExecutionDetails.  # noqa: E501
        :type: int
        """

        self._actioned_resource_count = actioned_resource_count

    @property
    def actioned_resource_file_name(self):
        """Gets the actioned_resource_file_name of this SubRuleExecutionDetails.  # noqa: E501


        :return: The actioned_resource_file_name of this SubRuleExecutionDetails.  # noqa: E501
        :rtype: str
        """
        return self._actioned_resource_file_name

    @actioned_resource_file_name.setter
    def actioned_resource_file_name(self, actioned_resource_file_name):
        """Sets the actioned_resource_file_name of this SubRuleExecutionDetails.


        :param actioned_resource_file_name: The actioned_resource_file_name of this SubRuleExecutionDetails.  # noqa: E501
        :type: str
        """

        self._actioned_resource_file_name = actioned_resource_file_name

    @property
    def bq_data_ingestion_status(self):
        """Gets the bq_data_ingestion_status of this SubRuleExecutionDetails.  # noqa: E501


        :return: The bq_data_ingestion_status of this SubRuleExecutionDetails.  # noqa: E501
        :rtype: str
        """
        return self._bq_data_ingestion_status

    @bq_data_ingestion_status.setter
    def bq_data_ingestion_status(self, bq_data_ingestion_status):
        """Sets the bq_data_ingestion_status of this SubRuleExecutionDetails.


        :param bq_data_ingestion_status: The bq_data_ingestion_status of this SubRuleExecutionDetails.  # noqa: E501
        :type: str
        """
        allowed_values = ["NOT_STARTED", "FAILED", "IN_PROGRESS", "SUCCESSFUL"]  # noqa: E501
        if bq_data_ingestion_status not in allowed_values:
            raise ValueError(
                "Invalid value for `bq_data_ingestion_status` ({0}), must be one of {1}"  # noqa: E501
                .format(bq_data_ingestion_status, allowed_values)
            )

        self._bq_data_ingestion_status = bq_data_ingestion_status

    @property
    def cost(self):
        """Gets the cost of this SubRuleExecutionDetails.  # noqa: E501


        :return: The cost of this SubRuleExecutionDetails.  # noqa: E501
        :rtype: float
        """
        return self._cost

    @cost.setter
    def cost(self, cost):
        """Sets the cost of this SubRuleExecutionDetails.


        :param cost: The cost of this SubRuleExecutionDetails.  # noqa: E501
        :type: float
        """

        self._cost = cost

    @property
    def cost_computation_message(self):
        """Gets the cost_computation_message of this SubRuleExecutionDetails.  # noqa: E501


        :return: The cost_computation_message of this SubRuleExecutionDetails.  # noqa: E501
        :rtype: str
        """
        return self._cost_computation_message

    @cost_computation_message.setter
    def cost_computation_message(self, cost_computation_message):
        """Sets the cost_computation_message of this SubRuleExecutionDetails.


        :param cost_computation_message: The cost_computation_message of this SubRuleExecutionDetails.  # noqa: E501
        :type: str
        """

        self._cost_computation_message = cost_computation_message

    @property
    def cost_computed(self):
        """Gets the cost_computed of this SubRuleExecutionDetails.  # noqa: E501


        :return: The cost_computed of this SubRuleExecutionDetails.  # noqa: E501
        :rtype: bool
        """
        return self._cost_computed

    @cost_computed.setter
    def cost_computed(self, cost_computed):
        """Sets the cost_computed of this SubRuleExecutionDetails.


        :param cost_computed: The cost_computed of this SubRuleExecutionDetails.  # noqa: E501
        :type: bool
        """

        self._cost_computed = cost_computed

    @property
    def error_message(self):
        """Gets the error_message of this SubRuleExecutionDetails.  # noqa: E501


        :return: The error_message of this SubRuleExecutionDetails.  # noqa: E501
        :rtype: str
        """
        return self._error_message

    @error_message.setter
    def error_message(self, error_message):
        """Sets the error_message of this SubRuleExecutionDetails.


        :param error_message: The error_message of this SubRuleExecutionDetails.  # noqa: E501
        :type: str
        """

        self._error_message = error_message

    @property
    def execution_completed_at(self):
        """Gets the execution_completed_at of this SubRuleExecutionDetails.  # noqa: E501


        :return: The execution_completed_at of this SubRuleExecutionDetails.  # noqa: E501
        :rtype: int
        """
        return self._execution_completed_at

    @execution_completed_at.setter
    def execution_completed_at(self, execution_completed_at):
        """Sets the execution_completed_at of this SubRuleExecutionDetails.


        :param execution_completed_at: The execution_completed_at of this SubRuleExecutionDetails.  # noqa: E501
        :type: int
        """

        self._execution_completed_at = execution_completed_at

    @property
    def execution_log_bucket_type(self):
        """Gets the execution_log_bucket_type of this SubRuleExecutionDetails.  # noqa: E501


        :return: The execution_log_bucket_type of this SubRuleExecutionDetails.  # noqa: E501
        :rtype: str
        """
        return self._execution_log_bucket_type

    @execution_log_bucket_type.setter
    def execution_log_bucket_type(self, execution_log_bucket_type):
        """Sets the execution_log_bucket_type of this SubRuleExecutionDetails.


        :param execution_log_bucket_type: The execution_log_bucket_type of this SubRuleExecutionDetails.  # noqa: E501
        :type: str
        """

        self._execution_log_bucket_type = execution_log_bucket_type

    @property
    def execution_log_path(self):
        """Gets the execution_log_path of this SubRuleExecutionDetails.  # noqa: E501


        :return: The execution_log_path of this SubRuleExecutionDetails.  # noqa: E501
        :rtype: str
        """
        return self._execution_log_path

    @execution_log_path.setter
    def execution_log_path(self, execution_log_path):
        """Sets the execution_log_path of this SubRuleExecutionDetails.


        :param execution_log_path: The execution_log_path of this SubRuleExecutionDetails.  # noqa: E501
        :type: str
        """

        self._execution_log_path = execution_log_path

    @property
    def execution_status(self):
        """Gets the execution_status of this SubRuleExecutionDetails.  # noqa: E501


        :return: The execution_status of this SubRuleExecutionDetails.  # noqa: E501
        :rtype: str
        """
        return self._execution_status

    @execution_status.setter
    def execution_status(self, execution_status):
        """Sets the execution_status of this SubRuleExecutionDetails.


        :param execution_status: The execution_status of this SubRuleExecutionDetails.  # noqa: E501
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
    def execution_type(self):
        """Gets the execution_type of this SubRuleExecutionDetails.  # noqa: E501


        :return: The execution_type of this SubRuleExecutionDetails.  # noqa: E501
        :rtype: str
        """
        return self._execution_type

    @execution_type.setter
    def execution_type(self, execution_type):
        """Sets the execution_type of this SubRuleExecutionDetails.


        :param execution_type: The execution_type of this SubRuleExecutionDetails.  # noqa: E501
        :type: str
        """
        allowed_values = ["INTERNAL", "EXTERNAL"]  # noqa: E501
        if execution_type not in allowed_values:
            raise ValueError(
                "Invalid value for `execution_type` ({0}), must be one of {1}"  # noqa: E501
                .format(execution_type, allowed_values)
            )

        self._execution_type = execution_type

    @property
    def is_cost_breakdown_generated(self):
        """Gets the is_cost_breakdown_generated of this SubRuleExecutionDetails.  # noqa: E501


        :return: The is_cost_breakdown_generated of this SubRuleExecutionDetails.  # noqa: E501
        :rtype: bool
        """
        return self._is_cost_breakdown_generated

    @is_cost_breakdown_generated.setter
    def is_cost_breakdown_generated(self, is_cost_breakdown_generated):
        """Sets the is_cost_breakdown_generated of this SubRuleExecutionDetails.


        :param is_cost_breakdown_generated: The is_cost_breakdown_generated of this SubRuleExecutionDetails.  # noqa: E501
        :type: bool
        """

        self._is_cost_breakdown_generated = is_cost_breakdown_generated

    @property
    def policy_name(self):
        """Gets the policy_name of this SubRuleExecutionDetails.  # noqa: E501


        :return: The policy_name of this SubRuleExecutionDetails.  # noqa: E501
        :rtype: str
        """
        return self._policy_name

    @policy_name.setter
    def policy_name(self, policy_name):
        """Sets the policy_name of this SubRuleExecutionDetails.


        :param policy_name: The policy_name of this SubRuleExecutionDetails.  # noqa: E501
        :type: str
        """

        self._policy_name = policy_name

    @property
    def resource_breakdown_list(self):
        """Gets the resource_breakdown_list of this SubRuleExecutionDetails.  # noqa: E501


        :return: The resource_breakdown_list of this SubRuleExecutionDetails.  # noqa: E501
        :rtype: list[ResourceBreakdown]
        """
        return self._resource_breakdown_list

    @resource_breakdown_list.setter
    def resource_breakdown_list(self, resource_breakdown_list):
        """Sets the resource_breakdown_list of this SubRuleExecutionDetails.


        :param resource_breakdown_list: The resource_breakdown_list of this SubRuleExecutionDetails.  # noqa: E501
        :type: list[ResourceBreakdown]
        """

        self._resource_breakdown_list = resource_breakdown_list

    @property
    def resource_count(self):
        """Gets the resource_count of this SubRuleExecutionDetails.  # noqa: E501


        :return: The resource_count of this SubRuleExecutionDetails.  # noqa: E501
        :rtype: int
        """
        return self._resource_count

    @resource_count.setter
    def resource_count(self, resource_count):
        """Sets the resource_count of this SubRuleExecutionDetails.


        :param resource_count: The resource_count of this SubRuleExecutionDetails.  # noqa: E501
        :type: int
        """

        self._resource_count = resource_count

    @property
    def resource_type(self):
        """Gets the resource_type of this SubRuleExecutionDetails.  # noqa: E501


        :return: The resource_type of this SubRuleExecutionDetails.  # noqa: E501
        :rtype: str
        """
        return self._resource_type

    @resource_type.setter
    def resource_type(self, resource_type):
        """Sets the resource_type of this SubRuleExecutionDetails.


        :param resource_type: The resource_type of this SubRuleExecutionDetails.  # noqa: E501
        :type: str
        """

        self._resource_type = resource_type

    @property
    def savings(self):
        """Gets the savings of this SubRuleExecutionDetails.  # noqa: E501


        :return: The savings of this SubRuleExecutionDetails.  # noqa: E501
        :rtype: float
        """
        return self._savings

    @savings.setter
    def savings(self, savings):
        """Sets the savings of this SubRuleExecutionDetails.


        :param savings: The savings of this SubRuleExecutionDetails.  # noqa: E501
        :type: float
        """

        self._savings = savings

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
        if issubclass(SubRuleExecutionDetails, dict):
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
        if not isinstance(other, SubRuleExecutionDetails):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
