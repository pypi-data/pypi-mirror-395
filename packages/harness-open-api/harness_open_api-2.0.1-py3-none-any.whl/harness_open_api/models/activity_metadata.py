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

class ActivityMetadata(object):
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
        'planned_changes_count': 'int',
        'activity_status': 'str',
        'activity_type': 'str',
        'cost_breakdown_uuid': 'str',
        'cost_currency': 'str',
        'cost_diff_total_monthly': 'str',
        'cost_diff_uuid': 'str',
        'cost_past_total_monthly': 'str',
        'cost_total_monthly': 'str',
        'cost_total_monthly_percentage_change': 'str',
        'data_length': 'int',
        'drift_counts': 'Counts',
        'enable_solutions_factory': 'bool',
        'git_branch': 'str',
        'git_commit_message': 'str',
        'git_commit_sha': 'str',
        'git_repo': 'str',
        'modules_uuid': 'str',
        'output_counts': 'Counts',
        'pipeline': 'str',
        'pipeline_execution_id': 'str',
        'pipeline_execution_number': 'str',
        'pipeline_name': 'str',
        'pipeline_stage_id': 'str',
        'plan_uuid': 'str',
        'providers_uuid': 'str',
        'provisioner': 'str',
        'provisioner_version': 'str',
        'resource_counts': 'Counts',
        'state_checksum': 'str',
        'state_uuid': 'str',
        'terragrunt_details': 'list[TerragruntDetail]',
        'trigger': 'dict(str, object)'
    }

    attribute_map = {
        'planned_changes_count': 'PlannedChangesCount',
        'activity_status': 'activity_status',
        'activity_type': 'activity_type',
        'cost_breakdown_uuid': 'cost_breakdown_uuid',
        'cost_currency': 'cost_currency',
        'cost_diff_total_monthly': 'cost_diff_total_monthly',
        'cost_diff_uuid': 'cost_diff_uuid',
        'cost_past_total_monthly': 'cost_past_total_monthly',
        'cost_total_monthly': 'cost_total_monthly',
        'cost_total_monthly_percentage_change': 'cost_total_monthly_percentage_change',
        'data_length': 'data_length',
        'drift_counts': 'drift_counts',
        'enable_solutions_factory': 'enable_solutions_factory',
        'git_branch': 'git_branch',
        'git_commit_message': 'git_commit_message',
        'git_commit_sha': 'git_commit_sha',
        'git_repo': 'git_repo',
        'modules_uuid': 'modules_uuid',
        'output_counts': 'output_counts',
        'pipeline': 'pipeline',
        'pipeline_execution_id': 'pipeline_execution_id',
        'pipeline_execution_number': 'pipeline_execution_number',
        'pipeline_name': 'pipeline_name',
        'pipeline_stage_id': 'pipeline_stage_id',
        'plan_uuid': 'plan_uuid',
        'providers_uuid': 'providers_uuid',
        'provisioner': 'provisioner',
        'provisioner_version': 'provisioner_version',
        'resource_counts': 'resource_counts',
        'state_checksum': 'state_checksum',
        'state_uuid': 'state_uuid',
        'terragrunt_details': 'terragrunt_details',
        'trigger': 'trigger'
    }

    def __init__(self, planned_changes_count=0, activity_status=None, activity_type=None, cost_breakdown_uuid=None, cost_currency=None, cost_diff_total_monthly=None, cost_diff_uuid=None, cost_past_total_monthly=None, cost_total_monthly=None, cost_total_monthly_percentage_change=None, data_length=0, drift_counts=None, enable_solutions_factory=None, git_branch=None, git_commit_message=None, git_commit_sha=None, git_repo=None, modules_uuid=None, output_counts=None, pipeline=None, pipeline_execution_id=None, pipeline_execution_number=None, pipeline_name=None, pipeline_stage_id=None, plan_uuid=None, providers_uuid=None, provisioner=None, provisioner_version=None, resource_counts=None, state_checksum=None, state_uuid=None, terragrunt_details=None, trigger=None):  # noqa: E501
        """ActivityMetadata - a model defined in Swagger"""  # noqa: E501
        self._planned_changes_count = None
        self._activity_status = None
        self._activity_type = None
        self._cost_breakdown_uuid = None
        self._cost_currency = None
        self._cost_diff_total_monthly = None
        self._cost_diff_uuid = None
        self._cost_past_total_monthly = None
        self._cost_total_monthly = None
        self._cost_total_monthly_percentage_change = None
        self._data_length = None
        self._drift_counts = None
        self._enable_solutions_factory = None
        self._git_branch = None
        self._git_commit_message = None
        self._git_commit_sha = None
        self._git_repo = None
        self._modules_uuid = None
        self._output_counts = None
        self._pipeline = None
        self._pipeline_execution_id = None
        self._pipeline_execution_number = None
        self._pipeline_name = None
        self._pipeline_stage_id = None
        self._plan_uuid = None
        self._providers_uuid = None
        self._provisioner = None
        self._provisioner_version = None
        self._resource_counts = None
        self._state_checksum = None
        self._state_uuid = None
        self._terragrunt_details = None
        self._trigger = None
        self.discriminator = None
        if planned_changes_count is not None:
            self.planned_changes_count = planned_changes_count
        if activity_status is not None:
            self.activity_status = activity_status
        if activity_type is not None:
            self.activity_type = activity_type
        if cost_breakdown_uuid is not None:
            self.cost_breakdown_uuid = cost_breakdown_uuid
        if cost_currency is not None:
            self.cost_currency = cost_currency
        if cost_diff_total_monthly is not None:
            self.cost_diff_total_monthly = cost_diff_total_monthly
        if cost_diff_uuid is not None:
            self.cost_diff_uuid = cost_diff_uuid
        if cost_past_total_monthly is not None:
            self.cost_past_total_monthly = cost_past_total_monthly
        if cost_total_monthly is not None:
            self.cost_total_monthly = cost_total_monthly
        if cost_total_monthly_percentage_change is not None:
            self.cost_total_monthly_percentage_change = cost_total_monthly_percentage_change
        if data_length is not None:
            self.data_length = data_length
        if drift_counts is not None:
            self.drift_counts = drift_counts
        if enable_solutions_factory is not None:
            self.enable_solutions_factory = enable_solutions_factory
        if git_branch is not None:
            self.git_branch = git_branch
        if git_commit_message is not None:
            self.git_commit_message = git_commit_message
        if git_commit_sha is not None:
            self.git_commit_sha = git_commit_sha
        if git_repo is not None:
            self.git_repo = git_repo
        if modules_uuid is not None:
            self.modules_uuid = modules_uuid
        if output_counts is not None:
            self.output_counts = output_counts
        if pipeline is not None:
            self.pipeline = pipeline
        if pipeline_execution_id is not None:
            self.pipeline_execution_id = pipeline_execution_id
        if pipeline_execution_number is not None:
            self.pipeline_execution_number = pipeline_execution_number
        if pipeline_name is not None:
            self.pipeline_name = pipeline_name
        if pipeline_stage_id is not None:
            self.pipeline_stage_id = pipeline_stage_id
        if plan_uuid is not None:
            self.plan_uuid = plan_uuid
        if providers_uuid is not None:
            self.providers_uuid = providers_uuid
        if provisioner is not None:
            self.provisioner = provisioner
        if provisioner_version is not None:
            self.provisioner_version = provisioner_version
        if resource_counts is not None:
            self.resource_counts = resource_counts
        if state_checksum is not None:
            self.state_checksum = state_checksum
        if state_uuid is not None:
            self.state_uuid = state_uuid
        if terragrunt_details is not None:
            self.terragrunt_details = terragrunt_details
        if trigger is not None:
            self.trigger = trigger

    @property
    def planned_changes_count(self):
        """Gets the planned_changes_count of this ActivityMetadata.  # noqa: E501

        Deprecated: use resource_count_xxxx fields instead  # noqa: E501

        :return: The planned_changes_count of this ActivityMetadata.  # noqa: E501
        :rtype: int
        """
        return self._planned_changes_count

    @planned_changes_count.setter
    def planned_changes_count(self, planned_changes_count):
        """Sets the planned_changes_count of this ActivityMetadata.

        Deprecated: use resource_count_xxxx fields instead  # noqa: E501

        :param planned_changes_count: The planned_changes_count of this ActivityMetadata.  # noqa: E501
        :type: int
        """

        self._planned_changes_count = planned_changes_count

    @property
    def activity_status(self):
        """Gets the activity_status of this ActivityMetadata.  # noqa: E501

        The status of this activity  # noqa: E501

        :return: The activity_status of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._activity_status

    @activity_status.setter
    def activity_status(self, activity_status):
        """Sets the activity_status of this ActivityMetadata.

        The status of this activity  # noqa: E501

        :param activity_status: The activity_status of this ActivityMetadata.  # noqa: E501
        :type: str
        """
        allowed_values = ["success", "failure", "incomplete"]  # noqa: E501
        if activity_status not in allowed_values:
            raise ValueError(
                "Invalid value for `activity_status` ({0}), must be one of {1}"  # noqa: E501
                .format(activity_status, allowed_values)
            )

        self._activity_status = activity_status

    @property
    def activity_type(self):
        """Gets the activity_type of this ActivityMetadata.  # noqa: E501

        The type of this activity  # noqa: E501

        :return: The activity_type of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._activity_type

    @activity_type.setter
    def activity_type(self, activity_type):
        """Sets the activity_type of this ActivityMetadata.

        The type of this activity  # noqa: E501

        :param activity_type: The activity_type of this ActivityMetadata.  # noqa: E501
        :type: str
        """
        allowed_values = ["apply", "destroy", "plan", "drifted", "import"]  # noqa: E501
        if activity_type not in allowed_values:
            raise ValueError(
                "Invalid value for `activity_type` ({0}), must be one of {1}"  # noqa: E501
                .format(activity_type, allowed_values)
            )

        self._activity_type = activity_type

    @property
    def cost_breakdown_uuid(self):
        """Gets the cost_breakdown_uuid of this ActivityMetadata.  # noqa: E501

        The ID of any associated cost breakdown data  # noqa: E501

        :return: The cost_breakdown_uuid of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._cost_breakdown_uuid

    @cost_breakdown_uuid.setter
    def cost_breakdown_uuid(self, cost_breakdown_uuid):
        """Sets the cost_breakdown_uuid of this ActivityMetadata.

        The ID of any associated cost breakdown data  # noqa: E501

        :param cost_breakdown_uuid: The cost_breakdown_uuid of this ActivityMetadata.  # noqa: E501
        :type: str
        """

        self._cost_breakdown_uuid = cost_breakdown_uuid

    @property
    def cost_currency(self):
        """Gets the cost_currency of this ActivityMetadata.  # noqa: E501

        The currency used in cost data for this change  # noqa: E501

        :return: The cost_currency of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._cost_currency

    @cost_currency.setter
    def cost_currency(self, cost_currency):
        """Sets the cost_currency of this ActivityMetadata.

        The currency used in cost data for this change  # noqa: E501

        :param cost_currency: The cost_currency of this ActivityMetadata.  # noqa: E501
        :type: str
        """

        self._cost_currency = cost_currency

    @property
    def cost_diff_total_monthly(self):
        """Gets the cost_diff_total_monthly of this ActivityMetadata.  # noqa: E501

        The currency used in cost data for this change  # noqa: E501

        :return: The cost_diff_total_monthly of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._cost_diff_total_monthly

    @cost_diff_total_monthly.setter
    def cost_diff_total_monthly(self, cost_diff_total_monthly):
        """Sets the cost_diff_total_monthly of this ActivityMetadata.

        The currency used in cost data for this change  # noqa: E501

        :param cost_diff_total_monthly: The cost_diff_total_monthly of this ActivityMetadata.  # noqa: E501
        :type: str
        """

        self._cost_diff_total_monthly = cost_diff_total_monthly

    @property
    def cost_diff_uuid(self):
        """Gets the cost_diff_uuid of this ActivityMetadata.  # noqa: E501

        The ID of any associated cost diff data  # noqa: E501

        :return: The cost_diff_uuid of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._cost_diff_uuid

    @cost_diff_uuid.setter
    def cost_diff_uuid(self, cost_diff_uuid):
        """Sets the cost_diff_uuid of this ActivityMetadata.

        The ID of any associated cost diff data  # noqa: E501

        :param cost_diff_uuid: The cost_diff_uuid of this ActivityMetadata.  # noqa: E501
        :type: str
        """

        self._cost_diff_uuid = cost_diff_uuid

    @property
    def cost_past_total_monthly(self):
        """Gets the cost_past_total_monthly of this ActivityMetadata.  # noqa: E501

        The currency used in cost data for this change  # noqa: E501

        :return: The cost_past_total_monthly of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._cost_past_total_monthly

    @cost_past_total_monthly.setter
    def cost_past_total_monthly(self, cost_past_total_monthly):
        """Sets the cost_past_total_monthly of this ActivityMetadata.

        The currency used in cost data for this change  # noqa: E501

        :param cost_past_total_monthly: The cost_past_total_monthly of this ActivityMetadata.  # noqa: E501
        :type: str
        """

        self._cost_past_total_monthly = cost_past_total_monthly

    @property
    def cost_total_monthly(self):
        """Gets the cost_total_monthly of this ActivityMetadata.  # noqa: E501

        The currency used in cost data for this change  # noqa: E501

        :return: The cost_total_monthly of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._cost_total_monthly

    @cost_total_monthly.setter
    def cost_total_monthly(self, cost_total_monthly):
        """Sets the cost_total_monthly of this ActivityMetadata.

        The currency used in cost data for this change  # noqa: E501

        :param cost_total_monthly: The cost_total_monthly of this ActivityMetadata.  # noqa: E501
        :type: str
        """

        self._cost_total_monthly = cost_total_monthly

    @property
    def cost_total_monthly_percentage_change(self):
        """Gets the cost_total_monthly_percentage_change of this ActivityMetadata.  # noqa: E501

        The currency used in cost data for this change  # noqa: E501

        :return: The cost_total_monthly_percentage_change of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._cost_total_monthly_percentage_change

    @cost_total_monthly_percentage_change.setter
    def cost_total_monthly_percentage_change(self, cost_total_monthly_percentage_change):
        """Sets the cost_total_monthly_percentage_change of this ActivityMetadata.

        The currency used in cost data for this change  # noqa: E501

        :param cost_total_monthly_percentage_change: The cost_total_monthly_percentage_change of this ActivityMetadata.  # noqa: E501
        :type: str
        """

        self._cost_total_monthly_percentage_change = cost_total_monthly_percentage_change

    @property
    def data_length(self):
        """Gets the data_length of this ActivityMetadata.  # noqa: E501

        The length of the data  # noqa: E501

        :return: The data_length of this ActivityMetadata.  # noqa: E501
        :rtype: int
        """
        return self._data_length

    @data_length.setter
    def data_length(self, data_length):
        """Sets the data_length of this ActivityMetadata.

        The length of the data  # noqa: E501

        :param data_length: The data_length of this ActivityMetadata.  # noqa: E501
        :type: int
        """

        self._data_length = data_length

    @property
    def drift_counts(self):
        """Gets the drift_counts of this ActivityMetadata.  # noqa: E501


        :return: The drift_counts of this ActivityMetadata.  # noqa: E501
        :rtype: Counts
        """
        return self._drift_counts

    @drift_counts.setter
    def drift_counts(self, drift_counts):
        """Sets the drift_counts of this ActivityMetadata.


        :param drift_counts: The drift_counts of this ActivityMetadata.  # noqa: E501
        :type: Counts
        """

        self._drift_counts = drift_counts

    @property
    def enable_solutions_factory(self):
        """Gets the enable_solutions_factory of this ActivityMetadata.  # noqa: E501

        Indicates if Harness Solution Factory functionality is enabled  # noqa: E501

        :return: The enable_solutions_factory of this ActivityMetadata.  # noqa: E501
        :rtype: bool
        """
        return self._enable_solutions_factory

    @enable_solutions_factory.setter
    def enable_solutions_factory(self, enable_solutions_factory):
        """Sets the enable_solutions_factory of this ActivityMetadata.

        Indicates if Harness Solution Factory functionality is enabled  # noqa: E501

        :param enable_solutions_factory: The enable_solutions_factory of this ActivityMetadata.  # noqa: E501
        :type: bool
        """

        self._enable_solutions_factory = enable_solutions_factory

    @property
    def git_branch(self):
        """Gets the git_branch of this ActivityMetadata.  # noqa: E501

        Git branch associated with this execution  # noqa: E501

        :return: The git_branch of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._git_branch

    @git_branch.setter
    def git_branch(self, git_branch):
        """Sets the git_branch of this ActivityMetadata.

        Git branch associated with this execution  # noqa: E501

        :param git_branch: The git_branch of this ActivityMetadata.  # noqa: E501
        :type: str
        """

        self._git_branch = git_branch

    @property
    def git_commit_message(self):
        """Gets the git_commit_message of this ActivityMetadata.  # noqa: E501

        Git commit message associated with this execution  # noqa: E501

        :return: The git_commit_message of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._git_commit_message

    @git_commit_message.setter
    def git_commit_message(self, git_commit_message):
        """Sets the git_commit_message of this ActivityMetadata.

        Git commit message associated with this execution  # noqa: E501

        :param git_commit_message: The git_commit_message of this ActivityMetadata.  # noqa: E501
        :type: str
        """

        self._git_commit_message = git_commit_message

    @property
    def git_commit_sha(self):
        """Gets the git_commit_sha of this ActivityMetadata.  # noqa: E501

        Git commit SHA associated with this execution  # noqa: E501

        :return: The git_commit_sha of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._git_commit_sha

    @git_commit_sha.setter
    def git_commit_sha(self, git_commit_sha):
        """Sets the git_commit_sha of this ActivityMetadata.

        Git commit SHA associated with this execution  # noqa: E501

        :param git_commit_sha: The git_commit_sha of this ActivityMetadata.  # noqa: E501
        :type: str
        """

        self._git_commit_sha = git_commit_sha

    @property
    def git_repo(self):
        """Gets the git_repo of this ActivityMetadata.  # noqa: E501

        Git repo associated with this execution  # noqa: E501

        :return: The git_repo of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._git_repo

    @git_repo.setter
    def git_repo(self, git_repo):
        """Sets the git_repo of this ActivityMetadata.

        Git repo associated with this execution  # noqa: E501

        :param git_repo: The git_repo of this ActivityMetadata.  # noqa: E501
        :type: str
        """

        self._git_repo = git_repo

    @property
    def modules_uuid(self):
        """Gets the modules_uuid of this ActivityMetadata.  # noqa: E501

        The ID of any associated modules data  # noqa: E501

        :return: The modules_uuid of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._modules_uuid

    @modules_uuid.setter
    def modules_uuid(self, modules_uuid):
        """Sets the modules_uuid of this ActivityMetadata.

        The ID of any associated modules data  # noqa: E501

        :param modules_uuid: The modules_uuid of this ActivityMetadata.  # noqa: E501
        :type: str
        """

        self._modules_uuid = modules_uuid

    @property
    def output_counts(self):
        """Gets the output_counts of this ActivityMetadata.  # noqa: E501


        :return: The output_counts of this ActivityMetadata.  # noqa: E501
        :rtype: Counts
        """
        return self._output_counts

    @output_counts.setter
    def output_counts(self, output_counts):
        """Sets the output_counts of this ActivityMetadata.


        :param output_counts: The output_counts of this ActivityMetadata.  # noqa: E501
        :type: Counts
        """

        self._output_counts = output_counts

    @property
    def pipeline(self):
        """Gets the pipeline of this ActivityMetadata.  # noqa: E501

        The unique identifier of any associated pipeline  # noqa: E501

        :return: The pipeline of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._pipeline

    @pipeline.setter
    def pipeline(self, pipeline):
        """Sets the pipeline of this ActivityMetadata.

        The unique identifier of any associated pipeline  # noqa: E501

        :param pipeline: The pipeline of this ActivityMetadata.  # noqa: E501
        :type: str
        """

        self._pipeline = pipeline

    @property
    def pipeline_execution_id(self):
        """Gets the pipeline_execution_id of this ActivityMetadata.  # noqa: E501

        The unique identifier for any associated pipeline execution  # noqa: E501

        :return: The pipeline_execution_id of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_execution_id

    @pipeline_execution_id.setter
    def pipeline_execution_id(self, pipeline_execution_id):
        """Sets the pipeline_execution_id of this ActivityMetadata.

        The unique identifier for any associated pipeline execution  # noqa: E501

        :param pipeline_execution_id: The pipeline_execution_id of this ActivityMetadata.  # noqa: E501
        :type: str
        """

        self._pipeline_execution_id = pipeline_execution_id

    @property
    def pipeline_execution_number(self):
        """Gets the pipeline_execution_number of this ActivityMetadata.  # noqa: E501

        The unique number for any associated pipeline execution  # noqa: E501

        :return: The pipeline_execution_number of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_execution_number

    @pipeline_execution_number.setter
    def pipeline_execution_number(self, pipeline_execution_number):
        """Sets the pipeline_execution_number of this ActivityMetadata.

        The unique number for any associated pipeline execution  # noqa: E501

        :param pipeline_execution_number: The pipeline_execution_number of this ActivityMetadata.  # noqa: E501
        :type: str
        """

        self._pipeline_execution_number = pipeline_execution_number

    @property
    def pipeline_name(self):
        """Gets the pipeline_name of this ActivityMetadata.  # noqa: E501

        The name of any associated pipeline  # noqa: E501

        :return: The pipeline_name of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_name

    @pipeline_name.setter
    def pipeline_name(self, pipeline_name):
        """Sets the pipeline_name of this ActivityMetadata.

        The name of any associated pipeline  # noqa: E501

        :param pipeline_name: The pipeline_name of this ActivityMetadata.  # noqa: E501
        :type: str
        """

        self._pipeline_name = pipeline_name

    @property
    def pipeline_stage_id(self):
        """Gets the pipeline_stage_id of this ActivityMetadata.  # noqa: E501

        The unique identifier for the associated pipeline stage  # noqa: E501

        :return: The pipeline_stage_id of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_stage_id

    @pipeline_stage_id.setter
    def pipeline_stage_id(self, pipeline_stage_id):
        """Sets the pipeline_stage_id of this ActivityMetadata.

        The unique identifier for the associated pipeline stage  # noqa: E501

        :param pipeline_stage_id: The pipeline_stage_id of this ActivityMetadata.  # noqa: E501
        :type: str
        """

        self._pipeline_stage_id = pipeline_stage_id

    @property
    def plan_uuid(self):
        """Gets the plan_uuid of this ActivityMetadata.  # noqa: E501

        The ID of any associated plan data  # noqa: E501

        :return: The plan_uuid of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._plan_uuid

    @plan_uuid.setter
    def plan_uuid(self, plan_uuid):
        """Sets the plan_uuid of this ActivityMetadata.

        The ID of any associated plan data  # noqa: E501

        :param plan_uuid: The plan_uuid of this ActivityMetadata.  # noqa: E501
        :type: str
        """

        self._plan_uuid = plan_uuid

    @property
    def providers_uuid(self):
        """Gets the providers_uuid of this ActivityMetadata.  # noqa: E501

        The ID of any associated providers data  # noqa: E501

        :return: The providers_uuid of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._providers_uuid

    @providers_uuid.setter
    def providers_uuid(self, providers_uuid):
        """Sets the providers_uuid of this ActivityMetadata.

        The ID of any associated providers data  # noqa: E501

        :param providers_uuid: The providers_uuid of this ActivityMetadata.  # noqa: E501
        :type: str
        """

        self._providers_uuid = providers_uuid

    @property
    def provisioner(self):
        """Gets the provisioner of this ActivityMetadata.  # noqa: E501

        The provisioner in use  # noqa: E501

        :return: The provisioner of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._provisioner

    @provisioner.setter
    def provisioner(self, provisioner):
        """Sets the provisioner of this ActivityMetadata.

        The provisioner in use  # noqa: E501

        :param provisioner: The provisioner of this ActivityMetadata.  # noqa: E501
        :type: str
        """

        self._provisioner = provisioner

    @property
    def provisioner_version(self):
        """Gets the provisioner_version of this ActivityMetadata.  # noqa: E501

        The current version of the provisioner in use  # noqa: E501

        :return: The provisioner_version of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._provisioner_version

    @provisioner_version.setter
    def provisioner_version(self, provisioner_version):
        """Sets the provisioner_version of this ActivityMetadata.

        The current version of the provisioner in use  # noqa: E501

        :param provisioner_version: The provisioner_version of this ActivityMetadata.  # noqa: E501
        :type: str
        """

        self._provisioner_version = provisioner_version

    @property
    def resource_counts(self):
        """Gets the resource_counts of this ActivityMetadata.  # noqa: E501


        :return: The resource_counts of this ActivityMetadata.  # noqa: E501
        :rtype: Counts
        """
        return self._resource_counts

    @resource_counts.setter
    def resource_counts(self, resource_counts):
        """Sets the resource_counts of this ActivityMetadata.


        :param resource_counts: The resource_counts of this ActivityMetadata.  # noqa: E501
        :type: Counts
        """

        self._resource_counts = resource_counts

    @property
    def state_checksum(self):
        """Gets the state_checksum of this ActivityMetadata.  # noqa: E501

        The checksum of the last-seen state file  # noqa: E501

        :return: The state_checksum of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._state_checksum

    @state_checksum.setter
    def state_checksum(self, state_checksum):
        """Sets the state_checksum of this ActivityMetadata.

        The checksum of the last-seen state file  # noqa: E501

        :param state_checksum: The state_checksum of this ActivityMetadata.  # noqa: E501
        :type: str
        """

        self._state_checksum = state_checksum

    @property
    def state_uuid(self):
        """Gets the state_uuid of this ActivityMetadata.  # noqa: E501

        The ID of any associated state data  # noqa: E501

        :return: The state_uuid of this ActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._state_uuid

    @state_uuid.setter
    def state_uuid(self, state_uuid):
        """Sets the state_uuid of this ActivityMetadata.

        The ID of any associated state data  # noqa: E501

        :param state_uuid: The state_uuid of this ActivityMetadata.  # noqa: E501
        :type: str
        """

        self._state_uuid = state_uuid

    @property
    def terragrunt_details(self):
        """Gets the terragrunt_details of this ActivityMetadata.  # noqa: E501

        Terragrunt details for any associated execution  # noqa: E501

        :return: The terragrunt_details of this ActivityMetadata.  # noqa: E501
        :rtype: list[TerragruntDetail]
        """
        return self._terragrunt_details

    @terragrunt_details.setter
    def terragrunt_details(self, terragrunt_details):
        """Sets the terragrunt_details of this ActivityMetadata.

        Terragrunt details for any associated execution  # noqa: E501

        :param terragrunt_details: The terragrunt_details of this ActivityMetadata.  # noqa: E501
        :type: list[TerragruntDetail]
        """

        self._terragrunt_details = terragrunt_details

    @property
    def trigger(self):
        """Gets the trigger of this ActivityMetadata.  # noqa: E501

        Trigger info for any associated pipeline execution  # noqa: E501

        :return: The trigger of this ActivityMetadata.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._trigger

    @trigger.setter
    def trigger(self, trigger):
        """Sets the trigger of this ActivityMetadata.

        Trigger info for any associated pipeline execution  # noqa: E501

        :param trigger: The trigger of this ActivityMetadata.  # noqa: E501
        :type: dict(str, object)
        """

        self._trigger = trigger

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
        if issubclass(ActivityMetadata, dict):
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
        if not isinstance(other, ActivityMetadata):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
