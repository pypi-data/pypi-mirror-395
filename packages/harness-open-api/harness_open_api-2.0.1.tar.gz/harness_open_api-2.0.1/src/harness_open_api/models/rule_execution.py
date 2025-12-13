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

class RuleExecution(object):
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
        'ootb': 'bool',
        'account_id': 'str',
        'action_file_present': 'bool',
        'action_type': 'str',
        'actioned_resource_count': 'int',
        'actioned_resource_file_name': 'str',
        'bq_data_ingestion_status': 'str',
        'cloud_provider': 'str',
        'cost': 'float',
        'cost_computation_message': 'str',
        'cost_computed': 'bool',
        'cost_type': 'str',
        'created_at': 'int',
        'error_message': 'str',
        'execution_completed_at': 'int',
        'execution_log_bucket_type': 'str',
        'execution_log_path': 'str',
        'execution_status': 'str',
        'execution_type': 'str',
        'is_cost_breakdown_generated': 'bool',
        'is_dry_run': 'bool',
        'is_multi_policy_rule': 'bool',
        'job_id': 'str',
        'last_updated_at': 'int',
        'ootb': 'bool',
        'org_identifier': 'str',
        'project_identifier': 'str',
        'resource_breakdown_list': 'list[ResourceBreakdown]',
        'resource_count': 'int',
        'resource_type': 'str',
        'rule_enforcement_identifier': 'str',
        'rule_enforcement_name': 'str',
        'rule_enforcement_recommendation_identifier': 'str',
        'rule_enforcement_recommendation_name': 'str',
        'rule_identifier': 'str',
        'rule_name': 'str',
        'rule_pack_identifier': 'str',
        'savings': 'float',
        'sub_rule_execution_details': 'list[SubRuleExecutionDetails]',
        'target_account': 'str',
        'target_account_name': 'str',
        'target_regions': 'list[str]',
        'ttl': 'datetime',
        'uuid': 'str'
    }

    attribute_map = {
        'ootb': 'OOTB',
        'account_id': 'accountId',
        'action_file_present': 'actionFilePresent',
        'action_type': 'actionType',
        'actioned_resource_count': 'actionedResourceCount',
        'actioned_resource_file_name': 'actionedResourceFileName',
        'bq_data_ingestion_status': 'bqDataIngestionStatus',
        'cloud_provider': 'cloudProvider',
        'cost': 'cost',
        'cost_computation_message': 'costComputationMessage',
        'cost_computed': 'costComputed',
        'cost_type': 'costType',
        'created_at': 'createdAt',
        'error_message': 'errorMessage',
        'execution_completed_at': 'executionCompletedAt',
        'execution_log_bucket_type': 'executionLogBucketType',
        'execution_log_path': 'executionLogPath',
        'execution_status': 'executionStatus',
        'execution_type': 'executionType',
        'is_cost_breakdown_generated': 'isCostBreakdownGenerated',
        'is_dry_run': 'isDryRun',
        'is_multi_policy_rule': 'isMultiPolicyRule',
        'job_id': 'jobId',
        'last_updated_at': 'lastUpdatedAt',
        'ootb': 'ootb',
        'org_identifier': 'orgIdentifier',
        'project_identifier': 'projectIdentifier',
        'resource_breakdown_list': 'resourceBreakdownList',
        'resource_count': 'resourceCount',
        'resource_type': 'resourceType',
        'rule_enforcement_identifier': 'ruleEnforcementIdentifier',
        'rule_enforcement_name': 'ruleEnforcementName',
        'rule_enforcement_recommendation_identifier': 'ruleEnforcementRecommendationIdentifier',
        'rule_enforcement_recommendation_name': 'ruleEnforcementRecommendationName',
        'rule_identifier': 'ruleIdentifier',
        'rule_name': 'ruleName',
        'rule_pack_identifier': 'rulePackIdentifier',
        'savings': 'savings',
        'sub_rule_execution_details': 'subRuleExecutionDetails',
        'target_account': 'targetAccount',
        'target_account_name': 'targetAccountName',
        'target_regions': 'targetRegions',
        'ttl': 'ttl',
        'uuid': 'uuid'
    }

    def __init__(self, account_id=None, action_file_present=None, action_type=None, actioned_resource_count=None, actioned_resource_file_name=None, bq_data_ingestion_status=None, cloud_provider=None, cost=None, cost_computation_message=None, cost_computed=None, cost_type=None, created_at=None, error_message=None, execution_completed_at=None, execution_log_bucket_type=None, execution_log_path=None, execution_status=None, execution_type=None, is_cost_breakdown_generated=None, is_dry_run=None, is_multi_policy_rule=False, job_id=None, last_updated_at=None, ootb=None, org_identifier=None, project_identifier=None, resource_breakdown_list=None, resource_count=None, resource_type=None, rule_enforcement_identifier=None, rule_enforcement_name=None, rule_enforcement_recommendation_identifier=None, rule_enforcement_recommendation_name=None, rule_identifier=None, rule_name=None, rule_pack_identifier=None, savings=None, sub_rule_execution_details=None, target_account=None, target_account_name=None, target_regions=None, ttl=None, uuid=None):  # noqa: E501
        """RuleExecution - a model defined in Swagger"""  # noqa: E501
        self._account_id = None
        self._action_file_present = None
        self._action_type = None
        self._actioned_resource_count = None
        self._actioned_resource_file_name = None
        self._bq_data_ingestion_status = None
        self._cloud_provider = None
        self._cost = None
        self._cost_computation_message = None
        self._cost_computed = None
        self._cost_type = None
        self._created_at = None
        self._error_message = None
        self._execution_completed_at = None
        self._execution_log_bucket_type = None
        self._execution_log_path = None
        self._execution_status = None
        self._execution_type = None
        self._is_cost_breakdown_generated = None
        self._is_dry_run = None
        self._is_multi_policy_rule = None
        self._job_id = None
        self._last_updated_at = None
        self._ootb = None
        self._org_identifier = None
        self._project_identifier = None
        self._resource_breakdown_list = None
        self._resource_count = None
        self._resource_type = None
        self._rule_enforcement_identifier = None
        self._rule_enforcement_name = None
        self._rule_enforcement_recommendation_identifier = None
        self._rule_enforcement_recommendation_name = None
        self._rule_identifier = None
        self._rule_name = None
        self._rule_pack_identifier = None
        self._savings = None
        self._sub_rule_execution_details = None
        self._target_account = None
        self._target_account_name = None
        self._target_regions = None
        self._ttl = None
        self._uuid = None
        self.discriminator = None
        if ootb is not None:
            self.ootb = ootb
        if account_id is not None:
            self.account_id = account_id
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
        if cloud_provider is not None:
            self.cloud_provider = cloud_provider
        if cost is not None:
            self.cost = cost
        if cost_computation_message is not None:
            self.cost_computation_message = cost_computation_message
        if cost_computed is not None:
            self.cost_computed = cost_computed
        if cost_type is not None:
            self.cost_type = cost_type
        if created_at is not None:
            self.created_at = created_at
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
        if is_dry_run is not None:
            self.is_dry_run = is_dry_run
        if is_multi_policy_rule is not None:
            self.is_multi_policy_rule = is_multi_policy_rule
        if job_id is not None:
            self.job_id = job_id
        if last_updated_at is not None:
            self.last_updated_at = last_updated_at
        if ootb is not None:
            self.ootb = ootb
        if org_identifier is not None:
            self.org_identifier = org_identifier
        if project_identifier is not None:
            self.project_identifier = project_identifier
        if resource_breakdown_list is not None:
            self.resource_breakdown_list = resource_breakdown_list
        if resource_count is not None:
            self.resource_count = resource_count
        if resource_type is not None:
            self.resource_type = resource_type
        if rule_enforcement_identifier is not None:
            self.rule_enforcement_identifier = rule_enforcement_identifier
        if rule_enforcement_name is not None:
            self.rule_enforcement_name = rule_enforcement_name
        if rule_enforcement_recommendation_identifier is not None:
            self.rule_enforcement_recommendation_identifier = rule_enforcement_recommendation_identifier
        if rule_enforcement_recommendation_name is not None:
            self.rule_enforcement_recommendation_name = rule_enforcement_recommendation_name
        if rule_identifier is not None:
            self.rule_identifier = rule_identifier
        if rule_name is not None:
            self.rule_name = rule_name
        if rule_pack_identifier is not None:
            self.rule_pack_identifier = rule_pack_identifier
        if savings is not None:
            self.savings = savings
        if sub_rule_execution_details is not None:
            self.sub_rule_execution_details = sub_rule_execution_details
        if target_account is not None:
            self.target_account = target_account
        if target_account_name is not None:
            self.target_account_name = target_account_name
        if target_regions is not None:
            self.target_regions = target_regions
        if ttl is not None:
            self.ttl = ttl
        if uuid is not None:
            self.uuid = uuid

    @property
    def ootb(self):
        """Gets the ootb of this RuleExecution.  # noqa: E501


        :return: The ootb of this RuleExecution.  # noqa: E501
        :rtype: bool
        """
        return self._ootb

    @ootb.setter
    def ootb(self, ootb):
        """Sets the ootb of this RuleExecution.


        :param ootb: The ootb of this RuleExecution.  # noqa: E501
        :type: bool
        """

        self._ootb = ootb

    @property
    def account_id(self):
        """Gets the account_id of this RuleExecution.  # noqa: E501

        account id  # noqa: E501

        :return: The account_id of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """Sets the account_id of this RuleExecution.

        account id  # noqa: E501

        :param account_id: The account_id of this RuleExecution.  # noqa: E501
        :type: str
        """

        self._account_id = account_id

    @property
    def action_file_present(self):
        """Gets the action_file_present of this RuleExecution.  # noqa: E501

        actionFilePresent  # noqa: E501

        :return: The action_file_present of this RuleExecution.  # noqa: E501
        :rtype: bool
        """
        return self._action_file_present

    @action_file_present.setter
    def action_file_present(self, action_file_present):
        """Sets the action_file_present of this RuleExecution.

        actionFilePresent  # noqa: E501

        :param action_file_present: The action_file_present of this RuleExecution.  # noqa: E501
        :type: bool
        """

        self._action_file_present = action_file_present

    @property
    def action_type(self):
        """Gets the action_type of this RuleExecution.  # noqa: E501

        actionType  # noqa: E501

        :return: The action_type of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._action_type

    @action_type.setter
    def action_type(self, action_type):
        """Sets the action_type of this RuleExecution.

        actionType  # noqa: E501

        :param action_type: The action_type of this RuleExecution.  # noqa: E501
        :type: str
        """

        self._action_type = action_type

    @property
    def actioned_resource_count(self):
        """Gets the actioned_resource_count of this RuleExecution.  # noqa: E501

        actionedResourceCount  # noqa: E501

        :return: The actioned_resource_count of this RuleExecution.  # noqa: E501
        :rtype: int
        """
        return self._actioned_resource_count

    @actioned_resource_count.setter
    def actioned_resource_count(self, actioned_resource_count):
        """Sets the actioned_resource_count of this RuleExecution.

        actionedResourceCount  # noqa: E501

        :param actioned_resource_count: The actioned_resource_count of this RuleExecution.  # noqa: E501
        :type: int
        """

        self._actioned_resource_count = actioned_resource_count

    @property
    def actioned_resource_file_name(self):
        """Gets the actioned_resource_file_name of this RuleExecution.  # noqa: E501

        actionedResourceFileName  # noqa: E501

        :return: The actioned_resource_file_name of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._actioned_resource_file_name

    @actioned_resource_file_name.setter
    def actioned_resource_file_name(self, actioned_resource_file_name):
        """Sets the actioned_resource_file_name of this RuleExecution.

        actionedResourceFileName  # noqa: E501

        :param actioned_resource_file_name: The actioned_resource_file_name of this RuleExecution.  # noqa: E501
        :type: str
        """

        self._actioned_resource_file_name = actioned_resource_file_name

    @property
    def bq_data_ingestion_status(self):
        """Gets the bq_data_ingestion_status of this RuleExecution.  # noqa: E501

        bqDataIngestionStatus  # noqa: E501

        :return: The bq_data_ingestion_status of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._bq_data_ingestion_status

    @bq_data_ingestion_status.setter
    def bq_data_ingestion_status(self, bq_data_ingestion_status):
        """Sets the bq_data_ingestion_status of this RuleExecution.

        bqDataIngestionStatus  # noqa: E501

        :param bq_data_ingestion_status: The bq_data_ingestion_status of this RuleExecution.  # noqa: E501
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
    def cloud_provider(self):
        """Gets the cloud_provider of this RuleExecution.  # noqa: E501

        cloudProvider  # noqa: E501

        :return: The cloud_provider of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._cloud_provider

    @cloud_provider.setter
    def cloud_provider(self, cloud_provider):
        """Sets the cloud_provider of this RuleExecution.

        cloudProvider  # noqa: E501

        :param cloud_provider: The cloud_provider of this RuleExecution.  # noqa: E501
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
    def cost(self):
        """Gets the cost of this RuleExecution.  # noqa: E501

        cost  # noqa: E501

        :return: The cost of this RuleExecution.  # noqa: E501
        :rtype: float
        """
        return self._cost

    @cost.setter
    def cost(self, cost):
        """Sets the cost of this RuleExecution.

        cost  # noqa: E501

        :param cost: The cost of this RuleExecution.  # noqa: E501
        :type: float
        """

        self._cost = cost

    @property
    def cost_computation_message(self):
        """Gets the cost_computation_message of this RuleExecution.  # noqa: E501

        costComputationMessage  # noqa: E501

        :return: The cost_computation_message of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._cost_computation_message

    @cost_computation_message.setter
    def cost_computation_message(self, cost_computation_message):
        """Sets the cost_computation_message of this RuleExecution.

        costComputationMessage  # noqa: E501

        :param cost_computation_message: The cost_computation_message of this RuleExecution.  # noqa: E501
        :type: str
        """

        self._cost_computation_message = cost_computation_message

    @property
    def cost_computed(self):
        """Gets the cost_computed of this RuleExecution.  # noqa: E501

        costComputed  # noqa: E501

        :return: The cost_computed of this RuleExecution.  # noqa: E501
        :rtype: bool
        """
        return self._cost_computed

    @cost_computed.setter
    def cost_computed(self, cost_computed):
        """Sets the cost_computed of this RuleExecution.

        costComputed  # noqa: E501

        :param cost_computed: The cost_computed of this RuleExecution.  # noqa: E501
        :type: bool
        """

        self._cost_computed = cost_computed

    @property
    def cost_type(self):
        """Gets the cost_type of this RuleExecution.  # noqa: E501

        costType  # noqa: E501

        :return: The cost_type of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._cost_type

    @cost_type.setter
    def cost_type(self, cost_type):
        """Sets the cost_type of this RuleExecution.

        costType  # noqa: E501

        :param cost_type: The cost_type of this RuleExecution.  # noqa: E501
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
    def created_at(self):
        """Gets the created_at of this RuleExecution.  # noqa: E501

        Time at which the entity was created  # noqa: E501

        :return: The created_at of this RuleExecution.  # noqa: E501
        :rtype: int
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this RuleExecution.

        Time at which the entity was created  # noqa: E501

        :param created_at: The created_at of this RuleExecution.  # noqa: E501
        :type: int
        """

        self._created_at = created_at

    @property
    def error_message(self):
        """Gets the error_message of this RuleExecution.  # noqa: E501

        error generated by custodian  # noqa: E501

        :return: The error_message of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._error_message

    @error_message.setter
    def error_message(self, error_message):
        """Sets the error_message of this RuleExecution.

        error generated by custodian  # noqa: E501

        :param error_message: The error_message of this RuleExecution.  # noqa: E501
        :type: str
        """

        self._error_message = error_message

    @property
    def execution_completed_at(self):
        """Gets the execution_completed_at of this RuleExecution.  # noqa: E501

        executionCompletedAt  # noqa: E501

        :return: The execution_completed_at of this RuleExecution.  # noqa: E501
        :rtype: int
        """
        return self._execution_completed_at

    @execution_completed_at.setter
    def execution_completed_at(self, execution_completed_at):
        """Sets the execution_completed_at of this RuleExecution.

        executionCompletedAt  # noqa: E501

        :param execution_completed_at: The execution_completed_at of this RuleExecution.  # noqa: E501
        :type: int
        """

        self._execution_completed_at = execution_completed_at

    @property
    def execution_log_bucket_type(self):
        """Gets the execution_log_bucket_type of this RuleExecution.  # noqa: E501

        executionLogBucketType  # noqa: E501

        :return: The execution_log_bucket_type of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._execution_log_bucket_type

    @execution_log_bucket_type.setter
    def execution_log_bucket_type(self, execution_log_bucket_type):
        """Sets the execution_log_bucket_type of this RuleExecution.

        executionLogBucketType  # noqa: E501

        :param execution_log_bucket_type: The execution_log_bucket_type of this RuleExecution.  # noqa: E501
        :type: str
        """

        self._execution_log_bucket_type = execution_log_bucket_type

    @property
    def execution_log_path(self):
        """Gets the execution_log_path of this RuleExecution.  # noqa: E501

        executionLogPath  # noqa: E501

        :return: The execution_log_path of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._execution_log_path

    @execution_log_path.setter
    def execution_log_path(self, execution_log_path):
        """Sets the execution_log_path of this RuleExecution.

        executionLogPath  # noqa: E501

        :param execution_log_path: The execution_log_path of this RuleExecution.  # noqa: E501
        :type: str
        """

        self._execution_log_path = execution_log_path

    @property
    def execution_status(self):
        """Gets the execution_status of this RuleExecution.  # noqa: E501

        executionStatus  # noqa: E501

        :return: The execution_status of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._execution_status

    @execution_status.setter
    def execution_status(self, execution_status):
        """Sets the execution_status of this RuleExecution.

        executionStatus  # noqa: E501

        :param execution_status: The execution_status of this RuleExecution.  # noqa: E501
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
        """Gets the execution_type of this RuleExecution.  # noqa: E501

        executionType  # noqa: E501

        :return: The execution_type of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._execution_type

    @execution_type.setter
    def execution_type(self, execution_type):
        """Sets the execution_type of this RuleExecution.

        executionType  # noqa: E501

        :param execution_type: The execution_type of this RuleExecution.  # noqa: E501
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
        """Gets the is_cost_breakdown_generated of this RuleExecution.  # noqa: E501

        isCostBreakdownGenerated  # noqa: E501

        :return: The is_cost_breakdown_generated of this RuleExecution.  # noqa: E501
        :rtype: bool
        """
        return self._is_cost_breakdown_generated

    @is_cost_breakdown_generated.setter
    def is_cost_breakdown_generated(self, is_cost_breakdown_generated):
        """Sets the is_cost_breakdown_generated of this RuleExecution.

        isCostBreakdownGenerated  # noqa: E501

        :param is_cost_breakdown_generated: The is_cost_breakdown_generated of this RuleExecution.  # noqa: E501
        :type: bool
        """

        self._is_cost_breakdown_generated = is_cost_breakdown_generated

    @property
    def is_dry_run(self):
        """Gets the is_dry_run of this RuleExecution.  # noqa: E501

        isDryRun  # noqa: E501

        :return: The is_dry_run of this RuleExecution.  # noqa: E501
        :rtype: bool
        """
        return self._is_dry_run

    @is_dry_run.setter
    def is_dry_run(self, is_dry_run):
        """Sets the is_dry_run of this RuleExecution.

        isDryRun  # noqa: E501

        :param is_dry_run: The is_dry_run of this RuleExecution.  # noqa: E501
        :type: bool
        """

        self._is_dry_run = is_dry_run

    @property
    def is_multi_policy_rule(self):
        """Gets the is_multi_policy_rule of this RuleExecution.  # noqa: E501

        isMultiPolicyRule  # noqa: E501

        :return: The is_multi_policy_rule of this RuleExecution.  # noqa: E501
        :rtype: bool
        """
        return self._is_multi_policy_rule

    @is_multi_policy_rule.setter
    def is_multi_policy_rule(self, is_multi_policy_rule):
        """Sets the is_multi_policy_rule of this RuleExecution.

        isMultiPolicyRule  # noqa: E501

        :param is_multi_policy_rule: The is_multi_policy_rule of this RuleExecution.  # noqa: E501
        :type: bool
        """

        self._is_multi_policy_rule = is_multi_policy_rule

    @property
    def job_id(self):
        """Gets the job_id of this RuleExecution.  # noqa: E501

        faktory job id  # noqa: E501

        :return: The job_id of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._job_id

    @job_id.setter
    def job_id(self, job_id):
        """Sets the job_id of this RuleExecution.

        faktory job id  # noqa: E501

        :param job_id: The job_id of this RuleExecution.  # noqa: E501
        :type: str
        """

        self._job_id = job_id

    @property
    def last_updated_at(self):
        """Gets the last_updated_at of this RuleExecution.  # noqa: E501

        Time at which the entity was last updated  # noqa: E501

        :return: The last_updated_at of this RuleExecution.  # noqa: E501
        :rtype: int
        """
        return self._last_updated_at

    @last_updated_at.setter
    def last_updated_at(self, last_updated_at):
        """Sets the last_updated_at of this RuleExecution.

        Time at which the entity was last updated  # noqa: E501

        :param last_updated_at: The last_updated_at of this RuleExecution.  # noqa: E501
        :type: int
        """

        self._last_updated_at = last_updated_at

    @property
    def ootb(self):
        """Gets the ootb of this RuleExecution.  # noqa: E501


        :return: The ootb of this RuleExecution.  # noqa: E501
        :rtype: bool
        """
        return self._ootb

    @ootb.setter
    def ootb(self, ootb):
        """Sets the ootb of this RuleExecution.


        :param ootb: The ootb of this RuleExecution.  # noqa: E501
        :type: bool
        """

        self._ootb = ootb

    @property
    def org_identifier(self):
        """Gets the org_identifier of this RuleExecution.  # noqa: E501

        Organization Identifier for the Entity.  # noqa: E501

        :return: The org_identifier of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._org_identifier

    @org_identifier.setter
    def org_identifier(self, org_identifier):
        """Sets the org_identifier of this RuleExecution.

        Organization Identifier for the Entity.  # noqa: E501

        :param org_identifier: The org_identifier of this RuleExecution.  # noqa: E501
        :type: str
        """

        self._org_identifier = org_identifier

    @property
    def project_identifier(self):
        """Gets the project_identifier of this RuleExecution.  # noqa: E501

        Project Identifier for the Entity.  # noqa: E501

        :return: The project_identifier of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._project_identifier

    @project_identifier.setter
    def project_identifier(self, project_identifier):
        """Sets the project_identifier of this RuleExecution.

        Project Identifier for the Entity.  # noqa: E501

        :param project_identifier: The project_identifier of this RuleExecution.  # noqa: E501
        :type: str
        """

        self._project_identifier = project_identifier

    @property
    def resource_breakdown_list(self):
        """Gets the resource_breakdown_list of this RuleExecution.  # noqa: E501

        resourceBreakdownList  # noqa: E501

        :return: The resource_breakdown_list of this RuleExecution.  # noqa: E501
        :rtype: list[ResourceBreakdown]
        """
        return self._resource_breakdown_list

    @resource_breakdown_list.setter
    def resource_breakdown_list(self, resource_breakdown_list):
        """Sets the resource_breakdown_list of this RuleExecution.

        resourceBreakdownList  # noqa: E501

        :param resource_breakdown_list: The resource_breakdown_list of this RuleExecution.  # noqa: E501
        :type: list[ResourceBreakdown]
        """

        self._resource_breakdown_list = resource_breakdown_list

    @property
    def resource_count(self):
        """Gets the resource_count of this RuleExecution.  # noqa: E501

        resourceCount  # noqa: E501

        :return: The resource_count of this RuleExecution.  # noqa: E501
        :rtype: int
        """
        return self._resource_count

    @resource_count.setter
    def resource_count(self, resource_count):
        """Sets the resource_count of this RuleExecution.

        resourceCount  # noqa: E501

        :param resource_count: The resource_count of this RuleExecution.  # noqa: E501
        :type: int
        """

        self._resource_count = resource_count

    @property
    def resource_type(self):
        """Gets the resource_type of this RuleExecution.  # noqa: E501

        resourceType  # noqa: E501

        :return: The resource_type of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._resource_type

    @resource_type.setter
    def resource_type(self, resource_type):
        """Sets the resource_type of this RuleExecution.

        resourceType  # noqa: E501

        :param resource_type: The resource_type of this RuleExecution.  # noqa: E501
        :type: str
        """

        self._resource_type = resource_type

    @property
    def rule_enforcement_identifier(self):
        """Gets the rule_enforcement_identifier of this RuleExecution.  # noqa: E501

        ruleEnforcementIdentifier  # noqa: E501

        :return: The rule_enforcement_identifier of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._rule_enforcement_identifier

    @rule_enforcement_identifier.setter
    def rule_enforcement_identifier(self, rule_enforcement_identifier):
        """Sets the rule_enforcement_identifier of this RuleExecution.

        ruleEnforcementIdentifier  # noqa: E501

        :param rule_enforcement_identifier: The rule_enforcement_identifier of this RuleExecution.  # noqa: E501
        :type: str
        """

        self._rule_enforcement_identifier = rule_enforcement_identifier

    @property
    def rule_enforcement_name(self):
        """Gets the rule_enforcement_name of this RuleExecution.  # noqa: E501

        ruleEnforcementName  # noqa: E501

        :return: The rule_enforcement_name of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._rule_enforcement_name

    @rule_enforcement_name.setter
    def rule_enforcement_name(self, rule_enforcement_name):
        """Sets the rule_enforcement_name of this RuleExecution.

        ruleEnforcementName  # noqa: E501

        :param rule_enforcement_name: The rule_enforcement_name of this RuleExecution.  # noqa: E501
        :type: str
        """

        self._rule_enforcement_name = rule_enforcement_name

    @property
    def rule_enforcement_recommendation_identifier(self):
        """Gets the rule_enforcement_recommendation_identifier of this RuleExecution.  # noqa: E501

        ruleEnforcementRecommendationIdentifier  # noqa: E501

        :return: The rule_enforcement_recommendation_identifier of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._rule_enforcement_recommendation_identifier

    @rule_enforcement_recommendation_identifier.setter
    def rule_enforcement_recommendation_identifier(self, rule_enforcement_recommendation_identifier):
        """Sets the rule_enforcement_recommendation_identifier of this RuleExecution.

        ruleEnforcementRecommendationIdentifier  # noqa: E501

        :param rule_enforcement_recommendation_identifier: The rule_enforcement_recommendation_identifier of this RuleExecution.  # noqa: E501
        :type: str
        """

        self._rule_enforcement_recommendation_identifier = rule_enforcement_recommendation_identifier

    @property
    def rule_enforcement_recommendation_name(self):
        """Gets the rule_enforcement_recommendation_name of this RuleExecution.  # noqa: E501

        ruleEnforcementRecommendationName  # noqa: E501

        :return: The rule_enforcement_recommendation_name of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._rule_enforcement_recommendation_name

    @rule_enforcement_recommendation_name.setter
    def rule_enforcement_recommendation_name(self, rule_enforcement_recommendation_name):
        """Sets the rule_enforcement_recommendation_name of this RuleExecution.

        ruleEnforcementRecommendationName  # noqa: E501

        :param rule_enforcement_recommendation_name: The rule_enforcement_recommendation_name of this RuleExecution.  # noqa: E501
        :type: str
        """

        self._rule_enforcement_recommendation_name = rule_enforcement_recommendation_name

    @property
    def rule_identifier(self):
        """Gets the rule_identifier of this RuleExecution.  # noqa: E501

        ruleIdentifier  # noqa: E501

        :return: The rule_identifier of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._rule_identifier

    @rule_identifier.setter
    def rule_identifier(self, rule_identifier):
        """Sets the rule_identifier of this RuleExecution.

        ruleIdentifier  # noqa: E501

        :param rule_identifier: The rule_identifier of this RuleExecution.  # noqa: E501
        :type: str
        """

        self._rule_identifier = rule_identifier

    @property
    def rule_name(self):
        """Gets the rule_name of this RuleExecution.  # noqa: E501

        ruleName  # noqa: E501

        :return: The rule_name of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._rule_name

    @rule_name.setter
    def rule_name(self, rule_name):
        """Sets the rule_name of this RuleExecution.

        ruleName  # noqa: E501

        :param rule_name: The rule_name of this RuleExecution.  # noqa: E501
        :type: str
        """

        self._rule_name = rule_name

    @property
    def rule_pack_identifier(self):
        """Gets the rule_pack_identifier of this RuleExecution.  # noqa: E501

        rulePackIdentifier  # noqa: E501

        :return: The rule_pack_identifier of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._rule_pack_identifier

    @rule_pack_identifier.setter
    def rule_pack_identifier(self, rule_pack_identifier):
        """Sets the rule_pack_identifier of this RuleExecution.

        rulePackIdentifier  # noqa: E501

        :param rule_pack_identifier: The rule_pack_identifier of this RuleExecution.  # noqa: E501
        :type: str
        """

        self._rule_pack_identifier = rule_pack_identifier

    @property
    def savings(self):
        """Gets the savings of this RuleExecution.  # noqa: E501

        savings  # noqa: E501

        :return: The savings of this RuleExecution.  # noqa: E501
        :rtype: float
        """
        return self._savings

    @savings.setter
    def savings(self, savings):
        """Sets the savings of this RuleExecution.

        savings  # noqa: E501

        :param savings: The savings of this RuleExecution.  # noqa: E501
        :type: float
        """

        self._savings = savings

    @property
    def sub_rule_execution_details(self):
        """Gets the sub_rule_execution_details of this RuleExecution.  # noqa: E501

        subRuleExecutionDetails  # noqa: E501

        :return: The sub_rule_execution_details of this RuleExecution.  # noqa: E501
        :rtype: list[SubRuleExecutionDetails]
        """
        return self._sub_rule_execution_details

    @sub_rule_execution_details.setter
    def sub_rule_execution_details(self, sub_rule_execution_details):
        """Sets the sub_rule_execution_details of this RuleExecution.

        subRuleExecutionDetails  # noqa: E501

        :param sub_rule_execution_details: The sub_rule_execution_details of this RuleExecution.  # noqa: E501
        :type: list[SubRuleExecutionDetails]
        """

        self._sub_rule_execution_details = sub_rule_execution_details

    @property
    def target_account(self):
        """Gets the target_account of this RuleExecution.  # noqa: E501

        targetAccount  # noqa: E501

        :return: The target_account of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._target_account

    @target_account.setter
    def target_account(self, target_account):
        """Sets the target_account of this RuleExecution.

        targetAccount  # noqa: E501

        :param target_account: The target_account of this RuleExecution.  # noqa: E501
        :type: str
        """

        self._target_account = target_account

    @property
    def target_account_name(self):
        """Gets the target_account_name of this RuleExecution.  # noqa: E501

        targetAccountName  # noqa: E501

        :return: The target_account_name of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._target_account_name

    @target_account_name.setter
    def target_account_name(self, target_account_name):
        """Sets the target_account_name of this RuleExecution.

        targetAccountName  # noqa: E501

        :param target_account_name: The target_account_name of this RuleExecution.  # noqa: E501
        :type: str
        """

        self._target_account_name = target_account_name

    @property
    def target_regions(self):
        """Gets the target_regions of this RuleExecution.  # noqa: E501

        targetRegions  # noqa: E501

        :return: The target_regions of this RuleExecution.  # noqa: E501
        :rtype: list[str]
        """
        return self._target_regions

    @target_regions.setter
    def target_regions(self, target_regions):
        """Sets the target_regions of this RuleExecution.

        targetRegions  # noqa: E501

        :param target_regions: The target_regions of this RuleExecution.  # noqa: E501
        :type: list[str]
        """

        self._target_regions = target_regions

    @property
    def ttl(self):
        """Gets the ttl of this RuleExecution.  # noqa: E501


        :return: The ttl of this RuleExecution.  # noqa: E501
        :rtype: datetime
        """
        return self._ttl

    @ttl.setter
    def ttl(self, ttl):
        """Sets the ttl of this RuleExecution.


        :param ttl: The ttl of this RuleExecution.  # noqa: E501
        :type: datetime
        """

        self._ttl = ttl

    @property
    def uuid(self):
        """Gets the uuid of this RuleExecution.  # noqa: E501

        unique id  # noqa: E501

        :return: The uuid of this RuleExecution.  # noqa: E501
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the uuid of this RuleExecution.

        unique id  # noqa: E501

        :param uuid: The uuid of this RuleExecution.  # noqa: E501
        :type: str
        """

        self._uuid = uuid

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
        if issubclass(RuleExecution, dict):
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
        if not isinstance(other, RuleExecution):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
